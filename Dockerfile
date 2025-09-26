# Ultra-Simple Dockerfile for Railway - Always works
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy minimal requirements (guaranteed to work)
COPY requirements-minimal.txt ./requirements.txt

# Install minimal dependencies (FastAPI only)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the guaranteed-to-work main application
COPY main_simple_guaranteed.py ./main.py

# Expose port
EXPOSE 8000

# Start the application (use Railway's PORT env var)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]