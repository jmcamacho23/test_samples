from tests.testrail import testrail as tr
from tests.testrail import testrail_config as trc
from tests.testrail import testrail_delete_cases as tdlt
import time
from support import utils as u, vars
"""
    This file will post results from the _reports.json files in the /reports
    directory to a Testrail automated project. It will aggregate 
    the file results that are marked as scenarios and are not skipped in the 
    process. It will get those and save them to the scenarios.txt file and use
    those strings to match them to the case IDs from Testrail. It will create 
    a run for the day, and post the results based on the case ID, and run ID--
    using the aggregated test results.
"""
batch_begin_time = u.get_time()
# Step 1: read _reports.json files and write them to the scenarios.txt file
step1_begin_time = u.get_time()
tr.delete_breaking_files()  # delete files that break stuff if present
time.sleep(1)
tr.write_scenarios_to_file()
time.sleep(0.5)
step1_end_time = u.get_time()
step1_time_lapsed = round(step1_end_time - step1_begin_time, 2)
print(f'Scenarios written to file ✔ - Finished in {step1_time_lapsed}s')
# Step 2: delete cases just in case
tdlt.delete_the_testrail_cases()
# Step 3: use the scenarios.txt file to create cases through the API
step3_begin_time = u.get_time()
tr.create_missing_cases_with_api()
time.sleep(0.5)
step3_end_time = u.get_time()
step3_time_lapsed = round(step3_end_time - step3_begin_time, 2)
print(f'Cases created through the API ✔ - Finished in {step3_time_lapsed}s')
# Step 4: create a new run that will use the cases created
step4_begin_time = u.get_time()
refs = vars.datetime_alpha
tr.create_test_run_custom_ref(refs)
time.sleep(0.5)
step4_end_time = u.get_time()
step4_time_lapsed = round(step4_end_time - step4_begin_time, 2)
print(f'Test run created ✔ - Finished in {step4_time_lapsed}s')
# Step 5: get the run id for today's run, store it below
time.sleep(1)
step5_begin_time = u.get_time()
custom_run = tr.get_custom_run_id(refs)
time.sleep(0.5)
step5_end_time = u.get_time()
step5_time_lapsed = round(step5_end_time - step5_begin_time, 2)
print(f'Run ID retrieved: {custom_run} ✔  - Finished in {step5_time_lapsed}s')
# Step 6: get the case names and ids, post results
time.sleep(1)  # let's wait for the API?
step6_begin_time = u.get_time()
scenario_xml_data = tr.get_scenario_xml_data()
time.sleep(0.5)
# now loop through scenario names and post
for case in scenario_xml_data:
    case_begin_time = u.get_time()
    scenario_name = case[0]
    case_id = tr.get_case_id_by_name(scenario_name)
    time.sleep(0.5)
    scenario_status = case[1].capitalize()
    status_id = trc.status_id_array[scenario_status]
    sys_output = case[3]

    find_string = sys_output.find('** APP VERSION TESTED: ')
    if find_string == -1:
        version = ''
    else:
        app_version = sys_output.split('** APP VERSION TESTED: ')[1].split(' **')[0]
        version = app_version

    scenario_timestamp = case[4]
    elapsed = u.format_elapsed_time(case[2])
    elapsed_secs = str(elapsed) + 's'
    app_name = tr.get_app_name_from_output(sys_output)
    browser_version = tr.get_browser_version(sys_output)
    if app_name == '[Web]':
        version = browser_version
    elif app_name == '[API]':
        version = vars.version

    app_abbrev = f'{app_name} {version}'
    all_output = f'█ █ TEST START DATETIME: {scenario_timestamp} █ █ Version: {version} \n █ █ SYTSTEM OUTPUT: {sys_output}'
    print(f'Run ID: {custom_run} | Case ID: {case_id} | App: {app_abbrev} | Status ID: {status_id} | Version: {version} | Elapsed: {elapsed_secs}')
    tr.add_case_results_to_run(custom_run, case_id, status_id, all_output, elapsed_secs, app_abbrev)
    time.sleep(0.5)
step6_end_time = u.get_time()
step6_time_lapsed = round(step6_end_time - step6_begin_time, 2)
print(f'Results posted to Testrail ✔ - Finished in {step6_time_lapsed}s')

batch_end_time = u.get_time()
batch_time_lapsed = round(batch_end_time - batch_begin_time, 2)
batch_time_lapsed_mins = round(batch_time_lapsed/60, 2)
print(f'** COMPLETED ** - All finished in {batch_time_lapsed}s ({batch_time_lapsed_mins}m)')
