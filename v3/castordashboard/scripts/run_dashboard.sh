#!/usr/bin/env bash

export SECRET_KEY=1234
export PARAMS_FILE_PATH=params.json
export SQLITE3_DIR=$HOME/castordashboard
export CASTOR_DASHBOARD_OUTPUT_DIR=${HOME}/data/castordashboard
export CASTOR_DASHBOARD_LOG_DIR=${CASTOR_DASHBOARD_OUTPUT_DIR}/logs

python manage.py makemigrations app
python manage.py migrate
python manage.py runserver 0.0.0.0:80
