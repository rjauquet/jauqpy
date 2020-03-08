"""
{{ cookiecutter.import_name }} specific settings for all environments
"""

from .default import *

INSTALLED_APPS += [
    '{{ cookiecutter.import_name }}.base',
    '{{ cookiecutter.import_name }}.api',
]

# Open API
SWAGGER_SETTINGS = {
    'DEFAULT_INFO': '{{ cookiecutter.import_name }}.api.urls.api_info',
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Bearer',
            'in': 'header'
        }
    },
}
