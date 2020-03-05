from demisto_sdk.commands.common.git_tools import git_path

GIT_ROOT = "{}".format(git_path())
INVALID_PLAYBOOK_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks.playbook-invalid.yml"
VALID_TEST_PLAYBOOK_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks.playbook-test.yml"
VALID_PLAYBOOK_ARCSIGHT_ADD_DOMAIN_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/Playbooks." \
                                          f"playbook-ArcSight_Add_Domain_Indicators.yml"
VALID_INTEGRATION_TEST_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-test.yml"
VALID_INTEGRATION_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-valid-id-test.yml"
INVALID_INTEGRATION_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-id-test.yml"
VALID_PLAYBOOK_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-valid-id-test.yml"
INVALID_PLAYBOOK_ID_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/playbook-invalid-id-test.yml"
VALID_REPUTATION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputations-valid.json"
INVALID_REPUTATION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputations-invalid.json"
VALID_LAYOUT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/layout-valid.json"
INVALID_LAYOUT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/layout-invalid.json"
VALID_WIDGET_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-valid.json"
INVALID_WIDGET_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-invalid.json"
VALID_DASHBOARD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/dashboard-valid.json"
INVALID_DASHBOARD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/dashboard-invalid.json"
VALID_INCIDENT_FIELD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/incidentfield-valid.json"
INVALID_INCIDENT_FIELD_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/incidentfield-invalid.json"
INVALID_WIDGET_VERSION_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/widget-invalid-version.json"
VALID_SCRIPT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/script-valid.yml"
INVALID_SCRIPT_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/script-invalid.yml"
VALID_ONE_LINE_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-one-line_CHANGELOG.md"
VALID_ONE_LINE_LIST_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-one-line-list_CHANGELOG.md"
VALID_MULTI_LINE_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-multi-line_CHANGELOG.md"
VALID_MULTI_LINE_LIST_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/valid-multi-line-list_CHANGELOG.md"
INVALID_ONE_LINE_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line_1_CHANGELOG.md"
INVALID_ONE_LINE_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line_2_CHANGELOG.md"
INVALID_ONE_LINE_LIST_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line-list_1_CHANGELOG.md"
INVALID_ONE_LINE_LIST_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-one-line-list_2_CHANGELOG.md"
INVALID_MULTI_LINE_1_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-multi-line_1_CHANGELOG.md"
INVALID_MULTI_LINE_2_CHANGELOG_PATH = f"{GIT_ROOT}/demisto_sdk/tests/test_files/invalid-multi-line_2_CHANGELOG.md"
LAYOUT_TARGET = "./Layouts/layout-mock.json"
REPUTATION_TARGET = "./Misc/reputations.json"
WIDGET_TARGET = "./Widgets/widget-mocks.json"
DASHBOARD_TARGET = "./Dashboards/dashboard-mocks.json"
PLAYBOOK_TARGET = "Playbooks/playbook-test.yml"
INTEGRATION_TARGET = "./Integrations/integration-test.yml"
INCIDENT_FIELD_TARGET = "IncidentFields/incidentfield-test.json"
PLAYBOOK_PACK_TARGET = "Packs/Int/Playbooks/playbook-test.yml"
SCRIPT_TARGET = "./Scripts/script-test.yml"
SCRIPT_RELEASE_NOTES_TARGET = "./Scripts/script-test_CHANGELOG.md"
INTEGRATION_RELEASE_NOTES_TARGET = "./Integrations/integration-test_CHANGELOG.md"
SOURCE_FORMAT_INTEGRATION_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_New_Integration_copy.yml"
DESTINATION_FORMAT_INTEGRATION_COPY = "new_format_New_Integration_copy.yml"
SOURCE_FORMAT_SCRIPT_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_New_script_copy.yml"
DESTINATION_FORMAT_SCRIPT_COPY = f"new_format_New_script_copy.yml"
SOURCE_FORMAT_PLAYBOOK_COPY = f"{GIT_ROOT}/demisto_sdk/tests/test_files/format_new_playbook_copy.yml"
DESTINATION_FORMAT_PLAYBOOK_COPY = "playbook-new_format_new_playbook_copy.yml"
INDICATORFIELD_EXTRA_FIELDS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicatorfield-extra-fields.json"
INDICATORFIELD_EXACT_SCHEME = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicator-field-exact-scheme.json"
INDICATORFIELD_MISSING_FIELD = f"{GIT_ROOT}/demisto_sdk/tests/test_files/indicator-field-missing-field.json"
INDICATORFIELD_MISSING_AND_EXTRA_FIELDS = f"{GIT_ROOT}/demisto_sdk/tests/test_files/" \
                                          f"indicatorfield-missing-and-extra-fields.json"
INVALID_INTEGRATION_YML_1 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml1.yml"
INVALID_INTEGRATION_YML_2 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml2.yml"
INVALID_INTEGRATION_YML_3 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml3.yml"
INVALID_INTEGRATION_YML_4 = f"{GIT_ROOT}/demisto_sdk/tests/test_files/integration-invalid-yml4.yml"
VALID_REPUTATION_FILE = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputation-cidr-valid.json"
INVALID_REPUTATION_FILE = f"{GIT_ROOT}/demisto_sdk/tests/test_files/reputation-cidr-invalid.json"
