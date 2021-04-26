#!/usr/bin/env bash

export CASTOR_DASHBOARD_OUTPUT_DIR=${HOME}/data/castordashboard
export CASTOR_DASHBOARD_LOG_DIR=${CASTOR_DASHBOARD_OUTPUT_DIR}/logs
export PYTHONPATH=.

python etl/script_runner.py
