from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load FastAPI
app = FastAPI(title="Text Classifier API")

# Load model and tokenizer
model_path = "model/saved_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Define request body
class TextRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Text Classifier API is running!"}

@app.post("/predict")
def predict(request: TextRequest):
    inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=1).item()
    
    return {
        "text": request.text,
        "predicted_class": int(predicted_class),
        "confidence": predictions[0][predicted_class].item()
    }
