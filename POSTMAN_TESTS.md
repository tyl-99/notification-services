# Postman Test Collection

Use these requests to test your notification service from Postman.

## Base URL
```
http://localhost:5001
```

## 1. Health Check (No Auth Required)

**Method:** `GET`  
**URL:** `http://localhost:5001/api/health`  
**Headers:** None  
**Body:** None

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "notification-service",
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00"
}
```

---

## 2. Register Device Token

**Method:** `POST`  
**URL:** `http://localhost:5001/api/register-token`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "token": "test_fcm_token_12345",
  "app_id": "trading-app",
  "user_id": "user123",
  "device_type": "web",
  "platform": "chrome"
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Token registered successfully",
  "app_id": "trading-app",
  "user_id": "user123"
}
```

---

## 3. Send Notification to App (Most Important)

**Method:** `POST`  
**URL:** `http://localhost:5001/api/send-to-app`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "app_id": "trading-app",
  "title": "💰 Trade Alert",
  "body": "Your trade closed with profit!",
  "data": {
    "trade_id": "12345",
    "profit": 150.50
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "app_id": "trading-app",
  "sent_to": 1,
  "failed": 0,
  "tokens": ["test_fcm_token_12345"]
}
```

---

## 4. Send Notification to User

**Method:** `POST`  
**URL:** `http://localhost:5001/api/send-to-user`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "user_id": "user123",
  "app_id": "trading-app",
  "title": "Account Update",
  "body": "Your account balance has been updated",
  "data": {
    "balance": 1000.00
  }
}
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "user_id": "user123",
  "app_id": "trading-app",
  "sent_to": 1,
  "failed": 0
}
```

---

## 5. Send Notification to Single Device

**Method:** `POST`  
**URL:** `http://localhost:5001/api/send-notification`  
**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "token": "test_fcm_token_12345",
  "app_id": "trading-app",
  "title": "Single Device Test",
  "body": "This is a test notification",
  "data": {
    "test": true
  }
}
```

**Note:** This will fail with invalid token error (expected for test token), but tests the endpoint.

---

## Testing Order

1. **First:** Test Health Check - verifies service is running
2. **Second:** Register Token - stores a test token in Firestore
3. **Third:** Send to App - tests Firebase FCM integration
4. **Fourth:** Send to User - tests user-based queries
5. **Fifth:** Send to Device - tests single device (will fail with test token)

---

## Common Errors

### Error: "Firebase credentials not found"
- Check `.env` file exists and has correct path
- Verify `my-trader.json` file exists in project root

### Error: "Token is unregistered or invalid"
- Normal for test tokens - use real FCM token from your app

### Error: "app_id is required"
- Make sure JSON body includes `app_id` field

### Error: Connection refused
- Service not running - start with `python app.py`

