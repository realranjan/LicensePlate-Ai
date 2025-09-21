@echo off
REM License Plate Recognition System Setup Script for Windows
REM This script helps initialize the project environment

echo License Plate Recognition System Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed
python --version

REM Run the Python setup script
echo.
echo Running Python setup script...
python setup.py %*

if errorlevel 1 (
    echo.
    echo Setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
echo.
echo Next steps:
echo 1. For web app: cd web_app ^&^& python manage.py runserver
echo 2. For desktop app: cd desktop_app ^&^& python gui.py
echo 3. For ML models: python ml_models/detection/detect2.py --help
echo.
echo See component README files for detailed usage instructions.
pause