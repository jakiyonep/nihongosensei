from .base import *

import os

SECRET_KEY = os.environ.get('NIHONGOSENSEI_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'name',
        'USER': 'user',
        'PASSWORD': '',
        'HOST': 'host',
        'PORT': '',
    }
}


import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

import django_heroku
django_heroku.settings(locals())

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


#AWS
from nihongosensei.aws.conf import *