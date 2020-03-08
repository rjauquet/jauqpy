"""
{{ cookiecutter.import_name }} specific settings for all environments
"""

from .default import *

INSTALLED_APPS += [
    '{{ cookiecutter.import_name }}.base'
]
