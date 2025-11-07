# -*- coding: utf-8 -*-
"""Django settings for bots project."""

import os
import platform
from pathlib import Path

import bots
from bots.botsinit import BotsConfig


BOTS_PATH = bots.__path__[0]

# BOTSENV
BOTSENV = os.environ.get('BOTSENV') or os.environ.get('USER') or 'default'
BOTS_CONFIG_DIR = os.path.abspath(os.path.dirname(__file__))

# BOTSSYS
config = BotsConfig()
config.read(os.path.join(BOTS_CONFIG_DIR, 'bots.ini'))
BOTSSYS = os.environ.get('BOTSSYS_DIR') or config.get('directories', 'botssys', 'botssys')
if os.path.sep not in BOTSSYS:
    # Set absolute botssys path relative to config directory (not bots package)
    # Go up two levels from config dir to get to env/default, then add botssys
    BOTSSYS = os.path.join(os.path.dirname(os.path.dirname(BOTS_CONFIG_DIR)), BOTSSYS)

HOSTNAME = platform.node()

# Load environment variables from .env file if it exists
env_file = Path(__file__).resolve().parent.parent.parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ.setdefault(key.strip(), value.strip())

# *******settings for sending bots error reports via email**********************************
# Configure email recipients
MANAGERS = (
    # bots will send error reports to the MANAGERS
    ('EDI Admin', os.environ.get('EMAIL_RECIPIENT', 'your-email@example.com')),
)

# Gmail SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')  # Your Gmail address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')  # Gmail App Password
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', EMAIL_HOST_USER)
EMAIL_SUBJECT_PREFIX = '[Bots EDI] '

# *********database settings*************************
# Database configuration from environment variables
DATABASE_ENGINE = os.environ.get('DATABASE_ENGINE', 'sqlite3')

if DATABASE_ENGINE == 'sqlite3':
    # SQLite database (default bots database)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BOTSSYS, 'sqlitedb', 'botsdb'),
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
            "OPTIONS": {},
        }
    }
elif DATABASE_ENGINE in ['postgresql', 'postgresql_psycopg2']:
    # PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DATABASE_NAME', 'botsdb'),
            'USER': os.environ.get('DATABASE_USER', 'bots'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DATABASE_PORT', '5432'),
            'OPTIONS': {},
        }
    }
elif DATABASE_ENGINE == 'mysql':
    # MySQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DATABASE_NAME', 'botsdb'),
            'USER': os.environ.get('DATABASE_USER', 'bots'),
            'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
            'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
            'PORT': os.environ.get('DATABASE_PORT', '3306'),
            'OPTIONS': {'use_unicode': True, 'charset': 'utf8', 'init_command': 'SET storage_engine=INNODB'},
        }
    }
else:
    # Fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BOTSSYS, 'sqlitedb', 'botsdb'),
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
            "OPTIONS": {},
        }
    }
# # MySQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'botsdb',
#         'USER': 'bots',
#         'PASSWORD': 'botsbots',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {'use_unicode':True,'charset':'utf8','init_command': 'SET storage_engine=INNODB'},
#     }
# }
# PostgreSQL:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'botsdb',
#         'USER': 'bots',
#         'PASSWORD': 'botsbots',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         'OPTIONS': {},
#     }
# }

# *********setting date/time zone and formats *************************
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')
# Bots engine always use localtime
USE_TZ = False

# ******language code/internationalization*************************
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
# LANGUAGE_CODE = 'nl'
# LANGUAGE_CODE = 'fr'
USE_I18N = True

# *************************************************************************
# *********other django setting. please consult django docs.***************
# *************************************************************************
# *************************************************************************

# *********path settings*************************
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BOTSSYS, 'static')
ROOT_URLCONF = 'bots.urls'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/bots/home'
LOGOUT_URL = '/logout/'
# LOGOUT_REDIRECT_URL = # not such parameter; is set in urls.py
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',') if os.environ.get('ALLOWED_HOSTS') else ['*']

# *********sessions, cookies, log out time*************************
SESSION_EXPIRE_AT_BROWSER_CLOSE = True    # True: always log in when browser is closed
SESSION_COOKIE_AGE = 3600                 # seconds a user needs to login when no activity
SESSION_SAVE_EVERY_REQUEST = True         # if True: SESSION_COOKIE_AGE is interpreted as: since last activity
SESSION_COOKIE_NAME = f"bots_sessionid_{BOTSENV}"
CSRF_COOKIE_NAME = f"bots_csrftoken_{BOTSENV}"

# set in bots.ini or environment
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')
# TEMPLATE_DEBUG = DEBUG
SITE_ID = 1
# Make this unique, and don't share it with anybody.
# SECURITY WARNING: Use environment variable in production!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', "e^)aa+0m-ya6_@8)3hqxhw&zb-mx_sz(s8e5qb=5^-=u7!a+j4")

# *******includes for django*************************************************************************
LOCALE_PATHS = (
    os.path.join(BOTS_PATH, 'locale'),
)

# save uploaded file (=plugin) always to file. no path for temp storage is used, so system default is used.
FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bots',
    'usersys',  # Modern EDI Interface and API
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
        'DIRS': [
            os.path.join(BOTS_PATH, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bots.bots_context.set_context',
            ],
        },
    },
]

# Password validation
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


# ========================================
# Security Settings for Production
# ========================================

# Import additional security settings if available
try:
    from .security_settings import *
except ImportError:
    pass

# Security Middleware (ensure these are in MIDDLEWARE list above)
# - django.middleware.security.SecurityMiddleware
# - django.middleware.csrf.CsrfViewMiddleware
# - django.middleware.clickjacking.XFrameOptionsMiddleware

# SSL/HTTPS Settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
if SECURE_SSL_REDIRECT:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Cookie Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
if SECURE_SSL_REDIRECT:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# ========================================
# Performance Settings
# ========================================

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'bots-cache',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# For production with Redis:
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         },
#         'KEY_PREFIX': 'bots',
#         'TIMEOUT': 300,
#     }
# }

# Database Connection Pooling (for production)
# Requires: pip install django-db-connection-pool
# DATABASES['default']['ENGINE'] = 'dj_db_conn_pool.backends.postgresql'
# DATABASES['default']['POOL_OPTIONS'] = {
#     'POOL_SIZE': 10,
#     'MAX_OVERFLOW': 10,
# }

# Gzip Compression
# Add 'django.middleware.gzip.GZipMiddleware' to MIDDLEWARE at the top

# ========================================
# Partner Portal Settings
# ========================================

PARTNER_SESSION_TIMEOUT = int(os.environ.get('PARTNER_SESSION_TIMEOUT', '1800'))
PARTNER_MAX_UPLOAD_SIZE = int(os.environ.get('PARTNER_MAX_UPLOAD_SIZE', '10485760'))
PARTNER_FAILED_LOGIN_LOCKOUT = int(os.environ.get('PARTNER_FAILED_LOGIN_LOCKOUT', '5'))
PARTNER_LOCKOUT_DURATION = int(os.environ.get('PARTNER_LOCKOUT_DURATION', '900'))
PARTNER_PASSWORD_MIN_LENGTH = int(os.environ.get('PARTNER_PASSWORD_MIN_LENGTH', '8'))

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = PARTNER_MAX_UPLOAD_SIZE
DATA_UPLOAD_MAX_MEMORY_SIZE = PARTNER_MAX_UPLOAD_SIZE
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Allowed file extensions
ALLOWED_UPLOAD_EXTENSIONS = ['.edi', '.x12', '.txt', '.xml']

# ========================================
# Logging Configuration
# ========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BOTSSYS, 'logging', 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BOTSSYS, 'logging', 'security.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'usersys': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}
