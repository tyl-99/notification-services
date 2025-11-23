"""
Firebase Admin SDK initialization and FCM push notification sending.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
import app_configs


def convert_data_to_strings(data: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """
    Convert all values in data dictionary to strings.
    FCM requires all data values to be strings.
    
    Args:
        data: Dictionary with potentially non-string values
        
    Returns:
        Dictionary with all values converted to strings
    """
    if not data:
        return {}
    
    return {key: str(value) for key, value in data.items()}

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
_firebase_app = None


def initialize_firebase():
    """Initialize Firebase Admin SDK with credentials from environment."""
    global _firebase_app
    
    if _firebase_app is not None:
        logger.info("Firebase Admin SDK already initialized")
        return _firebase_app
    
    try:
        # Try to get credentials from path first
        creds_path = os.getenv('FIREBASE_ADMIN_CREDENTIALS_PATH')
        creds_json = os.getenv('FIREBASE_ADMIN_CREDENTIALS')
        
        if creds_path:
            # Resolve relative paths to absolute
            if not os.path.isabs(creds_path):
                creds_path = os.path.abspath(creds_path)
            
            if os.path.exists(creds_path):
                logger.info(f"Loading Firebase credentials from file: {creds_path}")
                cred = credentials.Certificate(creds_path)
            else:
                # File not found, but check if we have JSON env var as fallback
                if creds_json:
                    logger.warning(f"Firebase credentials file not found at: {creds_path}, using environment variable instead")
                    cred_dict = json.loads(creds_json)
                    cred = credentials.Certificate(cred_dict)
                else:
                    raise ValueError(
                        f"Firebase credentials file not found at: {creds_path}. "
                        "Please upload the file to Railway or set FIREBASE_ADMIN_CREDENTIALS environment variable."
                    )
        elif creds_json:
            logger.info("Loading Firebase credentials from environment variable")
            cred_dict = json.loads(creds_json)
            cred = credentials.Certificate(cred_dict)
        else:
            raise ValueError(
                "Firebase credentials not found. Set either FIREBASE_ADMIN_CREDENTIALS_PATH "
                "or FIREBASE_ADMIN_CREDENTIALS environment variable."
            )
        
        _firebase_app = firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully")
        return _firebase_app
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
        raise


def send_push_notification(
    token: str,
    title: str,
    body: str,
    app_id: Optional[str] = None,
    icon: Optional[str] = None,
    badge: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    sound: str = "default"
) -> messaging.SendResponse:
    """
    Send a push notification to a single device token.
    
    Args:
        token: FCM device token
        title: Notification title
        body: Notification body text
        app_id: App identifier (used to get default icon/badge if not provided)
        icon: Custom icon URL (overrides app default)
        badge: Custom badge URL (overrides app default)
        data: Custom data payload (key-value pairs)
        sound: Sound to play (default: "default")
        
    Returns:
        SendResponse object with message_id
        
    Raises:
        ValueError: If token is invalid
        Exception: If sending fails
    """
    # Ensure Firebase is initialized
    if _firebase_app is None:
        initialize_firebase()
    
    # Get app-specific defaults if app_id provided
    if app_id:
        if icon is None:
            icon = app_configs.get_app_icon(app_id)
        if badge is None:
            badge = app_configs.get_app_badge(app_id)
    
    # Convert data values to strings (FCM requirement)
    string_data = convert_data_to_strings(data)
    
    # Build the message
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=string_data,
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=title,
                body=body,
                icon=icon or "/icon-192x192.png",
                badge=badge or "/icon-96x96.png",
                require_interaction=False,
                vibrate=[200, 100, 200]
            )
            # Note: fcm_options.link requires HTTPS URL, so we omit it
            # The notification will use the default action (opening the app)
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title=title,
                        body=body
                    ),
                    sound=sound,
                    badge=1
                )
            )
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                icon="ic_notification",
                sound=sound,
                channel_id="default"
            )
        )
    )
    
    try:
        response = messaging.send(message)
        logger.info(f"Successfully sent message to token {token[:20]}...: {response}")
        return response
    except messaging.UnregisteredError:
        logger.warning(f"Token {token[:20]}... is unregistered or invalid")
        raise ValueError("Token is unregistered or invalid")
    except messaging.InvalidArgumentError as e:
        logger.error(f"Invalid argument: {str(e)}")
        raise ValueError(f"Invalid argument: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to send notification: {str(e)}")
        raise


def send_multicast_notification(
    tokens: list,
    title: str,
    body: str,
    app_id: Optional[str] = None,
    icon: Optional[str] = None,
    badge: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    sound: str = "default"
) -> messaging.BatchResponse:
    """
    Send push notifications to multiple device tokens.
    
    Args:
        tokens: List of FCM device tokens
        title: Notification title
        body: Notification body text
        app_id: App identifier (used to get default icon/badge if not provided)
        icon: Custom icon URL (overrides app default)
        badge: Custom badge URL (overrides app default)
        data: Custom data payload (key-value pairs)
        sound: Sound to play (default: "default")
        
    Returns:
        BatchResponse object with success/failure counts
    """
    # Ensure Firebase is initialized
    if _firebase_app is None:
        initialize_firebase()
    
    if not tokens:
        logger.warning("No tokens provided for multicast notification")
        return None
    
    # Get app-specific defaults if app_id provided
    if app_id:
        if icon is None:
            icon = app_configs.get_app_icon(app_id)
        if badge is None:
            badge = app_configs.get_app_badge(app_id)
    
    # Convert data values to strings (FCM requirement)
    string_data = convert_data_to_strings(data)
    
    # Build the message
    message = messaging.MulticastMessage(
        tokens=tokens,
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=string_data,
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=title,
                body=body,
                icon=icon or "/icon-192x192.png",
                badge=badge or "/icon-96x96.png",
                require_interaction=False,
                vibrate=[200, 100, 200]
            )
            # Note: fcm_options.link requires HTTPS URL, so we omit it
            # The notification will use the default action (opening the app)
        ),
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title=title,
                        body=body
                    ),
                    sound=sound,
                    badge=1
                )
            )
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                icon="ic_notification",
                sound=sound,
                channel_id="default"
            )
        )
    )
    
    try:
        # Use send_each_for_multicast instead of send_multicast
        response = messaging.send_each_for_multicast(message)
        logger.info(
            f"Multicast notification sent: {response.success_count} successful, "
            f"{response.failure_count} failed"
        )
        
        # Log failed tokens
        if response.failure_count > 0:
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    logger.warning(f"Failed to send to token {tokens[idx][:20]}...: {resp.exception}")
        
        return response
    except Exception as e:
        logger.error(f"Failed to send multicast notification: {str(e)}")
        raise

