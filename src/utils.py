"""
Utility functions and helpers for YouTube Watch Later Cleaner.
"""

import os
from typing import Dict, Any, Optional


def get_api_config() -> Dict[str, Any]:
    """Get API configuration from environment variables.
    
    Returns:
        Dictionary with API configuration and status
    """
    # Get the credentials file path from environment
    google_creds_path = os.getenv('GOOGLE_CREDENTIALS_FILE')
    
    # YouTube OAuth configuration
    youtube_oauth_token = os.getenv('YOUTUBE_OAUTH_TOKEN', 'token.json')
    youtube_oauth_creds = os.getenv('YOUTUBE_OAUTH_CREDENTIALS', 'credentials.json')
    
    return {
        'youtube_api_key': os.getenv('YOUTUBE_API_KEY'),
        'notion_api_key': os.getenv('NOTION_API_KEY'),
        'google_credentials_file': google_creds_path,
        'youtube_oauth_token': youtube_oauth_token,
        'youtube_oauth_credentials': youtube_oauth_creds,
        'has_youtube': bool(os.getenv('YOUTUBE_API_KEY')),
        'has_notion': bool(os.getenv('NOTION_API_KEY')),
        'has_google_creds': bool(google_creds_path and os.path.exists(google_creds_path)),
        'has_youtube_oauth': bool(os.path.exists(youtube_oauth_token) and os.path.exists(youtube_oauth_creds))
    }


def format_duration(seconds: int) -> str:
    """Format video duration from seconds to human readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "1h 23m 45s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def get_default_categories() -> Dict[str, str]:
    """Get default video categories and their descriptions.
    
    Returns:
        Dictionary mapping category names to descriptions
    """
    return {
        "Education": "Tutorials, courses, how-to videos",
        "Tech": "Programming, software reviews, tech news", 
        "Entertainment": "Gaming, comedy, vlogs",
        "Productivity": "Business, self-improvement, life hacks",
        "Conference": "Talks, presentations, lectures",
        "Short": "Videos under 10 minutes",
        "Long": "Videos over 1 hour"
    }


def create_mock_video_data(count: int = 247) -> Dict[str, Any]:
    """Create mock video data for testing purposes.
    
    Args:
        count: Number of mock videos to generate
        
    Returns:
        Mock video data structure
    """
    return {
        "total_videos": count,
        "categories": {
            "Education": 89,
            "Tech": 67,
            "Entertainment": 45,
            "Productivity": 32,
            "Conference": 14
        },
        "stats": {
            "total_duration_hours": 67.5,
            "avg_video_length_minutes": 16.4,
            "oldest_video_days": 180,
            "unavailable_count": 23
        }
    }


def load_youtube_oauth_credentials(token_file: str = 'token.json') -> Optional[Any]:
    """Load YouTube OAuth credentials from token file.
    
    Args:
        token_file: Path to the OAuth token file
        
    Returns:
        OAuth credentials object or None if not available
    """
    if not os.path.exists(token_file):
        return None
    
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        
        # Load existing credentials
        creds = Credentials.from_authorized_user_file(
            token_file, 
            ['https://www.googleapis.com/auth/youtube.readonly', 
             'https://www.googleapis.com/auth/youtube']
        )
        
        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            
            # Save refreshed token
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        return creds if creds and creds.valid else None
        
    except Exception as e:
        print(f"Error loading OAuth credentials: {e}")
        return None 