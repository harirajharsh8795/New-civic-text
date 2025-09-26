# Super Simple Dockerfile for Railway
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install
COPY requirements-minimal.txt requirements.txt
RUN pip install -r requirements.txt

# Copy application
COPY main_simple_fixed.py main.py

# Use Railway's PORT environment variable
CMD uvicorn main:app --host 0.0.0.0 --port $PORT