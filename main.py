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
                "endpoints": ["/", "/health", "/predict", "/docs"],
                "documentation": "https://new-civic-text-production.up.railway.app/docs",
                "swagger_ui": "Visit /docs for interactive API testing"
            }
            self.send_json(response)
            
        elif parsed_path.path == '/health':
            print("🏥 HEALTH CHECK CALLED!")
            response = {"status": "healthy", "message": "OK"}
            self.send_json(response)
            
        elif parsed_path.path == '/docs':
            # Swagger-like documentation interface
            html_docs = self.get_docs_html()
            self.send_html(html_docs)
            
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
                "supported_categories": ["streetlight", "garbage", "potholes"],
                "docs_url": "https://new-civic-text-production.up.railway.app/docs"
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
    
    def send_html(self, html_content, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def get_docs_html(self):
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Civic Text Classifier API - Documentation</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }
        .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { background: #007bff; color: white; padding: 30px; border-radius: 8px 8px 0 0; }
        .content { padding: 30px; }
        .endpoint { background: #f8f9fa; margin: 20px 0; padding: 20px; border-radius: 6px; border-left: 4px solid #007bff; }
        .method { display: inline-block; padding: 4px 8px; border-radius: 4px; font-weight: bold; color: white; }
        .get { background: #28a745; }
        .post { background: #fd7e14; }
        .test-form { background: #e9ecef; padding: 20px; border-radius: 6px; margin-top: 20px; }
        textarea { width: 100%; padding: 10px; border: 1px solid #ced4da; border-radius: 4px; font-family: monospace; }
        button { background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        .response { margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 4px; white-space: pre-wrap; font-family: monospace; }
        .example { background: #f1f3f4; padding: 15px; margin: 10px 0; border-radius: 4px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏛️ Civic Text Classifier API</h1>
            <p>Interactive API Documentation & Testing Interface</p>
        </div>
        
        <div class="content">
            <div class="endpoint">
                <h3><span class="method get">GET</span> /</h3>
                <p>Get API status and information</p>
                <button onclick="testEndpoint('/', 'GET')">Test</button>
                <div id="response-root" class="response" style="display:none;"></div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method get">GET</span> /health</h3>
                <p>Health check endpoint for monitoring</p>
                <button onclick="testEndpoint('/health', 'GET')">Test</button>
                <div id="response-health" class="response" style="display:none;"></div>
            </div>
            
            <div class="endpoint">
                <h3><span class="method post">POST</span> /predict</h3>
                <p>Classify civic text into categories: streetlight, garbage, or potholes</p>
                
                <div class="test-form">
                    <h4>🧪 Test the Prediction API:</h4>
                    <textarea id="predict-input" rows="3" placeholder='{"text": "The street light is not working"}'></textarea>
                    <br><br>
                    <button onclick="testPredict()">🚀 Predict</button>
                    <div id="response-predict" class="response" style="display:none;"></div>
                </div>
                
                <h4>📋 Example Requests:</h4>
                <div class="example">{"text": "The street light is broken"}</div>
                <div class="example">{"text": "There is garbage on the street"}</div>
                <div class="example">{"text": "The road has many potholes"}</div>
                
                <h4>📤 Example Response:</h4>
                <div class="example">{
  "text": "The street light is broken",
  "predicted_class": 0,
  "predicted_label": "streetlight", 
  "confidence": 0.85,
  "model_type": "rule_based"
}</div>
            </div>
        </div>
    </div>
    
    <script>
        // Set default test input
        document.getElementById('predict-input').value = '{"text": "The street light is not working"}';
        
        function testEndpoint(path, method) {
            const responseId = 'response-' + path.replace('/', 'root');
            const responseDiv = document.getElementById(responseId);
            
            fetch(path, { method: method })
                .then(response => response.json())
                .then(data => {
                    responseDiv.style.display = 'block';
                    responseDiv.textContent = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    responseDiv.style.display = 'block';
                    responseDiv.textContent = 'Error: ' + error.message;
                });
        }
        
        function testPredict() {
            const input = document.getElementById('predict-input').value;
            const responseDiv = document.getElementById('response-predict');
            
            try {
                const jsonData = JSON.parse(input);
                
                fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(jsonData)
                })
                .then(response => response.json())
                .then(data => {
                    responseDiv.style.display = 'block';
                    responseDiv.textContent = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    responseDiv.style.display = 'block';
                    responseDiv.textContent = 'Error: ' + error.message;
                });
            } catch (e) {
                responseDiv.style.display = 'block';
                responseDiv.textContent = 'Invalid JSON: ' + e.message;
            }
        }
    </script>
</body>
</html>'''

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