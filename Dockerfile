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

# Copy the robust main application (works with or without ML libs)
COPY main_robust.py ./main.py

# Copy model folder (optional - app works without it)
COPY model ./model

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]