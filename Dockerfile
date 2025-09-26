# Simplified Dockerfile for Railway - Prioritizes Model Accuracy
FROM python:3.9-slim

# Set environment variables for better performance
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Copy requirements (use balanced dependencies that support both models)
COPY requirements-balanced.txt ./requirements.txt

# Install dependencies efficiently
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the main application (prioritizes trained model)
COPY main.py .

# Copy trained model (optional - will fallback if not available)
COPY model ./model

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]