#!/usr/bin/env python3
"""
Project Structure Validation Script

This script validates that the License Plate Recognition System
has been properly organized according to the design specifications.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class ProjectValidator:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.errors = []
        self.warnings = []
        
    def validate_directory_structure(self) -> bool:
        """Validate that all required directories exist."""
        print("🔍 Validating directory structure...")
        
        required_dirs = [
            "web_app",
            "desktop_app", 
            "ml_models",
            "data",
            "docs",
            "scripts",
            "outputs",
            "config"
        ]
        
        # Check main directories
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                self.errors.append(f"Missing required directory: {dir_name}")
            elif not dir_path.is_dir():
                self.errors.append(f"{dir_name} exists but is not a directory")
            else:
                print(f"  ✅ {dir_name}/ exists")
        
        # Check subdirectories
        subdirs = {
            "data": ["images", "models", "videos", "databases"],
            "data/images": ["test", "samples", "training"],
            "ml_models": ["detection", "yolov5"],
            "docs": ["notebooks", "examples"],
            "outputs": ["detections", "crops", "videos", "temp"]
        }
        
        for parent, children in subdirs.items():
            parent_path = self.project_root / parent
            if parent_path.exists():
                for child in children:
                    child_path = parent_path / child
                    if not child_path.exists():
                        self.warnings.append(f"Missing subdirectory: {parent}/{child}")
                    else:
                        print(f"  ✅ {parent}/{child}/ exists")
        
        return len(self.errors) == 0
    
    def validate_required_files(self) -> bool:
        """Validate that required files exist in correct locations."""
        print("\n🔍 Validating required files...")
        
        required_files = {
            ".": ["README.md", "requirements.txt", ".gitignore"],
            "web_app": ["manage.py", "README.md", "requirements.txt"],
            "desktop_app": ["gui.py", "README.md", "requirements.txt"],
            "ml_models": ["hubconf.py", "README.md", "requirements.txt"],
            "scripts": ["sample.py"],
            "config": ["__init__.py", "base.py", "development.py", "production.py"]
        }
        
        for dir_path, files in required_files.items():
            base_path = self.project_root if dir_path == "." else self.project_root / dir_path
            
            for file_name in files:
                file_path = base_path / file_name
                if not file_path.exists():
                    self.errors.append(f"Missing required file: {dir_path}/{file_name}")
                elif not file_path.is_file():
                    self.errors.append(f"{dir_path}/{file_name} exists but is not a file")
                else:
                    print(f"  ✅ {dir_path}/{file_name} exists")
        
        return len(self.errors) == 0
    
    def validate_django_structure(self) -> bool:
        """Validate Django web app structure."""
        print("\n🔍 Validating Django web app structure...")
        
        web_app_path = self.project_root / "web_app"
        if not web_app_path.exists():
            self.errors.append("web_app directory missing - cannot validate Django structure")
            return False
        
        django_files = [
            "web_app/lpUI/settings.py",
            "web_app/lpUI/urls.py", 
            "web_app/lpUI/wsgi.py",
            "web_app/templates",
            "web_app/static"
        ]
        
        for item in django_files:
            item_path = self.project_root / item
            if not item_path.exists():
                self.errors.append(f"Missing Django component: {item}")
            else:
                print(f"  ✅ {item} exists")
        
        return len(self.errors) == 0
    
    def validate_ml_structure(self) -> bool:
        """Validate ML models structure."""
        print("\n🔍 Validating ML models structure...")
        
        ml_path = self.project_root / "ml_models"
        if not ml_path.exists():
            self.errors.append("ml_models directory missing - cannot validate ML structure")
            return False
        
        # Check for detection scripts
        detection_path = ml_path / "detection"
        if detection_path.exists():
            detection_files = ["detect.py", "detect2.py", "detect3.py"]
            for file_name in detection_files:
                file_path = detection_path / file_name
                if file_path.exists():
                    print(f"  ✅ ml_models/detection/{file_name} exists")
                else:
                    self.warnings.append(f"Detection script not found: ml_models/detection/{file_name}")
        
        # Check for YOLOv5
        yolo_path = ml_path / "yolov5"
        if yolo_path.exists():
            print(f"  ✅ ml_models/yolov5/ exists")
        else:
            self.warnings.append("YOLOv5 directory not found in ml_models/")
        
        return True
    
    def validate_data_organization(self) -> bool:
        """Validate data files organization."""
        print("\n🔍 Validating data organization...")
        
        data_path = self.project_root / "data"
        if not data_path.exists():
            self.errors.append("data directory missing")
            return False
        
        # Check for model files
        models_path = data_path / "models"
        if models_path.exists():
            model_files = list(models_path.glob("*.pt"))
            if model_files:
                print(f"  ✅ Found {len(model_files)} model files in data/models/")
                for model_file in model_files:
                    print(f"    - {model_file.name}")
            else:
                self.warnings.append("No .pt model files found in data/models/")
        
        # Check for database
        db_path = data_path / "databases" / "db.sqlite3"
        if db_path.exists():
            print(f"  ✅ Database found at data/databases/db.sqlite3")
        else:
            self.warnings.append("Database file not found at data/databases/db.sqlite3")
        
        return True
    
    def validate_imports(self) -> bool:
        """Validate that Python imports work correctly."""
        print("\n🔍 Validating Python imports...")
        
        # Test config imports
        try:
            sys.path.insert(0, str(self.project_root))
            import config
            print("  ✅ config module imports successfully")
        except ImportError as e:
            self.errors.append(f"Failed to import config module: {e}")
        
        # Test if Django settings can be imported
        web_app_path = self.project_root / "web_app"
        if web_app_path.exists():
            try:
                sys.path.insert(0, str(web_app_path))
                os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpUI.settings')
                import django
                print("  ✅ Django imports successfully")
            except ImportError as e:
                self.warnings.append(f"Django import issue (may need dependencies): {e}")
        
        return True
    
    def run_validation(self) -> bool:
        """Run all validation checks."""
        print(f"🚀 Starting validation for project at: {self.project_root}")
        print("=" * 60)
        
        checks = [
            self.validate_directory_structure,
            self.validate_required_files,
            self.validate_django_structure,
            self.validate_ml_structure,
            self.validate_data_organization,
            self.validate_imports
        ]
        
        success = True
        for check in checks:
            if not check():
                success = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 VALIDATION RESULTS")
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
            print("🎉 All validation checks passed! Project structure is correct.")
        elif success:
            print("✅ Validation passed with warnings. Project structure is mostly correct.")
        else:
            print("❌ Validation failed. Please fix the errors above.")
        
        return success

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate License Plate Recognition project structure")
    parser.add_argument("--project-root", default=".", help="Path to project root directory")
    args = parser.parse_args()
    
    validator = ProjectValidator(args.project_root)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()