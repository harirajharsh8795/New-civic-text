import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Model load
model_path = "model/saved_model"   # make sure ye folder repo me upload kare
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=1).item()
        confidence = predictions[0][predicted_class].item()
    return {"predicted_class": int(predicted_class), "confidence": float(confidence)}

# Gradio UI
demo = gr.Interface(
    fn=predict,
    inputs="text",
    outputs="json",
    title="Text Classifier",
    description="Enter text to get predicted class"
)

if __name__ == "__main__":
    demo.launch()
