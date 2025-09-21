"""
Production-specific configuration settings.
Used for production deployment with security and performance optimizations.
"""

from .base import *
import os

# Production environment flag
ENVIRONMENT = 'production'

# Django settings for production
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Security settings for production
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set in production")

# Security middleware and settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'lpui_prod'),
        'USER': os.environ.get('DB_USER', 'lpui'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Static files configuration for production
STATIC_URL = '/static/'
STATIC_ROOT = os.environ.get('STATIC_ROOT', PROJECT_ROOT / 'staticfiles')
STATICFILES_DIRS = [STATIC_DIR]

# Media files configuration for production
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', OUTPUTS_DIR)

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_ROOT / 'logs' / 'production.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_ROOT / 'logs' / 'errors.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'lpui': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ML Model settings for production
MODEL_PATH = os.environ.get('MODEL_PATH', DEFAULT_MODEL_PATH)
CONFIDENCE_THRESHOLD = float(os.environ.get('CONFIDENCE_THRESHOLD', '0.5'))  # Higher threshold for production
IOU_THRESHOLD = float(os.environ.get('IOU_THRESHOLD', '0.45'))
IMAGE_SIZE = int(os.environ.get('IMAGE_SIZE', '640'))

# Production-specific paths
TEMP_UPLOAD_DIR = TEMP_DIR / 'uploads'

# Performance settings for production
CACHE_MODELS = True  # Cache models in memory for better performance
ENABLE_GPU = os.environ.get('ENABLE_GPU', 'true').lower() == 'true'
MAX_CONCURRENT_DETECTIONS = int(os.environ.get('MAX_CONCURRENT_DETECTIONS', '5'))

# Production flags
SAVE_DEBUG_IMAGES = False
VERBOSE_LOGGING = False
ENABLE_PROFILING = False

# File cleanup settings for production
AUTO_CLEANUP_TEMP = True
CLEANUP_INTERVAL_MINUTES = int(os.environ.get('CLEANUP_INTERVAL_MINUTES', '30'))

# Rate limiting and resource management
MAX_REQUESTS_PER_MINUTE = int(os.environ.get('MAX_REQUESTS_PER_MINUTE', '60'))
MAX_FILE_SIZE_MB = int(os.environ.get('MAX_FILE_SIZE_MB', '10'))
REQUEST_TIMEOUT_SECONDS = int(os.environ.get('REQUEST_TIMEOUT_SECONDS', '30'))

# Monitoring and health checks
HEALTH_CHECK_ENABLED = True
METRICS_ENABLED = True
SENTRY_DSN = os.environ.get('SENTRY_DSN')  # For error tracking