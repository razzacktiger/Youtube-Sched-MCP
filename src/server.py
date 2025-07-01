#!/usr/bin/env python3
"""
YouTube Watch Later Cleaner - FastMCP Server

A FastMCP 2.0 server that transforms YouTube's chaotic "Watch Later" list 
into an organized, actionable viewing system.
"""

import argparse
import asyncio
import json
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP, Context
from dotenv import load_dotenv
import os

# Import our organized modules
from youtube_api import analyze_watch_later_impl, cleanup_unavailable_impl, create_filtered_playlists_impl
from categorizer import categorize_videos_impl
from exporters import create_notion_database_impl, schedule_viewing_impl
from utils import get_api_config, get_default_categories

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
    return await analyze_watch_later_impl(max_results, include_stats, ctx)


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
    return await cleanup_unavailable_impl(dry_run, ctx)


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
    return await categorize_videos_impl(recategorize, custom_rules, ctx)


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
    return await create_notion_database_impl(database_name, template_id, ctx)


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
    return await schedule_viewing_impl(time_slots, categories, duration_limit, ctx)


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
    return await create_filtered_playlists_impl(categories, max_videos_per_playlist, ctx)

# ============================================================================
# RESOURCES (configuration and stats)
# ============================================================================

@mcp.resource("config://categories")
def get_available_categories() -> dict:
    """Returns available video categories and their descriptions."""
    return get_default_categories()


@mcp.resource("stats://server")
def get_server_stats() -> dict:
    """Returns server status and statistics."""
    config = get_api_config()
    return {
        "server_name": "YouTube Watch Later Cleaner",
        "version": "1.0.0-dev",
        "fastmcp_version": "2.9.0+",
        "status": "development",
        "tools_available": 8,
        "resources_available": 2,
        "api_keys_configured": {
            "youtube": config['has_youtube'],
            "notion": config['has_notion'],
            "google_calendar": config['has_google_creds']
        },
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
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="YouTube Watch Later Cleaner - FastMCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", 
                       help="Transport type: stdio for local/Claude Desktop, http for deployment")
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    parser.add_argument("--path", default="/mcp", help="Path for HTTP transport")
    
    args = parser.parse_args()
    
    print("🎬 YouTube Watch Later Cleaner - FastMCP Server")
    print("=" * 50)
    print(f"Server: {mcp.name}")
    print(f"Transport: {args.transport.upper()}")
    # FastMCP 2.0 doesn't expose tool counts directly, so we'll count manually
    print(f"Tools: 8 available (hello_world, test_async, analyze_watch_later, cleanup_unavailable, categorize_videos, create_notion_database, schedule_viewing, create_filtered_playlists)")
    print(f"Resources: 2 available (config://categories, stats://server)")
    print("=" * 50)
    
    # Check API configuration using utility function
    config = get_api_config()
    
    if not config['has_youtube']:
        print("⚠️  WARNING: YOUTUBE_API_KEY not set in environment")
    else:
        print("✅ YouTube API key configured")
    
    if not config['has_notion']:
        print("⚠️  WARNING: NOTION_API_KEY not set in environment")
    else:
        print("✅ Notion API key configured")
    
    if not config['has_google_creds']:
        print("⚠️  WARNING: Google Calendar credentials not found")
    else:
        print("✅ Google Calendar credentials configured")
    
    if not any([config['has_youtube'], config['has_notion'], config['has_google_creds']]):
        print("📝 See .env.example for required API keys")
    
    print("=" * 50)
    
    if args.transport == "stdio":
        print("🚀 Starting FastMCP server (STDIO)...")
        print("   Use 'fastmcp dev src/server.py' for MCP Inspector")
        print("   Use 'fastmcp install src/server.py' for Claude Desktop")
        print("=" * 50)
        # Run the FastMCP server with stdio transport
        mcp.run(transport="stdio")
    else:
        print(f"🌐 Starting FastMCP server (HTTP)...")
        print(f"   URL: http://{args.host}:{args.port}{args.path}")
        print(f"   Use this URL to connect MCP clients")
        print("=" * 50)
        # Run the FastMCP server with HTTP transport
        mcp.run(
            transport="http",
            host=args.host,
            port=args.port,
            path=args.path
        )


if __name__ == "__main__":
    main() 