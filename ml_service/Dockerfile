FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PORT 5000
ENV PYTHONPATH=/app/yolov5:$PYTHONPATH

# Install OpenCV dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libtool \
    libgl1-mesa-glx \
    libxext6 \
    libsm6 \
    libxrender1 \
    libglib2.0-0 \
    libgtk2.0-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip cache purge

# Install git and wget
RUN apt-get update && apt-get install -y git wget && rm -rf /var/lib/apt/lists/*

# Clone YOLOv5 repository
RUN git clone https://github.com/ultralytics/yolov5.git /app/yolov5

# Download a smaller YOLOv5 model if not already present
RUN mkdir -p /app/data/models
RUN if [ ! -f /app/data/models/yolov5s.pt ]; then \
        wget -P /app/data/models https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt; \
    fi

# Copy and run quantization script
COPY quantize_model.py /app/quantize_model.py
RUN python /app/quantize_model.py

# Copy application files
COPY app.py /app/app.py
COPY data /app/data

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
