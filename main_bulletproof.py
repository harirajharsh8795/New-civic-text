#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class CivicClassifier:
    def predict(self, text):
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight']):
            return {"predicted_class": 0, "predicted_label": "streetlight", "confidence": 0.85}
        elif any(word in text_lower for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
            return {"predicted_class": 1, "predicted_label": "garbage", "confidence": 0.88}
        elif any(word in text_lower for word in ['pothole', 'road', 'street', 'crack', 'hole']):
            return {"predicted_class": 2, "predicted_label": "potholes", "confidence": 0.82}
        else:
            return {"predicted_class": 2, "predicted_label": "potholes", "confidence": 0.3}

classifier = CivicClassifier()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log all incoming requests for debugging
        print(f"📥 GET {self.path} from {self.client_address[0]}")
        print(f"🏠 Host header: {self.headers.get('Host', 'None')}")
        print(f"🕸️ User-Agent: {self.headers.get('User-Agent', 'None')}")
        
        # Accept requests from Railway's healthcheck hostname
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            if self.path == '/health':
                response = {
                    "status": "healthy",
                    "message": "API is working perfectly",
                    "hostname": self.headers.get('Host', 'unknown'),
                    "user_agent": self.headers.get('User-Agent', 'unknown')
                }
            else:
                response = {
                    "message": "Civic Text Classifier API is running!",
                    "status": "healthy",
                    "endpoints": ["/", "/health", "/predict"],
                    "port": os.environ.get("PORT", "8000")
                }
            
            self.wfile.write(json.dumps(response).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/predict':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                result = classifier.predict(text)
                result['text'] = text
                result['model_type'] = 'rule_based_classifier'
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                error_response = {"error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting Civic Text Classifier on 0.0.0.0:{port}")
    print(f"✅ Health check endpoint: http://0.0.0.0:{port}/health")
    print(f"🔍 Ready for Railway healthcheck from: healthcheck.railway.app")
    print(f"📝 Accepting all hostnames and origins")
    
    try:
        server = HTTPServer(('0.0.0.0', port), Handler)
        print(f"🎯 Server successfully bound to 0.0.0.0:{port}")
        print(f"⚡ Server is READY for traffic!")
        server.serve_forever()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        raise