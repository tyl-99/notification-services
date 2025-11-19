"""
Token CRUD operations in Firestore for managing FCM device tokens.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import firebase_admin
from firebase_admin import firestore
from firebase_service import initialize_firebase

logger = logging.getLogger(__name__)

# Firestore collection name
COLLECTION_NAME = "device_tokens"


def get_firestore_client():
    """Get Firestore client instance."""
    initialize_firebase()
    return firestore.client()


def save_token(
    token: str,
    app_id: str,
    user_id: Optional[str] = None,
    device_type: Optional[str] = None,
    platform: Optional[str] = None
) -> Dict[str, Any]:
    """
    Save or update a device token in Firestore.
    
    Args:
        token: FCM device token
        app_id: App identifier (required)
        user_id: User identifier (optional)
        device_type: Device type - "ios", "android", "web" (optional)
        platform: Platform name - "safari", "chrome", etc. (optional)
        
    Returns:
        Dictionary with token information
    """
    try:
        db = get_firestore_client()
        now = datetime.utcnow()
        
        token_data = {
            "token": token,
            "app_id": app_id,
            "updated_at": now,
            "last_active": now
        }
        
        if user_id:
            token_data["user_id"] = user_id
        if device_type:
            token_data["device_type"] = device_type
        if platform:
            token_data["platform"] = platform
        
        # Check if token already exists
        doc_ref = db.collection(COLLECTION_NAME).document(token)
        doc = doc_ref.get()
        
        if doc.exists:
            # Update existing token
            token_data["created_at"] = doc.to_dict().get("created_at", now)
            doc_ref.update(token_data)
            logger.info(f"Updated token for app_id: {app_id}, user_id: {user_id}")
        else:
            # Create new token
            token_data["created_at"] = now
            doc_ref.set(token_data)
            logger.info(f"Registered new token for app_id: {app_id}, user_id: {user_id}")
        
        return token_data
        
    except Exception as e:
        logger.error(f"Failed to save token: {str(e)}")
        raise


def get_tokens_for_app(
    app_id: str,
    user_id: Optional[str] = None
) -> List[str]:
    """
    Get all device tokens registered for a specific app.
    
    Args:
        app_id: App identifier
        user_id: Optional user identifier to filter by
        
    Returns:
        List of FCM device tokens
    """
    try:
        db = get_firestore_client()
        query = db.collection(COLLECTION_NAME).where("app_id", "==", app_id)
        
        if user_id:
            query = query.where("user_id", "==", user_id)
        
        docs = query.stream()
        tokens = [doc.to_dict()["token"] for doc in docs]
        
        logger.info(f"Found {len(tokens)} tokens for app_id: {app_id}, user_id: {user_id}")
        return tokens
        
    except Exception as e:
        logger.error(f"Failed to get tokens for app: {str(e)}")
        raise


def get_tokens_for_user(
    user_id: str,
    app_id: Optional[str] = None
) -> List[str]:
    """
    Get all device tokens registered for a specific user.
    
    Args:
        user_id: User identifier
        app_id: Optional app identifier to filter by
        
    Returns:
        List of FCM device tokens
    """
    try:
        db = get_firestore_client()
        query = db.collection(COLLECTION_NAME).where("user_id", "==", user_id)
        
        if app_id:
            query = query.where("app_id", "==", app_id)
        
        docs = query.stream()
        tokens = [doc.to_dict()["token"] for doc in docs]
        
        logger.info(f"Found {len(tokens)} tokens for user_id: {user_id}, app_id: {app_id}")
        return tokens
        
    except Exception as e:
        logger.error(f"Failed to get tokens for user: {str(e)}")
        raise


def get_all_tokens() -> List[str]:
    """
    Get all registered device tokens (for broadcast).
    
    Returns:
        List of all FCM device tokens
    """
    try:
        db = get_firestore_client()
        docs = db.collection(COLLECTION_NAME).stream()
        tokens = [doc.to_dict()["token"] for doc in docs]
        
        logger.info(f"Found {len(tokens)} total tokens")
        return tokens
        
    except Exception as e:
        logger.error(f"Failed to get all tokens: {str(e)}")
        raise


def delete_token(token: str) -> bool:
    """
    Delete a device token from Firestore.
    
    Args:
        token: FCM device token to delete
        
    Returns:
        True if deleted, False if not found
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(token)
        doc = doc_ref.get()
        
        if doc.exists:
            doc_ref.delete()
            logger.info(f"Deleted token: {token[:20]}...")
            return True
        else:
            logger.warning(f"Token not found: {token[:20]}...")
            return False
            
    except Exception as e:
        logger.error(f"Failed to delete token: {str(e)}")
        raise


def get_token_info(token: str) -> Optional[Dict[str, Any]]:
    """
    Get metadata for a specific token.
    
    Args:
        token: FCM device token
        
    Returns:
        Dictionary with token metadata or None if not found
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(token)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
            
    except Exception as e:
        logger.error(f"Failed to get token info: {str(e)}")
        raise


def update_token_activity(token: str) -> None:
    """
    Update the last_active timestamp for a token.
    
    Args:
        token: FCM device token
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection(COLLECTION_NAME).document(token)
        doc_ref.update({"last_active": datetime.utcnow()})
        
    except Exception as e:
        logger.warning(f"Failed to update token activity: {str(e)}")

