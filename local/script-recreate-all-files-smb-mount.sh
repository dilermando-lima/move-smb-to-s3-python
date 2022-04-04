#!/bin/bash

# sudo bash ./local/script-recreate-all-files-smb-mount.sh ./local/local.env

set -e

# ====================== read variables file
if [ -n "$1"  ]; then
        echo "reading $1 into enviromment variables"
        set -a
        source $1
        set +a
fi

echo "Executing script-clean-all-files-smb-mount.sh"
sudo bash ./local/script-clean-all-files-smb-mount.sh $1

FOLDER_MOUNT=./local/mount

PREFIX_FOLDER1=folder1

NAME_IGNORE_CONFIG_FILE=local.ignore

DATE_YYYYMMDD=20220301

echo "Adding files $PREFIX_FOLDER1..."
mkdir -p $FOLDER_MOUNT/$PREFIX_FOLDER1
echo ${PREFIX_FOLDER1}_content > $FOLDER_MOUNT/$PREFIX_FOLDER1/FILE1_${DATE_YYYYMMDD}.txt
echo ${PREFIX_FOLDER1}_content > $FOLDER_MOUNT/$PREFIX_FOLDER1/FILE2_${DATE_YYYYMMDD}.csv

echo "Adding ignore config..."
echo $PREFIX_IGNORE > $FOLDER_MOUNT/$NAME_IGNORE_CONFIG_FILE
echo "ignore-equals" >> $FOLDER_MOUNT/$NAME_IGNORE_CONFIG_FILE
echo "ignore-start*" >> $FOLDER_MOUNT/$NAME_IGNORE_CONFIG_FILE
echo "*ends-with" >> $FOLDER_MOUNT/$NAME_IGNORE_CONFIG_FILE
echo "*nore-contai*" >> $FOLDER_MOUNT/$NAME_IGNORE_CONFIG_FILE

echo "Adding files $PREFIX_IGNORE..."
mkdir -p $FOLDER_MOUNT/ignore-equals
echo some_content > $FOLDER_MOUNT/ignore-equals/will-be-ignored-by-folder-1.ret
mkdir -p $FOLDER_MOUNT/ignore-start-with
echo some_content > $FOLDER_MOUNT/ignore-start-with/will-be-ignored-by-folder-1.ret
mkdir -p $FOLDER_MOUNT/ignore-ends-with
echo some_content > $FOLDER_MOUNT/ignore-ends-with/will-be-ignored-by-folder-1.ret
mkdir -p $FOLDER_MOUNT/ignore-contains
echo some_content > $FOLDER_MOUNT/ignore-contains/will-be-ignored-by-folder-1.ret


chmod -R a+rw $FOLDER_MOUNT/

echo -e "\n\nAll contents in $FOLDER_MOUNT has been recreated!!! \n"