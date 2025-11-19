"""
App-specific configurations for different Progressive Web Apps (PWAs).
Each app can have its own icon, badge, and notification settings.
"""

APP_CONFIGS = {
    "trading-app": {
        "name": "Trading Dashboard",
        "icon": "/trading-icon-192x192.png",
        "badge": "/trading-badge-96x96.png",
        "default_title_prefix": "💰",
        "color": "#00ff00"
    },
    "weather-app": {
        "name": "Weather App",
        "icon": "/weather-icon-192x192.png",
        "badge": "/weather-badge-96x96.png",
        "default_title_prefix": "🌤️",
        "color": "#00aaff"
    },
    "news-app": {
        "name": "News Reader",
        "icon": "/news-icon-192x192.png",
        "badge": "/news-badge-96x96.png",
        "default_title_prefix": "📰",
        "color": "#ff6600"
    }
}


def get_app_config(app_id: str) -> dict:
    """
    Get configuration for a specific app.
    
    Args:
        app_id: The identifier for the PWA app
        
    Returns:
        Dictionary containing app configuration with defaults if app_id not found
    """
    return APP_CONFIGS.get(app_id, {
        "name": f"App: {app_id}",
        "icon": "/icon-192x192.png",
        "badge": "/icon-96x96.png",
        "default_title_prefix": "",
        "color": "#000000"
    })


def get_app_icon(app_id: str) -> str:
    """Get icon path for an app."""
    config = get_app_config(app_id)
    return config.get("icon", "/icon-192x192.png")


def get_app_badge(app_id: str) -> str:
    """Get badge path for an app."""
    config = get_app_config(app_id)
    return config.get("badge", "/icon-96x96.png")


def get_app_title_prefix(app_id: str) -> str:
    """Get default title prefix for an app."""
    config = get_app_config(app_id)
    return config.get("default_title_prefix", "")

