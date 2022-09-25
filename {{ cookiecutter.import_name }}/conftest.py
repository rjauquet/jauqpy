import os
from unittest.mock import patch

import pytest
from django.db import connection, utils
from django.apps import apps
from django.conf import settings

from {{ cookiecutter.import_name }}.{{ cookiecutter.app }}.constants import ENVIRONMENT_TESTING

@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop():
    """
    Modified from https://stackoverflow.com/questions/61607752/how-to-test-unmanaged-models-using-pytest-django
    """
    from django.apps import apps

    os.environ['ENVIRONMENT'] = ENVIRONMENT_TESTING

    unmanaged_models = []
    for app in apps.get_app_configs():
        unmanaged_models += [m for m in app.get_models() if not m._meta.managed]
    for m in unmanaged_models:
        m._meta.managed = True

@pytest.fixture(scope="session", autouse=True)
def always_patch(request):

    patches = [
        # this is slow when it is initialized, so we're just patching for tests
        patch('django.core.mail.message.make_msgid'),
    ]
    for p in patches:
        p.start()

    def unpatch():
        for p in patches:
            p.stop()

    request.addfinalizer(unpatch)


