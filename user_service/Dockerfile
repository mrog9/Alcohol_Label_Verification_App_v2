# Use a slim Python base image
FROM python:3.9-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (Flask needs very little)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask requests

# Set working directory
WORKDIR /app

# Copy service code
COPY . /app

# Expose port for Flask
EXPOSE 5000

# Run the frontend service
CMD ["python", "app.py"]
