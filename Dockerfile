FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy pipeline scripts
COPY scripts/ scripts/

# Default command: run full pipeline
CMD ["python", "scripts/run_pipeline.py"]
