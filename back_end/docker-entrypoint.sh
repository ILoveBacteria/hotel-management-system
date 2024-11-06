#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn --bind 0.0.0.0:8000 --threads 4 core.wsgi:application