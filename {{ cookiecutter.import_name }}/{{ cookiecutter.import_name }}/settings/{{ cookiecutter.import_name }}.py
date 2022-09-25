"""
{{ cookiecutter.import_name }} specific settings for all environments
"""
import os
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
from decouple import config

VERSION = config("VERSION", default="0.1.0")

BASE_DIR = Path(__file__).resolve().parent.parent

USE_TZ = True
DEBUG = True
TEST = False

ALLOWED_HOSTS = ["*"]
PROJECT_NAME = "{{ cookiecutter.import_name }}"
ENVIRONMENT = config("ENVIRONMENT", default="local")

CSRF_TRUSTED_ORIGINS = [
    # this is used for local proxy testing via a nginx proxy on port 80
    "http://localhost"
]

SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_extensions",
    "polymorphic",
    "rest_framework",
    "drf_spectacular",
    "{{ cookiecutter.import_name }}.base",
    "{{ cookiecutter.import_name }}.api",
    "{{ cookiecutter.import_name }}.{{ cookiecutter.app }}",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "api/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

# Django Extensions
SHELL_PLUS = "ipython"
IPYTHON_ARGUMENTS = ["--ext", "autoreload"]

DATABASES = {"default": config("DATABASE_URL", cast=dj_database_url.parse)}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ cookiecutter.project_name }} API",
    "DESCRIPTION": "{{ cookiecutter.project_name }} API",
    "VERSION": VERSION,
    "SERVE_INCLUDE_SCHEMA": False,
}

ROOT_URLCONF = "{{ cookiecutter.import_name }}.api.urls"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

CELERYBEAT_SCHEDULE = {
    # "task-name": {
    #    "task": "{{ cookiecutter.import_name }}.tasks.task_name",
    #    "schedule": crontab(minute=30, hour="*/12"),  # run every 12 hours
    # },
}
CELERY_TIMEZONE = "UTC"
