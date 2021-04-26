#!/usr/bin/env bash

export command="from django.contrib.auth.models import User"
export command="${command}; User.objects.create_superuser('ralph', 'ralph@example.com', 'foobar')"
export command="${command}; User.objects.create_user('marielle', 'marielle@example.com', 'foobar')"

python manage.py migrate

echo ${command} | python manage.py shell
