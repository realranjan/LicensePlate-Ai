#!/usr/bin/env python3
"""
File Path Resolution Test Script

This script tests that all file paths resolve correctly in the reorganized
License Plate Recognition System structure.
"""

import os
import sys
from pathlib import Path
import importlib.util

class FilePathTester:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.errors = []
        self.warnings = []
        
    def test_web_app_paths(self) -> bool:
        """Test Django web app file path resolution."""
        print("🔍 Testing web app file paths...")
        
        web_app_path = self.project_root / "web_app"
        if not web_app_path.exists():
            self.errors.append("web_app directory not found")
            return False
        
        # Test manage.py path resolution
        manage_py = web_app_path / "manage.py"
        if manage_py.exists():
            print("  ✅ manage.py found in web_app/")
            
            # Check if manage.py references correct settings
            try:
                with open(manage_py, 'r') as f:
                    content = f.read()
                    if 'lpUI.settings' in content:
                        print("  ✅ manage.py references correct settings module")
                    else:
                        self.warnings.append("manage.py may not reference correct settings module")
            except Exception as e:
                self.warnings.append(f"Could not read manage.py: {e}")
        
        # Test Django settings path resolution
        settings_py = web_app_path / "lpUI" / "settings.py"
        if settings_py.exists():
            print("  ✅ Django settings.py found")
            
            # Check template and static file paths in settings
            try:
                with open(settings_py, 'r') as f:
                    content = f.read()
                    
                    # Check for template directories
                    if 'templates' in content:
                        print("  ✅ Template paths configured in settings")
                    else:
                        self.warnings.append("Template paths may not be configured in settings")
                    
                    # Check for static files configuration
                    if 'STATIC' in content:
                        print("  ✅ Static files configuration found in settings")
                    else:
                        self.warnings.append("Static files may not be configured in settings")
                        
            except Exception as e:
                self.warnings.append(f"Could not analyze settings.py: {e}")
        
        return len(self.errors) == 0
    
    def test_desktop_app_paths(self) -> bool:
        """Test desktop app file path resolution."""
        print("\n🔍 Testing desktop app file paths...")
        
        desktop_app_path = self.project_root / "desktop_app"
        if not desktop_app_path.exists():
            self.errors.append("desktop_app directory not found")
            return False
        
        # Test gui.py
        gui_py = desktop_app_path / "gui.py"
        if gui_py.exists():
            print("  ✅ gui.py found in desktop_app/")
            
            # Check if gui.py references correct ML model paths
            try:
                with open(gui_py, 'r') as f:
                    content = f.read()
                    
                    # Look for references to ml_models directory
                    if 'ml_models' in content:
                        print("  ✅ gui.py references ml_models directory")
                    else:
                        self.warnings.append("gui.py may not reference correct ml_models path")
                    
                    # Look for data directory references
                    if 'data/' in content or 'data\\' in content:
                        print("  ✅ gui.py references data directory")
                    else:
                        self.warnings.append("gui.py may not reference correct data paths")
                        
            except Exception as e:
                self.warnings.append(f"Could not analyze gui.py: {e}")
        
        return len(self.errors) == 0
    
    def test_ml_model_paths(self) -> bool:
        """Test ML model file path resolution."""
        print("\n🔍 Testing ML model file paths...")
        
        ml_models_path = self.project_root / "ml_models"
        if not ml_models_path.exists():
            self.errors.append("ml_models directory not found")
            return False
        
        # Test detection scripts
        detection_path = ml_models_path / "detection"
        if detection_path.exists():
            detection_scripts = ["detect.py", "detect2.py", "detect3.py"]
            
            for script_name in detection_scripts:
                script_path = detection_path / script_name
                if script_path.exists():
                    print(f"  ✅ {script_name} found in ml_models/detection/")
                    
                    # Check if detection scripts reference correct model paths
                    try:
                        with open(script_path, 'r') as f:
                            content = f.read()
                            
                            # Look for model file references
                            if 'data/models' in content or 'data\\models' in content:
                                print(f"    ✅ {script_name} references correct model path")
                            elif '.pt' in content:
                                self.warnings.append(f"{script_name} may have hardcoded model paths")
                            
                            # Look for output directory references
                            if 'outputs/' in content or 'outputs\\' in content:
                                print(f"    ✅ {script_name} references outputs directory")
                            
                    except Exception as e:
                        self.warnings.append(f"Could not analyze {script_name}: {e}")
        
        # Test hubconf.py
        hubconf_py = ml_models_path / "hubconf.py"
        if hubconf_py.exists():
            print("  ✅ hubconf.py found in ml_models/")
        
        return len(self.errors) == 0
    
    def test_data_file_paths(self) -> bool:
        """Test data file path accessibility."""
        print("\n🔍 Testing data file paths...")
        
        data_path = self.project_root / "data"
        if not data_path.exists():
            self.errors.append("data directory not found")
            return False
        
        # Test model files accessibility
        models_path = data_path / "models"
        if models_path.exists():
            model_files = list(models_path.glob("*.pt"))
            if model_files:
                print(f"  ✅ Found {len(model_files)} accessible model files")
                for model_file in model_files:
                    if model_file.is_file() and os.access(model_file, os.R_OK):
                        print(f"    ✅ {model_file.name} is readable")
                    else:
                        self.errors.append(f"Model file not readable: {model_file.name}")
            else:
                self.warnings.append("No model files found in data/models/")
        
        # Test image directories
        images_path = data_path / "images"
        if images_path.exists():
            subdirs = ["test", "samples", "training"]
            for subdir in subdirs:
                subdir_path = images_path / subdir
                if subdir_path.exists():
                    image_files = list(subdir_path.glob("*.jpg")) + list(subdir_path.glob("*.png"))
                    if image_files:
                        print(f"  ✅ Found {len(image_files)} images in data/images/{subdir}/")
                    else:
                        self.warnings.append(f"No image files found in data/images/{subdir}/")
        
        # Test database accessibility
        db_path = data_path / "databases" / "db.sqlite3"
        if db_path.exists():
            if os.access(db_path, os.R_OK):
                print("  ✅ Database file is accessible")
            else:
                self.errors.append("Database file is not readable")
        
        return len(self.errors) == 0
    
    def test_output_paths(self) -> bool:
        """Test output directory accessibility."""
        print("\n🔍 Testing output paths...")
        
        outputs_path = self.project_root / "outputs"
        if not outputs_path.exists():
            self.errors.append("outputs directory not found")
            return False
        
        # Test output subdirectories
        output_subdirs = ["detections", "crops", "videos", "temp"]
        for subdir in output_subdirs:
            subdir_path = outputs_path / subdir
            if subdir_path.exists():
                if os.access(subdir_path, os.W_OK):
                    print(f"  ✅ outputs/{subdir}/ is writable")
                else:
                    self.errors.append(f"outputs/{subdir}/ is not writable")
            else:
                self.warnings.append(f"outputs/{subdir}/ directory not found")
        
        return len(self.errors) == 0
    
    def test_config_imports(self) -> bool:
        """Test configuration file imports."""
        print("\n🔍 Testing configuration imports...")
        
        config_path = self.project_root / "config"
        if not config_path.exists():
            self.errors.append("config directory not found")
            return False
        
        # Add project root to Python path
        sys.path.insert(0, str(self.project_root))
        
        # Test config module imports
        config_files = ["base.py", "development.py", "production.py"]
        for config_file in config_files:
            config_file_path = config_path / config_file
            if config_file_path.exists():
                try:
                    module_name = f"config.{config_file[:-3]}"  # Remove .py extension
                    spec = importlib.util.spec_from_file_location(module_name, config_file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        print(f"  ✅ config.{config_file[:-3]} imports successfully")
                    else:
                        self.errors.append(f"Could not create spec for {module_name}")
                except Exception as e:
                    self.errors.append(f"Failed to import config.{config_file[:-3]}: {e}")
        
        return len(self.errors) == 0
    
    def test_script_paths(self) -> bool:
        """Test script file paths."""
        print("\n🔍 Testing script paths...")
        
        scripts_path = self.project_root / "scripts"
        if not scripts_path.exists():
            self.errors.append("scripts directory not found")
            return False
        
        # Test sample.py
        sample_py = scripts_path / "sample.py"
        if sample_py.exists():
            print("  ✅ sample.py found in scripts/")
            
            # Check if sample.py references correct data paths
            try:
                with open(sample_py, 'r') as f:
                    content = f.read()
                    
                    if 'data/' in content or 'data\\' in content:
                        print("  ✅ sample.py references data directory")
                    else:
                        self.warnings.append("sample.py may not reference correct data paths")
                        
            except Exception as e:
                self.warnings.append(f"Could not analyze sample.py: {e}")
        
        return len(self.errors) == 0
    
    def run_tests(self) -> bool:
        """Run all file path tests."""
        print(f"🚀 Starting file path tests for project at: {self.project_root}")
        print("=" * 60)
        
        tests = [
            self.test_web_app_paths,
            self.test_desktop_app_paths,
            self.test_ml_model_paths,
            self.test_data_file_paths,
            self.test_output_paths,
            self.test_config_imports,
            self.test_script_paths
        ]
        
        success = True
        for test in tests:
            if not test():
                success = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 FILE PATH TEST RESULTS")
        print("=" * 60)
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            success = False
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if success and not self.warnings:
            print("🎉 All file path tests passed!")
        elif success:
            print("✅ File path tests passed with warnings.")
        else:
            print("❌ File path tests failed. Please fix the errors above.")
        
        return success

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test file path resolution in License Plate Recognition project")
    parser.add_argument("--project-root", default=".", help="Path to project root directory")
    args = parser.parse_args()
    
    tester = FilePathTester(args.project_root)
    success = tester.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()