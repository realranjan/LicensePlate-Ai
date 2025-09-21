# Quick Start Guide

Get the License Plate Recognition System running in under 5 minutes!

## 🚀 One-Command Setup

### Windows
```cmd
setup.bat
```

### Linux/macOS
```bash
chmod +x setup.sh && ./setup.sh
```

### Python (Any OS)
```bash
python setup.py
```

## 🎯 Choose Your Interface

After setup, pick your preferred interface:

### 🌐 Web Interface (Recommended)
```bash
cd web_app
python manage.py runserver
```
→ Open http://127.0.0.1:8000

### 🖥️ Desktop GUI
```bash
cd desktop_app
python gui.py
```

### 💻 Command Line
```bash
python ml_models/detection/detect2.py --source path/to/image.jpg
```

## 📋 Requirements Check

- ✅ Python 3.7+
- ✅ 4GB RAM minimum
- ✅ 2GB free space
- ✅ Internet connection (for setup)

## 🆘 Quick Fixes

**Import errors?**
```bash
pip install -r requirements.txt
```

**Permission denied?**
```bash
chmod +x setup.sh
```

**Port 8000 busy?**
```bash
python manage.py runserver 8001
```

## 📚 Need More Help?

- 📖 [Complete Setup Guide](docs/PROJECT_SETUP.md)
- 🌐 [Web App Guide](web_app/README.md)
- 🖥️ [Desktop App Guide](desktop_app/README.md)
- 🤖 [ML Models Guide](ml_models/README.md)

## 🎉 That's It!

You're ready to detect license plates! Upload an image and see the magic happen.