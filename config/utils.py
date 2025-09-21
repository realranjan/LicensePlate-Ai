"""
Configuration utilities for License Plate Recognition System.
Provides easy access to configuration settings for all components.
"""

import os
import sys
from pathlib import Path

# Add project root to path if not already there
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def get_config():
    """
    Get the appropriate configuration based on environment.
    
    Returns:
        module: Configuration module (development or production)
    """
    environment = os.environ.get('LP_ENVIRONMENT', 'development')
    
    if environment == 'production':
        import config.production as config_module
    else:
        import config.development as config_module
    
    return config_module


def get_model_path():
    """Get the path to the ML model file."""
    config = get_config()
    return config.MODEL_PATH


def get_data_dirs():
    """Get all data directory paths."""
    config = get_config()
    return {
        'data': config.DATA_DIR,
        'images': config.IMAGES_DIR,
        'models': config.MODELS_DIR,
        'videos': config.VIDEOS_DIR,
        'databases': config.DATABASES_DIR,
    }


def get_output_dirs():
    """Get all output directory paths."""
    config = get_config()
    return {
        'outputs': config.OUTPUTS_DIR,
        'detections': config.DETECTIONS_DIR,
        'crops': config.CROPS_DIR,
        'videos': config.OUTPUT_VIDEOS_DIR,
        'temp': config.TEMP_DIR,
    }


def get_ml_settings():
    """Get ML model configuration settings."""
    config = get_config()
    return {
        'model_path': config.MODEL_PATH,
        'confidence_threshold': config.CONFIDENCE_THRESHOLD,
        'iou_threshold': config.IOU_THRESHOLD,
        'image_size': config.IMAGE_SIZE,
        'enable_gpu': getattr(config, 'ENABLE_GPU', True),
        'cache_models': getattr(config, 'CACHE_MODELS', False),
    }


def ensure_directories():
    """
    Ensure all required directories exist.
    Creates directories if they don't exist.
    """
    config = get_config()
    
    directories = [
        config.DATA_DIR,
        config.IMAGES_DIR,
        config.MODELS_DIR,
        config.VIDEOS_DIR,
        config.DATABASES_DIR,
        config.OUTPUTS_DIR,
        config.DETECTIONS_DIR,
        config.CROPS_DIR,
        config.OUTPUT_VIDEOS_DIR,
        config.TEMP_DIR,
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Create logs directory if logging is configured
    if hasattr(config, 'LOGGING'):
        logs_dir = PROJECT_ROOT / 'logs'
        logs_dir.mkdir(exist_ok=True)


def get_environment():
    """Get the current environment name."""
    return os.environ.get('LP_ENVIRONMENT', 'development')


def is_production():
    """Check if running in production environment."""
    return get_environment() == 'production'


def is_development():
    """Check if running in development environment."""
    return get_environment() == 'development'