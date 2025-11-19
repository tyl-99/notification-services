"""
Example integration code for using the Notification Service API.
Copy and adapt these examples for your use case.
"""

import requests
import json
from typing import Optional, Dict, Any


class NotificationServiceClient:
    """Client class for interacting with the Notification Service API."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize the notification service client.
        
        Args:
            base_url: Base URL of the notification service (e.g., "http://localhost:6000")
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json'
        }
        if api_key:
            self.headers['X-API-Key'] = api_key
    
    def register_token(
        self,
        token: str,
        app_id: str,
        user_id: Optional[str] = None,
        device_type: Optional[str] = None,
        platform: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register a device token."""
        url = f"{self.base_url}/api/register-token"
        payload = {
            'token': token,
            'app_id': app_id
        }
        if user_id:
            payload['user_id'] = user_id
        if device_type:
            payload['device_type'] = device_type
        if platform:
            payload['platform'] = platform
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def send_to_app(
        self,
        app_id: str,
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send notification to all devices for an app."""
        url = f"{self.base_url}/api/send-to-app"
        payload = {
            'app_id': app_id,
            'title': title,
            'body': body
        }
        if data:
            payload['data'] = data
        if user_id:
            payload['user_id'] = user_id
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def send_to_user(
        self,
        user_id: str,
        title: str,
        body: str,
        app_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send notification to all devices for a user."""
        url = f"{self.base_url}/api/send-to-user"
        payload = {
            'user_id': user_id,
            'title': title,
            'body': body
        }
        if app_id:
            payload['app_id'] = app_id
        if data:
            payload['data'] = data
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def send_to_device(
        self,
        token: str,
        title: str,
        body: str,
        app_id: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send notification to a specific device."""
        url = f"{self.base_url}/api/send-notification"
        payload = {
            'token': token,
            'title': title,
            'body': body
        }
        if app_id:
            payload['app_id'] = app_id
        if data:
            payload['data'] = data
        
        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if the service is healthy."""
        url = f"{self.base_url}/api/health"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


# Usage Examples:

if __name__ == '__main__':
    # Initialize client
    client = NotificationServiceClient(
        base_url='http://localhost:6000',
        api_key='your-secret-api-key-here'  # Optional
    )
    
    # Example 1: Register a token
    try:
        result = client.register_token(
            token='fcm_token_here',
            app_id='weather-app',
            user_id='user123',
            device_type='web',
            platform='chrome'
        )
        print(f"✅ Token registered: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Send to all weather app users
    try:
        result = client.send_to_app(
            app_id='weather-app',
            title='🌧️ Rain Alert',
            body='Heavy rain expected in 30 minutes',
            data={'alert_type': 'rain', 'severity': 'high'}
        )
        print(f"✅ Sent to {result['sent_to']} devices")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Send to specific user
    try:
        result = client.send_to_user(
            user_id='user123',
            app_id='trading-app',
            title='💰 Trade Alert',
            body='Your trade closed with profit!',
            data={'trade_id': '12345', 'profit': 150.50}
        )
        print(f"✅ Sent to {result['sent_to']} devices")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 4: Health check
    try:
        health = client.health_check()
        print(f"✅ Service status: {health['status']}")
    except Exception as e:
        print(f"❌ Error: {e}")

