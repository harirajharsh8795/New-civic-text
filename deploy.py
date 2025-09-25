#!/usr/bin/env python3
"""
Deployment script for Civic Text Classification API
"""

import subprocess
import sys
import os

def check_model_exists():
    """Check if the trained model exists"""
    model_path = "./model/saved_model"
    if not os.path.exists(model_path):
        print("❌ Model not found!")
        print(f"Expected model at: {model_path}")
        print("\n🔧 To fix this:")
        print("1. Run the Jupyter notebook: notebook/text_classifier.ipynb")
        print("2. Make sure the model is saved in the correct location")
        return False
    else:
        print("✅ Model found!")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_server(host="127.0.0.1", port=8000, reload=True):
    """Start the FastAPI server"""
    print(f"🚀 Starting FastAPI server at http://{host}:{port}")
    print("📖 API Documentation available at: http://127.0.0.1:8000/docs")
    print("🔄 Interactive API at: http://127.0.0.1:8000/redoc")
    print("\n⏹️  Press Ctrl+C to stop the server")
    
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "app:app", 
        f"--host={host}", 
        f"--port={port}"
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")

def main():
    print("🏛️  Civic Text Classification API Deployment")
    print("=" * 50)
    
    # Check if model exists
    if not check_model_exists():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()