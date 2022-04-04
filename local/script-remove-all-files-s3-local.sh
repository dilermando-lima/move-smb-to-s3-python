#!/bin/bash

# bash ./local/script-remove-all-files-s3-local.sh ./local/local.env

set -e

# ====================== read variables file
if [ -n "$1"  ]; then
        echo "reading $1 into enviromment variables"
        set -a
        source $1
        set +a
fi
aws --endpoint-url=$LOCAL_AWS_CONTAINER_ENDPOINT s3 rm s3://$LOCAL_AWS_S3_NAME_BUCKET_TARGET/$LOCAL_AWS_S3_NAME_PREFIX_TARGET/ --recursive

echo -e "\n\nAll contents in s3://$LOCAL_AWS_S3_NAME_BUCKET_TARGET/$LOCAL_AWS_S3_NAME_PREFIX_TARGET has been removed sucessfully!!! \n"
