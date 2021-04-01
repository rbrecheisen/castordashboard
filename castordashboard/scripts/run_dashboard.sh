#!/usr/bin/env bash

export SECRET_KEY=1234
export DEBUG=0

scripts/stop.sh

docker-compose up -d
docker-compose logs -f
