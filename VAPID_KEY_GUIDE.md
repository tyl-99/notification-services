# VAPID Key Guide

## What is VAPID Key?

VAPID (Voluntary Application Server Identification) key is used by **your web application frontend** to get FCM tokens from Firebase. It's NOT required for the notification service backend.

## When Do You Need VAPID Key?

### ✅ NEEDED: Frontend (Your Web App)
When your web app requests notification permission and gets FCM tokens:
```javascript
const fcmToken = await getToken(messaging, {
  vapidKey: 'your-vapid-key-here'  // ← Required here
});
```

### ❌ NOT NEEDED: Notification Service Backend
Your notification service (`app.py`) uses **service account credentials** (`my-trader.json`) to send notifications. VAPID key is NOT used by the backend.

## How to Get VAPID Key

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (`my-trader-9e446`)
3. Click ⚙️ Settings → **Project Settings**
4. Go to **Cloud Messaging** tab
5. Scroll down to **Web configuration**
6. Under **Web Push certificates**, you'll see:
   - **Key pair** (this is your VAPID key)
   - If you don't see one, click **Generate key pair**

## Where to Use VAPID Key

### In Your Frontend Code (Not in Notification Service)

```javascript
// In your web app (React/Vue/Vanilla JS)
import { getMessaging, getToken } from 'firebase/messaging';

const messaging = getMessaging(app);

// Use VAPID key here
const fcmToken = await getToken(messaging, {
  vapidKey: 'BEl62iUYgUivxIkv...' // Your VAPID key from Firebase Console
});

// Then register with your notification service
fetch('http://localhost:6000/api/register-token', {
  method: 'POST',
  body: JSON.stringify({
    token: fcmToken,  // Token obtained using VAPID key
    app_id: 'trading-app',
    user_id: 'user123'
  })
});
```

## Summary

| Component | Needs VAPID Key? | Needs Service Account? |
|-----------|------------------|------------------------|
| **Frontend (Web App)** | ✅ YES | ❌ NO |
| **Notification Service** | ❌ NO | ✅ YES (my-trader.json) |

## Current Status

✅ **Notification Service**: Ready (has service account)  
⏳ **Frontend**: Will need VAPID key when you build your web app

## Quick Check

- ✅ Firebase Service Account (`my-trader.json`) → **You have this**  
- ⏳ VAPID Key → **Get from Firebase Console when building frontend**

Your notification service is ready to send notifications. VAPID key is only needed when you build the frontend that requests notification permissions.

