import os

# LOCAL ENV =====================================================================
LOCAL_READ_ONLY="true"
LOCAL_AWS_S3_NAME_BUCKET_TARGET=os.environ.get("LOCAL_AWS_S3_NAME_BUCKET_TARGET")
LOCAL_AWS_S3_NAME_PREFIX_TARGET=os.environ.get("LOCAL_AWS_S3_NAME_PREFIX_TARGET")
LOCAL_AWS_CONTAINER_DEFAULT_REGION=os.environ.get("LOCAL_AWS_CONTAINER_DEFAULT_REGION")
LOCAL_AWS_CONTAINER_ENDPOINT=os.environ.get("LOCAL_AWS_CONTAINER_ENDPOINT")
LOCAL_SMB_USER=os.environ.get("LOCAL_SMB_USER")
LOCAL_SMB_PASS=os.environ.get("LOCAL_SMB_PASS")
LOCAL_SMB_MOUNT=os.environ.get("LOCAL_SMB_MOUNT")

# DEV ENV =====================================================================
DEV_READ_ONLY="true"
DEV_AWS_S3_NAME_BUCKET_TARGET="bucket-target"
DEV_AWS_S3_NAME_PREFIX_TARGET="folder-s3"
DEV_AWS_SECRET_NAME="secret-dev"
DEV_SMB_MOUNT="//000.000.000.000/mount-smb-dev"

# HML ENV =====================================================================
HML_READ_ONLY="false"
HML_AWS_S3_NAME_BUCKET_TARGET="bucket-target"
HML_AWS_S3_NAME_PREFIX_TARGET="folder-s3"
HML_AWS_SECRET_NAME="secret-dev"
HML_SMB_MOUNT="//000.000.000.000/mount-smb-hml"

# PRD ENV =====================================================================
PRD_READ_ONLY="false"
PRD_AWS_S3_NAME_BUCKET_TARGET="bucket-target"
PRD_AWS_S3_NAME_PREFIX_TARGET="folder-s3"
PRD_AWS_SECRET_NAME="secret-prd"
PRD_SMB_MOUNT="//000.000.000.000/mount-smb-prd"