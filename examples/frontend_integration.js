/**
 * Frontend JavaScript integration example for registering tokens
 * and handling notifications from your website.
 */

// Configuration
const NOTIFICATION_SERVICE_URL = 'http://localhost:6000';
const API_KEY = 'your-secret-api-key-here'; // Optional, if API_KEY is set
const APP_ID = 'weather-app'; // Your app identifier
const USER_ID = 'user123'; // Your user identifier (from your auth system)

/**
 * Register FCM token with the notification service
 */
async function registerNotificationToken(fcmToken) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    // Add API key if configured
    if (API_KEY) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const response = await fetch(`${NOTIFICATION_SERVICE_URL}/api/register-token`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        token: fcmToken,
        app_id: APP_ID,
        user_id: USER_ID,
        device_type: 'web',
        platform: navigator.userAgent.includes('Chrome') ? 'chrome' : 
                  navigator.userAgent.includes('Firefox') ? 'firefox' : 
                  navigator.userAgent.includes('Safari') ? 'safari' : 'unknown'
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('✅ Token registered successfully!');
      return true;
    } else {
      console.error('❌ Failed to register token:', data.error);
      return false;
    }
  } catch (error) {
    console.error('❌ Error registering token:', error);
    return false;
  }
}

/**
 * Request notification permission and register token
 * This should be called when user clicks "Enable Notifications" button
 */
async function enableNotifications() {
  try {
    // Request permission
    const permission = await Notification.requestPermission();
    
    if (permission !== 'granted') {
      console.warn('Notification permission denied');
      return false;
    }
    
    // Initialize Firebase (you need to set this up)
    // This is a placeholder - you'll need to configure Firebase in your app
    const { getMessaging, getToken } = await import('firebase/messaging');
    const { initializeApp } = await import('firebase/app');
    
    // Your Firebase config
    const firebaseConfig = {
      apiKey: "your-api-key",
      authDomain: "your-project.firebaseapp.com",
      projectId: "your-project-id",
      storageBucket: "your-project.appspot.com",
      messagingSenderId: "123456789",
      appId: "your-app-id"
    };
    
    const app = initializeApp(firebaseConfig);
    const messaging = getMessaging(app);
    
    // Get FCM token
    const fcmToken = await getToken(messaging, {
      vapidKey: 'your-vapid-key' // Get from Firebase Console
    });
    
    if (fcmToken) {
      // Register with notification service
      return await registerNotificationToken(fcmToken);
    } else {
      console.error('Failed to get FCM token');
      return false;
    }
  } catch (error) {
    console.error('Error enabling notifications:', error);
    return false;
  }
}

/**
 * Handle incoming notifications (service worker)
 * Add this to your service worker file (sw.js)
 */
self.addEventListener('push', function(event) {
  const data = event.data ? event.data.json() : {};
  
  const title = data.notification?.title || 'Notification';
  const body = data.notification?.body || '';
  const icon = data.notification?.icon || '/icon-192x192.png';
  const badge = data.notification?.badge || '/icon-96x96.png';
  
  const options = {
    body: body,
    icon: icon,
    badge: badge,
    data: data.data || {},
    requireInteraction: false,
    vibrate: [200, 100, 200]
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

/**
 * Handle notification click
 */
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  
  const data = event.notification.data;
  const url = data.action_url || '/';
  
  event.waitUntil(
    clients.openWindow(url)
  );
});

/**
 * Example: React component for notification registration
 */
/*
import React, { useState, useEffect } from 'react';

function NotificationButton({ userId, appId }) {
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    // Check if notifications are already enabled
    if ('Notification' in window && Notification.permission === 'granted') {
      setEnabled(true);
    }
  }, []);
  
  const handleEnable = async () => {
    setLoading(true);
    const success = await enableNotifications();
    if (success) {
      setEnabled(true);
    }
    setLoading(false);
  };
  
  if (!('Notification' in window)) {
    return <p>Notifications are not supported in this browser.</p>;
  }
  
  if (enabled) {
    return <p>✅ Notifications are enabled!</p>;
  }
  
  return (
    <button onClick={handleEnable} disabled={loading}>
      {loading ? 'Enabling...' : 'Enable Notifications'}
    </button>
  );
}

export default NotificationButton;
*/

/**
 * Example: Send notification from frontend (admin panel)
 * Note: This should typically be done from your backend, not frontend
 */
async function sendNotificationFromAdmin(appId, title, body, data = null) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (API_KEY) {
      headers['X-API-Key'] = API_KEY;
    }
    
    const payload = {
      app_id: appId,
      title: title,
      body: body
    };
    
    if (data) {
      payload.data = data;
    }
    
    const response = await fetch(`${NOTIFICATION_SERVICE_URL}/api/send-to-app`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload)
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log(`✅ Sent to ${result.sent_to} devices`);
      return result;
    } else {
      console.error('❌ Failed to send notification:', result.error);
      return null;
    }
  } catch (error) {
    console.error('❌ Error sending notification:', error);
    return null;
  }
}

// Export functions for use in your app
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    registerNotificationToken,
    enableNotifications,
    sendNotificationFromAdmin
  };
}

