import os
import warnings
from modulefinder import Module
from typing import List

import smbclient
from botocore.exceptions import ClientError

from .config import CONF, get_client_s3, get_client_smb
from .counter_handler import Counter
from .file_handler import check_to_ignore_folder, is_date_file_name_equal_to

"""
All root folder must contains a file to define which folder would be ignored
This file must be '{env}.ignore'
If there is no any folder to be ignored it's necessary to create a empty config file
"""
def read_ignore_config(client_smb: smbclient) -> List[str]:

    list_to_be_ignored: List[str]
    file_ignore_config = f"{CONF.smb_mount}/{str(CONF.environment.value).lower()}.ignore"
    print(f"Loading required folder-ignoring settings from {file_ignore_config}")
    
    try:
        with client_smb.open_file(file_ignore_config) as content:
            list_to_be_ignored = content.read().splitlines()

            print(f"Files to be skipped by ignoring settings {list_to_be_ignored}")
    except Exception as e:
        raise Exception(f"error when reading required file '{file_ignore_config}', msg = {str(e)}")

    return list_to_be_ignored
    

def move_from_smb_to_s3(date_target_yyyymmdd: str) -> Counter:

    print(f"Starting proccess of moving files from  {CONF.smb_mount} to {CONF.s3_bucket}/{CONF.s3_prefix} on date {date_target_yyyymmdd}")

    client_s3 = get_client_s3()
    client_smb = get_client_smb()
    counter = Counter()

    list_folder_to_be_ignored = read_ignore_config(client_smb)

    # ====  reading each file in samba directory
    for dirpath, _, files in client_smb.walk(CONF.smb_mount):

        # ignore root folder
        if dirpath == CONF.smb_mount: continue

        if check_to_ignore_folder(dirpath, list_folder_to_be_ignored):
            print(f"Skiping '{dirpath}'. ignored by [env].ignore file")
            continue

        counter.init_counter_new_folder()
        print(f"Reading {dirpath}")

        for file_name in files:

            try:

            # ====  handling file names
                counter.increment_current_file()
                path_file_name = os.path.join(dirpath, file_name)
     
                final_key_to_s3 = CONF.s3_prefix + "/" + file_name

                print(f"{counter.get_id_log_file()} Moving */{file_name} to */{final_key_to_s3}")

                if not is_date_file_name_equal_to(final_key_to_s3, date_target_yyyymmdd):
                    # won't raise error to not increment counter erros in this date... only will pass to the next one
                    counter.increment_file_from_other_date()
                    warnings.warn(f"{counter.get_id_log_file()} {final_key_to_s3} has skipped... not matched to date request {date_target_yyyymmdd}")
                    continue
                
                with client_smb.open_file(path_file_name, mode='rb') as data:

                    # ==== checking file already exists in S3
                    try:
                        client_s3.get_object(Bucket=CONF.s3_bucket, Key=final_key_to_s3)
                    except ClientError as e:
                        pass
                    else:
                        raise Warning(f"{counter.get_id_log_file()} {path_file_name} has already been uploaded to s3 as */{final_key_to_s3}")

                
                    try:
                        # ==== uploading file into S3   
                        print(f"{counter.get_id_log_file()} Uploading */{file_name} to s3 */{final_key_to_s3}")
                        if not CONF.read_only :
                            client_s3.upload_fileobj(data, CONF.s3_bucket, final_key_to_s3)
                        else:
                            print(f"{counter.get_id_log_file()} App is 'read_only'. Upload to S3 has not actually been done")
                    except ClientError as e:
                        raise e
                    else:
                        # ==== removing file just uploaded to s3 from smb 
                        print(f"{counter.get_id_log_file()} Removing {path_file_name} from smb directory")
                        if not CONF.read_only :
                            client_smb.remove(path_file_name)
                        else:
                            print(f"{counter.get_id_log_file()} App is 'read_only'. Removing from smb has not actually been done")

                        counter.increment_file_moved_sucessfully()

            except Exception as e:
                counter.increment_file_on_error()
                warnings.warn(e)
        
        if len(files) > 0:
            if counter.total_count_files_from_other_date_in_folder > 0:
                print(f"{counter.total_count_files_moved_sucessfully_in_folder}/{len(files)} files moved sucessfully from {dirpath} ( {counter.total_count_files_on_error_in_folder} with errors and {counter.total_count_files_from_other_date_in_folder} has diff date )")
            else:
                print(f"{counter.total_count_files_moved_sucessfully_in_folder}/{len(files)} files moved sucessfully from {dirpath} ( {counter.total_count_files_on_error_in_folder} with errors )")
        else:
            print(f"{counter.total_count_files_moved_sucessfully_in_folder}/{len(files)} files. There is no file in {dirpath}")

    return counter
