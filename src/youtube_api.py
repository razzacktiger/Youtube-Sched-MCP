"""
YouTube API functions for Watch Later playlist analysis and management.
"""

from typing import Optional, List, Dict, Any
from fastmcp import Context
import asyncio
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httpx
from utils import get_api_config, create_mock_video_data


async def analyze_watch_later_impl(
    max_results: Optional[int] = None,
    include_stats: bool = True,
    ctx: Context = None
) -> Dict[str, Any]:
    """Implementation for Watch Later playlist analysis.
    
    Args:
        max_results: Limit number of videos to analyze
        include_stats: Include detailed statistics in response
        ctx: FastMCP context for logging
        
    Returns:
        Analysis summary with categorization breakdown and statistics
    """
    if ctx:
        await ctx.info("Starting Watch Later analysis...")
        await ctx.report_progress(0, 5)
    
    # Get API configuration
    config = get_api_config()
    
    if not config['has_youtube']:
        if ctx:
            await ctx.info("No YouTube API key found - returning mock data")
        return {
            **create_mock_video_data(),
            "status": "no_api_key",
            "max_results": max_results,
            "include_stats": include_stats,
            "message": "Add YOUTUBE_API_KEY to .env file for real data"
        }
    
    try:
        # Initialize YouTube API client
        youtube_client = YouTubeAPIClient(config['youtube_api_key'])
        
        if ctx:
            await ctx.info("Fetching Watch Later playlist...")
            await ctx.report_progress(1, 5)
        
        # Get Watch Later videos
        max_fetch = max_results or 50
        videos = youtube_client.get_watch_later_videos(max_fetch)
        
        if not videos:
            return {
                "status": "empty_playlist",
                "total_videos": 0,
                "message": "Your Watch Later playlist is empty"
            }
        
        if ctx:
            await ctx.info(f"Found {len(videos)} videos, analyzing...")
            await ctx.report_progress(2, 5)
        
        # Get detailed video information
        video_ids = [video['id'] for video in videos]
        video_details = youtube_client.get_video_details(video_ids)
        
        if ctx:
            await ctx.info("Categorizing videos...")
            await ctx.report_progress(3, 5)
        
        # Analyze and categorize
        categories = {}
        total_duration = 0
        unavailable_count = 0
        video_analysis = []
        
        for video in videos:
            video_id = video['id']
            details = video_details.get(video_id)
            
            if not details:
                # Video is unavailable (deleted/private)
                unavailable_count += 1
                continue
            
            # Simple categorization based on title and tags
            category = _categorize_video_simple(details)
            categories[category] = categories.get(category, 0) + 1
            total_duration += details['duration_seconds']
            
            # Add to analysis
            video_analysis.append({
                'id': video_id,
                'title': details['title'],
                'channel': details['channel'],
                'duration': details['duration_formatted'],
                'category': category,
                'view_count': details['view_count'],
                'url': f"https://youtube.com/watch?v={video_id}"
            })
        
        if ctx:
            await ctx.info("Analysis complete!")
            await ctx.report_progress(5, 5)
        
        # Build comprehensive result
        result = {
            "status": "success",
            "total_videos": len(videos),
            "available_videos": len(videos) - unavailable_count,
            "unavailable_videos": unavailable_count,
            "categories": categories,
            "total_duration_seconds": total_duration,
            "total_duration_formatted": _format_total_duration(total_duration),
            "max_results": max_results,
            "include_stats": include_stats
        }
        
        # Add detailed stats if requested
        if include_stats:
            result["detailed_stats"] = {
                "average_duration_seconds": total_duration // max(1, len(video_analysis)),
                "most_common_category": max(categories.items(), key=lambda x: x[1])[0] if categories else "None",
                "channels": list(set(v['channel'] for v in video_analysis)),
                "total_views": sum(v['view_count'] for v in video_analysis)
            }
            result["videos"] = video_analysis[:10]  # First 10 videos for preview
        
        return result
        
    except Exception as e:
        error_msg = f"Error analyzing Watch Later playlist: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        
        return {
            "status": "error",
            "error": error_msg,
            "message": "Check your YouTube API key and quota limits"
        }


async def cleanup_unavailable_impl(
    dry_run: bool = True,
    ctx: Context = None
) -> Dict[str, Any]:
    """Implementation for cleaning up deleted/private videos.
    
    Args:
        dry_run: Preview changes without applying them
        ctx: FastMCP context for logging
        
    Returns:
        List of videos that would be/were removed
    """
    if ctx:
        await ctx.info(f"{'Previewing' if dry_run else 'Executing'} cleanup...")
    
    config = get_api_config()
    
    if not config['has_youtube']:
        return {
            "status": "no_api_key",
            "message": "YouTube API key required for cleanup operations"
        }
    
    # TODO: Implement real cleanup logic in Task 1.3
    mock_result = {
        "status": "stub_implementation",
        "dry_run": dry_run,
        "removed_count": 23,
        "removed_videos": [
            {"id": "abc123", "title": "[Deleted Video]", "reason": "deleted"},
            {"id": "def456", "title": "[Private Video]", "reason": "private"},
            {"id": "ghi789", "title": "Old Tutorial", "reason": "unavailable"}
        ]
    }
    
    if ctx:
        await ctx.info(f"Cleanup completed (stub) - {mock_result['removed_count']} videos")
    
    return mock_result


async def create_filtered_playlists_impl(
    categories: List[str],
    max_videos_per_playlist: int = 50,
    ctx: Context = None
) -> Dict[str, Any]:
    """Implementation for creating filtered YouTube playlists.
    
    Args:
        categories: Categories to create playlists for
        max_videos_per_playlist: Limit playlist size
        ctx: FastMCP context for logging
        
    Returns:
        Created playlist URLs and video counts
    """
    if ctx:
        await ctx.info(f"Creating filtered playlists for: {categories}")
    
    config = get_api_config()
    
    if not config['has_youtube']:
        return {
            "status": "no_api_key",
            "message": "YouTube API key required for playlist creation"
        }
    
    # TODO: Implement real playlist creation in Task 1.4
    mock_result = {
        "status": "stub_implementation",
        "categories": categories,
        "max_videos_per_playlist": max_videos_per_playlist,
        "playlists_created": [
            {
                "category": cat,
                "playlist_url": f"https://youtube.com/playlist?list=PL{cat.lower()}123",
                "video_count": min(50, 89 if cat == "Education" else 67 if cat == "Tech" else 45),
                "total_available": 89 if cat == "Education" else 67 if cat == "Tech" else 45
            }
            for cat in categories[:3]  # Limit mock data
        ]
    }
    
    if ctx:
        await ctx.info(f"Playlists created (stub) - {len(mock_result['playlists_created'])} playlists")
    
    return mock_result


async def test_public_playlist_impl(
    playlist_id: str,
    max_results: Optional[int] = None,
    include_stats: bool = True,
    ctx: Context = None
) -> Dict[str, Any]:
    """Test implementation using a public playlist instead of Watch Later.
    
    Args:
        playlist_id: Public YouTube playlist ID
        max_results: Limit number of videos to analyze
        include_stats: Include detailed statistics in response
        ctx: FastMCP context for logging
        
    Returns:
        Analysis summary with categorization breakdown and statistics
    """
    if ctx:
        await ctx.info(f"Testing with public playlist: {playlist_id}")
        await ctx.report_progress(0, 5)
    
    # Get API configuration
    config = get_api_config()
    
    if not config['has_youtube']:
        if ctx:
            await ctx.info("No YouTube API key found")
        return {
            "status": "no_api_key",
            "message": "Add YOUTUBE_API_KEY to .env file"
        }
    
    try:
        # Initialize YouTube API client
        youtube_client = YouTubeAPIClient(config['youtube_api_key'])
        
        if ctx:
            await ctx.info("Fetching public playlist...")
            await ctx.report_progress(1, 5)
        
        # Get public playlist videos
        max_fetch = max_results or 50
        videos = youtube_client.get_public_playlist_videos(playlist_id, max_fetch)
        
        if not videos:
            return {
                "status": "empty_playlist",
                "total_videos": 0,
                "message": f"Playlist {playlist_id} is empty or not accessible"
            }
        
        if ctx:
            await ctx.info(f"Found {len(videos)} videos, analyzing...")
            await ctx.report_progress(2, 5)
        
        # Get detailed video information
        video_ids = [video['id'] for video in videos]
        video_details = youtube_client.get_video_details(video_ids)
        
        if ctx:
            await ctx.info("Categorizing videos...")
            await ctx.report_progress(3, 5)
        
        # Analyze and categorize
        categories = {}
        total_duration = 0
        unavailable_count = 0
        video_analysis = []
        
        for video in videos:
            video_id = video['id']
            details = video_details.get(video_id)
            
            if not details:
                # Video is unavailable (deleted/private)
                unavailable_count += 1
                continue
            
            # Simple categorization based on title and tags
            category = _categorize_video_simple(details)
            categories[category] = categories.get(category, 0) + 1
            total_duration += details['duration_seconds']
            
            # Add to analysis
            video_analysis.append({
                'id': video_id,
                'title': details['title'],
                'channel': details['channel'],
                'duration': details['duration_formatted'],
                'category': category,
                'view_count': details['view_count'],
                'url': f"https://youtube.com/watch?v={video_id}"
            })
        
        if ctx:
            await ctx.info("Analysis complete!")
            await ctx.report_progress(5, 5)
        
        # Build comprehensive result
        result = {
            "status": "success",
            "playlist_id": playlist_id,
            "total_videos": len(videos),
            "available_videos": len(videos) - unavailable_count,
            "unavailable_videos": unavailable_count,
            "categories": categories,
            "total_duration_seconds": total_duration,
            "total_duration_formatted": _format_total_duration(total_duration),
            "max_results": max_results,
            "include_stats": include_stats
        }
        
        # Add detailed stats if requested
        if include_stats:
            result["detailed_stats"] = {
                "average_duration_seconds": total_duration // max(1, len(video_analysis)),
                "most_common_category": max(categories.items(), key=lambda x: x[1])[0] if categories else "None",
                "channels": list(set(v['channel'] for v in video_analysis)),
                "total_views": sum(v['view_count'] for v in video_analysis)
            }
            result["videos"] = video_analysis[:10]  # First 10 videos for preview
        
        return result
        
    except Exception as e:
        error_msg = f"Error analyzing playlist: {str(e)}"
        if ctx:
            await ctx.error(error_msg)
        
        return {
            "status": "error",
            "error": error_msg,
            "message": "Check your YouTube API key and playlist ID"
        }


# Real YouTube API Client Implementation
class YouTubeAPIClient:
    """Real YouTube API client using Google API with OAuth support."""
    
    def __init__(self, api_key: str = None, oauth_creds = None):
        self.api_key = api_key
        self.oauth_creds = oauth_creds
        
        if oauth_creds:
            # Use OAuth credentials for authenticated requests (Watch Later access)
            self.youtube = build('youtube', 'v3', credentials=oauth_creds)
            self.has_oauth = True
        elif api_key:
            # Use API key for public data only
            self.youtube = build('youtube', 'v3', developerKey=api_key)
            self.has_oauth = False
        else:
            raise ValueError("Either api_key or oauth_creds must be provided")
    
    def get_public_playlist_videos(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """Fetch videos from any public playlist with pagination support.
        
        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to fetch (can be > 50)
            
        Returns:
            List of video data dictionaries
        """
        try:
            videos = []
            next_page_token = None
            videos_fetched = 0
            
            while videos_fetched < max_results:
                # Calculate how many to fetch in this request
                remaining = max_results - videos_fetched
                per_request = min(remaining, 50)  # YouTube API limit per request
                
                # Make API request
                request = self.youtube.playlistItems().list(
                    part='snippet,contentDetails',
                    playlistId=playlist_id,
                    maxResults=per_request,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                # Process videos from this page
                for item in response['items']:
                    if videos_fetched >= max_results:
                        break
                        
                    video_data = {
                        'id': item['contentDetails']['videoId'],
                        'title': item['snippet']['title'],
                        'channel': item['snippet']['channelTitle'],
                        'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'thumbnail': item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                        'position': item['snippet']['position']
                    }
                    videos.append(video_data)
                    videos_fetched += 1
                
                # Check if there are more pages
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break  # No more pages
                
            return videos
            
        except HttpError as e:
            if e.resp.status == 404:
                raise Exception(f"Playlist {playlist_id} not found or not accessible")
            elif e.resp.status == 403:
                raise Exception("YouTube API quota exceeded or invalid API key")
            else:
                raise Exception(f"YouTube API error: {e}")

    def get_watch_later_videos(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """Fetch videos from Watch Later playlist.
        
        Args:
            max_results: Maximum number of videos to fetch
            
        Returns:
            List of video data dictionaries
        """
        try:
            # Get Watch Later playlist items
            request = self.youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId='WL',  # WL = Watch Later playlist ID
                maxResults=min(max_results, 50)  # YouTube API limit per request
            )
            response = request.execute()
            
            videos = []
            for item in response['items']:
                video_data = {
                    'id': item['contentDetails']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnail': item['snippet']['thumbnails'].get('medium', {}).get('url', ''),
                    'position': item['snippet']['position']
                }
                videos.append(video_data)
                
            return videos
            
        except HttpError as e:
            if e.resp.status == 404:
                raise Exception("Watch Later playlist not found or empty")
            elif e.resp.status == 403:
                raise Exception("YouTube API quota exceeded or invalid API key")
            else:
                raise Exception(f"YouTube API error: {e}")
    
    def check_video_availability(self, video_id: str) -> bool:
        """Check if a video is still available (not deleted/private).
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            True if video is available, False otherwise
        """
        try:
            request = self.youtube.videos().list(
                part='id',
                id=video_id
            )
            response = request.execute()
            return len(response['items']) > 0
            
        except HttpError:
            return False
    
    def get_video_details(self, video_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Get detailed information for multiple videos with batch processing.
        
        Args:
            video_ids: List of YouTube video IDs (any length, processed in batches of 50)
            
        Returns:
            Dictionary mapping video IDs to their details
        """
        if not video_ids:
            return {}
            
        try:
            video_details = {}
            
            # Process videos in batches of 50 (YouTube API limit)
            for i in range(0, len(video_ids), 50):
                batch = video_ids[i:i+50]
                
                request = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(batch)
                )
                response = request.execute()
                
                # Process this batch
                for item in response['items']:
                    # Parse duration from ISO 8601 format (PT4M13S -> 253 seconds)
                    duration_str = item['contentDetails']['duration']
                    duration_seconds = self._parse_duration(duration_str)
                    
                    video_details[item['id']] = {
                        'title': item['snippet']['title'],
                        'channel': item['snippet']['channelTitle'],
                        'description': item['snippet']['description'],
                        'duration_seconds': duration_seconds,
                        'duration_formatted': self._format_duration(duration_seconds),
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'published_at': item['snippet']['publishedAt'],
                        'category_id': item['snippet']['categoryId'],
                        'tags': item['snippet'].get('tags', [])
                    }
                
            return video_details
            
        except HttpError as e:
            raise Exception(f"Error fetching video details: {e}")
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration (PT4M13S) to seconds."""
        import re
        
        # Match patterns like PT4M13S, PT1H2M3S, PT45S
        pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
        match = re.match(pattern, duration_str)
        
        if not match:
            return 0
            
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0) 
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _format_duration(self, seconds: int) -> str:
        """Format seconds to human readable duration."""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"


# Helper functions for video analysis
def _categorize_video_simple(video_details: Dict[str, Any]) -> str:
    """Simple video categorization based on title, channel, and tags.
    
    Args:
        video_details: Video metadata from YouTube API
        
    Returns:
        Category string
    """
    title = video_details['title'].lower()
    channel = video_details['channel'].lower()
    tags = [tag.lower() for tag in video_details.get('tags', [])]
    
    # Combine all text for analysis
    text_content = f"{title} {channel} {' '.join(tags)}"
    
    # Education keywords
    if any(keyword in text_content for keyword in [
        'tutorial', 'course', 'learn', 'education', 'lesson', 'guide', 
        'how to', 'explained', 'lecture', 'training', 'skill'
    ]):
        return "Education"
    
    # Technology keywords
    if any(keyword in text_content for keyword in [
        'tech', 'programming', 'coding', 'software', 'ai', 'python', 
        'javascript', 'web dev', 'computer', 'algorithm', 'data'
    ]):
        return "Technology"
    
    # Entertainment keywords
    if any(keyword in text_content for keyword in [
        'funny', 'comedy', 'entertainment', 'meme', 'reaction', 'gaming',
        'game', 'stream', 'podcast', 'music', 'song'
    ]):
        return "Entertainment"
    
    # News/Documentary keywords
    if any(keyword in text_content for keyword in [
        'news', 'documentary', 'analysis', 'review', 'investigation',
        'politics', 'history', 'science', 'research'
    ]):
        return "News & Documentary"
    
    # Health & Fitness keywords
    if any(keyword in text_content for keyword in [
        'fitness', 'workout', 'health', 'diet', 'exercise', 'yoga',
        'meditation', 'wellness', 'nutrition'
    ]):
        return "Health & Fitness"
    
    # Default category
    return "Other"


def _format_total_duration(total_seconds: int) -> str:
    """Format total duration in a human-readable way.
    
    Args:
        total_seconds: Total duration in seconds
        
    Returns:
        Formatted duration string
    """
    if total_seconds < 3600:  # Less than 1 hour
        minutes = total_seconds // 60
        return f"{minutes} minutes"
    elif total_seconds < 86400:  # Less than 1 day
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:  # More than 1 day
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        return f"{days} days, {hours}h" 