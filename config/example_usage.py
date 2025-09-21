#!/usr/bin/env python3
"""
Example usage of the configuration system in different components.
This file demonstrates how to integrate the config system with existing code.
"""

import sys
import os
from pathlib import Path

# Add project root to path (do this in your scripts)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def example_ml_script():
    """Example of using config in ML detection scripts."""
    print("ML Script Configuration Example:")
    print("-" * 40)
    
    from config.utils import get_ml_settings, get_output_dirs, ensure_directories
    
    # Ensure output directories exist
    ensure_directories()
    
    # Get ML configuration
    ml_config = get_ml_settings()
    output_dirs = get_output_dirs()
    
    print(f"Model path: {ml_config['model_path']}")
    print(f"Confidence threshold: {ml_config['confidence_threshold']}")
    print(f"Image size: {ml_config['image_size']}")
    print(f"GPU enabled: {ml_config['enable_gpu']}")
    print(f"Output directory: {output_dirs['detections']}")
    
    # Example of how to use in detection script:
    """
    # In your detect.py script:
    from config.utils import get_ml_settings, get_output_dirs
    
    ml_config = get_ml_settings()
    output_dirs = get_output_dirs()
    
    # Load model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=ml_config['model_path'])
    model.conf = ml_config['confidence_threshold']
    
    # Set output directory
    save_dir = output_dirs['detections']
    """


def example_desktop_app():
    """Example of using config in desktop GUI application."""
    print("\nDesktop App Configuration Example:")
    print("-" * 40)
    
    from config.utils import get_config, get_data_dirs, get_ml_settings
    
    config = get_config()
    data_dirs = get_data_dirs()
    ml_settings = get_ml_settings()
    
    print(f"Environment: {config.ENVIRONMENT}")
    print(f"Images directory: {data_dirs['images']}")
    print(f"Model path: {ml_settings['model_path']}")
    print(f"Max upload size: {config.MAX_UPLOAD_SIZE}")
    
    # Example of how to use in gui.py:
    """
    # In your gui.py script:
    from config.utils import get_config, get_data_dirs, get_ml_settings
    
    config = get_config()
    data_dirs = get_data_dirs()
    ml_settings = get_ml_settings()
    
    # Configure file dialog
    filetypes = [(ext.upper(), f"*{ext}") for ext in config.ALLOWED_IMAGE_EXTENSIONS]
    
    # Set default directories
    default_dir = data_dirs['images']
    
    # Configure model
    model_path = ml_settings['model_path']
    """


def example_web_app():
    """Example of using config in Django web application."""
    print("\nWeb App Configuration Example:")
    print("-" * 40)
    
    # Django automatically uses the config through settings.py
    # But you can also access config directly in views:
    
    from config.utils import get_ml_settings, get_output_dirs, is_production
    
    ml_settings = get_ml_settings()
    output_dirs = get_output_dirs()
    
    print(f"Is production: {is_production()}")
    print(f"Model path: {ml_settings['model_path']}")
    print(f"Crops directory: {output_dirs['crops']}")
    
    # Example of how to use in Django views:
    """
    # In your views.py:
    from config.utils import get_ml_settings, get_output_dirs
    
    def detect_license_plate(request):
        ml_settings = get_ml_settings()
        output_dirs = get_output_dirs()
        
        # Load model with config settings
        model = load_model(ml_settings['model_path'])
        model.conf = ml_settings['confidence_threshold']
        
        # Save results to configured directory
        results_dir = output_dirs['detections']
    """


def example_environment_switching():
    """Example of switching between environments."""
    print("\nEnvironment Switching Example:")
    print("-" * 40)
    
    from config.utils import get_environment, is_development, is_production
    
    current_env = get_environment()
    print(f"Current environment: {current_env}")
    print(f"Is development: {is_development()}")
    print(f"Is production: {is_production()}")
    
    # Example of environment-specific behavior:
    """
    from config.utils import is_development, get_config
    
    config = get_config()
    
    if is_development():
        # Development-specific settings
        print("Running in development mode")
        verbose_logging = config.VERBOSE_LOGGING
        save_debug = config.SAVE_DEBUG_IMAGES
    else:
        # Production-specific settings
        print("Running in production mode")
        max_requests = config.MAX_REQUESTS_PER_MINUTE
        enable_monitoring = config.METRICS_ENABLED
    """


if __name__ == "__main__":
    example_ml_script()
    example_desktop_app()
    example_web_app()
    example_environment_switching()
    
    print("\n" + "=" * 50)
    print("Configuration system is ready to use!")
    print("See config/README.md for detailed documentation.")