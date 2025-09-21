#!/usr/bin/env python3
"""
Test script to verify configuration integration works correctly.
"""

import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_configuration():
    """Test configuration system integration."""
    print("Testing Configuration System Integration...")
    print("=" * 50)
    
    # Test 1: Basic configuration loading
    from config.utils import get_config, get_environment
    config = get_config()
    env = get_environment()
    print(f"✓ Environment: {env}")
    print(f"✓ Configuration loaded: {config.__name__}")
    
    # Test 2: ML settings
    from config.utils import get_ml_settings
    ml_settings = get_ml_settings()
    print(f"✓ Model path: {ml_settings['model_path']}")
    print(f"✓ Confidence threshold: {ml_settings['confidence_threshold']}")
    
    # Test 3: Directory paths
    from config.utils import get_data_dirs, get_output_dirs
    data_dirs = get_data_dirs()
    output_dirs = get_output_dirs()
    print(f"✓ Data directory: {data_dirs['data']}")
    print(f"✓ Output directory: {output_dirs['outputs']}")
    
    # Test 4: Environment switching
    print("\nTesting environment switching...")
    
    # Test development
    os.environ['LP_ENVIRONMENT'] = 'development'
    dev_config = get_config()
    print(f"✓ Development config: {dev_config.ENVIRONMENT}")
    
    # Test production (with temporary SECRET_KEY)
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['LP_ENVIRONMENT'] = 'production'
    prod_config = get_config()
    print(f"✓ Production config: {prod_config.ENVIRONMENT}")
    
    # Reset to development
    os.environ['LP_ENVIRONMENT'] = 'development'
    if 'SECRET_KEY' in os.environ:
        del os.environ['SECRET_KEY']
    
    # Test 5: Directory creation
    from config.utils import ensure_directories
    ensure_directories()
    print("✓ Directories ensured")
    
    print("\n" + "=" * 50)
    print("✓ All integration tests passed!")
    
    return True

if __name__ == "__main__":
    success = test_configuration()
    sys.exit(0 if success else 1)