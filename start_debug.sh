#!/bin/bash
echo "=== Railway Startup Debug ==="
echo "PORT: $PORT"
echo "Python version: $(python --version)"
echo "Working directory: $(pwd)"
echo "Files in directory:"
ls -la
echo "Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info