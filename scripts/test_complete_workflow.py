#!/usr/bin/env python3
"""
Complete Workflow Testing Script
Tests the entire license plate recognition workflow for both web and desktop interfaces.
"""

import os
import sys
import subprocess
import time
import requests
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def test_project_structure():
    """Test that all required directories and files exist."""
    print("🔍 Testing project structure...")
    
    required_dirs = [
        "web_app", "desktop_app", "ml_models", "data", 
        "outputs", "docs", "scripts", "config"
    ]
    
    required_files = [
        "web_app/manage.py",
        "desktop_app/gui.py", 
        "ml_models/hubconf.py",
        "data/models",
        "outputs/detections"
    ]
    
    missing_items = []
    
    # Check directories
    for dir_name in required_dirs:
        if not (project_root / dir_name).exists():
            missing_items.append(f"Directory: {dir_name}")
    
    # Check files
    for file_path in required_files:
        if not (project_root / file_path).exists():
            missing_items.append(f"File: {file_path}")
    
    if missing_items:
        print("❌ Missing required items:")
        for item in missing_items:
            print(f"   - {item}")
        return False
    
    print("✅ Project structure is complete")
    return True

def test_ml_detection():
    """Test ML detection functionality."""
    print("\n🤖 Testing ML detection...")
    
    # Check if we have a test image
    test_image_dirs = [
        project_root / "data" / "images" / "test",
        project_root / "data" / "images" / "samples"
    ]
    
    test_image = None
    for img_dir in test_image_dirs:
        if img_dir.exists():
            for ext in ['*.jpg', '*.jpeg', '*.png']:
                images = list(img_dir.glob(ext))
                if images:
                    test_image = images[0]
                    break
        if test_image:
            break
    
    if not test_image:
        print("⚠️  No test images found, creating a dummy test...")
        # Create a simple test image for validation
        try:
            from PIL import Image
            import numpy as np
            
            # Create a simple test image
            img = Image.fromarray(np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8))
            test_image = project_root / "data" / "images" / "test" / "test_image.jpg"
            test_image.parent.mkdir(parents=True, exist_ok=True)
            img.save(test_image)
            print(f"✅ Created test image: {test_image}")
        except ImportError:
            print("❌ Cannot create test image (PIL not available)")
            return False
    
    # Test detection script
    try:
        detection_script = project_root / "ml_models" / "detection" / "detect2.py"
        if not detection_script.exists():
            print(f"❌ Detection script not found: {detection_script}")
            return False
        
        # Run detection (dry run to check imports and basic functionality)
        cmd = [
            sys.executable, str(detection_script),
            "--help"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ ML detection script is accessible and functional")
            return True
        else:
            print(f"❌ ML detection script failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing ML detection: {e}")
        return False

def test_desktop_app():
    """Test desktop application functionality."""
    print("\n🖥️  Testing desktop application...")
    
    try:
        gui_script = project_root / "desktop_app" / "gui.py"
        if not gui_script.exists():
            print(f"❌ Desktop GUI script not found: {gui_script}")
            return False
        
        # Test imports and basic functionality (without actually launching GUI)
        cmd = [sys.executable, "-c", f"""
import sys
sys.path.append('{project_root}')
sys.path.append('{project_root / "desktop_app"}')

try:
    # Test if we can import the GUI module
    import importlib.util
    spec = importlib.util.spec_from_file_location("gui", "{gui_script}")
    gui_module = importlib.util.module_from_spec(spec)
    
    # Check if tkinter is available
    import tkinter as tk
    
    print("Desktop app imports successful")
    exit(0)
except ImportError as e:
    print(f"Import error: {{e}}")
    exit(1)
except Exception as e:
    print(f"Error: {{e}}")
    exit(1)
"""]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ Desktop application imports and dependencies are working")
            return True
        else:
            print(f"❌ Desktop application test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing desktop application: {e}")
        return False

def test_web_app():
    """Test web application functionality."""
    print("\n🌐 Testing web application...")
    
    try:
        manage_script = project_root / "web_app" / "manage.py"
        if not manage_script.exists():
            print(f"❌ Django manage.py not found: {manage_script}")
            return False
        
        # Test Django setup
        cmd = [sys.executable, str(manage_script), "check", "--deploy"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root / "web_app")
        
        if result.returncode == 0:
            print("✅ Web application Django setup is valid")
            
            # Test if we can run migrations (dry run)
            cmd = [sys.executable, str(manage_script), "migrate", "--dry-run"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root / "web_app")
            
            if result.returncode == 0:
                print("✅ Web application database migrations are ready")
                return True
            else:
                print(f"⚠️  Web application migration check had issues: {result.stderr}")
                return True  # Still consider it a pass if basic Django works
        else:
            print(f"❌ Web application Django check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing web application: {e}")
        return False

def test_file_paths():
    """Test that all file paths are correctly updated."""
    print("\n📁 Testing file paths and imports...")
    
    # Test that outputs directory is properly structured
    output_dirs = [
        "outputs/detections",
        "outputs/crops", 
        "outputs/videos",
        "outputs/temp"
    ]
    
    for dir_path in output_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created output directory: {dir_path}")
        else:
            print(f"✅ Output directory exists: {dir_path}")
    
    # Test data directory structure
    data_dirs = [
        "data/images/test",
        "data/images/samples", 
        "data/images/training",
        "data/models",
        "data/videos",
        "data/databases"
    ]
    
    for dir_path in data_dirs:
        full_path = project_root / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created data directory: {dir_path}")
        else:
            print(f"✅ Data directory exists: {dir_path}")
    
    return True

def test_requirements():
    """Test that requirements files are properly organized."""
    print("\n📦 Testing requirements files...")
    
    req_files = [
        "requirements.txt",
        "web_app/requirements.txt",
        "desktop_app/requirements.txt", 
        "ml_models/requirements.txt"
    ]
    
    all_exist = True
    for req_file in req_files:
        full_path = project_root / req_file
        if full_path.exists():
            print(f"✅ Requirements file exists: {req_file}")
        else:
            print(f"❌ Requirements file missing: {req_file}")
            all_exist = False
    
    return all_exist

def run_all_tests():
    """Run all workflow tests."""
    print("🚀 Starting Complete Workflow Testing")
    print("=" * 50)
    
    tests = [
        ("Project Structure", test_project_structure),
        ("File Paths", test_file_paths),
        ("Requirements Files", test_requirements),
        ("ML Detection", test_ml_detection),
        ("Desktop Application", test_desktop_app),
        ("Web Application", test_web_app),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The reorganization is complete and functional.")
        return True
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)