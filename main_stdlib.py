import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class CivicClassifier:
    def predict(self, text):
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight']):
            return 0, "streetlight", 0.85
        elif any(word in text_lower for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
            return 1, "garbage", 0.88
        elif any(word in text_lower for word in ['pothole', 'road', 'street', 'crack', 'hole']):
            return 2, "potholes", 0.82
        else:
            return 2, "potholes", 0.3

classifier = CivicClassifier()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            response = {
                "message": "Civic Text Classifier API is running!",
                "status": "healthy",
                "framework": "Python Standard Library",
                "port": os.environ.get("PORT", "8000")
            }
        elif parsed_path.path == '/health':
            response = {
                "status": "healthy",
                "message": "Python HTTP server working",
                "classifier": "rule_based"
            }
        else:
            self.send_response(404)
            self.end_headers()
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                text = data.get('text', '')
                
                predicted_class, predicted_label, confidence = classifier.predict(text)
                
                response = {
                    "text": text,
                    "predicted_class": predicted_class,
                    "predicted_label": predicted_label,
                    "confidence": round(confidence, 3),
                    "model_type": "rule_based_stdlib"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Python HTTP Server on port {port}")
    server = HTTPServer(('0.0.0.0', port), RequestHandler)
    print(f"Server running at http://0.0.0.0:{port}")
    server.serve_forever()