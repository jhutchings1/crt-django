"""
Django settings for crt_portal project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# If ENV is not set explicitly, assume "UNDEFINED".
# Note that when using Docker, ENV is set to "LOCAL" by docker-compose.yml.
# We are using Docker for local development only.
# We are using the UNDEFINED setting for testing.
# For cloud.gov ENV is set in the manifest
environment = os.environ.get('ENV', 'UNDEFINED')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


if environment != 'LOCAL':
    """ This will default to prod settings and locally, setting the env
    to local will allow you to add the variables directly and not have
    to recreate the vacap structure."""
    vcap = json.loads(os.environ['VCAP_SERVICES'])

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = vcap['user-provided'][0]['credentials']['SECRET_KEY']

    db_credentials = vcap['aws-rds'][0]['credentials']

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': db_credentials['db_name'],
            'USER': db_credentials['username'],
            'PASSWORD': db_credentials['password'],
            'HOST': db_credentials['host'],
            'PORT': '',
        }
    }


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'crt-portal.app.cloud.gov',
    'crt-portal-django.app.cloud.gov',
    'crt-portal-django-prod.app.cloud.gov',
    'crt-portal-django-stage.app.cloud.gov',
    'crt-portal-django-dev.app.cloud.gov',
]

if environment != 'UNDEFINED':
    ALLOWED_HOSTS = ['127.0.0.1']
    logger.warning('CIRCLE test host added')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cts_forms',
    'compressor',
    'compressor_toolkit',
    'storages',
    'formtools',
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

ROOT_URLCONF = 'crt_portal.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'crt_portal.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


if environment != 'LOCAL':
    s3_creds = vcap['s3'][0]["credentials"]
    AWS_ACCESS_KEY_ID = s3_creds["access_key_id"]
    AWS_SECRET_ACCESS_KEY = s3_creds["secret_access_key"]
    AWS_STORAGE_BUCKET_NAME = s3_creds["bucket"]
    AWS_S3_REGION_NAME = s3_creds["region"]
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3-{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_QUERYSTRING_AUTH = False
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'

# This is where source assets are collect from by collect static
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
# Enable for admin storage
# MEDIA_URL = 'media/'
# Where assets are served by web server
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
    'compressor.filters.template.TemplateFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]
COMPRESS_PRECOMPILERS = (
    ('module', 'compressor_toolkit.precompilers.ES6Compiler'),
    ('css', 'compressor_toolkit.precompilers.SCSSCompiler'),
)
# COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

if environment == 'LOCAL':
    logger.warning('Importing local settings.')
    from .local_settings import *  # noqa: F401,F403
