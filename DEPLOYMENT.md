# Civic Text Classifier API - Deployment Guide

## Overview
This is a FastAPI application that classifies civic issues (streetlight, garbage, potholes) using a DistilBERT model.

## Render Deployment Settings

### Build Command
```bash
pip install -r requirements.txt
```

### Start Command
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Environment Variables
- `PORT`: Automatically set by Render
- `PYTHON_VERSION`: 3.9 (recommended)

## API Endpoints

### Health Check
- **GET** `/health`
- Returns the status of the API and model loading

### Text Classification
- **POST** `/predict`
- Body: `{"text": "Street light is not working"}`
- Returns: Classification result with confidence score

### Home
- **GET** `/`
- Basic API information

## Model Behavior
1. **Local Model**: If the custom trained model is available in `model/saved_model/`, it will use that for civic issue classification
2. **Fallback Model**: If local model is not available, it will use a lightweight DistilBERT sentiment model as a fallback

## Testing the API

### Health Check
```bash
curl https://your-app-name.onrender.com/health
```

### Prediction
```bash
curl -X POST https://your-app-name.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The streetlight on main street is broken"}'
```

## Troubleshooting
- If model fails to load, the API will still run with fallback model
- Check logs for model loading status
- Health endpoint shows model status

## Repository
https://github.com/2024021129-crypto/New-civic-text