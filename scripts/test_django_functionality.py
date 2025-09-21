#!/usr/bin/env python3
"""
Django Web App Functionality Test Script

This script tests Django web application functionality with the new directory structure.
"""

import os
import sys
import subprocess
from pathlib import Path
import django
from django.core.management import execute_from_command_line
from django.test.utils import get_runner
from django.conf import settings

class DjangoFunctionalityTester:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.web_app_path = self.project_root / "web_app"
        self.errors = []
        self.warnings = []
        
    def setup_django_environment(self) -> bool:
        """Setup Django environment for testing."""
        print("🔧 Setting up Django environment...")
        
        if not self.web_app_path.exists():
            self.errors.append("web_app directory not found")
            return False
        
        # Add web_app to Python path
        sys.path.insert(0, str(self.web_app_path))
        
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lpUI.settings')
        
        try:
            django.setup()
            print("  ✅ Django environment setup successful")
            return True
        except Exception as e:
            self.errors.append(f"Failed to setup Django environment: {e}")
            return False
    
    def test_django_settings(self) -> bool:
        """Test Django settings configuration."""
        print("\n🔍 Testing Django settings...")
        
        try:
            from django.conf import settings
            
            # Test basic settings
            if hasattr(settings, 'SECRET_KEY'):
                print("  ✅ SECRET_KEY is configured")
            else:
                self.errors.append("SECRET_KEY not found in settings")
            
            if hasattr(settings, 'INSTALLED_APPS'):
                print(f"  ✅ INSTALLED_APPS configured with {len(settings.INSTALLED_APPS)} apps")
            else:
                self.errors.append("INSTALLED_APPS not found in settings")
            
            # Test template configuration
            if hasattr(settings, 'TEMPLATES') and settings.TEMPLATES:
                template_dirs = settings.TEMPLATES[0].get('DIRS', [])
                print(f"  ✅ Template directories configured: {len(template_dirs)} dirs")
                
                # Check if template directories exist
                for template_dir in template_dirs:
                    if isinstance(template_dir, str):
                        template_path = Path(template_dir)
                        if not template_path.is_absolute():
                            template_path = self.web_app_path / template_dir
                        
                        if template_path.exists():
                            print(f"    ✅ Template directory exists: {template_dir}")
                        else:
                            self.warnings.append(f"Template directory not found: {template_dir}")
            
            # Test static files configuration
            if hasattr(settings, 'STATIC_URL'):
                print(f"  ✅ STATIC_URL configured: {settings.STATIC_URL}")
            else:
                self.warnings.append("STATIC_URL not configured")
            
            if hasattr(settings, 'STATICFILES_DIRS'):
                static_dirs = settings.STATICFILES_DIRS
                print(f"  ✅ STATICFILES_DIRS configured with {len(static_dirs)} directories")
                
                # Check if static directories exist
                for static_dir in static_dirs:
                    static_path = Path(static_dir)
                    if not static_path.is_absolute():
                        static_path = self.web_app_path / static_dir
                    
                    if static_path.exists():
                        print(f"    ✅ Static directory exists: {static_dir}")
                    else:
                        self.warnings.append(f"Static directory not found: {static_dir}")
            
            # Test database configuration
            if hasattr(settings, 'DATABASES') and settings.DATABASES:
                db_config = settings.DATABASES.get('default', {})
                db_engine = db_config.get('ENGINE', '')
                db_name = db_config.get('NAME', '')
                
                print(f"  ✅ Database configured: {db_engine}")
                
                if 'sqlite3' in db_engine and db_name:
                    db_path = Path(db_name)
                    if not db_path.is_absolute():
                        # Check if it's relative to web_app or project root
                        web_app_db_path = self.web_app_path / db_name
                        root_db_path = self.project_root / db_name
                        
                        if web_app_db_path.exists():
                            print(f"    ✅ SQLite database found: {web_app_db_path}")
                        elif root_db_path.exists():
                            print(f"    ✅ SQLite database found: {root_db_path}")
                        else:
                            self.warnings.append(f"SQLite database not found: {db_name}")
            
            return len(self.errors) == 0
            
        except Exception as e:
            self.errors.append(f"Failed to test Django settings: {e}")
            return False
    
    def test_django_urls(self) -> bool:
        """Test Django URL configuration."""
        print("\n🔍 Testing Django URL configuration...")
        
        try:
            from django.urls import get_resolver
            from django.core.urlresolvers import reverse
            
            resolver = get_resolver()
            print("  ✅ URL resolver loaded successfully")
            
            # Test if main URL patterns are accessible
            url_patterns = resolver.url_patterns
            print(f"  ✅ Found {len(url_patterns)} URL patterns")
            
            return True
            
        except ImportError:
            # Try Django 2.0+ import
            try:
                from django.urls import get_resolver, reverse
                
                resolver = get_resolver()
                print("  ✅ URL resolver loaded successfully")
                
                url_patterns = resolver.url_patterns
                print(f"  ✅ Found {len(url_patterns)} URL patterns")
                
                return True
                
            except Exception as e:
                self.errors.append(f"Failed to test Django URLs: {e}")
                return False
        except Exception as e:
            self.errors.append(f"Failed to test Django URLs: {e}")
            return False
    
    def test_django_models(self) -> bool:
        """Test Django models."""
        print("\n🔍 Testing Django models...")
        
        try:
            from django.apps import apps
            
            # Get all models
            all_models = apps.get_models()
            print(f"  ✅ Found {len(all_models)} Django models")
            
            # Test model imports
            for model in all_models:
                model_name = f"{model._meta.app_label}.{model.__name__}"
                print(f"    ✅ Model accessible: {model_name}")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Failed to test Django models: {e}")
            return False
    
    def test_django_management_commands(self) -> bool:
        """Test Django management commands."""
        print("\n🔍 Testing Django management commands...")
        
        # Change to web_app directory for management commands
        original_cwd = os.getcwd()
        os.chdir(self.web_app_path)
        
        try:
            # Test check command
            result = subprocess.run([
                sys.executable, "manage.py", "check"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("  ✅ Django check command passed")
            else:
                self.errors.append(f"Django check failed: {result.stderr}")
            
            # Test collectstatic --dry-run
            result = subprocess.run([
                sys.executable, "manage.py", "collectstatic", "--dry-run", "--noinput"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("  ✅ Django collectstatic dry-run passed")
            else:
                self.warnings.append(f"Django collectstatic dry-run had issues: {result.stderr}")
            
            return len(self.errors) == 0
            
        except subprocess.TimeoutExpired:
            self.errors.append("Django management commands timed out")
            return False
        except Exception as e:
            self.errors.append(f"Failed to test Django management commands: {e}")
            return False
        finally:
            os.chdir(original_cwd)
    
    def test_template_loading(self) -> bool:
        """Test Django template loading."""
        print("\n🔍 Testing Django template loading...")
        
        try:
            from django.template.loader import get_template
            from django.template import TemplateDoesNotExist
            
            # Look for common template files
            template_path = self.web_app_path / "templates"
            if template_path.exists():
                template_files = list(template_path.glob("**/*.html"))
                
                if template_files:
                    print(f"  ✅ Found {len(template_files)} template files")
                    
                    # Test loading a few templates
                    for template_file in template_files[:3]:  # Test first 3 templates
                        relative_path = template_file.relative_to(template_path)
                        template_name = str(relative_path).replace('\\', '/')
                        
                        try:
                            template = get_template(template_name)
                            print(f"    ✅ Template loads successfully: {template_name}")
                        except TemplateDoesNotExist:
                            self.warnings.append(f"Template not found in Django loader: {template_name}")
                        except Exception as e:
                            self.warnings.append(f"Template loading error for {template_name}: {e}")
                else:
                    self.warnings.append("No template files found in templates directory")
            else:
                self.warnings.append("Templates directory not found")
            
            return True
            
        except Exception as e:
            self.errors.append(f"Failed to test template loading: {e}")
            return False
    
    def run_tests(self) -> bool:
        """Run all Django functionality tests."""
        print(f"🚀 Starting Django functionality tests for project at: {self.project_root}")
        print("=" * 60)
        
        if not self.setup_django_environment():
            return False
        
        tests = [
            self.test_django_settings,
            self.test_django_urls,
            self.test_django_models,
            self.test_django_management_commands,
            self.test_template_loading
        ]
        
        success = True
        for test in tests:
            if not test():
                success = False
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 DJANGO FUNCTIONALITY TEST RESULTS")
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
            print("🎉 All Django functionality tests passed!")
        elif success:
            print("✅ Django functionality tests passed with warnings.")
        else:
            print("❌ Django functionality tests failed. Please fix the errors above.")
        
        return success

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Django web app functionality")
    parser.add_argument("--project-root", default=".", help="Path to project root directory")
    args = parser.parse_args()
    
    tester = DjangoFunctionalityTester(args.project_root)
    success = tester.run_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()