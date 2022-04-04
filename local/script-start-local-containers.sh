#!/bin/bash

# bash ./local/script-start-local-containers.sh up ./local/local.env
# bash ./local/script-start-local-containers.sh down ./local/local.env

set -e

echo "==== Starting ./script/start-local-environment.sh for acctrigger ===="

# ====================== read variables file
if [ -n "$2"  ]; then
        echo "reading $2 into enviromment variables"
        set -a
        source $2
        set +a
fi

# ======================= handle args
if [ "$1" != "up" ] && [ "$1" != "down" ]; then
    echo "argument not found. try 'file.bash up' or 'file.bash down'"
    exit -1;
fi

# ======================= handle arg down to remove container
if [ "$1" == "down" ] || [ "$1" == "DOWN"  ]; then
    docker-compose --file ./local/docker-compose.yml --env-file $2 down
    echo "aws_services_container container removed sucessfully!"
    exit 0;
fi

# ======================= handle arg up start process
if [ "$1" == "up" ] || [ "$1" == "UP"  ]; then
    echo "==== Starting AWS and SAMBA containers ===="
    docker-compose --file ./local/docker-compose.yml --env-file $2 up -d

    set +e
    # ======================= waiting container
    URL_HEALTH_CONTAINER="$LOCAL_AWS_CONTAINER_ENDPOINT/health"

    IS_SONAR_ON=NOT_200
    while [ "$IS_AWS_CONTAINER_ON" != "200" ]; do 
        IS_AWS_CONTAINER_ON=$(curl -LIsS -X GET $URL_HEALTH_CONTAINER -o /dev/null -w '%{http_code}\n'); 
        echo "waiting for aws_services_container..."
        sleep 5
    done;

    set -e
    echo "==== Creating s3 buckets ===="
    aws --endpoint-url=$LOCAL_AWS_CONTAINER_ENDPOINT s3api create-bucket --bucket $LOCAL_AWS_S3_NAME_BUCKET_TARGET

    echo "==== Creating s3 folders ===="
    aws --endpoint-url=$LOCAL_AWS_CONTAINER_ENDPOINT s3api put-object --bucket $LOCAL_AWS_S3_NAME_BUCKET_TARGET --key $LOCAL_AWS_S3_NAME_PREFIX_TARGET/
    # aws --endpoint-url=http://localhost:4566 s3 ls s3://lbucket1
fi

echo -e "\n\nThat's all ready!!! \n"
