# -*- coding: utf-8 -*-

"""
Django settings for chise project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from django.utils.translation import ugettext_lazy as _
import os
import json

with open('settings.json') as f:
    settings_file = json.load(f)


# Project Vars
PROJECT_CODENAME = 'chise'
PROJECT_NAME = settings_file['project']['name']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rxvm&*m3nssx^5=@bd&2@8b3mqbqpa((8!i^7))b$ou#y1@qns'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = settings_file['project']['debug']

ALLOWED_HOSTS = ['*']

CELERY_BROKER_URL = settings_file['celery']['broker_url']


# Application definition

INSTALLED_APPS = [
    'django_extensions',
    'rosetta',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chise.core',
    'chise.execution',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'
]

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

ROOT_URLCONF = 'chise.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'chise.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': settings_file['database']['name'],
        'USER': settings_file['database']['user'],
        'PASSWORD': settings_file['database']['password'],
        'HOST': settings_file['database']['host'],
        'PORT': settings_file['database']['port'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = settings_file['project']['language']

TIME_ZONE = settings_file['project']['timezone']

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOCALE_PATHS = (
    (os.path.join(BASE_DIR, 'locale')),
)

LANGUAGES = (
    ('en', _('English')),
    ('pt_br', _('Brazilian')),
)

FIREFOX_BIN = settings_file['bin']['firefox']
FIREFOX_PROFILE = settings_file['etc']['firefox_profile']

GECKODRIVER_BIN = settings_file['bin']['geckodriver']