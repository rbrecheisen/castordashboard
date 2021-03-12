#!/usr/bin/env bash
docker run --rm --name dashboard_nginx -p 8000:80 -d nginx:1.15.0
