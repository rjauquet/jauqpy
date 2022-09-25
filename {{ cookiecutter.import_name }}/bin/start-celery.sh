#!/bin/bash

poetry run python manage.py migrate
poetry run python -m celery -A {{ cookiecutter.import_name }}.tasks.tasks worker --loglevel=info
