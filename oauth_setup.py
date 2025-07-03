#!/usr/bin/env python3
"""
YouTube OAuth Setup Script
Sets up OAuth 2.0 credentials for accessing YouTube Watch Later playlist
"""

import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# YouTube OAuth scopes needed for Watch Later access
SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',  # Read playlists
    'https://www.googleapis.com/auth/youtube'           # Modify playlists (for cleanup)
]

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def setup_oauth_credentials():
    """Interactive setup for YouTube OAuth credentials."""
    print("🎬 YouTube Watch Later Cleaner - OAuth Setup")
    print("=" * 50)
    
    # Check if credentials.json exists
    if not os.path.exists(CREDENTIALS_FILE):
        print("❌ credentials.json not found!")
        print("\n📋 To create credentials.json:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing project")
        print("3. Enable YouTube Data API v3")
        print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth 2.0 Client ID'")
        print("5. Choose 'Desktop Application' as application type")
        print("6. Download the JSON file and rename it to 'credentials.json'")
        print("7. Place credentials.json in this directory")
        print("\n🔄 Run this script again after creating credentials.json")
        return False
    
    print("✅ Found credentials.json")
    
    # Load existing token if available
    creds = None
    if os.path.exists(TOKEN_FILE):
        print(f"📄 Loading existing token from {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("✅ Token refreshed successfully!")
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                print("🔄 Starting new OAuth flow...")
                creds = None
        
        if not creds:
            print("🌐 Starting OAuth flow...")
            print("📱 Your browser will open for authentication")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=8080)
            print("✅ OAuth flow completed!")
        
        # Save the credentials for the next run
        print(f"💾 Saving token to {TOKEN_FILE}")
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    print("✅ OAuth setup complete!")
    
    # Test the credentials
    print("🧪 Testing YouTube API access...")
    try:
        youtube = build('youtube', 'v3', credentials=creds)
        
        # Test basic access
        channels_response = youtube.channels().list(
            part='snippet',
            mine=True
        ).execute()
        
        if channels_response['items']:
            channel_name = channels_response['items'][0]['snippet']['title']
            print(f"✅ Successfully authenticated as: {channel_name}")
        
        # Test Watch Later access
        try:
            wl_response = youtube.playlistItems().list(
                part='snippet',
                playlistId='WL',
                maxResults=1
            ).execute()
            
            video_count = wl_response['pageInfo']['totalResults']
            print(f"✅ Watch Later playlist accessible ({video_count} videos)")
            
        except Exception as e:
            print(f"⚠️  Watch Later access test failed: {e}")
            print("   This might be normal if your Watch Later is empty")
    
    except Exception as e:
        print(f"❌ YouTube API test failed: {e}")
        return False
    
    print("\n📝 Next steps:")
    print("1. Copy .env.example to .env if you haven't already")
    print("2. Update your .env file with:")
    print(f"   YOUTUBE_OAUTH_TOKEN={TOKEN_FILE}")
    print(f"   YOUTUBE_OAUTH_CREDENTIALS={CREDENTIALS_FILE}")
    print("3. Test your server: python src/server.py")
    print("4. Use 'analyze_watch_later' tool to access your real playlist!")
    
    return True

def check_oauth_status():
    """Check current OAuth setup status."""
    print("🔍 OAuth Status Check")
    print("=" * 30)
    
    status = {
        'credentials_file': os.path.exists(CREDENTIALS_FILE),
        'token_file': os.path.exists(TOKEN_FILE),
        'token_valid': False
    }
    
    print(f"credentials.json: {'✅' if status['credentials_file'] else '❌'}")
    print(f"token.json: {'✅' if status['token_file'] else '❌'}")
    
    if status['token_file']:
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            status['token_valid'] = creds and creds.valid
            print(f"Token valid: {'✅' if status['token_valid'] else '❌'}")
            
            if creds and creds.expired and creds.refresh_token:
                print("Token status: 🔄 Expired but refreshable")
            elif not creds.valid:
                print("Token status: ❌ Invalid, re-authentication needed")
            
        except Exception as e:
            print(f"Token status: ❌ Error reading token: {e}")
    
    return status

def main():
    """Main function with command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube OAuth Setup for Watch Later Cleaner")
    parser.add_argument('--check', action='store_true', help='Check OAuth status only')
    parser.add_argument('--reset', action='store_true', help='Reset OAuth (delete existing tokens)')
    
    args = parser.parse_args()
    
    if args.reset:
        print("🗑️  Resetting OAuth setup...")
        for file in [TOKEN_FILE]:
            if os.path.exists(file):
                os.remove(file)
                print(f"   Deleted {file}")
        print("✅ Reset complete. Run setup again to re-authenticate.")
        return
    
    if args.check:
        check_oauth_status()
        return
    
    # Default: run setup
    success = setup_oauth_credentials()
    if success:
        print("\n🎉 OAuth setup completed successfully!")
    else:
        print("\n❌ OAuth setup failed. Check the instructions above.")

if __name__ == '__main__':
    main()