#!/usr/bin/env python3
"""
YouTube Watch Later Cleaner - FastMCP Server

A FastMCP 2.0 server that transforms YouTube's chaotic "Watch Later" list 
into an organized, actionable viewing system.
"""

import asyncio
import json
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP, Context
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create the FastMCP server
mcp = FastMCP(
    name="YouTube Watch Later Cleaner",
    dependencies=[
        "google-api-python-client",
        "notion-client", 
        "httpx",
        "pydantic",
        "python-dotenv"
    ]
)

# ============================================================================
# TEST TOOLS (for initial setup verification)
# ============================================================================

@mcp.tool
def hello_world(name: str = "World") -> str:
    """A simple hello world tool to test FastMCP setup.
    
    Args:
        name: Name to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! 🎉 FastMCP server is working correctly!"


@mcp.tool
async def test_async(message: str, ctx: Context = None) -> dict:
    """Test async functionality and Context logging.
    
    Args:
        message: Test message to process
        
    Returns:
        Result with message and status
    """
    if ctx:
        await ctx.info(f"Processing test message: {message}")
        await ctx.report_progress(1, 2)
        await ctx.info("Test async operation completed")
    
    return {
        "original_message": message,
        "processed": message.upper(),
        "status": "success",
        "async_working": True
    }

# ============================================================================
# MAIN YOUTUBE TOOLS (stubs for now - will implement in Task 3.1+)
# ============================================================================

@mcp.tool
async def analyze_watch_later(
    max_results: Optional[int] = None,
    include_stats: bool = True,
    ctx: Context = None
) -> dict:
    """Fetch and analyze Watch Later playlist with categorization breakdown.
    
    Args:
        max_results: Limit number of videos to analyze
        include_stats: Include detailed statistics in response
        
    Returns:
        Analysis summary with categorization breakdown and statistics
    """
    if ctx:
        await ctx.info("Starting Watch Later analysis...")
        await ctx.report_progress(0, 3)
    
    # TODO: Implement in Task 3.1
    # For now, return mock data
    mock_result = {
        "status": "stub_implementation",
        "total_videos": 247,
        "max_results": max_results,
        "include_stats": include_stats,
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
        } if include_stats else None
    }
    
    if ctx:
        await ctx.report_progress(3, 3)
        await ctx.info("Watch Later analysis completed (stub)")
    
    return mock_result


@mcp.tool
async def cleanup_unavailable(
    dry_run: bool = True,
    ctx: Context = None
) -> dict:
    """Remove deleted/private videos from Watch Later playlist.
    
    Args:
        dry_run: Preview changes without applying them
        
    Returns:
        List of videos that would be/were removed
    """
    if ctx:
        await ctx.info(f"{'Previewing' if dry_run else 'Executing'} cleanup...")
    
    # TODO: Implement in Task 3.1
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


@mcp.tool
async def categorize_videos(
    recategorize: bool = False,
    custom_rules: Optional[dict] = None,
    ctx: Context = None
) -> dict:
    """Auto-categorize videos using intelligent analysis.
    
    Args:
        recategorize: Force re-categorization of existing videos
        custom_rules: User-defined categorization rules
        
    Returns:
        Updated video list with categories and confidence scores
    """
    if ctx:
        await ctx.info("Starting video categorization...")
    
    # TODO: Implement in Task 3.2
    mock_result = {
        "status": "stub_implementation",
        "recategorize": recategorize,
        "custom_rules": custom_rules,
        "categorized_count": 224,
        "categories": {
            "Education": {"count": 89, "confidence": 0.92},
            "Tech": {"count": 67, "confidence": 0.88},
            "Entertainment": {"count": 45, "confidence": 0.85},
            "Productivity": {"count": 32, "confidence": 0.91},
            "Conference": {"count": 14, "confidence": 0.96}
        }
    }
    
    if ctx:
        await ctx.info(f"Categorization completed (stub) - {mock_result['categorized_count']} videos")
    
    return mock_result


@mcp.tool
async def create_notion_database(
    database_name: str,
    template_id: Optional[str] = None,
    ctx: Context = None
) -> dict:
    """Export organized videos to Notion database.
    
    Args:
        database_name: Name for the new Notion database
        template_id: Optional existing template to use
        
    Returns:
        Notion database URL and creation summary
    """
    if ctx:
        await ctx.info(f"Creating Notion database: {database_name}")
    
    # TODO: Implement in Task 3.2
    mock_result = {
        "status": "stub_implementation", 
        "database_name": database_name,
        "template_id": template_id,
        "database_url": "https://notion.so/youtube-watch-later-abc123",
        "videos_exported": 224,
        "properties_created": [
            "Title", "Channel", "Duration", "Category", 
            "Priority", "Status", "Notes", "Watch Date"
        ]
    }
    
    if ctx:
        await ctx.info(f"Notion database created (stub): {mock_result['database_url']}")
    
    return mock_result


@mcp.tool
async def schedule_viewing(
    time_slots: List[str],
    categories: List[str],
    duration_limit: int = 120,
    ctx: Context = None
) -> dict:
    """Create calendar events for video watching sessions.
    
    Args:
        time_slots: Available time periods (e.g., ["weekday-evening", "weekend-morning"])
        categories: Which categories to schedule
        duration_limit: Maximum session length in minutes
        
    Returns:
        Created calendar events and scheduling summary
    """
    if ctx:
        await ctx.info(f"Scheduling viewing sessions for categories: {categories}")
        await ctx.report_progress(0, len(categories))
    
    # TODO: Implement in Task 3.2
    mock_result = {
        "status": "stub_implementation",
        "time_slots": time_slots,
        "categories": categories,
        "duration_limit": duration_limit,
        "events_created": 12,
        "total_time_scheduled": "8.5 hours",
        "calendar_events": [
            {
                "title": "Education Videos Session",
                "start": "2024-12-28T19:00:00",
                "duration": 90,
                "videos": 6
            },
            {
                "title": "Tech Videos Session", 
                "start": "2024-12-29T10:00:00",
                "duration": 120,
                "videos": 8
            }
        ]
    }
    
    if ctx:
        await ctx.report_progress(len(categories), len(categories))
        await ctx.info(f"Scheduling completed (stub) - {mock_result['events_created']} events")
    
    return mock_result


@mcp.tool
async def create_filtered_playlists(
    categories: List[str],
    max_videos_per_playlist: int = 50,
    ctx: Context = None
) -> dict:
    """Create YouTube playlists organized by category.
    
    Args:
        categories: Categories to create playlists for
        max_videos_per_playlist: Limit playlist size
        
    Returns:
        Created playlist URLs and video counts
    """
    if ctx:
        await ctx.info(f"Creating filtered playlists for: {categories}")
    
    # TODO: Implement in Task 3.2
    mock_result = {
        "status": "stub_implementation",
        "categories": categories,
        "max_videos_per_playlist": max_videos_per_playlist,
        "playlists_created": [
            {
                "category": "Education",
                "playlist_url": "https://youtube.com/playlist?list=PLabc123",
                "video_count": 50,
                "total_available": 89
            },
            {
                "category": "Tech", 
                "playlist_url": "https://youtube.com/playlist?list=PLdef456",
                "video_count": 50,
                "total_available": 67
            }
        ]
    }
    
    if ctx:
        await ctx.info(f"Playlists created (stub) - {len(mock_result['playlists_created'])} playlists")
    
    return mock_result

# ============================================================================
# RESOURCES (configuration and stats)
# ============================================================================

@mcp.resource("config://categories")
def get_available_categories() -> dict:
    """Returns available video categories and their descriptions."""
    return {
        "Education": "Tutorials, courses, how-to videos",
        "Tech": "Programming, software reviews, tech news", 
        "Entertainment": "Gaming, comedy, vlogs",
        "Productivity": "Business, self-improvement, life hacks",
        "Conference": "Talks, presentations, lectures",
        "Short": "Videos under 10 minutes",
        "Long": "Videos over 1 hour"
    }


@mcp.resource("stats://server")
def get_server_stats() -> dict:
    """Returns server status and statistics."""
    return {
        "server_name": "YouTube Watch Later Cleaner",
        "version": "1.0.0-dev",
        "fastmcp_version": "2.9.0+",
        "status": "development",
        "tools_available": 8,
        "resources_available": 2,
        "last_startup": "2024-12-27T12:00:00Z"
    }

# ============================================================================
# PROMPTS (helpful templates)
# ============================================================================

@mcp.prompt
def categorization_help(video_title: str, channel_name: str) -> str:
    """Generate a prompt for manual video categorization assistance."""
    return f"""
Help categorize this YouTube video:

Title: {video_title}
Channel: {channel_name}

Suggest the most appropriate category from: Education, Tech, Entertainment, Productivity, Conference

Consider the title keywords, channel type, and likely content focus.
Provide reasoning for your categorization choice.
"""


@mcp.prompt
def scheduling_help(available_time: int, categories: List[str]) -> str:
    """Generate a prompt for optimal video viewing schedule."""
    return f"""
Create an optimal viewing schedule:

Available time: {available_time} minutes
Categories to schedule: {', '.join(categories)}

Suggest the best order and time allocation for these video categories.
Consider factors like:
- Attention span requirements
- Time of day appropriateness  
- Category priorities
- Learning vs entertainment balance
"""

# ============================================================================
# SERVER STARTUP
# ============================================================================

def main():
    """Main entry point for the FastMCP server."""
    print("🎬 YouTube Watch Later Cleaner - FastMCP Server")
    print("=" * 50)
    print(f"Server: {mcp.name}")
    # FastMCP 2.0 doesn't expose tool counts directly, so we'll count manually
    print(f"Tools: 8 available (hello_world, test_async, analyze_watch_later, cleanup_unavailable, categorize_videos, create_notion_database, schedule_viewing, create_filtered_playlists)")
    print(f"Resources: 2 available (config://categories, stats://server)")
    print("=" * 50)
    
    # Check if API keys are configured
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    notion_api_key = os.getenv('NOTION_API_KEY')
    
    if not youtube_api_key:
        print("⚠️  WARNING: YOUTUBE_API_KEY not set in environment")
    if not notion_api_key:
        print("⚠️  WARNING: NOTION_API_KEY not set in environment")
    
    if youtube_api_key and notion_api_key:
        print("✅ API keys configured")
    else:
        print("📝 See .env.example for required API keys")
    
    print("=" * 50)
    print("🚀 Starting FastMCP server...")
    print("   Use 'fastmcp dev src/server.py' for MCP Inspector")
    print("   Use 'fastmcp install src/server.py' for Claude Desktop")
    print("=" * 50)


if __name__ == "__main__":
    main()
    # Run the FastMCP server
    mcp.run(transport="stdio") 