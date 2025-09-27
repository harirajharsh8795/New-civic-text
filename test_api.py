import requests
import json

# Test the API endpoints
BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print("Health endpoint:", response.json())

def test_predict():
    test_cases = [
        {"text": "The street light is not working"},
        {"text": "There is garbage everywhere"},
        {"text": "The road has many potholes"}
    ]
    
    for case in test_cases:
        response = requests.post(f"{BASE_URL}/predict", json=case)
        print(f"Input: {case['text']}")
        print(f"Output: {response.json()}")
        print("-" * 50)

if __name__ == "__main__":
    try:
        print("Testing FastAPI Civic Text Classifier")
        print("=" * 50)
        test_health()
        print("=" * 50) 
        test_predict()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the server is running with: python main.py")