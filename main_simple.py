from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Simple rule-based classifier as fallback
class SimpleClassifier:
    def __init__(self):
        self.streetlight_keywords = ['light', 'lamp', 'bulb', 'lighting', 'dark', 'illumination', 'street light', 'streetlight']
        self.garbage_keywords = ['garbage', 'trash', 'waste', 'litter', 'bin', 'dump', 'refuse', 'rubbish']
        self.pothole_keywords = ['pothole', 'road', 'street', 'pavement', 'crack', 'hole', 'surface', 'asphalt']
    
    def predict(self, text):
        text_lower = text.lower()
        
        streetlight_score = sum(1 for keyword in self.streetlight_keywords if keyword in text_lower)
        garbage_score = sum(1 for keyword in self.garbage_keywords if keyword in text_lower)
        pothole_score = sum(1 for keyword in self.pothole_keywords if keyword in text_lower)
        
        scores = [streetlight_score, garbage_score, pothole_score]
        predicted_class = scores.index(max(scores))
        confidence = max(scores) / (sum(scores) + 1)  # Normalize
        
        labels = ["streetlight", "garbage", "potholes"]
        return predicted_class, labels[predicted_class], confidence

# Global classifier
simple_classifier = SimpleClassifier()
model_loaded = False

# Try to load transformers model, fallback to simple classifier
def load_model():
    global model_loaded
    try:
        # Try to import transformers
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        
        # Try to load local model first
        model_path = "model/saved_model"
        if os.path.exists(model_path):
            logger.info("Loading local model...")
            global tokenizer, model
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
            model.eval()
            model_loaded = True
            logger.info("Local model loaded successfully!")
            return True
        else:
            logger.info("Local model not found, using simple rule-based classifier")
            return True
            
    except ImportError as e:
        logger.warning(f"Transformers not available: {e}. Using simple rule-based classifier")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}. Using simple rule-based classifier")
        return True

# Load model on startup
@app.on_event("startup")
async def startup_event():
    success = load_model()
    if success:
        logger.info("Classifier initialized successfully!")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Civic Text Classifier API is running!", "model_type": "advanced" if model_loaded else "simple"}

@app.post("/predict")
def predict(request: TextRequest):
    try:
        if model_loaded:
            # Use advanced model
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            import torch
            
            inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(predictions, dim=1).item()
            
            civic_labels = {0: "streetlight", 1: "garbage", 2: "potholes"}
            predicted_label = civic_labels.get(predicted_class, f"civic_issue_{predicted_class}")
            confidence = float(predictions[0][int(predicted_class)].item())
            model_type = "advanced_transformers"
            
        else:
            # Use simple classifier
            predicted_class, predicted_label, confidence = simple_classifier.predict(request.text)
            model_type = "simple_rules"
        
        return {
            "text": request.text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "model_type": model_type
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        # Fallback to simple classifier
        predicted_class, predicted_label, confidence = simple_classifier.predict(request.text)
        return {
            "text": request.text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "model_type": "fallback_simple",
            "note": "Used fallback classifier due to error"
        }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_status": "advanced" if model_loaded else "simple",
        "message": "Civic Text Classifier API is running"
    }