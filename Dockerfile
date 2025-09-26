# Super Simple Dockerfile for Railway
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements-minimal.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application
COPY main_minimal.py main.py

# Use Python to run uvicorn directly
CMD python main.py