from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Civic Text Classification API",
    description="API for classifying civic issues into categories: streetlight, garbage, potholes",
    version="1.0.0"
)

# Global variables for model and tokenizer
model = None
tokenizer = None

# Request/Response models
class TextInput(BaseModel):
    text: str
    
class ClassificationResult(BaseModel):
    text: str
    predicted_category: str
    confidence: float
    
class BatchTextInput(BaseModel):
    texts: List[str]
    
class BatchClassificationResult(BaseModel):
    results: List[ClassificationResult]

# Load model and tokenizer
def load_model():
    global model, tokenizer
    try:
        model_path = "./model/saved_model"
        
        # Check if model exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
            
        logger.info("Loading tokenizer and model...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        # Set model to evaluation mode
        model.eval()
        logger.info("Model loaded successfully!")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise e

# Classification function
def classify_text(text: str) -> Dict:
    """
    Classify a single text input
    """
    try:
        # Tokenize input
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_class_id = probs.argmax().item()
            confidence = probs[0][predicted_class_id].item()
        
        # Get predicted label
        predicted_label = model.config.id2label[predicted_class_id]
        
        return {
            "text": text,
            "predicted_category": predicted_label,
            "confidence": confidence
        }
        
    except Exception as e:
        logger.error(f"Error during classification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        load_model()
    except Exception as e:
        logger.error(f"Failed to load model on startup: {str(e)}")
        # Don't raise exception here to allow app to start even if model fails to load

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = model is not None and tokenizer is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded,
        "message": "API is running" if model_loaded else "Model not loaded"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Civic Text Classification API",
        "version": "1.0.0",
        "description": "Classify civic issues into: streetlight, garbage, potholes",
        "endpoints": {
            "classify": "/classify",
            "classify_batch": "/classify/batch",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Single text classification endpoint
@app.post("/classify", response_model=ClassificationResult)
async def classify_single_text(input_data: TextInput):
    """
    Classify a single text input
    
    **Categories:**
    - streetlight: Issues related to street lighting
    - garbage: Waste management and cleanliness issues  
    - potholes: Road condition and pothole problems
    
    **Supports both English and Hindi text**
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check model files.")
    
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    
    try:
        result = classify_text(input_data.text)
        return ClassificationResult(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Batch text classification endpoint
@app.post("/classify/batch", response_model=BatchClassificationResult)
async def classify_batch_text(input_data: BatchTextInput):
    """
    Classify multiple texts at once
    
    **Maximum 50 texts per request**
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check model files.")
    
    if len(input_data.texts) == 0:
        raise HTTPException(status_code=400, detail="No texts provided")
    
    if len(input_data.texts) > 50:
        raise HTTPException(status_code=400, detail="Maximum 50 texts allowed per request")
    
    try:
        results = []
        for text in input_data.texts:
            if text.strip():  # Skip empty texts
                result = classify_text(text)
                results.append(ClassificationResult(**result))
            else:
                results.append(ClassificationResult(
                    text=text,
                    predicted_category="unknown",
                    confidence=0.0
                ))
        
        return BatchClassificationResult(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get model information
@app.get("/model/info")
async def get_model_info():
    """Get information about the loaded model"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_name": model.config.name_or_path if hasattr(model.config, 'name_or_path') else "distilbert-base-uncased",
        "num_labels": model.config.num_labels,
        "label_mapping": model.config.id2label,
        "max_length": tokenizer.model_max_length,
        "tokenizer_vocab_size": tokenizer.vocab_size
    }

# Example texts endpoint
@app.get("/examples")
async def get_examples():
    """Get example texts for testing the API"""
    return {
        "examples": [
            {
                "text": "The streetlight near my home is broken",
                "expected_category": "streetlight"
            },
            {
                "text": "There is garbage dumped on the roadside",
                "expected_category": "garbage"
            },
            {
                "text": "The road has a big pothole causing accidents",
                "expected_category": "potholes"
            },
            {
                "text": "Hamari gali ki light kharab hai",
                "expected_category": "streetlight"
            },
            {
                "text": "Sadak mein gadha hai",
                "expected_category": "potholes"
            },
            {
                "text": "Kachra faila hua hai yahan",
                "expected_category": "garbage"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)