#!/bin/bash

# sudo bash ./local/script-clean-all-files-smb-mount.sh ./local/local.env

set -e

# ====================== read variables file
if [ -n "$1"  ]; then
        echo "reading $1 into enviromment variables"
        set -a
        source $1
        set +a
fi

FOLDER_MOUNT=./local/mount
rm -rf $FOLDER_MOUNT/*

echo -e "\n\nAll contents in $FOLDER_MOUNT has been cleaned sucessfully!!! \n"
