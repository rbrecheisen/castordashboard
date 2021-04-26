#!/usr/bin/env bash

export CASTOR_DASHBOARD_OUTPUT_DIR=${HOME}/data/castordashboard
export CASTOR_DASHBOARD_LOG_DIR=${CASTOR_DASHBOARD_OUTPUT_DIR}/logs
export CASTOR_DASHBOARD_SCRIPTS_PACKAGE=etl.scripts
export CASTOR_DASHBOARD_STUDY_NAME=ESPRESSO_v2.0_DPCA

python script_runner.py