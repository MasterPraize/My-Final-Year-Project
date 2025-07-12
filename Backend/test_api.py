"""
Test script for the Password Strength Analyzer API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_password_analysis():
    """Test password analysis endpoint"""
    print("Testing password analysis...")
    
    test_passwords = [
        "123456",
        "password",
        "Password123!",
        "MyVerySecureP@ssw0rd2024!",
        "Tr0ub4dor&3"
    ]
    
    for password in test_passwords:
        print(f"\nAnalyzing password: {'*' * len(password)}")
        
        payload = {
            "password": password,
            "check_breach": True
        }
        
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Overall Score: {result.get('overall', {}).get('score', 'N/A')}")
            print(f"Overall Strength: {result.get('overall', {}).get('strength', 'N/A')}")
            
            # Print breach check results
            if 'breach_check' in result:
                breach = result['breach_check']
                if breach.get('is_breached'):
                    print(f"⚠️  BREACH ALERT: Found in {breach.get('breach_count', 0)} breaches")
                else:
                    print("✅ No known breaches")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        print("-" * 30)
        time.sleep(2)  # Rate limiting for breach checks

def test_model_training():
    """Test model training endpoint"""
    print("Testing model training...")
    
    response = requests.post(
        f"{BASE_URL}/train",
        json={},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Training Results: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_model_performance():
    """Test model performance endpoint"""
    print("Testing model performance...")
    
    response = requests.get(f"{BASE_URL}/model-performance")
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Model Performance: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

def test_batch_analysis():
    """Test batch analysis endpoint"""
    print("Testing batch analysis...")
    
    test_passwords = [
        "weak123",
        "StrongerP@ssw0rd!",
        "VerySecurePassword2024!"
    ]
    
    payload = {
        "passwords": test_passwords,
        "check_breach": False  # Disable for batch to avoid rate limiting
    }
    
    response = requests.post(
        f"{BASE_URL}/batch-analyze",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Batch Results: {json.dumps(result, indent=2)}")
    else:
        print(f"Error: {response.text}")
    
    print("-" * 50)

if __name__ == "__main__":
    print("Password Strength Analyzer API Test Suite")
    print("=" * 50)
    
    try:
        # Test all endpoints
        test_health_check()
        test_password_analysis()
        test_model_training()
        test_model_performance()
        test_batch_analysis()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the Flask application is running on http://localhost:5000")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")