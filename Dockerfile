# Dockerfile for building custom base image with common module
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the common module and other project files
COPY common/ ./common/
COPY setup.py .

# Install the package to make common module accessible
RUN pip install -e .

# Set Python path to include the app directory
ENV PYTHONPATH=/app:$PYTHONPATH

# Default command
CMD ["python"]
