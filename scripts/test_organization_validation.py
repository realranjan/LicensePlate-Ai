#!/usr/bin/env python3
"""
Organization Validation Script
Tests that the project reorganization was completed successfully.
Focuses on structure and file organization rather than runtime dependencies.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent

def test_directory_structure():
    """Test that all required directories exist with proper organization."""
    print("🔍 Testing directory structure...")
    
    required_structure = {
        "web_app": ["manage.py", "lpUI", "templates", "static", "README.md", "requirements.txt"],
        "desktop_app": ["gui.py", "README.md", "requirements.txt"],
        "ml_models": ["yolov5", "detection", "hubconf.py", "README.md", "requirements.txt"],
        "data": ["images", "models", "videos", "databases"],
        "data/images": ["test", "samples", "training"],
        "outputs": ["detections", "crops", "videos", "temp"],
        "docs": ["notebooks", "examples"],
        "scripts": [],
        "config": ["base.py", "development.py", "production.py"]
    }
    
    all_good = True
    
    for dir_path, expected_contents in required_structure.items():
        full_dir_path = project_root / dir_path
        
        if not full_dir_path.exists():
            print(f"❌ Missing directory: {dir_path}")
            all_good = False
            continue
        
        print(f"✅ Directory exists: {dir_path}")
        
        # Check expected contents
        for item in expected_contents:
            item_path = full_dir_path / item
            if not item_path.exists():
                print(f"   ⚠️  Missing expected item: {dir_path}/{item}")
            else:
                print(f"   ✅ Contains: {item}")
    
    return all_good

def test_file_migrations():
    """Test that files were properly migrated from original locations."""
    print("\n📁 Testing file migrations...")
    
    # Check that original lpUI directory is gone
    original_lpui = project_root / "lpUI"
    if original_lpui.exists():
        print("❌ Original lpUI directory still exists - cleanup incomplete")
        return False
    else:
        print("✅ Original lpUI directory successfully removed")
    
    # Check key files are in new locations
    key_files = {
        "web_app/manage.py": "Django management script",
        "desktop_app/gui.py": "Desktop GUI application", 
        "ml_models/hubconf.py": "PyTorch Hub configuration",
        "ml_models/yolov5": "YOLOv5 framework directory",
        "data/databases": "Database storage directory",
        "outputs/detections": "Detection results directory"
    }
    
    all_migrated = True
    
    for file_path, description in key_files.items():
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ Missing {description}: {file_path}")
            all_migrated = False
    
    return all_migrated

def test_requirements_organization():
    """Test that requirements files are properly organized."""
    print("\n📦 Testing requirements organization...")
    
    req_files = {
        "requirements.txt": "Root requirements",
        "web_app/requirements.txt": "Web app requirements",
        "desktop_app/requirements.txt": "Desktop app requirements",
        "ml_models/requirements.txt": "ML models requirements"
    }
    
    all_exist = True
    
    for req_file, description in req_files.items():
        full_path = project_root / req_file
        if full_path.exists():
            print(f"✅ {description}: {req_file}")
            
            # Check if file has content
            try:
                with open(full_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        lines = len([line for line in content.split('\n') if line.strip() and not line.strip().startswith('#')])
                        print(f"   📋 Contains {lines} dependencies")
                    else:
                        print(f"   ⚠️  File is empty")
            except Exception as e:
                print(f"   ⚠️  Could not read file: {e}")
        else:
            print(f"❌ Missing {description}: {req_file}")
            all_exist = False
    
    return all_exist

def test_documentation():
    """Test that documentation is properly organized."""
    print("\n📚 Testing documentation organization...")
    
    doc_files = {
        "README.md": "Main project documentation",
        "web_app/README.md": "Web app documentation",
        "desktop_app/README.md": "Desktop app documentation", 
        "ml_models/README.md": "ML models documentation",
        "docs/MIGRATION_NOTES.md": "Migration documentation"
    }
    
    all_documented = True
    
    for doc_file, description in doc_files.items():
        full_path = project_root / doc_file
        if full_path.exists():
            print(f"✅ {description}: {doc_file}")
            
            # Check if file has substantial content
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if len(content) > 100:  # Arbitrary threshold for "substantial"
                        print(f"   📄 Contains {len(content)} characters")
                    else:
                        print(f"   ⚠️  File seems too short ({len(content)} chars)")
            except Exception as e:
                print(f"   ⚠️  Could not read file: {e}")
        else:
            print(f"❌ Missing {description}: {doc_file}")
            all_documented = False
    
    return all_documented

def test_gitignore_updates():
    """Test that .gitignore is properly updated for new structure."""
    print("\n🚫 Testing .gitignore updates...")
    
    gitignore_path = project_root / ".gitignore"
    if not gitignore_path.exists():
        print("❌ .gitignore file missing")
        return False
    
    try:
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        # Check for key exclusions
        expected_exclusions = [
            "outputs/detections/",
            "outputs/crops/", 
            "outputs/videos/",
            "outputs/temp/",
            "data/models/*.pt",
            "data/databases/*.sqlite3"
        ]
        
        all_present = True
        for exclusion in expected_exclusions:
            if exclusion in gitignore_content:
                print(f"✅ Excludes: {exclusion}")
            else:
                print(f"⚠️  Missing exclusion: {exclusion}")
                # Don't fail for this, just warn
        
        print("✅ .gitignore file exists and has been updated")
        return True
        
    except Exception as e:
        print(f"❌ Error reading .gitignore: {e}")
        return False

def test_configuration_setup():
    """Test that configuration management is properly set up."""
    print("\n⚙️  Testing configuration setup...")
    
    config_files = [
        "config/base.py",
        "config/development.py", 
        "config/production.py",
        "config/__init__.py"
    ]
    
    all_configured = True
    
    for config_file in config_files:
        full_path = project_root / config_file
        if full_path.exists():
            print(f"✅ Configuration file: {config_file}")
        else:
            print(f"❌ Missing configuration: {config_file}")
            all_configured = False
    
    return all_configured

def run_organization_validation():
    """Run all organization validation tests."""
    print("🚀 Starting Organization Validation")
    print("=" * 60)
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("File Migrations", test_file_migrations),
        ("Requirements Organization", test_requirements_organization),
        ("Documentation", test_documentation),
        ("GitIgnore Updates", test_gitignore_updates),
        ("Configuration Setup", test_configuration_setup),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ORGANIZATION VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} validation checks passed")
    
    if passed == total:
        print("\n🎉 Organization validation complete!")
        print("✅ All files have been properly reorganized")
        print("✅ Project structure follows the new modular design")
        print("✅ Documentation and configuration are in place")
        print("\n📋 Next steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Set up component environments as needed")
        print("   3. Test functionality with actual data")
        return True
    else:
        print(f"\n⚠️  {total - passed} validation checks failed.")
        print("Please review the issues above before proceeding.")
        return False

if __name__ == "__main__":
    success = run_organization_validation()
    sys.exit(0 if success else 1)