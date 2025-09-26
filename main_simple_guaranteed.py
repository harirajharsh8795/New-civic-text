from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Enhanced rule-based classifier for accurate civic issue detection
class CivicClassifier:
    def __init__(self):
        # Expanded keywords for better accuracy
        self.streetlight_keywords = [
            'light', 'lamp', 'bulb', 'lighting', 'dark', 'illumination', 
            'street light', 'streetlight', 'pole', 'electrical', 'brightness',
            'dim', 'flickering', 'not working', 'broken light', 'lamp post'
        ]
        self.garbage_keywords = [
            'garbage', 'trash', 'waste', 'litter', 'bin', 'dump', 'refuse', 
            'rubbish', 'disposal', 'collection', 'recycling', 'dumpster',
            'cleanup', 'dirty', 'smell', 'stinking', 'overflow'
        ]
        self.pothole_keywords = [
            'pothole', 'road', 'street', 'pavement', 'crack', 'hole', 
            'surface', 'asphalt', 'bump', 'rough', 'damaged', 'repair',
            'construction', 'uneven', 'dangerous', 'vehicle damage'
        ]
    
    def predict(self, text):
        text_lower = text.lower()
        
        # Score each category with weighted keywords
        streetlight_score = sum(2 if 'light' in keyword else 1 
                               for keyword in self.streetlight_keywords 
                               if keyword in text_lower)
        garbage_score = sum(2 if 'garbage' in keyword or 'trash' in keyword else 1 
                           for keyword in self.garbage_keywords 
                           if keyword in text_lower)
        pothole_score = sum(2 if 'pothole' in keyword or 'road' in keyword else 1 
                           for keyword in self.pothole_keywords 
                           if keyword in text_lower)
        
        scores = [streetlight_score, garbage_score, pothole_score]
        total_score = sum(scores)
        
        if total_score == 0:
            # Default to most common issue if no keywords found
            predicted_class = 2  # potholes as default
            confidence = 0.3
        else:
            predicted_class = scores.index(max(scores))
            confidence = max(scores) / total_score
        
        labels = ["streetlight", "garbage", "potholes"]
        return predicted_class, labels[predicted_class], min(confidence, 0.95)

# Initialize rule-based classifier
classifier = CivicClassifier()
logger.info("✅ Civic Text Classifier initialized successfully!")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {
        "message": "Civic Text Classifier API is running!",
        "model_type": "rule_based_classifier",
        "supported_categories": ["streetlight", "garbage", "potholes"],
        "status": "healthy"
    }

@app.post("/predict")
def predict(request: TextRequest):
    try:
        predicted_class, predicted_label, confidence = classifier.predict(request.text)
        
        return {
            "text": request.text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "model_type": "rule_based_classifier"
        }
            
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_status": "rule_based_active",
        "prediction_accuracy": "good",
        "message": "Civic Text Classifier API is running",
        "supported_categories": ["streetlight", "garbage", "potholes"]
    }

# Add a simple startup log
logger.info("🚀 FastAPI application ready to serve requests!")