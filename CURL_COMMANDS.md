# cURL Commands for Testing

## Your Registered Token Info:
- **app_id**: `trading-app`
- **token**: `eQ1vwjYmzWpDapvfWeW520:APA91bHI4sZnW3N9a2VluJuiP9du_cJ5oJ-ottJbf2LnxGc5sRoP1wDJ412SHsIu78geBvK3o0eyY23kh5WVg144Ui_XMgP7hCUMYJJTv7JcdLRte0vlW3c`
- **device_type**: `web`
- **platform**: `chrome`

---

## 1. Send Notification to App (All Devices for trading-app)

### Windows PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/send-to-app" -Method POST -ContentType "application/json" -Body '{"app_id":"trading-app","title":"💰 Trade Alert","body":"Your trade closed with profit!","data":{"trade_id":"12345","profit":150.50}}'
```

### cURL (Git Bash / WSL):
```bash
curl -X POST http://localhost:5001/api/send-to-app \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"trading-app\",\"title\":\"💰 Trade Alert\",\"body\":\"Your trade closed with profit!\",\"data\":{\"trade_id\":\"12345\",\"profit\":150.50}}"
```

### cURL (One-liner):
```bash
curl -X POST http://localhost:5001/api/send-to-app -H "Content-Type: application/json" -d "{\"app_id\":\"trading-app\",\"title\":\"💰 Trade Alert\",\"body\":\"Your trade closed with profit!\",\"data\":{\"trade_id\":\"12345\",\"profit\":150.50}}"
```

---

## 2. Send Notification to Specific Device Token

### Windows PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/send-notification" -Method POST -ContentType "application/json" -Body '{"token":"eQ1vwjYmzWpDapvfWeW520:APA91bHI4sZnW3N9a2VluJuiP9du_cJ5oJ-ottJbf2LnxGc5sRoP1wDJ412SHsIu78geBvK3o0eyY23kh5WVg144Ui_XMgP7hCUMYJJTv7JcdLRte0vlW3c","app_id":"trading-app","title":"📱 Direct Notification","body":"This is sent directly to your device!","data":{"test":true}}'
```

### cURL:
```bash
curl -X POST http://localhost:5001/api/send-notification \
  -H "Content-Type: application/json" \
  -d "{\"token\":\"eQ1vwjYmzWpDapvfWeW520:APA91bHI4sZnW3N9a2VluJuiP9du_cJ5oJ-ottJbf2LnxGc5sRoP1wDJ412SHsIu78geBvK3o0eyY23kh5WVg144Ui_XMgP7hCUMYJJTv7JcdLRte0vlW3c\",\"app_id\":\"trading-app\",\"title\":\"📱 Direct Notification\",\"body\":\"This is sent directly to your device!\",\"data\":{\"test\":true}}"
```

---

## 3. Simple Test Notification

### Windows PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/send-to-app" -Method POST -ContentType "application/json" -Body '{"app_id":"trading-app","title":"Test Notification","body":"Hello from notification service!"}'
```

### cURL:
```bash
curl -X POST http://localhost:5001/api/send-to-app -H "Content-Type: application/json" -d "{\"app_id\":\"trading-app\",\"title\":\"Test Notification\",\"body\":\"Hello from notification service!\"}"
```

---

## 4. Trading Alert Example

### Windows PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:5001/api/send-to-app" -Method POST -ContentType "application/json" -Body '{"app_id":"trading-app","title":"🚨 Price Alert","body":"BTC reached $50,000!","data":{"symbol":"BTC","price":50000,"alert_type":"price_target"}}'
```

### cURL:
```bash
curl -X POST http://localhost:5001/api/send-to-app -H "Content-Type: application/json" -d "{\"app_id\":\"trading-app\",\"title\":\"🚨 Price Alert\",\"body\":\"BTC reached \$50,000!\",\"data\":{\"symbol\":\"BTC\",\"price\":50000,\"alert_type\":\"price_target\"}}"
```

---

## Quick Copy-Paste Commands

### For PowerShell (Windows):
```powershell
# Simple test
Invoke-RestMethod -Uri "http://localhost:5001/api/send-to-app" -Method POST -ContentType "application/json" -Body '{"app_id":"trading-app","title":"Test","body":"Hello World!"}'
```

### For cURL:
```bash
# Simple test
curl -X POST http://localhost:5001/api/send-to-app -H "Content-Type: application/json" -d '{"app_id":"trading-app","title":"Test","body":"Hello World!"}'
```

---

## Expected Response:
```json
{
  "success": true,
  "message": "Notifications sent",
  "app_id": "trading-app",
  "sent_to": 1,
  "failed": 0,
  "tokens": ["eQ1vwjYmzWpDapvfWeW520:APA91bHI4sZnW3N9a2VluJuiP9du_cJ5oJ-ottJbf2LnxGc5sRoP1wDJ412SHsIu78geBvK3o0eyY23kh5WVg144Ui_XMgP7hCUMYJJTv7JcdLRte0vlW3c"]
}
```


