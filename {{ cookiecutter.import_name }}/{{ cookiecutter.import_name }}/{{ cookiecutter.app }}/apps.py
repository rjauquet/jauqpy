"""
{{ cookiecutter.app }} app config
"""
from django.apps import AppConfig


class {{ cookiecutter.app.title() }}Config(AppConfig):
    """
    Default config for {{ cookiecutter.app }} app
    """
    name = '{{ cookiecutter.import_name }}.{{ cookiecutter.app }}'
