#!/usr/bin/env bash

# check for virtualenv and datastore
[ -d "env" ] && python3 -m venv env

mkdir -p env/db

# activate virtualenv
source env/bin/activate

# launch server itself
python3 run.py

deactivate