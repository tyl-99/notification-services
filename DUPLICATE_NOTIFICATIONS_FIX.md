# Fix: PWA Receiving Duplicate Notifications

## Problem
Your PWA is receiving notifications at the same time (duplicate notifications).

## Common Causes

### 1. **Same Token Registered Multiple Times**
- Multiple browser tabs/windows registering the same token
- Token registration called multiple times on page load
- Service worker registering token multiple times

### 2. **Multiple Devices with Same Token**
- Same FCM token used across multiple devices (shouldn't happen, but possible)

### 3. **Frontend Issues**
- Token registration called in multiple places
- useEffect/componentDidMount running multiple times
- Service worker registering token on every activation

## Solutions Applied

### ✅ Backend Fix (Already Done)
- Updated `get_tokens_for_app()` to remove duplicate tokens
- Updated `get_tokens_for_user()` to remove duplicate tokens
- Now returns only unique tokens

### 🔧 Frontend Fixes Needed

#### 1. Prevent Multiple Registrations

**In your PWA frontend, add this check:**

```javascript
// Store registration status
let tokenRegistrationInProgress = false;
let tokenRegistered = false;

async function registerNotificationToken(fcmToken) {
  // Prevent multiple simultaneous registrations
  if (tokenRegistrationInProgress) {
    console.log('Token registration already in progress...');
    return;
  }
  
  if (tokenRegistered) {
    console.log('Token already registered');
    return;
  }
  
  tokenRegistrationInProgress = true;
  
  try {
    const response = await fetch('https://web-production-dbb3b.up.railway.app/api/register-token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        token: fcmToken,
        app_id: 'trading-app',
        user_id: 'user123',
        device_type: 'web',
        platform: 'safari'
      })
    });
    
    const data = await response.json();
    if (data.success) {
      tokenRegistered = true;
      console.log('✅ Token registered successfully!');
    }
  } catch (error) {
    console.error('❌ Error registering token:', error);
  } finally {
    tokenRegistrationInProgress = false;
  }
}
```

#### 2. Check LocalStorage Before Registering

```javascript
// Check if token already registered
const STORAGE_KEY = 'fcm_token_registered';

async function registerTokenOnce(fcmToken) {
  // Check if already registered
  const registered = localStorage.getItem(STORAGE_KEY);
  if (registered === fcmToken) {
    console.log('Token already registered in this session');
    return;
  }
  
  // Register token
  await registerNotificationToken(fcmToken);
  
  // Store in localStorage
  localStorage.setItem(STORAGE_KEY, fcmToken);
}
```

#### 3. Service Worker - Register Only Once

**In your service worker (sw.js):**

```javascript
// Prevent multiple registrations
let registrationInProgress = false;

self.addEventListener('push', function(event) {
  // Handle notification
  const data = event.data ? event.data.json() : {};
  // ... your notification handling code
});

// Don't register token in service worker
// Do it only in your main app JavaScript
```

## Check for Duplicates

Run this script to check for duplicate tokens:

```bash
python check_duplicate_tokens.py
```

Or use the existing script:

```bash
python check_tokens.py
```

## Manual Cleanup (If Needed)

If you find duplicates in Firestore:

1. Go to Firebase Console → Firestore
2. Check `device_tokens` collection
3. Look for documents with same token value
4. Delete duplicate documents (keep only one)

## Prevention

1. ✅ **Backend**: Now removes duplicates automatically
2. ✅ **Frontend**: Add registration guards (see examples above)
3. ✅ **Service Worker**: Don't register tokens in SW
4. ✅ **LocalStorage**: Check before registering

## Test

After applying fixes:

1. Clear browser cache/localStorage
2. Register token once
3. Send test notification
4. Should receive only ONE notification

## Summary

- **Backend is fixed** - duplicates are now removed automatically
- **Frontend needs fixes** - prevent multiple registrations
- **Check Firestore** - clean up any existing duplicates

The backend will now prevent duplicate notifications even if tokens are registered multiple times!

