"""
Main Flask application for FCM Notification Microservice.
"""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import firebase_service
import token_manager
import app_configs

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
allowed_origins = os.getenv('ALLOWED_ORIGINS', '')
if allowed_origins:
    origins = [origin.strip() for origin in allowed_origins.split(',')]
    CORS(app, origins=origins)
else:
    CORS(app)  # Allow all origins

# Optional API key authentication
API_KEY = os.getenv('API_KEY', '')


def check_api_key():
    """Check if API key is required and validate it."""
    if API_KEY:
        provided_key = request.headers.get('X-API-Key') or request.headers.get('Authorization', '').replace('Bearer ', '')
        if provided_key != API_KEY:
            return jsonify({
                "success": False,
                "error": "Invalid or missing API key"
            }), 401
    return None


def initialize_services():
    """Initialize Firebase services."""
    try:
        firebase_service.initialize_firebase()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "notification-service",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route('/api/register-token', methods=['POST'])
def register_token():
    """Register a device token with app_id and optional user_id."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        token = data.get('token')
        app_id = data.get('app_id')
        
        if not token:
            return jsonify({
                "success": False,
                "error": "token is required"
            }), 400
        
        if not app_id:
            return jsonify({
                "success": False,
                "error": "app_id is required"
            }), 400
        
        # Optional fields
        user_id = data.get('user_id')
        device_type = data.get('device_type')
        platform = data.get('platform')
        
        # Save token
        token_info = token_manager.save_token(
            token=token,
            app_id=app_id,
            user_id=user_id,
            device_type=device_type,
            platform=platform
        )
        
        logger.info(f"Token registered: app_id={app_id}, user_id={user_id}")
        
        return jsonify({
            "success": True,
            "message": "Token registered successfully",
            "app_id": app_id,
            "user_id": user_id
        }), 200
        
    except Exception as e:
        logger.error(f"Error registering token: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/send-notification', methods=['POST'])
def send_notification():
    """Send notification to a single device token."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        token = data.get('token')
        title = data.get('title')
        body = data.get('body')
        
        if not token:
            return jsonify({
                "success": False,
                "error": "token is required"
            }), 400
        
        if not title:
            return jsonify({
                "success": False,
                "error": "title is required"
            }), 400
        
        if not body:
            return jsonify({
                "success": False,
                "error": "body is required"
            }), 400
        
        # Optional fields
        app_id = data.get('app_id')
        icon = data.get('icon')
        badge = data.get('badge')
        custom_data = data.get('data', {})
        
        # Send notification
        response = firebase_service.send_push_notification(
            token=token,
            title=title,
            body=body,
            app_id=app_id,
            icon=icon,
            badge=badge,
            data=custom_data
        )
        
        logger.info(f"Notification sent to token {token[:20]}...")
        
        return jsonify({
            "success": True,
            "message": "Notification sent successfully",
            "message_id": response
        }), 200
        
    except ValueError as e:
        logger.warning(f"Invalid request: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/send-to-app', methods=['POST'])
def send_to_app():
    """
    Send notification to all devices registered for a specific app_id.
    This is the MOST IMPORTANT endpoint - automatically uses app-specific configs.
    """
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        app_id = data.get('app_id')
        title = data.get('title')
        body = data.get('body')
        
        if not app_id:
            return jsonify({
                "success": False,
                "error": "app_id is required"
            }), 400
        
        if not title:
            return jsonify({
                "success": False,
                "error": "title is required"
            }), 400
        
        if not body:
            return jsonify({
                "success": False,
                "error": "body is required"
            }), 400
        
        # Optional fields
        user_id = data.get('user_id')  # Filter by user if provided
        custom_data = data.get('data', {})
        icon = data.get('icon')  # Override app default if provided
        badge = data.get('badge')  # Override app default if provided
        
        # Get app configuration (for icon/badge defaults)
        app_config = app_configs.get_app_config(app_id)
        
        # Optionally add title prefix from app config
        if app_config.get('default_title_prefix') and not title.startswith(app_config['default_title_prefix']):
            title = f"{app_config['default_title_prefix']} {title}"
        
        # Get all tokens for this app
        tokens = token_manager.get_tokens_for_app(app_id=app_id, user_id=user_id)
        
        if not tokens:
            logger.warning(f"No tokens found for app_id: {app_id}, user_id: {user_id}")
            return jsonify({
                "success": True,
                "message": "No devices registered for this app",
                "app_id": app_id,
                "sent_to": 0,
                "tokens": []
            }), 200
        
        # Use app-specific icon/badge if not overridden
        if icon is None:
            icon = app_config.get('icon')
        if badge is None:
            badge = app_config.get('badge')
        
        # Send multicast notification
        batch_response = firebase_service.send_multicast_notification(
            tokens=tokens,
            title=title,
            body=body,
            app_id=app_id,
            icon=icon,
            badge=badge,
            data=custom_data
        )
        
        sent_count = batch_response.success_count if batch_response else 0
        
        logger.info(f"Sent notifications to {sent_count} devices for app_id: {app_id}")
        
        return jsonify({
            "success": True,
            "message": "Notifications sent",
            "app_id": app_id,
            "sent_to": sent_count,
            "failed": batch_response.failure_count if batch_response else 0,
            "tokens": tokens
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending to app: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/send-to-user', methods=['POST'])
def send_to_user():
    """Send notification to all devices for a specific user."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        user_id = data.get('user_id')
        title = data.get('title')
        body = data.get('body')
        
        if not user_id:
            return jsonify({
                "success": False,
                "error": "user_id is required"
            }), 400
        
        if not title:
            return jsonify({
                "success": False,
                "error": "title is required"
            }), 400
        
        if not body:
            return jsonify({
                "success": False,
                "error": "body is required"
            }), 400
        
        # Optional fields
        app_id = data.get('app_id')  # Filter by app if provided
        custom_data = data.get('data', {})
        icon = data.get('icon')
        badge = data.get('badge')
        
        # Get all tokens for this user
        tokens = token_manager.get_tokens_for_user(user_id=user_id, app_id=app_id)
        
        if not tokens:
            logger.warning(f"No tokens found for user_id: {user_id}, app_id: {app_id}")
            return jsonify({
                "success": True,
                "message": "No devices registered for this user",
                "user_id": user_id,
                "sent_to": 0
            }), 200
        
        # Send multicast notification
        batch_response = firebase_service.send_multicast_notification(
            tokens=tokens,
            title=title,
            body=body,
            app_id=app_id,
            icon=icon,
            badge=badge,
            data=custom_data
        )
        
        sent_count = batch_response.success_count if batch_response else 0
        
        logger.info(f"Sent notifications to {sent_count} devices for user_id: {user_id}")
        
        return jsonify({
            "success": True,
            "message": "Notifications sent",
            "user_id": user_id,
            "app_id": app_id,
            "sent_to": sent_count,
            "failed": batch_response.failure_count if batch_response else 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error sending to user: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/broadcast', methods=['POST'])
def broadcast():
    """Send notification to all registered devices (broadcast)."""
    auth_error = check_api_key()
    if auth_error:
        return auth_error
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required"
            }), 400
        
        # Validate required fields
        title = data.get('title')
        body = data.get('body')
        
        if not title:
            return jsonify({
                "success": False,
                "error": "title is required"
            }), 400
        
        if not body:
            return jsonify({
                "success": False,
                "error": "body is required"
            }), 400
        
        # Optional fields
        custom_data = data.get('data', {})
        icon = data.get('icon')
        badge = data.get('badge')
        
        # Get all tokens
        tokens = token_manager.get_all_tokens()
        
        if not tokens:
            logger.warning("No tokens found for broadcast")
            return jsonify({
                "success": True,
                "message": "No devices registered",
                "sent_to": 0
            }), 200
        
        # Send multicast notification
        batch_response = firebase_service.send_multicast_notification(
            tokens=tokens,
            title=title,
            body=body,
            icon=icon,
            badge=badge,
            data=custom_data
        )
        
        sent_count = batch_response.success_count if batch_response else 0
        
        logger.info(f"Broadcast sent to {sent_count} devices")
        
        return jsonify({
            "success": True,
            "message": "Broadcast sent",
            "sent_to": sent_count,
            "failed": batch_response.failure_count if batch_response else 0
        }), 200
        
    except Exception as e:
        logger.error(f"Error broadcasting: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Initialize Firebase before starting server
    initialize_services()
    
    # Get port from environment or use default
    # Railway automatically sets PORT environment variable
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting notification service on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

