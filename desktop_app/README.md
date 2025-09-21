# Desktop Application - License Plate Recognition

This directory contains the Tkinter-based desktop GUI application for the License Plate Recognition System.

## Overview

The desktop application provides a simple graphical interface for uploading images and performing license plate detection using YOLOv5 models. It features a clean, user-friendly interface built with Python's Tkinter library.

## Features

- Image file selection through native file dialog
- Real-time license plate detection using YOLOv5
- Output display in scrollable text area
- Cross-platform compatibility (Windows, macOS, Linux)

## Prerequisites

- Python 3.7 or higher
- Tkinter (usually included with Python)
- YOLOv5 models and detection scripts (located in `../ml_models/`)
- Trained model files (located in `../data/models/`)

## Installation

1. Navigate to the desktop_app directory:
   ```bash
   cd desktop_app
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the ML models and detection scripts are properly set up in the project structure:
   - ML detection scripts should be in `../ml_models/detection/`
   - Trained model files should be in `../data/models/`

## Usage

1. Run the desktop application:
   ```bash
   python gui.py
   ```

2. Click the "Upload Image" button to select an image file

3. The application will automatically run license plate detection on the selected image

4. Results will be displayed in the text area below the button

## File Structure

```
desktop_app/
├── gui.py              # Main GUI application
├── requirements.txt    # Desktop-specific dependencies
└── README.md          # This documentation file
```

## Dependencies

The application relies on the following components from other parts of the project:

- **ML Models**: `../ml_models/detection/detect2.py` - YOLOv5 detection script
- **Model Files**: `../data/models/1500img.pt` - Trained YOLOv5 model
- **YOLOv5**: `../ml_models/yolov5/` - YOLOv5 framework

## Troubleshooting

### Common Issues

1. **"No module named 'tkinter'"**
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On CentOS/RHEL: `sudo yum install tkinter`
   - On macOS: Tkinter should be included with Python

2. **"Detection script not found"**
   - Ensure the ML models directory structure is properly set up
   - Verify that `../ml_models/detection/detect2.py` exists

3. **"Model file not found"**
   - Ensure the trained model file exists at `../data/models/1500img.pt`
   - Check that the data directory structure is properly organized

4. **Permission errors**
   - Ensure the application has read access to model files and detection scripts
   - Check file permissions in the ml_models and data directories

## Development

To modify or extend the desktop application:

1. The main GUI logic is in `gui.py`
2. File path configurations are handled dynamically using relative paths
3. The application uses subprocess to call the YOLOv5 detection script
4. Output is captured and displayed in the GUI text widget

## Dependencies

### Core Dependencies
- **Python 3.7+**: Built-in tkinter GUI framework
- **Pillow 10.0.1**: Image handling and display in GUI
- **psutil 5.9.6**: System and process monitoring utilities
- **OpenCV 4.8.1**: Computer vision operations
- **NumPy 1.24.3**: Array operations and data handling

### GUI Enhancement Dependencies
- **tkinter-tooltip 2.1.0**: Enhanced tooltip functionality
- **tkfilebrowser 2.3.2**: Advanced file dialog capabilities
- **ttkthemes 3.2.2**: Additional GUI themes and styling
- **send2trash 1.8.2**: Safe file deletion to recycle bin

### System Dependencies
- **threading-timer 0.1.0**: Enhanced threading utilities for async operations
- **configparser 6.0.0**: Configuration file handling
- **pathlib2 2.3.7**: Enhanced path handling (compatibility)

### Installation Order
1. Install core dependencies: `pip install -r ../requirements.txt`
2. Install desktop-specific dependencies: `pip install -r requirements.txt`

### Platform-Specific Notes
- **Windows**: tkinter included with Python installation
- **Linux**: May need `sudo apt-get install python3-tk`
- **macOS**: tkinter included with Python installation

## Performance Optimization

### Memory Management
- Models are loaded once and cached for multiple detections
- Image processing uses efficient OpenCV operations
- Automatic cleanup of temporary files and variables

### Threading
- GUI remains responsive during detection operations
- Background processing for file operations
- Async handling of model inference

## Future Enhancements

### Planned Features
- **Image Preview**: Thumbnail display of selected images
- **Batch Processing**: Multiple file selection and processing
- **Configuration GUI**: Settings panel for detection parameters
- **Progress Indicators**: Real-time progress bars for operations
- **Export Options**: Save results in multiple formats (JSON, CSV, XML)
- **History**: Recent files and detection history
- **Themes**: Dark mode and custom GUI themes

### Advanced Features
- **Real-time Camera**: Live camera feed processing
- **Video Processing**: Frame-by-frame video analysis
- **Database Integration**: Local database for results storage
- **Cloud Integration**: Upload/download from cloud storage
- **API Integration**: Connect to web services and APIs