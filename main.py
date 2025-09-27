import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class RailwayHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"📝 {format % args}")
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            response = {
                "status": "healthy",
                "message": "Civic Text Classifier API - Railway Deployment",
                "version": "1.0",
                "endpoints": ["/", "/health", "/predict"]
            }
            self.send_json(response)
            
        elif parsed_path.path == '/health':
            print("🏥 HEALTH CHECK CALLED!")
            response = {"status": "healthy", "message": "OK"}
            self.send_json(response)
            
        elif parsed_path.path == '/predict':
            # Show usage instructions when accessed via GET (browser)
            response = {
                "message": "Prediction endpoint - Use POST method",
                "method": "POST",
                "url": "https://new-civic-text-production.up.railway.app/predict",
                "example": {
                    "input": {"text": "The street light is broken"},
                    "curl_example": 'curl -X POST "https://new-civic-text-production.up.railway.app/predict" -H "Content-Type: application/json" -d \'{"text": "The street light is broken"}\''
                },
                "supported_categories": ["streetlight", "garbage", "potholes"]
            }
            self.send_json(response)
            
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        if self.path == '/predict':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data)
                text = data.get('text', '').lower()
                
                # Classification logic
                if any(word in text for word in ['light', 'lamp', 'bulb', 'streetlight']):
                    result = {"predicted_class": 0, "predicted_label": "streetlight", "confidence": 0.85}
                elif any(word in text for word in ['garbage', 'trash', 'waste']):
                    result = {"predicted_class": 1, "predicted_label": "garbage", "confidence": 0.88}
                else:
                    result = {"predicted_class": 2, "predicted_label": "potholes", "confidence": 0.82}
                
                result['text'] = data.get('text', '')
                result['model_type'] = 'rule_based'
                self.send_json(result)
                
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 RAILWAY DEPLOYMENT - Starting server on port {port}")
    print(f"🌐 Health endpoint: http://0.0.0.0:{port}/health")
    
    server = HTTPServer(('0.0.0.0', port), RailwayHandler)
    print(f"✅ Server ready for Railway healthcheck!")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("🛑 Server stopped")
        server.server_close()