# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Prevent Python from writing pyc files to disk and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-turbo-progs \
    zlib1g \
    python3-dev \
    libffi-dev \
    curl \
    tzdata \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .  

# Debugging: Check if requirements.txt exists
RUN test -f requirements.txt && cat requirements.txt

# Install Python dependencies with increased timeout
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt  

# Copy the rest of the application code
COPY . .  

# Expose the port that uvicorn will run on
EXPOSE 8000  

# Health check to verify container status
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8000/ || exit 1

# Command to run the application with uvicorn
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
