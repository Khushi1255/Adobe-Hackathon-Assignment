FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pdfstructure source code
COPY src/ ./src/

# Copy the main processing script
COPY process_pdfs.py .

# Set the entry point
CMD ["python", "process_pdfs.py"] 