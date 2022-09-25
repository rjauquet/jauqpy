"""
Django app definition for Base app
"""
from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    Base app
    """

    name = '{{ cookiecutter.import_name }}.base'
