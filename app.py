import os#!/usr/bin/env python3#!/usr/bin/env python3

import json

from http.server import HTTPServer, BaseHTTPRequestHandlerimport osimport os



class CivicHandler(BaseHTTPRequestHandler):import jsonimport json

    def do_GET(self):

        if self.path in ['/', '/health']:from http.server import HTTPServer, BaseHTTPRequestHandlerimport urllib.parse

            self.send_response(200)

            self.send_header('Content-Type', 'application/json')from http.server import HTTPServer, BaseHTTPRequestHandler

            self.end_headers()

            response = {"status": "healthy", "message": "Civic Text Classifier"}class CivicTextHandler(BaseHTTPRequestHandler):

            self.wfile.write(json.dumps(response).encode('utf-8'))

        else:    def log_message(self, format, *args):class CivicTextHandler(BaseHTTPRequestHandler):

            self.send_response(404)

            self.send_header('Content-Type', 'application/json')        print(f"[{self.address_string()}] {format % args}")    def log_message(self, format, *args):

            self.end_headers()

            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))            print(f"[{self.address_string()}] {format % args}")

    

    def do_POST(self):    def do_GET(self):    

        if self.path == '/predict':

            try:        if self.path == '/':    def do_GET(self):

                content_length = int(self.headers.get('Content-Length', 0))

                post_data = self.rfile.read(content_length).decode('utf-8')            self.send_json_response({    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

                data = json.loads(post_data)

                text = data.get('text', '').lower()                "status": "healthy",    with torch.no_grad():

                

                # Simple classification                "message": "Civic Text Classifier API",        outputs = model(**inputs)

                if any(word in text for word in ['light', 'lamp', 'bulb', 'streetlight']):

                    result = {"predicted_class": 0, "predicted_label": "streetlight", "confidence": 0.85}                "version": "1.0",        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

                elif any(word in text for word in ['garbage', 'trash', 'waste']):

                    result = {"predicted_class": 1, "predicted_label": "garbage", "confidence": 0.88}                "endpoints": ["/", "/health", "/predict"],        predicted_class = torch.argmax(predictions, dim=1).item()

                else:

                    result = {"predicted_class": 2, "predicted_label": "potholes", "confidence": 0.82}                "port": os.environ.get("PORT", "8000")        confidence = predictions[0][predicted_class].item()

                

                result['text'] = data.get('text', '')            })    return {"predicted_class": int(predicted_class), "confidence": float(confidence)}

                

                self.send_response(200)        elif self.path == '/health':

                self.send_header('Content-Type', 'application/json')

                self.end_headers()            self.send_json_response({# Gradio UI

                self.wfile.write(json.dumps(result).encode('utf-8'))

                                "status": "healthy",demo = gr.Interface(

            except Exception as e:

                self.send_response(500)                "message": "OK",    fn=predict,

                self.send_header('Content-Type', 'application/json') 

                self.end_headers()                "port": os.environ.get("PORT", "8000")    inputs="text",

                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

        else:            })    outputs="json",

            self.send_response(404)

            self.send_header('Content-Type', 'application/json')        else:    title="Text Classifier",

            self.end_headers()

            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))            self.send_json_response({"error": "Not found"}, 404)    description="Enter text to get predicted class"



if __name__ == '__main__':    )

    port = int(os.environ.get('PORT', 8000))

    server = HTTPServer(('0.0.0.0', port), CivicHandler)    def do_POST(self):

    print(f"🚀 Civic Text Classifier running on port {port}")

    print(f"🌐 Endpoints: /, /health, /predict")        if self.path == '/predict':if __name__ == "__main__":

    try:

        server.serve_forever()            try:    demo.launch()

    except KeyboardInterrupt:

        print("Server stopped")                content_length = int(self.headers.get('Content-Length', 0))

        server.server_close()                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                text = data.get('text', '').lower()
                
                # Rule-based classification
                if any(word in text for word in ['light', 'lamp', 'bulb', 'lighting', 'streetlight', 'street light']):
                    result = {
                        "predicted_class": 0,
                        "predicted_label": "streetlight",
                        "confidence": 0.85
                    }
                elif any(word in text for word in ['garbage', 'trash', 'waste', 'litter', 'bin']):
                    result = {
                        "predicted_class": 1,
                        "predicted_label": "garbage", 
                        "confidence": 0.88
                    }
                else:
                    result = {
                        "predicted_class": 2,
                        "predicted_label": "potholes",
                        "confidence": 0.82
                    }
                
                result['text'] = data.get('text', '')
                result['model_type'] = 'rule_based'
                
                self.send_json_response(result)
                
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)
        else:
            self.send_json_response({"error": "Not found"}, 404)
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Civic Text Classifier on port {port}")
    
    server = HTTPServer(('0.0.0.0', port), CivicTextHandler)
    print(f"Server running at http://0.0.0.0:{port}")
    print("Endpoints: /, /health, /predict")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()