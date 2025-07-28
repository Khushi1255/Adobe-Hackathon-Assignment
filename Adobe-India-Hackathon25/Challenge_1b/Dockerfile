FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies including LibreOffice
RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Copy the main processing script and model downloader
COPY process_challenge1b.py .
COPY download_models.py .

# Download models during build for offline operation
RUN python download_models.py

# Set the entry point
CMD ["python", "process_challenge1b.py"] 