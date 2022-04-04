import json
from enum import Enum

import boto3
import smbclient
from botocore.exceptions import ClientError

from .environment import *


class Env(str,Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    HML = "HML"
    PRD = "PRD"

    def from_string(value) -> Enum:
        if value == Env.LOCAL : return Env.LOCAL
        if value == Env.DEV : return Env.DEV
        if value == Env.HML : return Env.HML
        if value == Env.PRD : return Env.PRD
        raise Exception("ENVIRONMENT must be 'local', 'dev', 'hml' or 'prd'")

class Config:
    def __init__(self):
        self.aws_secret_name: str
        self.smb_mount: str
        self.smb_user: str
        self.smb_pass: str
        self.s3_bucket: str
        self.s3_prefix: str
        self.environment: Env
        self.read_only: bool

CONF = Config()


def print_config():
    print(f"Config('environment': '{CONF.environment}', 'smb_mount': '{CONF.smb_mount}', 'aws_secret_name' : '{CONF.aws_secret_name}', 'smb_user': '{CONF.smb_user}','s3_bucket': '{CONF.s3_bucket}','s3_prefix':'{CONF.s3_prefix}' , 'read_only': {CONF.read_only})")



def load_env(read_only: str = None):

    CONF.environment = Env.from_string(os.environ.get("ENVIRONMENT"))

    # vars read from .environment.py constant according '{ENV}_VAR_NAME'
    CONF.aws_secret_name =  globals().get(CONF.environment.value + "_AWS_SECRET_NAME")
    CONF.smb_mount =        globals().get(CONF.environment.value + "_SMB_MOUNT")
    CONF.s3_bucket =        globals().get(CONF.environment.value + "_AWS_S3_NAME_BUCKET_TARGET")
    CONF.s3_prefix =        globals().get(CONF.environment.value + "_AWS_S3_NAME_PREFIX_TARGET")
    CONF.read_only =        get_read_only_env(globals().get(CONF.environment.value + "_READ_ONLY") if read_only is None else read_only)

    CONF.smb_user,          CONF.smb_pass = load_user_and_pass_smb()

    valid_config()
    print_config()


def get_read_only_env(value_read_only: str) -> bool:
    if value_read_only is None: return True
    if value_read_only.lower() == "false": return False
    else: return True

def valid_config():
    if CONF.smb_mount is None:
        raise ValueError("Env variable 'SMB_MOUNT' not found")
    if ( CONF.smb_user is None or CONF.smb_user is None ) and CONF.environment == Env.LOCAL:
        raise ValueError("Env variables 'SMB_USER' and 'SMB_PASS' are not found")
    if ( CONF.smb_user is None or CONF.smb_user is None ) and CONF.environment != Env.LOCAL:
        raise ValueError("Env variables 'AWS_SECRET_NAME' from aws secret")
    if CONF.s3_bucket is None:
        raise ValueError("Env variable 'AWS_S3_NAME_BUCKET_TARGET' not found")
    if CONF.s3_prefix is None:
        raise ValueError("Env variable 'AWS_S3_NAME_PREFIX_TARGET' not found")
    if CONF.read_only is None:
        raise ValueError("Env variable 'READ_ONLY' not found. try set 'READ_ONLY=true'")

def get_client_s3():
    
    if CONF.environment == Env.LOCAL:
        return boto3.client(
                service_name="s3",
                region_name=globals().get(CONF.environment.value + "_AWS_CONTAINER_DEFAULT_REGION"), 
                endpoint_url=globals().get(CONF.environment.value + "_AWS_CONTAINER_ENDPOINT"),
                aws_access_key_id="any",
                aws_secret_access_key="any",
                aws_session_token="any"
            )
    else:
        return boto3.client(service_name="s3")


def get_client_smb():
    smbclient.ClientConfig(username=CONF.smb_user, password=CONF.smb_pass)
    return smbclient




def load_user_and_pass_smb(): 

    if CONF.environment == Env.LOCAL:
        # not required when {ENV}_AWS_SECRET_NAME is passed
        return globals().get(CONF.environment.value + "_SMB_USER"), globals().get(CONF.environment.value + "_SMB_PASS")
    else:

        if CONF.aws_secret_name is not None:
            try:

                client_secret_manager = boto3.client(service_name="secretsmanager")

                secret_values_string = client_secret_manager.get_secret_value(SecretId=CONF.aws_secret_name).get("SecretString")
                secret_values = json.loads(secret_values_string)

                smb_user = secret_values.get("user_key") 
                smb_domain = secret_values.get("user_domain")

                if smb_user is not None and smb_domain is not None:
                    smb_user = smb_user + "@" +  smb_domain

                smb_pass = secret_values.get("user_secret")

                return smb_user , smb_pass

            except ClientError as e:
                raise Exception(f"Error when retrieving aws_secret '{CONF.aws_secret_name}', msg = " + str(e))


