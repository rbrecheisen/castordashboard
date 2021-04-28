#!/usr/bin/env bash

export SECRET_KEY=1234
export PARAMS_FILE_PATH=params.json
export OUTPUT_DIR=${HOME}/data/castordashboard
export SQLITE3_DIR=${OUTPUT_DIR}
export LOG_DIR=${OUTPUT_DIR}/logs
export DEBUG=1

cd dashboard
python manage.py makemigrations app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
