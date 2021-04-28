#!/usr/bin/env bash

export SECRET_KEY=1234
export PARAMS_FILE_PATH=params.json
export OUTPUT_DIR=${HOME}/data/castordashboard
export SQLITE3_DIR=${OUTPUT_DIR}
export LOG_DIR=${OUTPUT_DIR}/logs
export DEBUG=1

export command="from django.contrib.auth.models import User"
export command="${command}; User.objects.create_superuser('ralph', 'ralph@example.com', 'foobar')"

cd dashboard
echo ${command} | python manage.py shell
