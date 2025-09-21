# License Plate Recognition System - Complete Setup Guide

This comprehensive guide covers the complete setup, configuration, and deployment of the License Plate Recognition System.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Component Setup](#component-setup)
4. [Configuration](#configuration)
5. [Development Setup](#development-setup)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Performance Optimization](#performance-optimization)

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.7 or higher
- **Memory**: 4GB RAM
- **Storage**: 2GB free space
- **Network**: Internet connection for dependency installation

### Recommended Requirements
- **Operating System**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: 3.9 or higher
- **Memory**: 8GB RAM or more
- **Storage**: 5GB free space
- **GPU**: NVIDIA GPU with CUDA support (for faster processing)
- **Network**: Stable internet connection

### Hardware Acceleration
- **NVIDIA GPU**: GTX 1060 or better with 4GB+ VRAM
- **CUDA**: Version 11.0 or higher
- **cuDNN**: Compatible version with CUDA installation

## Installation Methods

### Method 1: Automated Setup (Recommended)

**Windows:**
```cmd
# Download and run setup script
setup.bat

# Or with specific component
setup.bat --component web
```

**Linux/macOS:**
```bash
# Make script executable and run
chmod +x setup.sh
./setup.sh

# Or with specific component
./setup.sh --component desktop
```

**Python Script (Cross-platform):**
```bash
# Full setup
python setup.py

# Component-specific setup
python setup.py --component ml

# Verification only
python setup.py --verify-only
```

### Method 2: Manual Installation

#### Step 1: Core Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt
```

#### Step 2: Component Dependencies
```bash
# Web application
cd web_app
pip install -r requirements.txt

# Desktop application
cd ../desktop_app
pip install -r requirements.txt

# ML models
cd ../ml_models
pip install -r requirements.txt
```

#### Step 3: Directory Structure
```bash
# Create required directories
mkdir -p data/{images/{test,samples,training},models,videos,databases}
mkdir -p outputs/{detections,crops,videos,temp}
mkdir -p logs
mkdir -p docs/examples
```

### Method 3: Virtual Environment Setup

```bash
# Create virtual environment
python -m venv lpui_env

# Activate virtual environment
# Windows:
lpui_env\Scripts\activate
# Linux/macOS:
source lpui_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup components
python setup.py
```

## Component Setup

### Web Application Setup

#### Basic Setup
```bash
cd web_app

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

#### Production Setup
```bash
# Set environment variables
export DJANGO_ENV=production
export SECRET_KEY="your-secret-key"
export ALLOWED_HOSTS="yourdomain.com"

# Install production dependencies
pip install gunicorn psycopg2-binary

# Run with Gunicorn
gunicorn lpUI.wsgi:application --bind 0.0.0.0:8000
```

### Desktop Application Setup

#### Basic Setup
```bash
cd desktop_app

# Install dependencies
pip install -r requirements.txt

# Run application
python gui.py
```

#### Platform-Specific Setup

**Linux (Ubuntu/Debian):**
```bash
# Install tkinter if not available
sudo apt-get update
sudo apt-get install python3-tk

# Install additional dependencies
sudo apt-get install python3-dev python3-pip
```

**macOS:**
```bash
# Install using Homebrew
brew install python-tk

# Or using MacPorts
sudo port install py39-tkinter
```

**Windows:**
```cmd
# tkinter is included with Python
# No additional setup required
```

### ML Models Setup

#### Basic Setup
```bash
cd ml_models

# Install dependencies
pip install -r requirements.txt

# Test detection
python detection/detect2.py --help
```

#### GPU Setup (NVIDIA)
```bash
# Install CUDA-enabled PyTorch
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

#### Model Download
```bash
# Download pre-trained models (if not included)
cd data/models

# YOLOv5 models
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m.pt
```

## Configuration

### Environment Configuration

#### Development Environment
```bash
# Create .env file
cat > .env << EOF
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=dev-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
EOF
```

#### Production Environment
```bash
# Create production .env file
cat > .env << EOF
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=your-secure-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_NAME=lpui_prod
DB_USER=lpui_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
EOF
```

### Database Configuration

#### SQLite (Development)
```python
# Automatic setup - no configuration needed
# Database file: data/databases/db.sqlite3
```

#### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE lpui_prod;
CREATE USER lpui_user WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE lpui_prod TO lpui_user;
\q

# Update environment variables
export DB_NAME=lpui_prod
export DB_USER=lpui_user
export DB_PASSWORD=secure-password
```

### Web Server Configuration

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /static/ {
        alias /path/to/project/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/project/outputs/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Apache Configuration
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    
    Alias /static /path/to/project/staticfiles
    Alias /media /path/to/project/outputs
    
    ProxyPass /static !
    ProxyPass /media !
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

## Development Setup

### IDE Configuration

#### VS Code Setup
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./lpui_env/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

#### PyCharm Setup
1. Open project directory
2. Configure Python interpreter to virtual environment
3. Set up run configurations for each component
4. Enable code style checks (PEP 8)

### Development Tools

#### Code Quality
```bash
# Install development tools
pip install black flake8 pytest mypy

# Format code
black .

# Check code style
flake8 .

# Type checking
mypy .

# Run tests
pytest
```

#### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install
```

### Testing Setup

#### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific component tests
pytest web_app/tests/
pytest desktop_app/tests/
pytest ml_models/tests/
```

#### Integration Tests
```bash
# Test web application
cd web_app
python manage.py test

# Test ML models
cd ml_models
python -m pytest tests/test_detection.py

# Test desktop application
cd desktop_app
python -m pytest tests/test_gui.py
```

## Production Deployment

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p data/models outputs logs

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "web_app.lpUI.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=lpui_prod
      - POSTGRES_USER=lpui_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Cloud Deployment

#### AWS EC2 Deployment
```bash
# Launch EC2 instance
aws ec2 run-instances --image-id ami-0abcdef1234567890 --instance-type t3.medium

# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Install dependencies
sudo apt-get update
sudo apt-get install python3 python3-pip git nginx

# Clone repository
git clone https://github.com/your-repo/license-plate-recognition.git
cd license-plate-recognition

# Setup application
python3 setup.py
```

#### Heroku Deployment
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn web_app.lpUI.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile

# Create runtime.txt
echo "python-3.9.18" > runtime.txt

# Deploy to Heroku
heroku create your-app-name
git push heroku main
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Problem: ModuleNotFoundError
# Solution: Check Python path and virtual environment
python -c "import sys; print(sys.path)"
pip list | grep torch

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### Memory Issues
```bash
# Problem: Out of memory during processing
# Solution: Reduce batch size or image resolution
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# Monitor memory usage
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

#### GPU Issues
```bash
# Problem: CUDA not available
# Solution: Check CUDA installation
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### Permission Issues
```bash
# Problem: Permission denied errors
# Solution: Fix file permissions
chmod +x setup.sh
sudo chown -R $USER:$USER .
```

### Performance Issues

#### Slow Detection
```bash
# Check GPU usage
nvidia-smi

# Optimize model settings
export CONFIDENCE_THRESHOLD=0.5
export IMAGE_SIZE=640

# Use smaller model
cp data/models/yolov5s.pt data/models/best.pt
```

#### Web Application Slow
```bash
# Enable caching
export CACHE_MODELS=true

# Use production server
gunicorn web_app.lpUI.wsgi:application --workers 4

# Optimize database
python web_app/manage.py dbshell
VACUUM;
ANALYZE;
```

## Performance Optimization

### Model Optimization

#### Model Quantization
```python
# Quantize model for faster inference
import torch

model = torch.jit.load('data/models/best.pt')
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
torch.jit.save(quantized_model, 'data/models/best_quantized.pt')
```

#### TensorRT Optimization (NVIDIA)
```bash
# Export to TensorRT
cd ml_models
python export.py --weights ../data/models/best.pt --include engine --device 0
```

### System Optimization

#### CPU Optimization
```bash
# Set CPU affinity
taskset -c 0-3 python ml_models/detection/detect2.py

# Optimize NumPy threads
export OMP_NUM_THREADS=4
export MKL_NUM_THREADS=4
```

#### Memory Optimization
```bash
# Limit memory usage
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:256

# Enable memory mapping
export PYTORCH_MMAP_ALLOCATOR=1
```

### Database Optimization

#### PostgreSQL Tuning
```sql
-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

#### Index Optimization
```sql
-- Add database indexes
CREATE INDEX idx_detection_timestamp ON detections(created_at);
CREATE INDEX idx_detection_confidence ON detections(confidence);
```

This completes the comprehensive setup guide. For additional help, refer to the component-specific README files and the troubleshooting section above.