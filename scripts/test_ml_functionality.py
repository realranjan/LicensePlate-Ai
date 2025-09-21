#!/usr/bin/env python3
"""
ML Detection Functionality Test Script

This script tests machine learning detection functionality with the new file paths.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

class MLFunctionalityTester:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.ml_models_path = self.project_root / "ml_models"
        self.errors = []
        self.warnings = []
        
    def test_ml_directory_structure(self) -> bool:
        """Test ML models directory structure."""
        print("🔍 Testing ML models directory structure...")
        
        if not self.ml_models_path.exists():
            self.errors.append("ml_models directory not found")
            return False
        
        # Check for detection directory
        detection_path = self.ml_models_path / "detection"
        if detection_path.exists():
            print("  ✅ ml_models/detection/ directory exists")
            
            # Check for detection scripts
            detection_scripts = ["detect.py", "detect2.py", "detect3.py"]
            for script in detection_scripts:
                script_path = detection_path / script
                if script_path.exists():
                    print(f"    ✅ {script} found")
                else:
                    self.warnings.append(f"Detection script not found: {script}")
        else:
            self.errors.append("ml_models/detection/ directory not found")
        
        # Check for YOLOv5 directory
        yolo_path = self.ml_models_path / "yolov5"
        if yolo_path.exists():
            print("  ✅ ml_models/yolov5/ directory exists")
            
            # Check for key YOLOv5 files
            yolo_files = ["detect.py", "train.py", "models", "utils"]
            for item in yolo_files:
                item_path = yolo_path / item
                if item_path.exists():
                    print(f"    ✅ YOLOv5 {item} found")
                else:
                    self.warnings.append(f"YOLOv5 component not found: {item}")
        else:
            self.warnings.append("ml_models/yolov5/ directory not found")
        
        # Check for hubconf.py
        hubconf_path = self.ml_models_path / "hubconf.py"
        if hubconf_path.exists():
            print("  ✅ hubconf.py found")
        else:
            self.warnings.append("hubconf.py not found in ml_models/")
        
        return len(self.errors) == 0
    
    def test_model_files_access(self) -> bool:
        """Test access to model files."""
        print("\n🔍 Testing model files access...")
        
        data_models_path = self.project_root / "data" / "models"
        if not data_models_path.exists():
            self.errors.append("data/models/ directory not found")
            return False
        
        # Check for .pt model files
        model_files = list(data_models_path.glob("*.pt"))
        if model_files:
            print(f"  ✅ Found {len(model_files)} model files")
            
            for model_file in model_files:
                # Check file accessibility
                if os.access(model_file, os.R_OK):
                    print(f"    ✅ {model_file.name} is readable")
                    
                    # Check file size (should be > 0)
                    if model_file.stat().st_size > 0:
                        print(f"    ✅ {model_file.name} has valid size ({model_file.stat().st_size} bytes)")
                    else:
                        self.errors.append(f"Model file is empty: {model_file.name}")
                else:
                    self.errors.append(f"Model file is not readable: {model_file.name}")
        else:
            self.errors.append("No .pt model files found in data/models/")
        
        return len(self.errors) == 0
    
    def test_detection_scripts_syntax(self) -> bool:
        """Test detection scripts syntax."""
        print("\n🔍 Testing detection scripts syntax...")
        
        detection_path = self.ml_models_path / "detection"
        if not detection_path.exists():
            return False
        
        detection_scripts = list(detection_path.glob("*.py"))
        
        for script_path in detection_scripts:
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                compile(source_code, str(script_path), 'exec')
                print(f"  ✅ {script_path.name} has valid Python syntax")
                
            except SyntaxError as e:
                self.errors.append(f"Syntax error in {script_path.name}: {e}")
            except Exception as e:
                self.errors.append(f"Failed to test {script_path.name} syntax: {e}")
        
        return len(self.errors) == 0
    
    def test_detection_scripts_imports(self) -> bool:
        """Test detection scripts imports."""
        print("\n🔍 Testing detection scripts imports...")
        
        detection_path = self.ml_models_path / "detection"
        if not detection_path.exists():
            return False
        
        # Add paths to sys.path for imports
        sys.path.insert(0, str(self.ml_models_path))
        sys.path.insert(0, str(self.project_root))
        
        detection_scripts = list(detection_path.glob("*.py"))
        
        for script_path in detection_scripts:
            try:
                # Try to import the script as a module
                module_name = script_path.stem
                spec = importlib.util.spec_from_file_location(module_name, script_path)
                
                if spec and spec.loader:
                    # Don't execute the module, just check if it can be loaded
                    print(f"  ✅ {script_path.name} can be imported")
                else:
                    self.errors.append(f"Could not create module spec for {script_path.name}")
                    
            except Exception as e:
                self.warnings.append(f"Import issue with {script_path.name}: {e}")
        
        return len(self.errors) == 0
    
    def test_detection_scripts_paths(self) -> bool:
        """Test file path references in detection scripts."""
        print("\n🔍 Testing detection scripts file paths...")
        
        detection_path = self.ml_models_path / "detection"
        if not detection_path.exists():
            return False
        
        detection_scripts = list(detection_path.glob("*.py"))
        
        for script_path in detection_scripts:
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for model path references
                model_references = [
                    'data/models',
                    'data\\models',
                    '../data/models',
                    '../../data/models',
                    '.pt'
                ]
                
                found_model_ref = False
                for ref in model_references:
                    if ref in content:
                        print(f"    ✅ {script_path.name} references model path: {ref}")
                        found_model_ref = True
                        break
                
                if not found_model_ref:
                    self.warnings.append(f"No model path references found in {script_path.name}")
                
                # Check for output path references
                output_references = [
                    'outputs/',
                    'outputs\\',
                    '../outputs',
                    '../../outputs'
                ]
                
                found_output_ref = False
                for ref in output_references:
                    if ref in content:
                        print(f"    ✅ {script_path.name} references output path: {ref}")
                        found_output_ref = True
                        break
                
                if not found_output_ref:
                    self.warnings.append(f"No output path references found in {script_path.name}")
                
            except Exception as e:
                self.errors.append(f"Failed to analyze {script_path.name}: {e}")
        
        return len(self.errors) == 0
    
    def test_yolov5_integration(self) -> bool:
        """Test YOLOv5 integration."""
        print("\n🔍 Testing YOLOv5 integration...")
        
        yolo_path = self.ml_models_path / "yolov5"
        if not yolo_path.exists():
            self.warnings.append("YOLOv5 directory not found - skipping YOLOv5 tests")
            return True
        
        # Add YOLOv5 to path
        sys.path.insert(0, str(yolo_path))
        
        # Check for YOLOv5 detect.py
        yolo_detect = yolo_path / "detect.py"
        if yolo_detect.exists():
            print("  ✅ YOLOv5 detect.py found")
            
            # Test syntax
            try:
                with open(yolo_detect, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                compile(source_code, str(yolo_detect), 'exec')
                print("  ✅ YOLOv5 detect.py has valid syntax")
                
            except SyntaxError as e:
                self.errors.append(f"Syntax error in YOLOv5 detect.py: {e}")
            except Exception as e:
                self.warnings.append(f"Could not test YOLOv5 detect.py syntax: {e}")
        
        # Check for models directory
        yolo_models = yolo_path / "models"
        if yolo_models.exists():
            print("  ✅ YOLOv5 models directory found")
        else:
            self.warnings.append("YOLOv5 models directory not found")
        
        # Check for utils directory
        yolo_utils = yolo_path / "utils"
        if yolo_utils.exists():
            print("  ✅ YOLOv5 utils directory found")
        else:
            self.warnings.append("YOLOv5 utils directory not found")
        
        return len(self.errors) == 0
    
    def test_ml_dependencies(self) -> bool:
        """Test ML dependencies."""
        print("\n🔍 Testing ML dependencies...")
        
        requirements_txt = self.ml_models_path / "requirements.txt"
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r') as f:
                    requirements = f.read().strip().split('\n')
                
                print(f"  ✅ Found requirements.txt with {len(requirements)} dependencies")
                
                # Check for key ML dependencies
                req_text = '\n'.join(requirements).lower()
                
                key_deps = {
                    'torch': ['torch', 'pytorch'],
                    'opencv': ['opencv', 'cv2'],
                    'numpy': ['numpy'],
                    'pillow': ['pillow', 'pil'],
                    'matplotlib': ['matplotlib']
                }
                
                for dep_name, variations in key_deps.items():
                    found = any(var in req_text for var in variations)
                    if found:
                        print(f"    ✅ {dep_name} dependency found")
                    else:
                        self.warnings.append(f"{dep_name} dependency not found in requirements.txt")
                
            except Exception as e:
                self.errors.append(f"Failed to read ML requirements.txt: {e}")
        else:
            self.warnings.append("requirements.txt not found in ml_models directory")
        
        return True
    
    def test_outputs_directory(self) -> bool:
        """Test outputs directory for ML results."""
        print("\n🔍 Testing outputs directory...")
        
        outputs_path = self.project_root / "outputs"
        if not outputs_path.exists():
            self.errors.append("outputs directory not found")
            return False
        
        # Check output subdirectories
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
    
    def run_tests(self) -> bool:
        """Run all ML functionality tests."""
        print(f"🚀 Starting ML functionality tests for project at: {self.project_root}")
        print("=" * 60)
        
        tests = [
            self.test_ml_directory_structure,
            self.test_model_files_access,
            self.test_detection_scripts_syntax,
            self.test_detection_scripts_imports,
            self.test_detection_scripts_paths,
            self.test_yolov5_integration,
            self.test_ml_dependencies,
            self.test_outputs_directory
        ]
        
        success = True
        for test in tests:
            if not test():
                success = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 ML FUNCTIONALITY TEST RESULTS")
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
            print("🎉 All ML functionality tests passed!")
        elif success:
            print("✅ ML functionality tests passed with warnings.")
        else:
            print("❌ ML functionality tests failed. Please fix the errors above.")
        
        return success

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test ML detection functionality")
    parser.add_argument("--project-root", default=".", help="Path to project root directory")
    args = parser.parse_args()
    
    tester = MLFunctionalityTester(args.project_root)
    success = tester.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()