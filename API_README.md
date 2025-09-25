# 🏛️ Civic Text Classification API

A FastAPI-based REST API for classifying civic issues into categories: **streetlight**, **garbage**, and **potholes**. The API supports both English and Hindi text inputs and uses a fine-tuned DistilBERT model.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Trained model (run the Jupyter notebook first)
- Virtual environment (recommended)

### 1. Setup Environment
```bash
# Activate your virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Train the Model (if not done already)
```bash
# Run the Jupyter notebook to train and save the model
jupyter notebook notebook/text_classifier.ipynb
```

### 3. Start the API Server

#### Option A: Using the deployment script
```bash
python deploy.py
```

#### Option B: Direct uvicorn command
```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Access the API
- **API Server**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📡 API Endpoints

### 🏠 Root Endpoint
```http
GET /
```
Returns API information and available endpoints.

### 🏥 Health Check
```http
GET /health
```
Check if the API and model are loaded properly.

### 🔍 Single Text Classification
```http
POST /classify
Content-Type: application/json

{
  "text": "The streetlight near my home is broken"
}
```

**Response:**
```json
{
  "text": "The streetlight near my home is broken",
  "predicted_category": "streetlight",
  "confidence": 0.9999548196792603
}
```

### 📊 Batch Classification
```http
POST /classify/batch
Content-Type: application/json

{
  "texts": [
    "The streetlight is not working",
    "Garbage is everywhere",
    "Road has potholes"
  ]
}
```

### 📋 Get Examples
```http
GET /examples
```
Returns example texts for testing the API.

### 🤖 Model Information
```http
GET /model/info
```
Returns information about the loaded model.

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the Docker image
docker build -t civic-text-api .

# Run the container
docker run -p 8000:8000 civic-text-api
```

### Using Docker Compose
```bash
# Start the service
docker-compose up -d

# Stop the service
docker-compose down
```

## 📝 Example Usage

### Python Client
```python
import requests

# Single classification
response = requests.post(
    "http://127.0.0.1:8000/classify",
    json={"text": "Street light is not working"}
)
result = response.json()
print(f"Category: {result['predicted_category']}")
print(f"Confidence: {result['confidence']:.4f}")

# Batch classification
response = requests.post(
    "http://127.0.0.1:8000/classify/batch",
    json={
        "texts": [
            "Streetlight khrab hai",
            "Sadak mein gadha hai",
            "Kachra faila hua hai"
        ]
    }
)
results = response.json()
for result in results['results']:
    print(f"{result['text']} -> {result['predicted_category']}")
```

### cURL Examples
```bash
# Single classification
curl -X POST "http://127.0.0.1:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "The streetlight is broken"}'

# Health check
curl http://127.0.0.1:8000/health

# Get examples
curl http://127.0.0.1:8000/examples
```

### JavaScript/Node.js
```javascript
const axios = require('axios');

async function classifyText(text) {
    try {
        const response = await axios.post('http://127.0.0.1:8000/classify', {
            text: text
        });
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
    }
}

// Usage
classifyText("The road has potholes").then(result => {
    console.log(`Category: ${result.predicted_category}`);
    console.log(`Confidence: ${result.confidence}`);
});
```

## 🎯 Supported Categories

| Category | Description | Example (English) | Example (Hindi) |
|----------|-------------|-------------------|-----------------|
| **streetlight** | Street lighting issues | "The streetlight is broken" | "Hamari gali ki light kharab hai" |
| **garbage** | Waste management issues | "Garbage is everywhere" | "Kachra faila hua hai" |
| **potholes** | Road condition problems | "Road has big potholes" | "Sadak mein gadha hai" |

## ⚙️ Configuration

### Environment Variables
```bash
# Optional environment variables
export MODEL_PATH="./model/saved_model"  # Path to the trained model
export API_HOST="0.0.0.0"                # API host
export API_PORT="8000"                    # API port
export LOG_LEVEL="INFO"                   # Logging level
```

### API Limits
- Maximum 50 texts per batch request
- Maximum text length: 128 tokens
- Request timeout: 30 seconds

## 🔧 Troubleshooting

### Model Not Found Error
```
❌ Model not found at ./model/saved_model
```
**Solution**: Run the Jupyter notebook `notebook/text_classifier.ipynb` to train and save the model.

### Port Already in Use
```
❌ Port 8000 is already in use
```
**Solution**: Use a different port:
```bash
uvicorn app:app --host 127.0.0.1 --port 8001
```

### Memory Issues
If you encounter memory issues, try:
1. Reducing batch size in requests
2. Using CPU-only inference
3. Increasing system memory

## 📊 Performance

- **Average Response Time**: ~100ms per text
- **Throughput**: ~10 requests/second (single worker)
- **Memory Usage**: ~500MB (model loaded)
- **Model Size**: ~250MB

## 🔒 Security Considerations

- The API runs without authentication by default
- For production deployment, consider adding:
  - API key authentication
  - Rate limiting
  - Input validation and sanitization
  - HTTPS/TLS encryption

## 📈 Monitoring

The API includes basic health checks. For production monitoring, consider:
- Prometheus metrics endpoint
- Structured logging
- Error tracking (Sentry)
- Performance monitoring (APM)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Support

For issues and questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Review the API documentation at `/docs`