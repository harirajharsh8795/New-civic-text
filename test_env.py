import os
import sys

print("=== RAILWAY ENVIRONMENT DEBUG ===")
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"Current working directory: {os.getcwd()}")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
print(f"All environment variables:")
for key, value in sorted(os.environ.items()):
    if 'PORT' in key or 'HOST' in key or 'BIND' in key:
        print(f"  {key}={value}")

print("\n=== FILES IN DIRECTORY ===")
try:
    import os
    files = os.listdir('.')
    for file in sorted(files):
        print(f"  {file}")
except Exception as e:
    print(f"Error listing files: {e}")

print("\n=== TESTING SIMPLE HTTP SERVER ===")
from http.server import HTTPServer, BaseHTTPRequestHandler

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"Received GET request to {self.path}")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status": "healthy", "message": "Simple HTTP server working"}')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting simple HTTP server on port {port}")
    server = HTTPServer(('0.0.0.0', port), TestHandler)
    print(f"Server started on http://0.0.0.0:{port}")
    server.serve_forever()