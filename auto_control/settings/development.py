"""
Django development settings for auto_control project.

Generated by 'django-admin startproject' using Django 3.2.15.
"""

from .base import *

DEBUG = True

# Development-specific apps
INSTALLED_APPS += ['debug_toolbar', ]

# Development-specific middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
ALLOWED_HOSTS = ['10.50.100.154', 'localhost', '127.0.0.1', '*']

# Emanuel Test DB
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'autocontrol_database',
#         'PORT': '3306',
#         'PASSWORD': '12345678',
#         'USER': 'root',
#         'HOST': 'localhost',
#     }
# }

# Karol Test DB
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
