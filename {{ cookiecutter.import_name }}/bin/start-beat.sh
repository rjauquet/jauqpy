#!/bin/bash

poetry run python -m celery -A {{ cookiecutter.import_name }}.tasks.tasks beat --loglevel=info
