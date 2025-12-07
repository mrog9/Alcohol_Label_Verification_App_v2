# Use a slim Python base image
FROM python:3.9-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir numpy opencv-python-headless flask

# Set working directory
WORKDIR /app

# Copy service code
COPY . /app

# Expose port for Flask
EXPOSE 5000

# Run the preprocessing service
CMD ["python", "preprocess_service.py"]
