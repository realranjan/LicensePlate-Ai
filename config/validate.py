#!/usr/bin/env python3
"""
Configuration validation script for License Plate Recognition System.
Validates that all configuration files are properly set up and accessible.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def validate_config():
    """Validate configuration setup."""
    print("Validating License Plate Recognition System Configuration...")
    print("=" * 60)
    
    errors = []
    warnings = []
    
    # Test importing configurations
    try:
        import config.base
        print("✓ Base configuration loaded successfully")
    except Exception as e:
        errors.append(f"Failed to load base configuration: {e}")
    
    try:
        import config.development
        print("✓ Development configuration loaded successfully")
    except Exception as e:
        errors.append(f"Failed to load development configuration: {e}")
    
    try:
        # Temporarily set required environment variables for production config test
        original_secret = os.environ.get('SECRET_KEY')
        os.environ['SECRET_KEY'] = 'test-key-for-validation'
        import config.production
        if original_secret is None:
            del os.environ['SECRET_KEY']
        else:
            os.environ['SECRET_KEY'] = original_secret
        print("✓ Production configuration loaded successfully")
    except Exception as e:
        errors.append(f"Failed to load production configuration: {e}")
    
    # Test configuration utilities
    try:
        from config.utils import get_config, get_ml_settings, ensure_directories
        config = get_config()
        ml_settings = get_ml_settings()
        print("✓ Configuration utilities working")
    except Exception as e:
        errors.append(f"Configuration utilities failed: {e}")
    
    # Check directory structure
    try:
        from config.utils import get_data_dirs, get_output_dirs
        data_dirs = get_data_dirs()
        output_dirs = get_output_dirs()
        
        # Check if key directories exist or can be created
        for name, path in data_dirs.items():
            if not path.exists():
                warnings.append(f"Data directory does not exist: {path}")
        
        for name, path in output_dirs.items():
            if not path.exists():
                warnings.append(f"Output directory does not exist: {path}")
        
        print("✓ Directory structure validated")
    except Exception as e:
        errors.append(f"Directory validation failed: {e}")
    
    # Check model file
    try:
        from config.utils import get_model_path
        model_path = get_model_path()
        if not model_path.exists():
            warnings.append(f"Model file does not exist: {model_path}")
        else:
            print("✓ Model file found")
    except Exception as e:
        warnings.append(f"Could not check model file: {e}")
    
    # Test Django settings integration
    try:
        os.environ['DJANGO_ENVIRONMENT'] = 'development'
        sys.path.insert(0, str(PROJECT_ROOT / 'web_app'))
        from lpUI import settings
        print("✓ Django settings integration working")
    except Exception as e:
        errors.append(f"Django settings integration failed: {e}")
    
    # Print results
    print("\n" + "=" * 60)
    
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ✗ {error}")
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    
    if not errors and not warnings:
        print("✓ All configuration checks passed!")
    elif not errors:
        print("✓ Configuration is valid (with warnings)")
    else:
        print("✗ Configuration validation failed")
        return False
    
    print("\nTo create missing directories, run:")
    print("  python -c \"from config.utils import ensure_directories; ensure_directories()\"")
    
    return len(errors) == 0


if __name__ == "__main__":
    success = validate_config()
    sys.exit(0 if success else 1)