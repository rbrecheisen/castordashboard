#!/usr/bin/env bash

docker-compose rm -sv web
docker-compose rm -sv nginx
docker-compose rm -sv db