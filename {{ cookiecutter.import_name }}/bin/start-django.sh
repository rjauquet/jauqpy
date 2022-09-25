#!/bin/bash

# Static files are served with WhiteNoise
# Consider serving these elswhere for production
poetry run python manage.py collectstatic --noinput
poetry run python manage.py migrate
poetry run python -m gunicorn --bind 0.0.0.0:7888 cabinet.api.wsgi
