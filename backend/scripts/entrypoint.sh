#!/usr/bin/env sh

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py loaddata apps/fixtures.json

uwsgi --ini uwsgi.ini --http-socket "0.0.0.0:${PORT}" --mime-file /app/mime.types
