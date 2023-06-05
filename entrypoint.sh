#!/bin/sh
echo 'Applyng migrations'
python manage.py wait_for_db
python manage.py migrate

echo 'Running server...'

gunicorn jet.wsgi --bind 0.0.0.0:$PORT
