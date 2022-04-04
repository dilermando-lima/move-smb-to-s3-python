import os
import re
from datetime import datetime, timedelta
from typing import List


def get_date_from_file_name(file_name: str) -> bool:
    # extract any _yyyymmdd_HHmmss format from file name
    match_date_rgx = re.search("_20[0-9]{6}_[0-9]{6}", file_name)

    if match_date_rgx is None:
        return "20990101"
    else:
        return file_name[match_date_rgx.start()+1:match_date_rgx.start()+9]

def normalize_path_bars(folder_path: str):
    folder_path =  folder_path[:-1] if folder_path.endswith("/") else folder_path
    return folder_path.replace("\\\\","/").replace("\\","/").replace("//","/").replace("\/","/").replace("\\\\","/")


"""
This function will check if folder name would be ignored according rules below
    diretory/folder_name*    -> will ignore folder starts with
    diretory/*folder_name    -> will ignore folder ends with
    diretory/*folder_name*   -> will ignore folder contains
    diretory/folder_name     -> will ignore folder with the same name
"""
def check_to_ignore_folder(folder_path: str, list_to_be_ignored: List[str]) -> bool:

    if list_to_be_ignored is None: return False
    if len(list_to_be_ignored) == 0: return False
    if folder_path is None: return False
    if folder_path.strip() == "": return False

    folder_name = os.path.basename(normalize_path_bars(folder_path))

    for ignore in list_to_be_ignored:

        if ignore.strip() == "":
            continue

        # 'folder_name' starts with 'folder*'
        if ignore.strip().endswith("*") and folder_name.startswith(ignore.strip().replace("*","")):
            print(f"Ignored by rule: folder_name '{folder_name}' matches to '{ignore.strip()}'")
            return True

        # 'folder_name' ends with '*folder'
        if ignore.strip().startswith("*") and folder_name.endswith(ignore.strip().replace("*","")):
            print(f"Ignored by rule: folder_name '{folder_name}' matches to '{ignore.strip()}'")
            return True
        
        # 'folder_name' contains '*folder*'
        if ignore.strip().startswith("*") and ignore.strip().endswith("*") and ignore.strip().replace("*","") in folder_name.strip():
            print(f"Ignored by rule: folder_name '{folder_name}' matches to '{ignore.strip()}'")
            return True

        # 'folder_name' is equals 'folder'
        if ignore.strip() in folder_name.strip():
            print(f"Ignored by rule: folder_name '{folder_name}' matches to '{ignore.strip()}'")
            return True

    return False
    

def is_date_file_name_equal_to(file_name: str, date_yyyymmdd: str) -> bool:
    return date_yyyymmdd == get_date_from_file_name(file_name)

def get_last_workday(date_yyyymmdd: str) -> str:
    date_current = datetime.strptime(date_yyyymmdd, "%Y%m%d")
    date_last_workday_return = None

    if date_current.weekday() in [0]: # Monday
        date_last_friday = date_current - timedelta(days=3)
        date_last_workday_return = date_last_friday

    elif date_current.weekday() in [6]: # Sunday
        date_last_friday = date_current - timedelta(days=2)
        date_last_workday_return = date_last_friday
    
    elif date_current.weekday() in [1,2,3,4,5]: # Tuesday, Wednesday, Thursday, Friday, Saturday
        date_last_workday_return = date_current - timedelta(days=1)

    return str(date_last_workday_return.strftime("%Y%m%d"))



 