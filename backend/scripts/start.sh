#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py loaddata apps/fixtures.json

python manage.py runserver 0.0.0.0:8000
