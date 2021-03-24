#!/usr/bin/env bash

export SECRET_KEY=1234

docker-compose up -d; docker-compose logs -f
