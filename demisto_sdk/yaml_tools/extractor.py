import yaml
import os
import base64
import subprocess
import shutil
import tempfile
from io import open
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import SingleQuotedScalarString
from ..common.tools import print_color, LOG_COLORS, get_docker_images, get_python_version, get_pipenv_dir, str2bool
from ..common.constants import SCRIPT_PREFIX, INTEGRATION_PREFIX
from ..common.configuration import Configuration

INTEGRATION = 'integration'
SCRIPT = 'script'


class Extractor:

    def __init__(self, yml_path: str, dest_path: str, add_demisto_mock: bool, add_common_server: bool, yml_type: str,
                 configuration: Configuration):
        self.yml_path = yml_path
        self.dest_path = dest_path
        self.demisto_mock = add_demisto_mock
        self.common_server = add_common_server
        self.yml_type = yml_type
        self.config = configuration

    def migrate(self):
        print("Starting migration of: {} to dir: {}".format(self.yml_path, self.dest_path))
        arg_path = self.dest_path
        output_path = os.path.abspath(self.dest_path)
        os.makedirs(output_path, exist_ok=True)
        base_name = os.path.basename(output_path)
        yml_type = self.get_yml_type()
        code_file = "{}/{}.py".format(output_path, base_name)
        self.extract_code(code_file)
        self.extract_image("{}/{}_image.png".format(output_path, base_name))
        self.extract_long_description("{}/{}_description.md".format(output_path, base_name))
        yaml_out = "{}/{}.yml".format(output_path, base_name)
        print("Creating yml file: {} ...".format(yaml_out))
        ryaml = YAML()
        ryaml.preserve_quotes = True
        with open(self.yml_path, 'r') as yf:
            yaml_obj = ryaml.load(yf)
        script_obj = yaml_obj
        if yml_type == INTEGRATION:
            script_obj = yaml_obj['script']
            del yaml_obj['image']
            if 'detaileddescription' in yaml_obj:
                del yaml_obj['detaileddescription']
        if script_obj['type'] != 'python':
            print('Script is not of type "python". Found type: {}. Nothing to do.'.format(script_obj['type']))
            return 1
        script_obj['script'] = SingleQuotedScalarString('')
        with open(yaml_out, 'w') as yf:
            ryaml.dump(yaml_obj, yf)
        print("Running autopep8 on file: {} ...".format(code_file))
        try:
            subprocess.call(["autopep8", "-i", "--max-line-length", "130", code_file])
        except FileNotFoundError:
            print_color("autopep8 skipped! It doesn't seem you have autopep8 installed.\n"
                        "Make sure to install it with: pip install autopep8.\n"
                        "Then run: autopep8 -i {}".format(code_file), LOG_COLORS.YELLOW)
        print("Detecting python version and setting up pipenv files ...")
        docker = get_docker_images(script_obj)[0]
        py_ver = get_python_version(docker, self.config.log_verbose)
        pip_env_dir = get_pipenv_dir(py_ver, self.config.envs_dirs_base)
        print("Copying pipenv files from: {}".format(pip_env_dir))
        shutil.copy("{}/Pipfile".format(pip_env_dir), output_path)
        shutil.copy("{}/Pipfile.lock".format(pip_env_dir), output_path)
        try:
            subprocess.call(["pipenv", "install", "--dev"], cwd=output_path)
            print("Installing all py requirements from docker: [{}] into pipenv".format(docker))
            requirements = subprocess.check_output(["docker", "run", "--rm", docker,
                                                    "pip", "freeze", "--disable-pip-version-check"],
                                                   universal_newlines=True, stderr=subprocess.DEVNULL).strip()
            fp = tempfile.NamedTemporaryFile(delete=False)
            fp.write(requirements.encode('utf-8'))
            fp.close()
            subprocess.check_call(["pipenv", "install", "-r", fp.name], cwd=output_path)
            os.unlink(fp.name)
            print("Installing flake8 for linting")
            subprocess.call(["pipenv", "install", "--dev", "flake8"], cwd=output_path)
        except FileNotFoundError:
            print_color("pipenv install skipped! It doesn't seem you have pipenv installed.\n"
                        "Make sure to install it with: pip3 install pipenv.\n"
                        "Then run in the package dir: pipenv install --dev", LOG_COLORS.YELLOW)
        # check if there is a changelog
        yml_changelog = os.path.splitext(self.yml_path)[0] + '_CHANGELOG.md'
        changelog = arg_path + '/CHANGELOG.md'
        if os.path.exists(yml_changelog):
            shutil.copy(yml_changelog, changelog)
        else:
            with open(changelog, 'wt', encoding='utf-8') as changelog_file:
                changelog_file.write("## [Unreleased]\n-\n")
        print_color("\nCompleted: setting up package: {}\n".format(arg_path), LOG_COLORS.GREEN)
        print("Next steps: \n",
              "* Install additional py packages for unit testing (if needed): cd {}; pipenv install <package>\n".format(
                  arg_path),
              "* Create unit tests\n",
              "* Check linting and unit tests by running: ./Tests/scripts/pkg_dev_test_tasks.py -d {}\n".format(
                  arg_path),
              "* When ready rm from git the source yml and add the new package:\n",
              "    git rm {}\n".format(self.yml_path),
              "    git add {}\n".format(arg_path),
              sep=''
              )
        return 0

    def extract_code(self, output_file):
        yml_type = self.get_yml_type()
        print("Extracting code to: {} ...".format(self.dest_path))
        common_server = self.common_server
        if common_server is None:
            common_server = "CommonServerPython" not in self.yml_path
        with open(self.yml_path, 'rb') as yml_file:
            yml_data = yaml.safe_load(yml_file)
            script = yml_data['script']
            if yml_type == INTEGRATION:  # in integration the script is stored at a second level
                script = script['script']
        with open(output_file, 'w', encoding='utf-8') as code_file:
            if self.demisto_mock:
                code_file.write("import demistomock as demisto\n")
            if common_server:
                code_file.write("from CommonServerPython import *\n")
            code_file.write(script)
            if script[-1] != '\n':  # make sure files end with a new line (pyml seems to strip the last newline)
                code_file.write("\n")
        return 0

    def extract_image(self, output_path):
        yml_type = self.get_yml_type()
        if yml_type == SCRIPT:
            return  # no image in script type
        print("Extracting image to: {} ...".format(output_path))
        with open(self.yml_path, 'rb') as yml_file:
            yml_data = yaml.safe_load(yml_file)
            image_b64 = yml_data['image'].split(',')[1]
        with open(output_path, 'wb') as image_file:
            image_file.write(base64.decodebytes(image_b64.encode('utf-8')))
        return 0

    def extract_long_description(self, output_path):
        yml_type = self.get_yml_type()
        if yml_type == SCRIPT:
            return  # no long description in script type
        with open(self.yml_path, 'rb') as yml_file:
            yml_data = yaml.safe_load(yml_file)
            long_description = yml_data.get('detaileddescription')
        if long_description:
            print("Extracting long description to: {} ...".format(output_path))
            with open(output_path, 'w', encoding='utf-8') as desc_file:
                desc_file.write(long_description)
        return 0

    def get_yml_type(self):
        yml_type = None
        if not self.yml_type:
            if SCRIPT in self.yml_path.lower():
                yml_type = SCRIPT
            elif INTEGRATION in self.yml_path.lower():
                yml_type = INTEGRATION
            else:
                raise ValueError('Could not auto determine yml type ({}/{}) based on path: {}'
                                 .format(SCRIPT, INTEGRATION, self.yml_path))
        return yml_type

    @staticmethod
    def add_sub_parser(subparsers):
        parser = subparsers.add_parser('extract', help='Extract code, image and description files' 
                                                       ' from a demisto integration or script yaml file')
        parser.add_argument("-i", "--infile", help="The yml file to extract from", required=True)
        parser.add_argument("-o", "--outfile",
                            help="The output file or dir (if doing migrate) to write the code to", required=True)
        parser.add_argument("-m", "--migrate", action='store_true',
                            help="Migrate an integration to package format."
                                 " Pass to -o option a directory in this case.")
        parser.add_argument("-t", "--type",
                            help="Yaml type. If not specified will try to determine type based upon path.",
                            choices=[SCRIPT_PREFIX, INTEGRATION_PREFIX], default=None)
        parser.add_argument("-d", "--demistomock", help="Add an import for demisto mock",
                            choices=[True, False], type=str2bool, default=True)
        parser.add_argument("-c", "--commonserver",
                            help=("Add an import for CommonServerPython. "
                                  " If not specified will import unless this is CommonServerPython"),
                            choices=[True, False], type=str2bool, default=None)
