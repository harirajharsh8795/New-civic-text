from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Civic Text Classifier API", version="1.0.0")

# Global variables
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    try:
        # Try to load local model first
        model_path = "model/saved_model"
        if os.path.exists(model_path):
            logger.info("Loading local tokenizer and model...")
            tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
        else:
            # Fallback to a lightweight pre-trained model for basic text classification
            logger.info("Local model not found, loading fallback model...")
            model_name = "distilbert-base-uncased"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            # For demo purposes, we'll use a generic sentiment model
            model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        
        model.eval()
        logger.info("Model loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        return False

# Load model on startup
@app.on_event("startup")
async def startup_event():
    success = load_model()
    if not success:
        logger.error("Failed to load model on startup")

class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Text Classifier API is running!"}

@app.post("/predict")
def predict(request: TextRequest):
    if tokenizer is None or model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class = torch.argmax(predictions, dim=1).item()
        
        # Define custom labels for civic issues if using our model
        civic_labels = {0: "streetlight", 1: "garbage", 2: "potholes"}
        
        # Check if we have custom labels or use the model's labels
        if hasattr(model.config, 'id2label') and model.config.id2label:
            predicted_label = model.config.id2label.get(predicted_class, f"class_{predicted_class}")
        else:
            # Use civic labels for our custom model
            predicted_label = civic_labels.get(predicted_class, f"civic_issue_{predicted_class}")
        
        return {
            "text": request.text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": float(predictions[0][int(predicted_class)].item()),
            "model_type": "custom_civic_model" if not hasattr(model.config, 'id2label') or not model.config.id2label else "fallback_model"
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/health")
def health_check():
    model_status = "loaded" if (tokenizer is not None and model is not None) else "not_loaded"
    return {
        "status": "healthy" if (tokenizer is not None and model is not None) else "unhealthy",
        "model_status": model_status,
        "model_loaded": tokenizer is not None and model is not None,
        "message": "Civic Text Classifier API is running"
    }
