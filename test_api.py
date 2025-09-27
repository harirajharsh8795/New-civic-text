import requests
import json

# Test the API endpoints
BASE_URL = "https://new-civic-text-production.up.railway.app"

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
        print("Testing Railway Deployed Civic Text Classifier")
        print("=" * 60)
        print(f"🌐 Testing API at: {BASE_URL}")
        print("=" * 60)
        test_health()
        print("=" * 60) 
        test_predict()
        print("=" * 60)
        print("✅ All tests completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check your internet connection and Railway deployment status")