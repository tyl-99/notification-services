# API Integration Guide

This guide explains how to integrate the Notification Service API from your website or application.

## Base URL

```
http://localhost:6000  (Development)
https://your-domain.com  (Production)
```

## Authentication

If you set `API_KEY` in your `.env` file, include it in requests:

**Header:**
```
X-API-Key: your-secret-api-key-here
```

**OR as Bearer token:**
```
Authorization: Bearer your-secret-api-key-here
```

## Common Use Cases

### 1. Register Device Token (From PWA Frontend)

When a user visits your website and grants notification permission, register their FCM token.

#### JavaScript (Vanilla JS)

```javascript
// After getting FCM token from Firebase SDK
async function registerToken(fcmToken, appId, userId) {
  try {
    const response = await fetch('http://localhost:6000/api/register-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'  // If API_KEY is set
      },
      body: JSON.stringify({
        token: fcmToken,
        app_id: appId,  // e.g., "weather-app", "trading-app"
        user_id: userId,  // Optional: your user ID
        device_type: 'web',
        platform: navigator.userAgent.includes('Chrome') ? 'chrome' : 'safari'
      })
    });
    
    const data = await response.json();
    if (data.success) {
      console.log('Token registered successfully!');
    }
  } catch (error) {
    console.error('Error registering token:', error);
  }
}

// Usage
registerToken('fcm_token_from_firebase', 'weather-app', 'user123');
```

#### React Example

```jsx
import { useEffect, useState } from 'react';
import { getMessaging, getToken } from 'firebase/messaging';
import { initializeApp } from 'firebase/app';

function NotificationRegistration({ userId, appId }) {
  const [tokenRegistered, setTokenRegistered] = useState(false);

  useEffect(() => {
    async function registerNotificationToken() {
      try {
        // Initialize Firebase
        const firebaseConfig = {
          // Your Firebase config
        };
        const app = initializeApp(firebaseConfig);
        const messaging = getMessaging(app);

        // Request permission and get token
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
          const fcmToken = await getToken(messaging, {
            vapidKey: 'your-vapid-key'
          });

          if (fcmToken) {
            // Register token with your notification service
            const response = await fetch('http://localhost:6000/api/register-token', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'your-secret-api-key-here'
              },
              body: JSON.stringify({
                token: fcmToken,
                app_id: appId,
                user_id: userId,
                device_type: 'web',
                platform: navigator.userAgent.includes('Chrome') ? 'chrome' : 'safari'
              })
            });

            const data = await response.json();
            if (data.success) {
              setTokenRegistered(true);
              console.log('Notification token registered!');
            }
          }
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }

    registerNotificationToken();
  }, [userId, appId]);

  return (
    <div>
      {tokenRegistered ? (
        <p>✓ Notifications enabled</p>
      ) : (
        <p>Registering notifications...</p>
      )}
    </div>
  );
}
```

### 2. Send Notification to All Users of Your App (Backend/Server)

This is typically called from your backend server, cron job, or admin panel.

#### Python (Backend Server)

```python
import requests

def send_notification_to_app(app_id, title, body, data=None, user_id=None):
    """
    Send notification to all devices registered for an app.
    
    Args:
        app_id: Your app identifier (e.g., "weather-app")
        title: Notification title
        body: Notification body
        data: Optional custom data dictionary
        user_id: Optional user ID to filter recipients
    """
    url = 'http://localhost:6000/api/send-to-app'
    
    payload = {
        'app_id': app_id,
        'title': title,
        'body': body
    }
    
    if data:
        payload['data'] = data
    
    if user_id:
        payload['user_id'] = user_id
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'  # If API_KEY is set
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Sent to {result['sent_to']} devices")
            return result
        else:
            print(f"❌ Error: {result.get('error')}")
            return None
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return None

# Usage Examples:

# Send to all weather app users
send_notification_to_app(
    app_id='weather-app',
    title='🌧️ Rain Alert',
    body='Heavy rain expected in 30 minutes',
    data={'alert_type': 'rain', 'severity': 'high'}
)

# Send to specific user
send_notification_to_app(
    app_id='trading-app',
    title='💰 Trade Alert',
    body='Your trade closed with profit!',
    data={'trade_id': '12345', 'profit': 150.50},
    user_id='user123'
)
```

#### Node.js/Express Example

```javascript
const axios = require('axios');

async function sendNotificationToApp(appId, title, body, data = null, userId = null) {
  const url = 'http://localhost:6000/api/send-to-app';
  
  const payload = {
    app_id: appId,
    title: title,
    body: body
  };
  
  if (data) payload.data = data;
  if (userId) payload.user_id = userId;
  
  try {
    const response = await axios.post(url, payload, {
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'
      }
    });
    
    if (response.data.success) {
      console.log(`✅ Sent to ${response.data.sent_to} devices`);
      return response.data;
    }
  } catch (error) {
    console.error('❌ Error sending notification:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
sendNotificationToApp(
  'weather-app',
  '🌧️ Rain Alert',
  'Heavy rain expected in 30 minutes',
  { alert_type: 'rain', severity: 'high' }
);
```

#### PHP Example

```php
<?php
function sendNotificationToApp($appId, $title, $body, $data = null, $userId = null) {
    $url = 'http://localhost:6000/api/send-to-app';
    
    $payload = [
        'app_id' => $appId,
        'title' => $title,
        'body' => $body
    ];
    
    if ($data !== null) {
        $payload['data'] = $data;
    }
    
    if ($userId !== null) {
        $payload['user_id'] = $userId;
    }
    
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'X-API-Key: your-secret-api-key-here'
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode === 200) {
        $result = json_decode($response, true);
        if ($result['success']) {
            echo "✅ Sent to {$result['sent_to']} devices\n";
            return $result;
        }
    }
    
    return null;
}

// Usage
sendNotificationToApp(
    'weather-app',
    '🌧️ Rain Alert',
    'Heavy rain expected in 30 minutes',
    ['alert_type' => 'rain', 'severity' => 'high']
);
?>
```

### 3. Send Notification to Specific User

```python
import requests

def send_notification_to_user(user_id, title, body, app_id=None, data=None):
    """Send notification to all devices of a specific user."""
    url = 'http://localhost:6000/api/send-to-user'
    
    payload = {
        'user_id': user_id,
        'title': title,
        'body': body
    }
    
    if app_id:
        payload['app_id'] = app_id
    
    if data:
        payload['data'] = data
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Usage
send_notification_to_user(
    user_id='user123',
    app_id='trading-app',  # Optional: filter by app
    title='Account Update',
    body='Your account balance has been updated',
    data={'balance': 1000.00}
)
```

### 4. Send Notification to Single Device

```python
import requests

def send_notification_to_device(token, title, body, app_id=None, data=None):
    """Send notification to a specific device token."""
    url = 'http://localhost:6000/api/send-notification'
    
    payload = {
        'token': token,
        'title': title,
        'body': body
    }
    
    if app_id:
        payload['app_id'] = app_id
    
    if data:
        payload['data'] = data
    
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'
    }
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Usage
send_notification_to_device(
    token='fcm_device_token_here',
    app_id='weather-app',
    title='Test Notification',
    body='This is a test message',
    data={'test': True}
)
```

## Real-World Integration Examples

### Example 1: E-commerce Order Update

```python
# In your order processing system
def notify_order_shipped(order_id, user_id):
    send_notification_to_user(
        user_id=user_id,
        app_id='ecommerce-app',
        title='📦 Order Shipped',
        body=f'Your order #{order_id} has been shipped!',
        data={
            'order_id': order_id,
            'type': 'order_shipped',
            'action_url': f'/orders/{order_id}'
        }
    )
```

### Example 2: Weather Alert System

```python
# In your weather monitoring cron job
def send_weather_alert(alert_type, severity, affected_users=None):
    if affected_users:
        # Send to specific users
        for user_id in affected_users:
            send_notification_to_user(
                user_id=user_id,
                app_id='weather-app',
                title=f'🌧️ {alert_type} Alert',
                body=f'{alert_type} warning: {severity} conditions expected',
                data={'alert_type': alert_type, 'severity': severity}
            )
    else:
        # Broadcast to all weather app users
        send_notification_to_app(
            app_id='weather-app',
            title=f'🌧️ {alert_type} Alert',
            body=f'{alert_type} warning: {severity} conditions expected',
            data={'alert_type': alert_type, 'severity': severity}
        )
```

### Example 3: Trading App Price Alert

```python
# In your trading price monitoring system
def notify_price_alert(user_id, symbol, price, threshold):
    send_notification_to_user(
        user_id=user_id,
        app_id='trading-app',
        title=f'💰 {symbol} Price Alert',
        body=f'{symbol} reached ${price} (threshold: ${threshold})',
        data={
            'symbol': symbol,
            'price': price,
            'threshold': threshold,
            'action_url': f'/trading/{symbol}'
        }
    )
```

### Example 4: News App Breaking News

```python
# In your news publishing system
def publish_breaking_news(headline, summary, article_id):
    send_notification_to_app(
        app_id='news-app',
        title=f'📰 Breaking: {headline}',
        body=summary,
        data={
            'article_id': article_id,
            'type': 'breaking_news',
            'action_url': f'/articles/{article_id}'
        }
    )
```

## cURL Examples

### Register Token
```bash
curl -X POST http://localhost:6000/api/register-token \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "token": "fcm_token_here",
    "app_id": "weather-app",
    "user_id": "user123",
    "device_type": "web",
    "platform": "chrome"
  }'
```

### Send to App
```bash
curl -X POST http://localhost:6000/api/send-to-app \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "app_id": "weather-app",
    "title": "🌧️ Rain Alert",
    "body": "Heavy rain expected in 30 minutes",
    "data": {
      "alert_type": "rain",
      "severity": "high"
    }
  }'
```

### Send to User
```bash
curl -X POST http://localhost:6000/api/send-to-user \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "user_id": "user123",
    "app_id": "trading-app",
    "title": "Trade Alert",
    "body": "Your trade closed"
  }'
```

## CORS Configuration

If your frontend website is on a different domain, make sure to configure CORS:

1. **Option 1**: Allow all origins (development only)
   - Leave `ALLOWED_ORIGINS` empty in `.env`

2. **Option 2**: Specify allowed origins (production)
   ```env
   ALLOWED_ORIGINS=https://yourwebsite.com,https://app.yourwebsite.com
   ```

## Error Handling

Always handle errors in your integration:

```python
import requests

def safe_send_notification(app_id, title, body):
    try:
        response = requests.post(
            'http://localhost:6000/api/send-to-app',
            json={'app_id': app_id, 'title': title, 'body': body},
            headers={'Content-Type': 'application/json', 'X-API-Key': 'your-key'},
            timeout=10  # 10 second timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Response Format

All endpoints return JSON in this format:

**Success:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "app_id": "weather-app",
  "sent_to": 5,
  "failed": 0
}
```

**Error:**
```json
{
  "success": false,
  "error": "app_id is required"
}
```

## Best Practices

1. **Always handle errors** - Network requests can fail
2. **Use timeouts** - Don't wait indefinitely for responses
3. **Log responses** - Track notification delivery
4. **Retry logic** - Implement retry for failed requests
5. **Rate limiting** - Be mindful of notification frequency
6. **User consent** - Always request permission before registering tokens
7. **Token refresh** - Handle token expiration and refresh

## Testing

Test your integration:

```python
# Test health endpoint
import requests
response = requests.get('http://localhost:6000/api/health')
print(response.json())
```

## Production Deployment

1. **Use HTTPS** - Always use HTTPS in production
2. **Set API_KEY** - Enable authentication
3. **Configure CORS** - Set specific allowed origins
4. **Monitor logs** - Track notification delivery
5. **Use environment variables** - Store API keys securely

