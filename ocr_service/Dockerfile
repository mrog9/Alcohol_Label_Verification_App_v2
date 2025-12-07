# Use a slim Python base image
FROM python:3.9-slim

# Prevent interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by PyTorch + EasyOCR
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Pin versions to avoid pulling in heavy CUDA builds
RUN pip install --no-cache-dir torch==2.0.1+cpu torchvision==0.15.2+cpu \
    -f https://download.pytorch.org/whl/cpu/torch_stable.html \
    easyocr==1.7.1 flask

# Copy your service code into the container
WORKDIR /app
COPY . /app

# Expose port for Flask
EXPOSE 5000

# Run the OCR service
CMD ["python", "ocr_service.py"]
