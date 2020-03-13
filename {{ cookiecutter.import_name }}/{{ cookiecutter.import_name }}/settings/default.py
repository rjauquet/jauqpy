# any non-standard django settings here
# by default, use all of django/conf/global_settings.py

from decouple import config
import dj_database_url

ALLOWED_HOSTS = ['*']
PROJECT_NAME = '{{ cookiecutter.project_name }}'

SECRET_KEY = config('SECRET_KEY')

TEST = False

INSTALLED_APPS = [
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
    'huey.contrib.djhuey',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

STATIC_URL = '/static/'

# Django Extensions
SHELL_PLUS = 'ipython'
IPYTHON_ARGUMENTS = [
    '--ext', 'autoreload',
]

DATABASES = {'default': config('DATABASE_URL', cast=dj_database_url.parse)}

HUEY = {
    'immediate': False,
    'connection': {
        'url': config('REDIS_URL', default='redis://localhost:6379/0')
    },
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
    },
}
