
from src.lambda_function import lambda_handler

EVENT_TRANSFER_ON_CURRENT_DATE = {"action":"transfer_on_current_date"}

# EVENT_TRANSFER_ON_SPECIFIC_DATE               = {"action":"transfer_on_specific_date","date":"20220309"}
# EVENT_TRANSFER_ON_SPECIFIC_DATE_READ_ONLY_TRUE    = {"action":"transfer_on_specific_date","date":"20220309","read_only":"true"}

lambda_handler(EVENT_TRANSFER_ON_CURRENT_DATE, None)

