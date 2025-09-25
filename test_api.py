#!/usr/bin/env python3
"""
Test script for Civic Text Classification API
"""

import requests
import json
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return data['model_loaded']
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_single_classification():
    """Test single text classification"""
    print("\n🔍 Testing single classification...")
    
    test_cases = [
        {
            "text": "The streetlight near my home is broken",
            "expected": "streetlight"
        },
        {
            "text": "There is garbage dumped on the roadside",
            "expected": "garbage"
        },
        {
            "text": "The road has a big pothole causing accidents",
            "expected": "potholes"
        },
        {
            "text": "Hamari gali ki light kharab hai",
            "expected": "streetlight"
        },
        {
            "text": "Sadak mein gadha hai",
            "expected": "potholes"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/classify",
                json={"text": case["text"]}
            )
            
            if response.status_code == 200:
                result = response.json()
                predicted = result['predicted_category']
                confidence = result['confidence']
                
                status = "✅" if predicted == case["expected"] else "❌"
                print(f"{status} Test {i}: '{case['text'][:30]}...'")
                print(f"   Expected: {case['expected']}, Got: {predicted} (confidence: {confidence:.4f})")
            else:
                print(f"❌ Test {i} failed with status code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test {i} failed with error: {str(e)}")

def test_batch_classification():
    """Test batch classification"""
    print("\n📊 Testing batch classification...")
    
    texts = [
        "The streetlight is not working",
        "Garbage is everywhere on the street",
        "Road has dangerous potholes",
        "Light kharab hai gali mein",
        "Kachra faila hua hai yahan"
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/classify/batch",
            json={"texts": texts}
        )
        
        if response.status_code == 200:
            results = response.json()['results']
            print("✅ Batch classification successful:")
            
            for i, result in enumerate(results, 1):
                print(f"   {i}. '{result['text'][:30]}...' -> {result['predicted_category']} ({result['confidence']:.4f})")
        else:
            print(f"❌ Batch classification failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Batch classification failed: {str(e)}")

def test_model_info():
    """Test model info endpoint"""
    print("\n🤖 Testing model info...")
    
    try:
        response = requests.get(f"{BASE_URL}/model/info")
        if response.status_code == 200:
            info = response.json()
            print("✅ Model info retrieved:")
            print(f"   Model: {info.get('model_name', 'Unknown')}")
            print(f"   Labels: {info.get('num_labels', 'Unknown')}")
            print(f"   Categories: {list(info.get('label_mapping', {}).values())}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Model info failed: {str(e)}")

def test_examples():
    """Test examples endpoint"""
    print("\n📋 Testing examples endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/examples")
        if response.status_code == 200:
            examples = response.json()['examples']
            print(f"✅ Retrieved {len(examples)} examples")
        else:
            print(f"❌ Examples endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Examples endpoint failed: {str(e)}")

def test_performance():
    """Test API performance"""
    print("\n⚡ Testing performance...")
    
    test_text = "The streetlight is broken and needs repair"
    num_requests = 10
    
    start_time = time.time()
    
    for i in range(num_requests):
        try:
            response = requests.post(
                f"{BASE_URL}/classify",
                json={"text": test_text}
            )
            if response.status_code != 200:
                print(f"❌ Request {i+1} failed")
        except Exception as e:
            print(f"❌ Request {i+1} error: {str(e)}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / num_requests
    
    print(f"✅ Performance test completed:")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Average time per request: {avg_time:.3f}s")
    print(f"   Requests per second: {num_requests/total_time:.2f}")

def main():
    print("🧪 Civic Text Classification API Test Suite")
    print("=" * 60)
    
    # Check if server is running
    print("🔌 Checking API connection...")
    if not test_health_check():
        print("\n❌ API is not available. Please:")
        print("1. Make sure the server is running: python deploy.py")
        print("2. Check if the model is trained and saved")
        print("3. Verify the server is listening on http://127.0.0.1:8000")
        sys.exit(1)
    
    # Run all tests
    test_single_classification()
    test_batch_classification()
    test_model_info()
    test_examples()
    test_performance()
    
    print("\n🎉 Test suite completed!")
    print("\n🌐 Try the interactive API documentation at:")
    print("   http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main()