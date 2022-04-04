import json
from datetime import datetime
import warnings

from .config import load_env
from .event import EVENT, ActionEvent, load_event
from .file_handler import get_last_workday
from .counter_handler import Counter
from .transfer import move_from_smb_to_s3




def lambda_handler(event, _ ):

    load_event(event)
    load_env(EVENT.read_only)

    counter_result = Counter()

    if EVENT.action_event == ActionEvent.TRANSFER_ON_CURRENT_DATE:
        
        EVENT.date = get_last_workday(datetime.now().strftime("%Y%m%d"))
        counter_result = move_from_smb_to_s3(EVENT.date)

    else:

         counter_result = move_from_smb_to_s3(EVENT.date)


    checking_return_function(counter_result)






def checking_return_function(counter_result: Counter):
    
    if counter_result.total_count_files_on_error_at_all > 0:
        warnings.warn(f"There are {counter_result.total_count_files_on_error_at_all} files with error that have not been moved to s3")
   
        return {
            "statusCode": 500,
            "body": json.dumps(f"There are {counter_result.total_count_files_on_error_at_all} files with error that have not been moved to s3")
        }

    else:

        return {
            "statusCode": 200,
            "body": json.dumps(f"{counter_result.total_count_files_moved_sucessfully_at_all} files have not been moved successfully to s3")
        }


