import os
import sys
import logging
from fastapi import FastAPI
from pydantic import BaseModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("=== STARTING CIVIC TEXT CLASSIFIER ===")
print(f"Python version: {sys.version}")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
print(f"Working directory: {os.getcwd()}")

app = FastAPI(title="Civic Text Classifier API")

# Simple classifier
class CivicClassifier:
    def predict(self, text):
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight']):
            return 0, "streetlight", 0.85
        elif any(word in text_lower for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
            return 1, "garbage", 0.88
        elif any(word in text_lower for word in ['pothole', 'road', 'street', 'crack', 'hole']):
            return 2, "potholes", 0.82
        else:
            return 2, "potholes", 0.3

classifier = CivicClassifier()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    print("HOME endpoint called")
    return {"message": "Civic Text Classifier API is running!", "status": "healthy", "port": os.environ.get('PORT', 'unknown')}

@app.get("/health")
def health():
    print("HEALTH endpoint called")
    return {"status": "healthy", "message": "API is working", "port": os.environ.get('PORT', 'unknown')}

@app.post("/predict")
def predict(request: TextRequest):
    print(f"PREDICT endpoint called with text: {request.text}")
    try:
        predicted_class, predicted_label, confidence = classifier.predict(request.text)
        return {
            "text": request.text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "model_type": "rule_based"
        }
    except Exception as e:
        print(f"ERROR in prediction: {e}")
        return {"error": str(e)}

print("=== FASTAPI APP CREATED SUCCESSFULLY ===")
print("Available routes: /, /health, /predict")