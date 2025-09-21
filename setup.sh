#!/bin/bash
# License Plate Recognition System Setup Script for Unix-like systems
# This script helps initialize the project environment

echo "License Plate Recognition System Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ using your system package manager"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "Python is installed"
python3 --version

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    echo "Please install pip3 using your system package manager"
    exit 1
fi

# Make setup.py executable
chmod +x setup.py

# Run the Python setup script
echo ""
echo "Running Python setup script..."
python3 setup.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo "Setup failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. For web app: cd web_app && python3 manage.py runserver"
echo "2. For desktop app: cd desktop_app && python3 gui.py"
echo "3. For ML models: python3 ml_models/detection/detect2.py --help"
echo ""
echo "See component README files for detailed usage instructions."