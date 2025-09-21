# Configuration Management

This directory contains configuration files for the License Plate Recognition System, providing environment-specific settings and centralized path management.

## Configuration Files

### `base.py`
Contains common settings shared across all environments:
- **Directory Paths**: Centralized path definitions for all project components
- **Model Settings**: Default model parameters and thresholds
- **File Handling**: Upload limits, allowed extensions, and cleanup settings
- **Processing Settings**: Image size, confidence thresholds, and performance parameters

### `development.py`
Development-specific configuration:
- **Debug Settings**: Enabled debug mode and verbose logging
- **Database**: SQLite database for local development
- **Security**: Relaxed security settings for development
- **Performance**: Lower thresholds and caching disabled for testing
- **Logging**: Console and file logging with debug level

### `production.py`
Production-specific configuration:
- **Security**: Enhanced security settings and HTTPS enforcement
- **Database**: PostgreSQL configuration with SSL
- **Performance**: Optimized settings for production workloads
- **Logging**: Structured logging with rotation and error tracking
- **Monitoring**: Health checks and metrics collection

## Usage

### Django Integration
```python
# In Django settings.py
import os
from config.base import *

# Load environment-specific config
if os.environ.get('DJANGO_ENV') == 'production':
    from config.production import *
else:
    from config.development import *
```

### Standalone Scripts
```python
# In Python scripts
from config.base import (
    MODELS_DIR, 
    DEFAULT_MODEL_PATH, 
    DEFAULT_CONFIDENCE_THRESHOLD
)

# Use configuration values
model_path = DEFAULT_MODEL_PATH
confidence = DEFAULT_CONFIDENCE_THRESHOLD
```

## Environment Variables

### Required for Production
```bash
# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=lpui_prod
DB_USER=lpui_user
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432

# Paths
STATIC_ROOT=/var/www/static
MEDIA_ROOT=/var/www/media

# ML Settings
MODEL_PATH=/path/to/custom/model.pt
CONFIDENCE_THRESHOLD=0.5
ENABLE_GPU=true
MAX_CONCURRENT_DETECTIONS=5
```

### Optional Settings
```bash
# Performance
CLEANUP_INTERVAL_MINUTES=30
MAX_REQUESTS_PER_MINUTE=60
MAX_FILE_SIZE_MB=10
REQUEST_TIMEOUT_SECONDS=30

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
HEALTH_CHECK_ENABLED=true
METRICS_ENABLED=true
```

## Directory Structure

The configuration system defines the following directory structure:

```
project_root/
├── data/
│   ├── images/
│   │   ├── test/
│   │   ├── samples/
│   │   └── training/
│   ├── models/          # Model files (.pt)
│   ├── videos/          # Video files
│   └── databases/       # Database files
├── outputs/
│   ├── detections/      # Detection results
│   ├── crops/           # Cropped license plates
│   ├── videos/          # Processed videos
│   └── temp/            # Temporary files
├── web_app/
│   ├── templates/       # HTML templates
│   └── static/          # Static files
├── ml_models/
│   ├── yolov5/          # YOLOv5 framework
│   └── detection/       # Detection scripts
└── logs/                # Log files
```

## Configuration Parameters

### Model Settings
- `DEFAULT_MODEL_PATH`: Path to primary trained model
- `BACKUP_MODEL_PATH`: Path to fallback model
- `DEFAULT_CONFIDENCE_THRESHOLD`: Minimum confidence for detections (0.0-1.0)
- `DEFAULT_IOU_THRESHOLD`: IoU threshold for non-maximum suppression
- `DEFAULT_IMAGE_SIZE`: Input image size for model inference

### File Handling
- `MAX_UPLOAD_SIZE`: Maximum file size for uploads (bytes)
- `ALLOWED_IMAGE_EXTENSIONS`: Supported image file formats
- `ALLOWED_VIDEO_EXTENSIONS`: Supported video file formats
- `TEMP_FILE_RETENTION_HOURS`: How long to keep temporary files

### Performance Settings
- `CACHE_MODELS`: Whether to cache models in memory
- `ENABLE_GPU`: Use GPU acceleration if available
- `MAX_CONCURRENT_DETECTIONS`: Limit concurrent processing
- `AUTO_CLEANUP_TEMP`: Automatically clean temporary files

## Environment Setup

### Development Environment
```bash
# Set environment variable
export DJANGO_ENV=development

# Or create .env file
echo "DJANGO_ENV=development" > .env
```

### Production Environment
```bash
# Set environment variable
export DJANGO_ENV=production

# Set required production variables
export SECRET_KEY="your-secret-key"
export ALLOWED_HOSTS="yourdomain.com"
export DB_PASSWORD="secure-password"
```

## Security Considerations

### Development
- Debug mode enabled for detailed error messages
- Relaxed CORS and security settings
- Local database with default credentials
- Verbose logging may include sensitive information

### Production
- Debug mode disabled
- HTTPS enforcement and security headers
- Secure database connections with SSL
- Rate limiting and request validation
- Structured logging without sensitive data

## Customization

### Adding New Settings
1. Add base settings to `base.py`
2. Override in environment-specific files as needed
3. Document new settings in this README
4. Update environment variable examples

### Custom Environments
Create new configuration files for additional environments:
```python
# config/staging.py
from .base import *

ENVIRONMENT = 'staging'
DEBUG = False
# ... staging-specific settings
```

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure config directory is in Python path
- Check for circular imports between config files

**Path Issues:**
- Verify all directories exist or are created automatically
- Check file permissions for read/write access

**Environment Variables:**
- Verify required variables are set in production
- Use `.env` files for local development

**Database Connections:**
- Check database credentials and connectivity
- Verify SSL settings for production databases

### Validation
```python
# Validate configuration
from config.base import *
import os

# Check required directories
for directory in [DATA_DIR, OUTPUTS_DIR, LOGS_DIR]:
    if not directory.exists():
        print(f"Creating directory: {directory}")
        directory.mkdir(parents=True, exist_ok=True)

# Check model files
if not DEFAULT_MODEL_PATH.exists():
    print(f"Warning: Model file not found: {DEFAULT_MODEL_PATH}")
```

## Best Practices

1. **Environment Separation**: Keep development and production settings separate
2. **Secret Management**: Use environment variables for sensitive data
3. **Path Management**: Use centralized path definitions
4. **Validation**: Validate configuration on startup
5. **Documentation**: Document all configuration options
6. **Defaults**: Provide sensible defaults for optional settings
7. **Security**: Follow security best practices for production