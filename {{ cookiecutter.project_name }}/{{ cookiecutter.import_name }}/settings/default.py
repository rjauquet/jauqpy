# any non-standard django settings here
# by default, use all of django/conf/global_settings.py

from decouple import config
import dj_database_url

ALLOWED_HOSTS = ['*']
PROJECT_NAME = '{{ cookiecutter.project_name }}'

SECRET_KEY = config('SECRET_KEY')

TEST = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_extensions',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
)

DATABASES = {'default': config('DATABASE_URL', cast=dj_database_url.parse)}


