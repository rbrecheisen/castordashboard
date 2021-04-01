#!/usr/bin/env bash

docker-compose exec web bash -c "/src/dashboard/createsuperuser.sh"
