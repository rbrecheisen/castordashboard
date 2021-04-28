#!/usr/bin/env bash

export OUTPUT_DIR=${HOME}/data/castordashboard
export LOG_DIR=${OUTPUT_DIR}/logs
export PYTHONPATH=.

python etl/script_runner.py
