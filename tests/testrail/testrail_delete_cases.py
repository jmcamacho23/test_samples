from tests.testrail import testrail as tr
import time
from support import utils as u

def delete_the_testrail_cases():
    # Step 2: delete cases just in case
    # this step removed in case you want to append in the single script
    step2_begin_time = u.get_time()
    tr.delete_all_cases()
    time.sleep(0.5)
    step2_end_time = u.get_time()
    step2_time_lapsed = round(step2_end_time - step2_begin_time, 2)
    print(f'Cases deleted ✔  - Finished in {step2_time_lapsed}s')