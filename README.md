# Firebase Cloud Messaging (FCM) Notification Microservice

A standalone Flask microservice for sending push notifications via Firebase Cloud Messaging (FCM). Supports multiple Progressive Web Apps (PWAs) with app-specific configurations for icons, badges, and notification settings.

## Features

- ✅ **Token Registration**: Register FCM device tokens with app_id and optional user_id
- ✅ **Send to Single Device**: Send notification to a specific device token
- ✅ **Send to App**: Send notification to all devices for a specific app (auto-uses app-specific icon/badge) ⭐ **MOST IMPORTANT**
- ✅ **Send to User**: Send notification to all devices for a specific user across apps
- ✅ **Broadcast**: Send notification to all registered devices
- ✅ **Multi-App Support**: Each PWA can have its own icon, badge, and notification settings
- ✅ **Firestore Integration**: Token storage and management in Firebase Firestore
- ✅ **CORS Enabled**: Cross-origin requests supported
- ✅ **Error Handling**: Comprehensive error handling and logging

## Project Structure

```
notification-service/
├── app.py                      # Main Flask application
├── firebase_service.py        # Firebase Admin SDK initialization and FCM sending
├── token_manager.py           # Token CRUD operations in Firestore
├── app_configs.py             # App-specific configurations (icons, badges, etc.)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Documentation
└── tests/
    └── test_api.py           # API tests
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Cloud Messaging API
4. Go to Project Settings → Service Accounts
5. Click "Generate New Private Key" to download the credentials JSON file
6. Save the file as `firebase-credentials.json` in the project root

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Firebase Configuration
FIREBASE_ADMIN_CREDENTIALS_PATH=./firebase-credentials.json

# Server Configuration
PORT=6000
DEBUG=False

# Optional: API Key for authentication
API_KEY=your-secret-api-key-here

# CORS Configuration (comma-separated origins, leave empty for all origins)
ALLOWED_ORIGINS=
```

### 4. Run the Service

```bash
python app.py
```

Or using gunicorn for production:

```bash
gunicorn -w 4 -b 0.0.0.0:6000 app:app
```

The service will start on `http://localhost:6000`

## API Endpoints

### 1. Health Check

**GET** `/api/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "notification-service",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00"
}
```

### 2. Register Device Token

**POST** `/api/register-token`

Register a device token with an app_id.

**Request Body:**
```json
{
  "token": "fcm_device_token_here",
  "app_id": "trading-app",
  "user_id": "user123",
  "device_type": "ios",
  "platform": "safari"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Token registered successfully",
  "app_id": "trading-app",
  "user_id": "user123"
}
```

### 3. Send Notification to Single Device

**POST** `/api/send-notification`

Send notification to a specific device token.

**Request Body:**
```json
{
  "token": "fcm_device_token_here",
  "app_id": "trading-app",
  "title": "💰 Trade Alert",
  "body": "Your trade closed with profit!",
  "data": {
    "trade_id": "12345",
    "profit": 150.50
  },
  "icon": "/custom-icon.png",
  "badge": "/custom-badge.png"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Notification sent successfully",
  "message_id": "projects/xxx/messages/yyy"
}
```

### 4. Send Notification to All Devices for an App ⭐ **MOST IMPORTANT**

**POST** `/api/send-to-app`

Send notification to all devices registered for a specific app_id. Automatically uses app-specific icon/badge.

**Request Body:**
```json
{
  "app_id": "weather-app",
  "title": "🌧️ Rain Alert",
  "body": "Heavy rain expected in 30 minutes",
  "data": {
    "alert_type": "rain",
    "severity": "high"
  },
  "user_id": "user123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "app_id": "weather-app",
  "sent_to": 5,
  "failed": 0,
  "tokens": ["token1", "token2", ...]
}
```

### 5. Send Notification to User (All Devices)

**POST** `/api/send-to-user`

Send notification to all devices for a specific user.

**Request Body:**
```json
{
  "user_id": "user123",
  "app_id": "trading-app",
  "title": "Account Update",
  "body": "Your account balance has been updated",
  "data": {}
}
```

**Response:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "user_id": "user123",
  "app_id": "trading-app",
  "sent_to": 3,
  "failed": 0
}
```

### 6. Broadcast to All Devices

**POST** `/api/broadcast`

Send notification to all registered devices.

**Request Body:**
```json
{
  "title": "System Update",
  "body": "New features available!",
  "data": {}
}
```

**Response:**
```json
{
  "success": true,
  "message": "Broadcast sent",
  "sent_to": 10,
  "failed": 0
}
```

## Usage Examples

### Example 1: Register Token (from PWA frontend)

```javascript
fetch('http://localhost:6000/api/register-token', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'X-API-Key': 'your-secret-api-key-here'  // If API_KEY is set
  },
  body: JSON.stringify({
    token: 'fcm_token_from_browser',
    app_id: 'weather-app',
    user_id: 'user123',
    device_type: 'web',
    platform: 'chrome'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Example 2: Send to All Weather App Users (from external service)

```python
import requests

response = requests.post(
    'http://localhost:6000/api/send-to-app',
    headers={
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'  # If API_KEY is set
    },
    json={
        "app_id": "weather-app",
        "title": "🌧️ Rain Alert",
        "body": "Heavy rain expected in 30 minutes",
        "data": {
            "alert_type": "rain",
            "severity": "high"
        }
    }
)

print(response.json())
# {"success": true, "sent_to": 5, ...}
```

### Example 3: Send to Specific User

```python
import requests

response = requests.post(
    'http://localhost:6000/api/send-to-user',
    headers={
        'Content-Type': 'application/json',
        'X-API-Key': 'your-secret-api-key-here'
    },
    json={
        "user_id": "user123",
        "app_id": "trading-app",
        "title": "Trade Alert",
        "body": "Your trade closed"
    }
)

print(response.json())
```

### Example 4: Using cURL

```bash
# Register token
curl -X POST http://localhost:6000/api/register-token \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "token": "fcm_token_here",
    "app_id": "weather-app",
    "user_id": "user123"
  }'

# Send to app
curl -X POST http://localhost:6000/api/send-to-app \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key-here" \
  -d '{
    "app_id": "weather-app",
    "title": "Rain Alert",
    "body": "Heavy rain expected"
  }'
```

## App Configurations

App-specific configurations are defined in `app_configs.py`. To add a new app:

```python
APP_CONFIGS = {
    "your-app-id": {
        "name": "Your App Name",
        "icon": "/your-icon-192x192.png",
        "badge": "/your-badge-96x96.png",
        "default_title_prefix": "🔔",
        "color": "#ff0000"
    }
}
```

## Firestore Structure

Tokens are stored in Firestore with the following structure:

**Collection:** `device_tokens`

**Document ID:** `{token}` (the FCM token itself)

**Fields:**
- `token`: string (FCM token)
- `app_id`: string (required: "trading-app", "weather-app", etc.)
- `user_id`: string (optional)
- `device_type`: string (optional: "ios", "android", "web")
- `platform`: string (optional: "safari", "chrome", etc.)
- `created_at`: timestamp
- `updated_at`: timestamp
- `last_active`: timestamp

## Authentication

If `API_KEY` is set in `.env`, all endpoints (except `/api/health`) will require authentication. Include the API key in the request header:

```
X-API-Key: your-secret-api-key-here
```

Or as a Bearer token:

```
Authorization: Bearer your-secret-api-key-here
```

## Error Handling

The service returns appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (missing or invalid parameters)
- `401`: Unauthorized (invalid API key)
- `404`: Not Found (invalid endpoint)
- `500`: Internal Server Error

Error responses follow this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual tests:

```bash
python tests/test_api.py
```

## Logging

All operations are logged with timestamps. Logs include:
- Token registrations
- Notification sends (success/failure)
- Errors and warnings
- Service initialization

## Production Deployment

### Railway Deployment (Recommended)

See [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) for detailed Railway deployment instructions.

Quick steps:
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Set environment variables in Railway dashboard
4. Upload Firebase credentials
5. Deploy!

### Other Platforms

For other platforms (Heroku, AWS, etc.):

1. Set `DEBUG=False` in environment variables
2. Use a production WSGI server like gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```
3. Set up proper API key authentication
4. Configure `ALLOWED_ORIGINS` for CORS
5. Use environment variables for sensitive data
6. Set up proper logging and monitoring

## Troubleshooting

### Firebase Initialization Error

- Ensure `firebase-credentials.json` exists and is valid
- Check that Cloud Messaging API is enabled in Firebase Console
- Verify the service account has proper permissions

### Token Registration Issues

- Ensure Firestore is enabled in Firebase Console
- Check Firestore security rules allow writes
- Verify the token format is correct

### Notification Not Received

- Check device token is valid and not expired
- Verify app has notification permissions
- Check browser console for errors (for web apps)
- Review Firebase Cloud Messaging logs

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.

