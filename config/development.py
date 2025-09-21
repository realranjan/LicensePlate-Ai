"""
Development-specific configuration settings.
Used for local development and testing.
"""

from .base import *

# Development environment flag
ENVIRONMENT = 'development'

# Django settings for development
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Security settings (relaxed for development)
SECRET_KEY = 'django-insecure-ka#e_%=w^xzimo2mzc1d__zf-y51@c&jtfv=^h-2b@$)fcmjnh'

# Database configuration for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASES_DIR / 'db.sqlite3',
    }
}

# Static files configuration for development
STATICFILES_DIRS = [STATIC_DIR]
STATIC_URL = '/static/'
STATIC_ROOT = None  # Not needed in development

# Media files configuration for development
MEDIA_URL = '/media/'
MEDIA_ROOT = OUTPUTS_DIR

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': PROJECT_ROOT / 'logs' / 'development.log',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'lpui': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# ML Model settings for development
MODEL_PATH = DEFAULT_MODEL_PATH
CONFIDENCE_THRESHOLD = 0.25  # Lower threshold for development testing
IOU_THRESHOLD = 0.45
IMAGE_SIZE = 640

# Development-specific paths
TEMP_UPLOAD_DIR = TEMP_DIR / 'uploads'
DEV_SAMPLE_IMAGES_DIR = IMAGES_DIR / 'samples'

# Performance settings for development
CACHE_MODELS = False  # Don't cache models in development for easier testing
ENABLE_GPU = True  # Use GPU if available
MAX_CONCURRENT_DETECTIONS = 2  # Limit concurrent processing

# Development flags
SAVE_DEBUG_IMAGES = True
VERBOSE_LOGGING = True
ENABLE_PROFILING = False

# File cleanup settings for development
AUTO_CLEANUP_TEMP = False  # Keep temp files for debugging
CLEANUP_INTERVAL_MINUTES = 60