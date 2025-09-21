FROM python:3.10-slim-bullseye

WORKDIR /app/ml_models

ENV PYTHONUNBUFFERED 1

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

COPY . .

EXPOSE 5000

# Default command if no specific command is provided
CMD ["python", "detection/detect2.py", "--source", "data/images/samples/KA63U5588.jpg", "--save-txt", "--save-conf"]
