import os
import time
import demisto_client
from demisto_client.demisto_api.rest import ApiException
from demisto_sdk.common.tools import print_error, print_color, LOG_COLORS


class PlaybookRunner:
    """PlaybookRunner is a class that's designed to run a playbook in a given Demisto instance.

    Attributes:
        playbook_id (str): the ID of the playbook to run
        should_wait (bool): whether to wait until the playbook run is completed or not.
        timeout (int): timeout for the command. The playbook will continue to run in Demisto
        base_link_to_workplan (str): the base link to see the full playbook run in Demisto.
        demisto_client (demisto_client): object for creating an incident in Demisto.
    """
    DEMISTO_API_KEY_ENV = 'DEMISTO_API_KEY'

    def __init__(self, playbook_id: str, url: str, wait: str, timeout: int):
        self.playbook_id = playbook_id
        self.should_wait = (wait == 'True')
        self.timeout = timeout
        self.base_link_to_workplan = f'{url}/#/WorkPlan/'
        self.demisto_client = demisto_client.configure(
            base_url=url,
            api_key=self.get_api_key(),
            verify_ssl=False)

    def run_playbook(self):
        # type: () -> int
        """Run a playbook in Demisto.

        Returns:
            int. 0 in success, 1 in a failure.
        """
        # create an incident with the given playbook
        try:
            incident_id = self.create_incident_with_playbook(
                incident_name=f'inc_{self.playbook_id}', playbook_id=self.playbook_id)
        except ApiException as a:
            print_error(str(a))
            return 1

        work_plan_link = self.base_link_to_workplan + str(incident_id)
        if self.should_wait:
            print(f'Waiting for the playbook to finish running.. \n'
                  f'To see the playbook run in real-time please go to : {work_plan_link}',
                  LOG_COLORS.GREEN)

            elasped_time = 0
            start_time = time.time()

            while elasped_time < self.timeout:
                playbook_results = self.get_playbook_results_dict(incident_id)
                if playbook_results["state"] == "inprogress":
                    time.sleep(10)
                    elasped_time = int(time.time() - start_time)
                else:   # the playbook has finished running
                    break

            # Ended the loop because of timeout
            if elasped_time >= self.timeout:
                print_error(f'The command had timed out while the playbook is in progress.\n'
                            f'To keep tracking the playbook please go to : {work_plan_link}')
            else:
                if playbook_results["state"] == "failed":
                    print_error("The playbook finished running with status: FAILED")
                else:
                    print_color("The playbook has completed its run successfully", LOG_COLORS.GREEN)

        # The command does not wait for the playbook to finish running
        else:
            print(f'To see results please go to : {work_plan_link}')

        return 0

    def create_incident_with_playbook(self, incident_name, playbook_id):
        # type: (str, str) -> int
        """Create an incident in Demisto with the given incident_name and the given playbook_id

        Args:
            incident_name (str): The name of the incident
            playbook_id (str): The id of the playbook

        Returns:
            int. The new incident's ID.
        """

        create_incident_request = demisto_client.demisto_api.CreateIncidentRequest()
        create_incident_request.create_investigation = True
        create_incident_request.playbook_id = playbook_id
        create_incident_request.name = incident_name

        try:
            response = self.demisto_client.create_incident(create_incident_request=create_incident_request)
        except ApiException as e:
            print_error(f'Failed to create incident with playbook id : "{playbook_id}", '
                        'possible reasons are:\n'
                        '1. This playbook name does not exist \n'
                        '2. Schema problems in the playbook \n'
                        '3. Unauthorized api key')
            raise e

        print_color(f'The playbook: {self.playbook_id} was triggered successfully.', LOG_COLORS.GREEN)
        return response.id

    def get_playbook_results_dict(self, inc_id):
        playbook_results = self.demisto_client.generic_request(method='GET', path=f'/inv-playbook/{inc_id}')
        return eval(playbook_results[0])

    def get_api_key(self):
        """Retrieve the API Key

        Raises:
            RuntimeError: if the API Key environment variable is not found

        Returns:
            str: API Key
        """
        api_key = os.environ.get(self.DEMISTO_API_KEY_ENV)
        if api_key is None:
            raise RuntimeError(f'Error: Environment variable {self.DEMISTO_API_KEY_ENV} not found')

        return api_key
