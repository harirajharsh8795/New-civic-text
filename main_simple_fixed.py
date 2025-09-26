from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Simple rule-based classifier
class CivicClassifier:
    def predict(self, text):
        text_lower = text.lower()
        
        # Simple keyword matching
        if any(word in text_lower for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight']):
            return 0, "streetlight", 0.85
        elif any(word in text_lower for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
            return 1, "garbage", 0.88
        elif any(word in text_lower for word in ['pothole', 'road', 'street', 'crack', 'hole']):
            return 2, "potholes", 0.82
        else:
            return 2, "potholes", 0.3  # Default

classifier = CivicClassifier()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Civic Text Classifier API is running!", "status": "healthy"}

@app.get("/health")
def health():
    return {"status": "healthy", "message": "API is working"}

@app.post("/predict")
def predict(request: TextRequest):
    predicted_class, predicted_label, confidence = classifier.predict(request.text)
    return {
        "text": request.text,
        "predicted_class": predicted_class,
        "predicted_label": predicted_label,
        "confidence": confidence,
        "model_type": "rule_based"
    }