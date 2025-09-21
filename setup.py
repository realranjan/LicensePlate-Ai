#!/usr/bin/env python3
"""
License Plate Recognition System Setup Script

This script helps initialize the project environment and install dependencies
for all components of the License Plate Recognition System.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if check:
            sys.exit(1)
        return e


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required.")
        sys.exit(1)
    print(f"Python version: {sys.version}")


def create_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        'data/images/test',
        'data/images/samples', 
        'data/images/training',
        'data/models',
        'data/videos',
        'data/databases',
        'outputs/detections',
        'outputs/crops',
        'outputs/videos',
        'outputs/temp',
        'logs',
        'docs/examples'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")


def install_dependencies(component=None):
    """Install dependencies for specified component or all components."""
    components = {
        'core': '.',
        'web': 'web_app',
        'desktop': 'desktop_app', 
        'ml': 'ml_models'
    }
    
    if component and component in components:
        install_component_deps(components[component], component)
    else:
        # Install all components
        for comp_name, comp_path in components.items():
            install_component_deps(comp_path, comp_name)


def install_component_deps(path, name):
    """Install dependencies for a specific component."""
    requirements_file = Path(path) / 'requirements.txt'
    
    if requirements_file.exists():
        print(f"\n--- Installing {name} dependencies ---")
        run_command(f"pip install -r {requirements_file}")
    else:
        print(f"Warning: {requirements_file} not found")


def setup_django():
    """Set up Django web application."""
    print("\n--- Setting up Django web application ---")
    
    web_app_path = Path('web_app')
    if not web_app_path.exists():
        print("Error: web_app directory not found")
        return
    
    # Run Django migrations
    manage_py = web_app_path / 'manage.py'
    if manage_py.exists():
        run_command("python manage.py migrate", cwd=web_app_path)
        
        # Collect static files
        run_command("python manage.py collectstatic --noinput", cwd=web_app_path, check=False)
        
        print("Django setup completed successfully!")
    else:
        print("Warning: manage.py not found in web_app directory")


def verify_installation():
    """Verify that the installation was successful."""
    print("\n--- Verifying installation ---")
    
    # Check Python packages
    required_packages = ['torch', 'torchvision', 'ultralytics', 'opencv-python', 'django']
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
    
    # Check directory structure
    required_dirs = ['data', 'outputs', 'web_app', 'desktop_app', 'ml_models']
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✓ {directory}/ directory exists")
        else:
            print(f"✗ {directory}/ directory is missing")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description='Setup License Plate Recognition System')
    parser.add_argument('--component', choices=['core', 'web', 'desktop', 'ml'], 
                       help='Install dependencies for specific component only')
    parser.add_argument('--skip-django', action='store_true', 
                       help='Skip Django setup (migrations, static files)')
    parser.add_argument('--verify-only', action='store_true',
                       help='Only verify installation, do not install')
    
    args = parser.parse_args()
    
    print("License Plate Recognition System Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    if args.verify_only:
        verify_installation()
        return
    
    # Create directories
    print("\n--- Creating directories ---")
    create_directories()
    
    # Install dependencies
    print("\n--- Installing dependencies ---")
    install_dependencies(args.component)
    
    # Setup Django (unless skipped or only installing specific non-web component)
    if not args.skip_django and (not args.component or args.component == 'web'):
        setup_django()
    
    # Verify installation
    verify_installation()
    
    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. For web app: cd web_app && python manage.py runserver")
    print("2. For desktop app: cd desktop_app && python gui.py")
    print("3. For ML models: python ml_models/detection/detect2.py --help")
    print("\nSee component README files for detailed usage instructions.")


if __name__ == '__main__':
    main()