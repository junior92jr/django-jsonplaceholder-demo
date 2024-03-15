#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py migrate --noinput
service cron start
python manage.py crontab add
python manage.py runserver "$APP_HOST":"$APP_PORT"
