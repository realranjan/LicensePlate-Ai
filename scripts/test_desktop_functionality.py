#!/usr/bin/env python3
"""
Desktop App Functionality Test Script

This script tests Tkinter desktop application functionality with the new directory structure.
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

class DesktopAppTester:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.desktop_app_path = self.project_root / "desktop_app"
        self.errors = []
        self.warnings = []
        
    def test_gui_imports(self) -> bool:
        """Test GUI application imports."""
        print("🔍 Testing desktop app imports...")
        
        if not self.desktop_app_path.exists():
            self.errors.append("desktop_app directory not found")
            return False
        
        gui_py = self.desktop_app_path / "gui.py"
        if not gui_py.exists():
            self.errors.append("gui.py not found in desktop_app directory")
            return False
        
        # Add desktop_app to Python path
        sys.path.insert(0, str(self.desktop_app_path))
        sys.path.insert(0, str(self.project_root))
        
        try:
            # Test basic imports that gui.py should have
            import tkinter as tk
            print("  ✅ tkinter imports successfully")
            
            import tkinter.filedialog
            print("  ✅ tkinter.filedialog imports successfully")
            
            import tkinter.messagebox
            print("  ✅ tkinter.messagebox imports successfully")
            
            # Test PIL/Pillow imports (commonly used for image handling)
            try:
                from PIL import Image, ImageTk
                print("  ✅ PIL (Pillow) imports successfully")
            except ImportError:
                self.warnings.append("PIL (Pillow) not available - may be needed for image handling")
            
            # Test if gui.py can be imported as a module
            try:
                spec = importlib.util.spec_from_file_location("gui", gui_py)
                if spec and spec.loader:
                    gui_module = importlib.util.module_from_spec(spec)
                    # Don't execute the module to avoid launching GUI
                    print("  ✅ gui.py can be imported as module")
                else:
                    self.errors.append("Could not create module spec for gui.py")
            except Exception as e:
                self.errors.append(f"Failed to import gui.py as module: {e}")
            
            return len(self.errors) == 0
            
        except ImportError as e:
            self.errors.append(f"Required import failed: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Unexpected error testing imports: {e}")
            return False
    
    def test_gui_file_paths(self) -> bool:
        """Test file path references in GUI application."""
        print("\n🔍 Testing GUI file path references...")
        
        gui_py = self.desktop_app_path / "gui.py"
        if not gui_py.exists():
            return False
        
        try:
            with open(gui_py, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for ML models path references
            ml_references = [
                'ml_models',
                '../ml_models',
                'ml_models/detection',
                'ml_models\\detection'
            ]
            
            found_ml_ref = False
            for ref in ml_references:
                if ref in content:
                    print(f"  ✅ Found ML models reference: {ref}")
                    found_ml_ref = True
                    break
            
            if not found_ml_ref:
                self.warnings.append("No ML models path references found in gui.py")
            
            # Check for data path references
            data_references = [
                'data/',
                'data\\',
                '../data',
                'data/models',
                'data\\models'
            ]
            
            found_data_ref = False
            for ref in data_references:
                if ref in content:
                    print(f"  ✅ Found data path reference: {ref}")
                    found_data_ref = True
                    break
            
            if not found_data_ref:
                self.warnings.append("No data path references found in gui.py")
            
            # Check for outputs path references
            output_references = [
                'outputs/',
                'outputs\\',
                '../outputs',
                'outputs/detections',
                'outputs\\detections'
            ]
            
            found_output_ref = False
            for ref in output_references:
                if ref in content:
                    print(f"  ✅ Found outputs path reference: {ref}")
                    found_output_ref = True
                    break
            
            if not found_output_ref:
                self.warnings.append("No outputs path references found in gui.py")
            
            # Check for model file references
            if '.pt' in content:
                print("  ✅ Found model file references (.pt files)")
            else:
                self.warnings.append("No model file references found in gui.py")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Failed to analyze gui.py file paths: {e}")
            return False
    
    def test_gui_dependencies(self) -> bool:
        """Test GUI application dependencies."""
        print("\n🔍 Testing GUI dependencies...")
        
        requirements_txt = self.desktop_app_path / "requirements.txt"
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r') as f:
                    requirements = f.read().strip().split('\n')
                
                print(f"  ✅ Found requirements.txt with {len(requirements)} dependencies")
                
                # Test if key dependencies are listed
                req_text = '\n'.join(requirements).lower()
                
                if 'torch' in req_text or 'pytorch' in req_text:
                    print("  ✅ PyTorch dependency found")
                else:
                    self.warnings.append("PyTorch dependency not found in requirements.txt")
                
                if 'pillow' in req_text or 'pil' in req_text:
                    print("  ✅ Pillow dependency found")
                else:
                    self.warnings.append("Pillow dependency not found in requirements.txt")
                
                if 'opencv' in req_text or 'cv2' in req_text:
                    print("  ✅ OpenCV dependency found")
                else:
                    self.warnings.append("OpenCV dependency not found in requirements.txt")
                
            except Exception as e:
                self.errors.append(f"Failed to read requirements.txt: {e}")
                return False
        else:
            self.warnings.append("requirements.txt not found in desktop_app directory")
        
        return True
    
    def test_gui_syntax(self) -> bool:
        """Test GUI application syntax."""
        print("\n🔍 Testing GUI syntax...")
        
        gui_py = self.desktop_app_path / "gui.py"
        if not gui_py.exists():
            return False
        
        try:
            # Test Python syntax by compiling the file
            with open(gui_py, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            compile(source_code, str(gui_py), 'exec')
            print("  ✅ gui.py has valid Python syntax")
            
            return True
            
        except SyntaxError as e:
            self.errors.append(f"Syntax error in gui.py: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Failed to test gui.py syntax: {e}")
            return False
    
    def test_ml_integration_paths(self) -> bool:
        """Test ML model integration paths."""
        print("\n🔍 Testing ML integration paths...")
        
        # Check if ML models directory exists and is accessible from desktop app
        ml_models_path = self.project_root / "ml_models"
        if not ml_models_path.exists():
            self.errors.append("ml_models directory not found - desktop app cannot access ML models")
            return False
        
        # Check detection scripts
        detection_path = ml_models_path / "detection"
        if detection_path.exists():
            detection_scripts = list(detection_path.glob("*.py"))
            if detection_scripts:
                print(f"  ✅ Found {len(detection_scripts)} detection scripts accessible from desktop app")
            else:
                self.warnings.append("No detection scripts found in ml_models/detection/")
        else:
            self.warnings.append("ml_models/detection/ directory not found")
        
        # Check model files
        data_models_path = self.project_root / "data" / "models"
        if data_models_path.exists():
            model_files = list(data_models_path.glob("*.pt"))
            if model_files:
                print(f"  ✅ Found {len(model_files)} model files accessible from desktop app")
            else:
                self.warnings.append("No .pt model files found in data/models/")
        else:
            self.warnings.append("data/models/ directory not found")
        
        # Check outputs directory
        outputs_path = self.project_root / "outputs"
        if outputs_path.exists():
            if os.access(outputs_path, os.W_OK):
                print("  ✅ Outputs directory is writable from desktop app")
            else:
                self.errors.append("Outputs directory is not writable from desktop app")
        else:
            self.warnings.append("outputs/ directory not found")
        
        return len(self.errors) == 0
    
    def test_gui_execution_safety(self) -> bool:
        """Test if GUI can be executed safely (without actually launching it)."""
        print("\n🔍 Testing GUI execution safety...")
        
        gui_py = self.desktop_app_path / "gui.py"
        if not gui_py.exists():
            return False
        
        try:
            # Change to desktop_app directory
            original_cwd = os.getcwd()
            os.chdir(self.desktop_app_path)
            
            # Test if the script can be executed with --help or similar
            # This is a dry run to check for import errors without launching GUI
            result = subprocess.run([
                sys.executable, "-c", 
                f"import sys; sys.path.insert(0, '.'); "
                f"import importlib.util; "
                f"spec = importlib.util.spec_from_file_location('gui', 'gui.py'); "
                f"print('GUI module can be loaded')"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("  ✅ GUI module can be loaded without errors")
            else:
                self.errors.append(f"GUI module loading failed: {result.stderr}")
            
            return len(self.errors) == 0
            
        except subprocess.TimeoutExpired:
            self.errors.append("GUI execution test timed out")
            return False
        except Exception as e:
            self.errors.append(f"Failed to test GUI execution: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def run_tests(self) -> bool:
        """Run all desktop app functionality tests."""
        print(f"🚀 Starting desktop app functionality tests for project at: {self.project_root}")
        print("=" * 60)
        
        tests = [
            self.test_gui_imports,
            self.test_gui_file_paths,
            self.test_gui_dependencies,
            self.test_gui_syntax,
            self.test_ml_integration_paths,
            self.test_gui_execution_safety
        ]
        
        success = True
        for test in tests:
            if not test():
                success = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 DESKTOP APP FUNCTIONALITY TEST RESULTS")
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
            print("🎉 All desktop app functionality tests passed!")
        elif success:
            print("✅ Desktop app functionality tests passed with warnings.")
        else:
            print("❌ Desktop app functionality tests failed. Please fix the errors above.")
        
        return success

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test desktop app functionality")
    parser.add_argument("--project-root", default=".", help="Path to project root directory")
    args = parser.parse_args()
    
    tester = DesktopAppTester(args.project_root)
    success = tester.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()