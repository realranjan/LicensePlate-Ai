FROM python:3.10-slim-bullseye

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PORT 5000

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

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
