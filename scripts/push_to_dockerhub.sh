#!/usr/bin/env bash
docker logout
docker login
docker push brecheisen/dashboard_web:latest
