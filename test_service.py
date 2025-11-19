"""
Quick test script for the notification service.
Run this after starting the service to test all endpoints.
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"
API_KEY = ""  # Set if you configured API_KEY in .env

def get_headers():
    """Get request headers."""
    headers = {'Content-Type': 'application/json'}
    if API_KEY:
        headers['X-API-Key'] = API_KEY
    return headers

def test_health():
    """Test health check endpoint."""
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_register_token():
    """Test token registration."""
    print("\n2. Testing Token Registration...")
    try:
        payload = {
            "token": "test_token_12345",
            "app_id": "trading-app",
            "user_id": "test_user_123",
            "device_type": "web",
            "platform": "chrome"
        }
        response = requests.post(
            f"{BASE_URL}/api/register-token",
            json=payload,
            headers=get_headers()
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_send_to_app():
    """Test sending notification to app."""
    print("\n3. Testing Send to App...")
    try:
        payload = {
            "app_id": "trading-app",
            "title": "💰 Test Notification",
            "body": "This is a test notification from the test script",
            "data": {
                "test": True,
                "timestamp": time.time()
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/send-to-app",
            json=payload,
            headers=get_headers()
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_send_to_user():
    """Test sending notification to user."""
    print("\n4. Testing Send to User...")
    try:
        payload = {
            "user_id": "test_user_123",
            "app_id": "trading-app",
            "title": "Test User Notification",
            "body": "This is a test notification for a specific user"
        }
        response = requests.post(
            f"{BASE_URL}/api/send-to-user",
            json=payload,
            headers=get_headers()
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_send_notification():
    """Test sending notification to single device."""
    print("\n5. Testing Send to Single Device...")
    try:
        payload = {
            "token": "test_token_12345",
            "app_id": "trading-app",
            "title": "Single Device Test",
            "body": "This is a test notification to a single device",
            "data": {"test": True}
        }
        response = requests.post(
            f"{BASE_URL}/api/send-notification",
            json=payload,
            headers=get_headers()
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        # Note: This will fail if token is invalid, which is expected for test token
        return response.status_code in [200, 400]
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Notification Service Test Suite")
    print("=" * 60)
    print(f"Testing service at: {BASE_URL}")
    
    results = []
    
    # Test health check first
    if not test_health():
        print("\n❌ Service is not running! Please start the service first:")
        print("   python app.py")
        return
    
    # Run other tests
    results.append(("Health Check", test_health()))
    results.append(("Register Token", test_register_token()))
    results.append(("Send to App", test_send_to_app()))
    results.append(("Send to User", test_send_to_user()))
    results.append(("Send to Device", test_send_notification()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    print(f"\nTotal: {passed_count}/{len(results)} tests passed")

if __name__ == "__main__":
    main()

