import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Create FastAPI app
app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Simple but effective civic classifier
class CivicClassifier:
    def __init__(self):
        self.streetlight_keywords = ['light', 'lamp', 'bulb', 'lighting', 'streetlight', 'illumination']
        self.garbage_keywords = ['garbage', 'trash', 'waste', 'litter', 'bin', 'rubbish']
        self.pothole_keywords = ['pothole', 'road', 'street', 'crack', 'hole', 'pavement']
    
    def predict(self, text):
        text_lower = text.lower()
        
        streetlight_score = sum(1 for word in self.streetlight_keywords if word in text_lower)
        garbage_score = sum(1 for word in self.garbage_keywords if word in text_lower)
        pothole_score = sum(1 for word in self.pothole_keywords if word in text_lower)
        
        scores = [streetlight_score, garbage_score, pothole_score]
        labels = ["streetlight", "garbage", "potholes"]
        
        if max(scores) == 0:
            predicted_class = 2  # default to potholes
            confidence = 0.3
        else:
            predicted_class = scores.index(max(scores))
            confidence = max(scores) / sum(scores) if sum(scores) > 0 else 0.3
        
        return predicted_class, labels[predicted_class], min(confidence, 0.95)

# Initialize classifier
classifier = CivicClassifier()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {
        "message": "Civic Text Classifier API is running!",
        "status": "healthy",
        "endpoints": ["/", "/health", "/predict"],
        "port": os.environ.get("PORT", "8000")
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "API is working perfectly",
        "classifier": "rule_based",
        "categories": ["streetlight", "garbage", "potholes"]
    }

@app.post("/predict")
def predict(request: TextRequest):
    predicted_class, predicted_label, confidence = classifier.predict(request.text)
    return {
        "text": request.text,
        "predicted_class": predicted_class,
        "predicted_label": predicted_label,
        "confidence": round(confidence, 3),
        "model_type": "rule_based_classifier"
    }

# This is the key part - Railway needs this for proper startup
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Civic Text Classifier API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")