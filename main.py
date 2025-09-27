from fastapi import FastAPI
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {
        "status": "healthy",
        "message": "Civic Text Classifier API",
        "version": "1.0",
        "port": os.environ.get("PORT", "8000")
    }

@app.get("/health")
def health():
    print("🏥 Health check endpoint called!")
    return {
        "status": "healthy",
        "message": "Railway healthcheck SUCCESS",
        "port": os.environ.get("PORT", "8000")
    }

@app.post("/predict")
def predict(request: TextRequest):
    text = request.text.lower()
    
    # Simple rule-based classification
    if any(word in text for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight', 'street light']):
        result = {
            "predicted_class": 0, 
            "predicted_label": "streetlight", 
            "confidence": 0.85
        }
    elif any(word in text for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
        result = {
            "predicted_class": 1, 
            "predicted_label": "garbage", 
            "confidence": 0.88
        }
    else:
        result = {
            "predicted_class": 2, 
            "predicted_label": "potholes", 
            "confidence": 0.82
        }
    
    result['text'] = request.text
    result['model_type'] = 'rule_based'
    
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting FastAPI server on port {port}")
    print(f"🌐 Health check available at: http://0.0.0.0:{port}/health")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")