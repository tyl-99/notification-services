# Railway Deployment Test Commands

Your Railway URL: `https://web-production-dbb3b.up.railway.app`

## 1. Health Check

```bash
curl https://web-production-dbb3b.up.railway.app/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "notification-service",
  "version": "1.0.0",
  "timestamp": "2025-11-23T00:00:00"
}
```

---

## 2. Register Device Token

```bash
curl -X POST https://web-production-dbb3b.up.railway.app/api/register-token \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_fcm_token_here",
    "app_id": "trading-app",
    "user_id": "user123",
    "device_type": "web",
    "platform": "chrome"
  }'
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

## 3. Send Notification to App (All Devices)

```bash
curl -X POST https://web-production-dbb3b.up.railway.app/api/send-to-app \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "trading-app",
    "title": "💰 Trade Alert",
    "body": "Your trade closed with profit!",
    "data": {
      "trade_id": "12345",
      "profit": "150.50"
    }
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Notifications sent",
  "app_id": "trading-app",
  "sent_to": 1,
  "failed": 0,
  "tokens": ["token1", "token2"]
}
```

---

## 4. Send Notification to Specific User

```bash
curl -X POST https://web-production-dbb3b.up.railway.app/api/send-to-user \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "app_id": "trading-app",
    "title": "Account Update",
    "body": "Your account balance has been updated",
    "data": {
      "balance": "1000.00"
    }
  }'
```

---

## 5. Send Notification to Single Device

```bash
curl -X POST https://web-production-dbb3b.up.railway.app/api/send-notification \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_fcm_token_here",
    "app_id": "trading-app",
    "title": "Direct Notification",
    "body": "This is sent directly to your device",
    "data": {
      "test": "true"
    }
  }'
```

---

## Quick Test Sequence

### Step 1: Check if service is running
```bash
curl https://web-production-dbb3b.up.railway.app/api/health
```

### Step 2: Send test notification to all trading-app devices
```bash
curl -X POST https://web-production-dbb3b.up.railway.app/api/send-to-app \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "trading-app",
    "title": "🚀 Test Notification",
    "body": "Hello from Railway! This is a test notification.",
    "data": {
      "test": "true",
      "timestamp": "2025-11-23"
    }
  }'
```

---

## Windows PowerShell Commands

If you're on Windows, use these instead:

### Health Check:
```powershell
Invoke-RestMethod -Uri "https://web-production-dbb3b.up.railway.app/api/health"
```

### Send to App:
```powershell
Invoke-RestMethod -Uri "https://web-production-dbb3b.up.railway.app/api/send-to-app" -Method POST -ContentType "application/json" -Body '{"app_id":"trading-app","title":"💰 Test","body":"Hello from Railway!"}'
```

---

## Testing Checklist

- [ ] Health check returns 200 OK
- [ ] Register token works (if you have FCM token)
- [ ] Send to app works (sends to all registered devices)
- [ ] Send to user works (sends to specific user's devices)
- [ ] Notifications appear on your devices

---

## Troubleshooting

### If you get connection errors:
- Check Railway dashboard - is the service running?
- Check Railway logs for errors
- Verify environment variables are set correctly

### If notifications don't arrive:
- Verify device tokens are registered
- Check Firebase Console for delivery status
- Verify FCM tokens are valid and not expired

