# move-smb-to-s3-python

This project is a `lamda aws project` in charge to get **files** from samba storage to aws s3 bucket.

  * [Source Architecture](#source-architecture)
  * [Prepare development environment](#prepare-development-environment)
    + [Requirements](#requirements)
    + [Install project's dependencies](#install-project-s-dependencies)
      - [Simple environment](#simple-environment)
      - [With virtual environment (venv)](#with-virtual-environment--venv-)
    + [Set up aws authentication](#set-up-aws-authentication)
  * [Run application locally](#run-application-locally)
      - [Environment variables](#environment-variables)
      - [Starting aws and samba locally](#starting-aws-and-samba-locally)
      - [Preparing folder smb/etransfer locally](#preparing-folder-smb-etransfer-locally)
      - [Run application by command line](#run-application-by-command-line)
      - [Run application by visual studio code](#run-application-by-visual-studio-code)
      - [Run unit tests and coverage by command line](#run-unit-tests-and-coverage-by-command-line)
  * [More About](#more-about)
    + [Ignoring folders](#ignoring-folders)

      
## Source Architecture
Below is the list of main files in this projects

```bash

.
│
├── src	  # all code to be running on aws lambda
│   ├── config.py			# module to manage all enviromment variables and settings
│   ├── event.py			# module to manage all request event before run any step in .lambda_function.py
│   ├── counter_handler.py	# module to support counters for files and folders in .transfer.py
│   ├── file_handler.py		  # module to handle transferring proces file
│   ├── lambda_function.py	# module has main method to be called from aws lambda
│   ├── environment.py      # module to save all environment values when initiating application
│   └── transfer.py			    # module to handle transferring proces file
│
├── local
│   ├── docker-compose.yml 	# compose to start up s3_aws and samba localy
│   ├── local.env			# file to setting all environment variables
│   ├── mount/*				# local samba folder
│   │
│   ├── script-clean-all-files-smb-mount.sh		  # script to remove all file from local samba folder
│   ├── script-recreate-all-files-smb-mount.sh	# script to create all fake files into local samba folder
│   ├── script-remove-all-files-s3-local.sh		  # script to remove all files from local s3
│   └── script-start-local-containers.sh		    # script to start and prepare samba and s3 localy
│
├── run 	# package to run locally
│   └── __main__.py # main launcher module to call lambda_function locally
│
└── tests 	# unit tests
    ├── test_counter_handler.py # unittests to src.counter_handler module
    └── test_file_handler.py	  # unittests to src.file_handler module

```

## Prepare development environment

### Requirements
It's required to install dependencies below:
 - **python3.8+**: Toolkit to developer application in python
 - **python3.8-venv**: Create virtual environment to install dependencies and running virtual python interpreters ( only if you wish to use venv )
 - **pip**: Dependence management for python applications
 - **aws cli**: Toolkit to work with aws from local environment
 - **docker and docker-compose**: Platform to manager containers ( only to run samba and s3 locally )

### Install project's dependencies 

#### Simple environment
If you are not going to use virtual env, run command below:

```bash
# install all required libraries used in project
pip3 install -r ./requirements.txt
```

#### With virtual environment (venv)
If you wish to create a virtual environment to be used in project, run command below:
```bash
# create virtual environment into 'venv-local' folder
python3.8 -m venv venv-local

# activate virtual environment to install all required dependencies
source ./venv-local/bin/activate

# install all required libraries used in project
pip3 install -r ./requirements.txt

```

> On virtual environment add `"python.defaultInterpreterPath": "venv-local/bin/python3"` in `./.vscode/settings.json` file so that vscode use virtual env on project debugging

### Set up aws authentication
Create 2 files named `config` and `credentials` in `{USER_HOME}/.aws/`


.aws/config
```
[default]
region = sa-east-1
```

.aws/credentials
```
[default]
aws_access_key_id={retrived_from_aws_console}
aws_secret_access_key={retrived_from_aws_console}
aws_session_token={retrived_from_aws_console}
```

> If you are going to use different environment to dev-aws, you need to check all env vars placed in `./local/local.env`

## Run application locally

> Don't forget to [Prepare development environment](#prepare-development-environment) before trying to run

#### Environment variables
Before prepare local environment and run application we need to check environment variables used in project.
These variables will lead us to manage running project on **LOCAL**, **DEV**, **HML** and **PRD** environment.

These variables are placed in `./src/environment.py` and will be swithed by environment variable `ENVIRONMENT=XXX`

It's necessary have the one environment variable below, this variable will lead all others variables from `./src/environment.py`

```bash
# LOCAL, DEV, HML, PRD
ENVIRONMENT=LOCAL
```

> this project are managing local environment variables on `./local/local.env` file. These variables is used in scripts, docker-compose and vscode settings

#### Starting aws and samba locally
In order to start aws and samba folder on local machine run script below:
```bash
bash ./local/script-start-local-containers.sh up ./local/local.env
```
After run application and move all files to local s3 you can see all moved file with:
```bash
# list all files in local bucket s3
aws --endpoint-url=http://localhost:4566 s3 ls s3://bucket1/folders3/
```
> required installed docker, docker-compose and aws cli

#### Preparing folder smb/etransfer locally
We can remove and recreate all local files as we need with scripts below:
```bash
# remove all files from smb mount
sudo bash ./local/script-clean-all-files-smb-mount.sh ./local/local.env

# remove all files from local s3
bash ./local/script-remove-all-files-s3-local.sh ./local/local.env

# recreating all files in smb mount
sudo bash ./local/script-recreate-all-files-smb-mount.sh ./local/local.env

```

#### Run application by command line
```bash
# use env variable from local/local.env file and run module ./run/__main__.py
set -a; source local/local.env; set +a; python3 -m run
```
> don't forget to check which process are you running in `./run/__main__.py` and which env variable is set in `./local/local.env`;

####  Run application by visual studio code
All we need is press F5 on vscode so `./run/__main__.py` will be called ( see more in `/.vscode/launch.json` file)

> If you have started up aws locally you can check all moved files in s3 with the command `aws --endpoint-url=http://localhost:4566 s3 ls s3://bucket1/folders3/`

#### Run unit tests and coverage by command line

To run all unit tests, use command below in root folder:

```bash
python3 -m unittest -v
```

To run specific unit tests, use command below in root folder:

```bash
python3 -m unittest tests.test_file_handler
```

To run covarage and process covering unit tests, use command below in root folder:

```bash
coverage run --source=src -m unittest discover -s tests/
```

To generate covering tests result in html, use command below in root folder:

```bash
coverage run --source=src -m unittest discover -s tests/
coverage html -d coverage_html
```
> you can see covering result tests in `./coverage_html/index.html`


## More About

### Ignoring folders

All root folder must contains a setting file `{env}.ignore` ( eg. 'prd.ignore' in prd environment )

This file `{env}.ignore` has all rules to ignore folders when reading files

This file `{env}.ignore` can be empty if there is no folders to be ignored and will ignore empty lines inside itself

All folders will be ignored by its names according rules below
  - **folder_name\***    -> will ignore folder `starts with` in root-diretory/**folder_name\***
  - **\*folder_name**    -> will ignore folder `ends with` in root-diretory/**\*folder_name**
  - **\*folder_name\***   -> will ignore folder `contains` in root-diretory/**\*folder_name\***
  - **folder_name**     -> will ignore folder `is equals` in root-diretory/**folder_name**
