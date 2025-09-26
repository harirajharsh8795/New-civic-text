#!/usr/bin/env python3
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class RailwayHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom logging for Railway
        print(f"🔍 [{self.address_string()}] {format % args}")
    
    def do_GET(self):
        # Log everything for Railway debugging
        print(f"🚀 HEALTHCHECK REQUEST: {self.path}")
        print(f"📍 Client IP: {self.client_address[0]}")
        print(f"🏠 Host: {self.headers.get('Host', 'Not provided')}")
        print(f"🌐 User-Agent: {self.headers.get('User-Agent', 'Not provided')}")
        
        # Always return 200 for health endpoints
        if self.path in ['/', '/health']:
            print(f"✅ Responding with 200 OK for {self.path}")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "message": "Railway healthcheck SUCCESS",
                "path": self.path,
                "port": os.environ.get("PORT", "unknown"),
                "host_header": self.headers.get('Host', 'unknown')
            }
            
            response_json = json.dumps(response)
            self.wfile.write(response_json.encode('utf-8'))
            print(f"📤 Sent response: {response_json}")
            
        else:
            print(f"❓ Unknown path {self.path}, returning 404")
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/predict':
            print(f"📥 POST request to /predict")
            
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '').lower()
                
                # Simple classification
                if any(word in text for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight']):
                    result = {"predicted_class": 0, "predicted_label": "streetlight", "confidence": 0.85}
                elif any(word in text for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
                    result = {"predicted_class": 1, "predicted_label": "garbage", "confidence": 0.88}
                else:
                    result = {"predicted_class": 2, "predicted_label": "potholes", "confidence": 0.82}
                
                result['text'] = data.get('text', '')
                result['model_type'] = 'rule_based'
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode('utf-8'))
                
            except Exception as e:
                print(f"❌ Error in /predict: {e}")
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    
    print("=" * 60)
    print("🚀 RAILWAY-OPTIMIZED CIVIC TEXT CLASSIFIER")
    print("=" * 60)
    print(f"🔧 PORT from environment: {port}")
    print(f"🌐 Binding to: 0.0.0.0:{port}")
    print(f"✅ Health endpoint: http://0.0.0.0:{port}/health")
    print(f"🏠 Ready for Railway healthcheck from: healthcheck.railway.app")
    print("📝 Will log all incoming requests")
    print("=" * 60)
    
    try:
        server = HTTPServer(('0.0.0.0', port), RailwayHandler)
        print(f"🎯 HTTP Server successfully started!")
        print(f"⚡ READY FOR RAILWAY HEALTHCHECK!")
        print("=" * 60)
        server.serve_forever()
        
    except Exception as e:
        print(f"💥 FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)