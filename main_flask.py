import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple civic classifier
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
            predicted_class = 2
            confidence = 0.3
        else:
            predicted_class = scores.index(max(scores))
            confidence = max(scores) / sum(scores) if sum(scores) > 0 else 0.3
        
        return predicted_class, labels[predicted_class], min(confidence, 0.95)

classifier = CivicClassifier()

@app.route('/')
def home():
    return jsonify({
        "message": "Civic Text Classifier API is running!",
        "status": "healthy",
        "framework": "Flask",
        "port": os.environ.get("PORT", "8000")
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "message": "Flask API is working",
        "classifier": "rule_based"
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field"}), 400
        
        text = data['text']
        predicted_class, predicted_label, confidence = classifier.predict(text)
        
        return jsonify({
            "text": text,
            "predicted_class": predicted_class,
            "predicted_label": predicted_label,
            "confidence": round(confidence, 3),
            "model_type": "rule_based_flask"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask Civic Text Classifier on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)