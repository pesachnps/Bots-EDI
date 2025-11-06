"""
Security Settings for Production
Add these settings to your settings.py or import this file in production
"""

import os

# SECURITY WARNING: These settings should be enabled in production!

# Security Middleware Settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') if SECURE_SSL_REDIRECT else None

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000'))  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie Security
SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT  # Only send session cookie over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT  # Only send CSRF cookie over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
CSRF_COOKIE_SAMESITE = 'Lax'

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing
SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking

# Additional Security Headers
SECURE_REFERRER_POLICY = 'same-origin'

# Partner Portal Specific Settings
PARTNER_SESSION_TIMEOUT = int(os.environ.get('PARTNER_SESSION_TIMEOUT', '1800'))  # 30 minutes
PARTNER_MAX_UPLOAD_SIZE = int(os.environ.get('PARTNER_MAX_UPLOAD_SIZE', '10485760'))  # 10 MB
PARTNER_FAILED_LOGIN_LOCKOUT = int(os.environ.get('PARTNER_FAILED_LOGIN_LOCKOUT', '5'))
PARTNER_LOCKOUT_DURATION = int(os.environ.get('PARTNER_LOCKOUT_DURATION', '900'))  # 15 minutes
PARTNER_PASSWORD_MIN_LENGTH = int(os.environ.get('PARTNER_PASSWORD_MIN_LENGTH', '8'))

# Rate Limiting (if using django-ratelimit)
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
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
            'filename': os.path.join(os.environ.get('BOTSSYS', 'botssys'), 'logging', 'django.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.environ.get('BOTSSYS', 'botssys'), 'logging', 'security.log'),
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        'usersys': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

# Cache Configuration for Performance
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# For production, consider using Redis or Memcached:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
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

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')

# Site Configuration
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8080')
SITE_NAME = os.environ.get('SITE_NAME', 'EDI System')

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Allowed file extensions for uploads
ALLOWED_UPLOAD_EXTENSIONS = ['.edi', '.x12', '.txt', '.xml']

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': PARTNER_PASSWORD_MIN_LENGTH,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Admin Security
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')  # Change this in production

# CORS Settings (if needed for API)
# Requires: pip install django-cors-headers
# CORS_ALLOWED_ORIGINS = [
#     "https://yourdomain.com",
# ]
# CORS_ALLOW_CREDENTIALS = True

# Security Checklist for Production:
# 1. Set DEBUG = False
# 2. Set unique SECRET_KEY from environment variable
# 3. Configure ALLOWED_HOSTS properly
# 4. Enable HTTPS (SECURE_SSL_REDIRECT = True)
# 5. Configure proper database (PostgreSQL/MySQL)
# 6. Set up proper email configuration
# 7. Configure caching (Redis/Memcached)
# 8. Set up monitoring and logging
# 9. Regular security updates
# 10. Regular backups
