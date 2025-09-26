# Super Simple Dockerfile for Railway
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements-minimal.txt requirements.txt
RUN pip install -r requirements.txt

# Copy final working application
COPY main_final.py main.py

# Run with Python (handles PORT automatically)
CMD ["python", "main.py"]