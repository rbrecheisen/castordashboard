#!/usr/bin/env bash

# Note: this script is meant to run on scalpel!
# I'm using hard-coded paths here because that is what the cron job likely requires.

export CASTOR_CLIENT_ID=$(cat /home/local/UNIMAAS/r.brecheisen/castorclientid.txt)
export CASTOR_CLIENT_SECRET=$(cat /home/local/UNIMAAS/r.brecheisen/castorclientsecret.txt)

/usr/local/bin/docker-compose run etl bash -c "python script_runner.py --param=/src/params.json"
