# ML Models

This directory contains the machine learning components for the License Plate Recognition System, including YOLOv5 models and detection scripts.

## Structure

```
ml_models/
├── yolov5/              # YOLOv5 framework and models
├── detection/           # Custom detection scripts
│   ├── detect.py        # Basic detection script
│   ├── detect2.py       # Enhanced detection with web integration
│   └── detect3.py       # Advanced detection with filtering
├── hubconf.py          # PyTorch Hub configuration
├── requirements.txt    # ML-specific dependencies
└── README.md          # This file
```

## Models

The system uses YOLOv5 for license plate detection. Pre-trained models are stored in the `data/models/` directory:

- `best.pt` - Custom trained model for license plate detection
- `1500img.pt` - Alternative trained model

## Detection Scripts

### detect.py
Basic YOLOv5 detection script with standard functionality.

### detect2.py  
Enhanced detection script with web application integration features.

### detect3.py
Advanced detection script with additional filtering and post-processing capabilities.

## Usage

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running Detection

From the project root directory:

```bash
# Basic detection
python ml_models/detection/detect.py --weights data/models/best.pt --source path/to/image.jpg

# Web-integrated detection
python ml_models/detection/detect2.py --weights data/models/best.pt --source path/to/image.jpg

# Advanced detection with filtering
python ml_models/detection/detect3.py --weights data/models/best.pt --source path/to/image.jpg
```

### Common Parameters

- `--weights`: Path to model weights (default: yolov5s.pt)
- `--source`: Input source (image, video, directory, webcam)
- `--conf-thres`: Confidence threshold (default: 0.25)
- `--iou-thres`: IoU threshold for NMS (default: 0.45)
- `--imgsz`: Inference size (default: 640)
- `--save-txt`: Save results to txt files
- `--save-crop`: Save cropped prediction boxes

## Model Information

### YOLOv5 Architecture
The system uses YOLOv5 (You Only Look Once version 5) for real-time object detection:

- **Input**: RGB images of various sizes (resized to 640x640 for inference)
- **Output**: Bounding boxes with confidence scores for detected license plates
- **Performance**: Optimized for real-time detection with good accuracy

### Custom Training
The models have been trained on license plate datasets to specifically detect:
- Indian license plates
- Various plate formats and orientations
- Different lighting conditions
- Multiple vehicle types

## Integration

The detection scripts are designed to work with:
- **Web Application**: Django-based interface in `web_app/`
- **Desktop Application**: Tkinter GUI in `desktop_app/`
- **Data Pipeline**: Automated processing of image batches

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running scripts from the project root directory
2. **CUDA Issues**: Install appropriate PyTorch version for your GPU
3. **Model Loading**: Verify model files exist in `data/models/`
4. **Path Issues**: Use absolute paths or run from project root

### Performance Optimization

- Use GPU acceleration when available
- Adjust batch size based on available memory
- Consider model quantization for deployment
- Use appropriate image sizes for your use case

## Dependencies

### Core ML Dependencies
- **PyTorch 2.1.0**: Deep learning framework with CUDA support
- **torchvision 0.16.0**: Computer vision utilities and transforms
- **torchaudio 2.1.0**: Audio processing (YOLOv5 dependency)
- **Ultralytics 8.0.232**: YOLOv5 implementation and training utilities

### Computer Vision
- **OpenCV 4.8.1**: Image and video processing operations
- **Pillow 10.0.1**: Image format support and basic operations
- **albumentations 1.3.1**: Advanced image augmentation techniques
- **imgaug 0.4.0**: Additional augmentation methods

### Scientific Computing
- **NumPy 1.24.3**: Numerical operations and array handling
- **SciPy 1.11.4**: Scientific computing and optimization
- **pandas 2.1.3**: Data manipulation and analysis
- **matplotlib 3.7.2**: Plotting and visualization
- **seaborn 0.13.0**: Statistical data visualization

### Model Optimization
- **thop 0.1.1**: FLOPs computation and model analysis
- **tensorboard 2.15.1**: Training visualization and monitoring
- **wandb 0.16.0**: Experiment tracking and model management (optional)

### Performance Monitoring
- **psutil 5.9.6**: System resource monitoring
- **py-cpuinfo 9.0.0**: CPU information and capabilities
- **GPUtil 1.4.0**: GPU monitoring and utilization

### Export and Deployment
- **onnx 1.15.0**: ONNX model export (optional)
- **onnxruntime 1.16.3**: ONNX model inference (optional)
- **flask 3.0.0**: Lightweight web server for model serving
- **fastapi 0.104.1**: Modern API framework for model deployment
- **uvicorn 0.24.0**: ASGI server for FastAPI

### Installation Order
1. Install core dependencies: `pip install -r ../requirements.txt`
2. Install ML-specific dependencies: `pip install -r requirements.txt`
3. For export features, uncomment optional dependencies in requirements.txt

## Model Performance

### Inference Speed
- **CPU**: ~200-500ms per image (depending on image size)
- **GPU (CUDA)**: ~50-100ms per image
- **Batch Processing**: Significant speedup for multiple images

### Accuracy Metrics
- **mAP@0.5**: >0.85 on test dataset
- **Precision**: >0.90 for license plate detection
- **Recall**: >0.85 for license plate detection

### Memory Usage
- **Model Size**: ~14MB (YOLOv5s) to ~140MB (YOLOv5x)
- **Runtime Memory**: 1-4GB depending on batch size and image resolution
- **GPU Memory**: 2-8GB recommended for training

## Development

### Model Training
```bash
# Train custom model
python train.py --data custom_dataset.yaml --weights yolov5s.pt --epochs 100

# Resume training
python train.py --resume runs/train/exp/weights/last.pt

# Validate model
python val.py --weights best.pt --data custom_dataset.yaml
```

### Model Export
```bash
# Export to ONNX
python export.py --weights best.pt --include onnx

# Export to TensorRT
python export.py --weights best.pt --include engine --device 0

# Export to CoreML (macOS)
python export.py --weights best.pt --include coreml
```

### Development Guidelines
1. **Testing**: Test with sample images before deployment
2. **Compatibility**: Verify output format works with web/desktop apps
3. **Documentation**: Update README for new parameters or features
4. **Versioning**: Maintain backward compatibility with existing integrations
5. **Performance**: Profile code for bottlenecks and optimization opportunities

### Code Quality
- Follow PEP 8 style guidelines
- Add type hints for function parameters and returns
- Include docstrings for all functions and classes
- Write unit tests for new functionality
- Use logging instead of print statements