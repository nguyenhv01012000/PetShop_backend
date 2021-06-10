from .base import *

import os
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '3@6wj-kujdan+1^cr@$53xiox1=m*!!smls%i-zo2f-ob8r*v6')
ALLOWED_HOSTS = ["*"]
DEBUG = True
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': os.environ.get('DATABASE_NAME', 'dev'),
'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
'USER': os.environ.get('DATABASE_USER', 'postgres'),
'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'docker'),
'PORT': os.environ.get('DATABASE_PORT', '5432'),
}
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {pathname} {lineno:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'consumer': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        's6': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': False,
        },
        # 'django.db.backends': {
        #     'level': 'DEBUG',
        #     'handlers': ['console'],
        #     'propagate': False,
        # }
   },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
