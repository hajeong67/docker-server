#!/bin/bash

echo "01_makemigrations"
python3 manage.py makemigrations --noinput

echo "02_migrate"
python3 manage.py migrate --noinput

gunicorn --bind 0.0.0.0:8000 config.wsgi:application