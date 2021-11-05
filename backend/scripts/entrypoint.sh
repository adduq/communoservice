#!/usr/bin/env sh

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py loaddata apps/fixtures.json

# uwsgi --http "0.0.0.0:${PORT}" --module config.wsgi:application --master --processes 4 --threads 2
uwsgi --ini uwsgi.ini:application
