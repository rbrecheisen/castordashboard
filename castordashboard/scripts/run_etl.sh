#!/usr/bin/env bash

export CASTOR_CLIENT_ID=$(cat $HOME/castorclientid.txt)
export CASTOR_CLIENT_SECRET=$(cat $HOME/castorclientsecret.txt)

docker-compose run etl
