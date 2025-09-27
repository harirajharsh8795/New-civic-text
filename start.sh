#!/bin/bash#!/bin/bash

echo "🚀 Starting Civic Text Classifier API"# Railway startup script

echo "📍 Port: ${PORT:-8000}"

python main.pyecho "Starting Civic Text Classifier API..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Install dependencies if needed
echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Start the application
echo "Starting FastAPI application..."
exec python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}