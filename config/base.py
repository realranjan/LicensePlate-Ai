"""
Base configuration settings for License Plate Recognition System.
Contains common settings shared across all environments.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Project root directory (one level up from config)
PROJECT_ROOT = BASE_DIR

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
IMAGES_DIR = DATA_DIR / 'images'
MODELS_DIR = DATA_DIR / 'models'
VIDEOS_DIR = DATA_DIR / 'videos'
DATABASES_DIR = DATA_DIR / 'databases'

# Output directories
OUTPUTS_DIR = PROJECT_ROOT / 'outputs'
DETECTIONS_DIR = OUTPUTS_DIR / 'detections'
CROPS_DIR = OUTPUTS_DIR / 'crops'
OUTPUT_VIDEOS_DIR = OUTPUTS_DIR / 'videos'
TEMP_DIR = OUTPUTS_DIR / 'temp'

# ML Models directories
ML_MODELS_DIR = PROJECT_ROOT / 'ml_models'
YOLOV5_DIR = ML_MODELS_DIR / 'yolov5'
DETECTION_SCRIPTS_DIR = ML_MODELS_DIR / 'detection'

# Web app directories
WEB_APP_DIR = PROJECT_ROOT / 'web_app'
TEMPLATES_DIR = WEB_APP_DIR / 'templates'
STATIC_DIR = WEB_APP_DIR / 'static'

# Desktop app directory
DESKTOP_APP_DIR = PROJECT_ROOT / 'desktop_app'

# Documentation directory
DOCS_DIR = PROJECT_ROOT / 'docs'
NOTEBOOKS_DIR = DOCS_DIR / 'notebooks'

# Scripts directory
SCRIPTS_DIR = PROJECT_ROOT / 'scripts'

# Model file paths
DEFAULT_MODEL_PATH = MODELS_DIR / 'best.pt'
BACKUP_MODEL_PATH = MODELS_DIR / '1500img.pt'

# Default image processing settings
DEFAULT_IMAGE_SIZE = 640
DEFAULT_CONFIDENCE_THRESHOLD = 0.25
DEFAULT_IOU_THRESHOLD = 0.45

# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']

# Output settings
SAVE_CROPS = True
SAVE_DETECTIONS = True
CLEANUP_TEMP_FILES = True
TEMP_FILE_RETENTION_HOURS = 24