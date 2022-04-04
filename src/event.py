
from datetime import datetime
from enum import Enum


class ActionEvent(str,Enum):
    """
    The main process is about executing process to move all files from smb to s3 with DATE equals last workday
    It doesn't require any extra argument ( date will be calculated by now )
    
    Can be called manually passion 'action=transfer_on_current_date'
    
    eg. aws lambda invoke --function-name ${lambda_function} --payload '{"action":"transfer_on_current_date"}' response.json
    """
    TRANSFER_ON_CURRENT_DATE = "transfer_on_current_date"

    """
    This action is a litle bit different to "transfer_on_specific_date" so requires "date" parameter
    The main process is about executing process to move all files from smb to s3 with specific date
    
    Requires "date" as parameter
    
    Can be called manually passion 'action=transfer_on_specific_date' and 'date=yyyymmdd'
    
    eg. aws lambda invoke --function-name ${lambda_function} --payload '{"action":"transfer_on_specific_date","date":"20220101"}' response.json
    """
    TRANSFER_ON_SPECIFIC_DATE = "transfer_on_specific_date"

    """
    Used on invalid parameter "action"
    It will raise exception
    """
    INVALID = "invalid"

    def from_string(event) -> Enum:
        if not "action" in event:   return None
        if str(event.get("action")).lower() == ActionEvent.TRANSFER_ON_CURRENT_DATE:   return ActionEvent.TRANSFER_ON_CURRENT_DATE
        if str(event.get("action")).lower() == ActionEvent.TRANSFER_ON_SPECIFIC_DATE:  return ActionEvent.TRANSFER_ON_SPECIFIC_DATE
        else:   EVENT.action_event = ActionEvent.INVALID

class Event:
    def __init__(self):
        self.read_only: str
        self.date: str
        self.action_event: ActionEvent
    
EVENT = Event()


def print_event():
    print(f"Event('action_event': '{EVENT.action_event}', 'read_only': '{EVENT.read_only}', 'date': '{EVENT.date}')")


def load_event(event: any):
    if event is None: raise Exception("event is none in lambda_handler")

    EVENT.read_only = event.get("read_only",None) # may be 'None' and may overrid by env variable READ_ONLY
    EVENT.action_event = ActionEvent.from_string(event)   
    EVENT.date = event.get("date", None)
    valid_event()
    print_event()


def valid_event():
    if EVENT.action_event is None:
        raise ValueError("'action' is not found in lambda event request")
    if EVENT.action_event == ActionEvent.INVALID:
        raise ValueError("'action' is invalid in lambda event request")
    if EVENT.action_event == ActionEvent.TRANSFER_ON_SPECIFIC_DATE:
        if EVENT.date is None:
            raise ValueError(f"'date' is required when 'action' is 'transfer_on_specific_date'")

        try : datetime.strptime(EVENT.date, '%Y%m%d')
        except: raise ValueError(f"'date' must be a valid date on format yyyymmdd")
