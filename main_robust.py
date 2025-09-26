from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Global variables
tokenizer = None
model = None
model_type = None

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
rule_classifier = CivicClassifier()

def load_model():
    global tokenizer, model, model_type
    try:
        # Try to import transformers and torch
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        
        # First priority: Load our trained civic model
        model_path = "model/saved_model"
        if os.path.exists(model_path):
            logger.info("Loading trained civic model...")
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
            model.eval()
            model_type = "trained_model"
            logger.info("✅ Trained civic model loaded successfully!")
            return True
        
        # Second priority: Use rule-based classifier
        logger.info("Trained model not found, using rule-based classifier")
        model_type = "rule_based"
        return "rule_based"
        
    except ImportError as e:
        logger.warning(f"ML libraries not available: {e}. Using rule-based classifier")
        model_type = "rule_based"
        return "rule_based"
    except Exception as e:
        logger.error(f"Error loading model: {e}. Using rule-based classifier")
        model_type = "rule_based"
        return "rule_based"

# Load model on startup
@app.on_event("startup")
async def startup_event():
    global model_type
    result = load_model()
    if result == True:
        model_type = "trained_model"
        logger.info("✅ Startup complete with trained model")
    else:
        model_type = "rule_based"
        logger.info("✅ Startup complete with rule-based classifier")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {
        "message": "Civic Text Classifier API is running!",
        "model_type": model_type or "rule_based",
        "supported_categories": ["streetlight", "garbage", "potholes"]
    }

@app.post("/predict")
def predict(request: TextRequest):
    try:
        # Try trained model first (highest accuracy)
        if tokenizer is not None and model is not None:
            import torch
            inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
            with torch.no_grad():
                outputs = model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = int(torch.argmax(predictions, dim=1).item())
            
            # Use civic labels for our trained model
            civic_labels = {0: "streetlight", 1: "garbage", 2: "potholes"}
            predicted_label = civic_labels.get(predicted_class, f"civic_issue_{predicted_class}")
            confidence = float(predictions[0][predicted_class].item())
            
            return {
                "text": request.text,
                "predicted_class": predicted_class,
                "predicted_label": predicted_label,
                "confidence": confidence,
                "model_type": "trained_civic_model"
            }
        
        # Use rule-based classifier (still accurate for civic issues)
        else:
            predicted_class, predicted_label, confidence = rule_classifier.predict(request.text)
            
            return {
                "text": request.text,
                "predicted_class": predicted_class,
                "predicted_label": predicted_label,
                "confidence": confidence,
                "model_type": "rule_based_classifier"
            }
            
    except Exception as e:
        logger.error(f"Prediction error with trained model: {str(e)}")
        # Final fallback to rule-based classifier
        try:
            predicted_class, predicted_label, confidence = rule_classifier.predict(request.text)
            return {
                "text": request.text,
                "predicted_class": predicted_class,
                "predicted_label": predicted_label,
                "confidence": confidence,
                "model_type": "rule_based_fallback",
                "note": "Used fallback due to model error"
            }
        except Exception as fallback_error:
            logger.error(f"Fallback error: {str(fallback_error)}")
            raise HTTPException(status_code=500, detail="All prediction methods failed")

@app.get("/health")
def health_check():
    if tokenizer is not None and model is not None:
        status = "healthy"
        model_status = "trained_model_loaded"
        accuracy = "high"
    else:
        status = "healthy"
        model_status = "rule_based_active"
        accuracy = "good"
    
    return {
        "status": status,
        "model_status": model_status,
        "prediction_accuracy": accuracy,
        "message": "Civic Text Classifier API is running",
        "supported_categories": ["streetlight", "garbage", "potholes"]
    }