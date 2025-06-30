# YouTube Watch Later Cleaner - MCP Server Planning (Revised)

## Project Overview

An MCP (Model Context Protocol) server that transforms YouTube's chaotic "Watch Later" list into an organized, actionable viewing system. Built with FastMCP 2.0, integrating YouTube API, Notion, and Google Calendar for smart categorization, scheduling, and progress tracking.

## Architecture Overview (FastMCP 2.0)

### Technology Stack

- **Core**: Python 3.10+ with FastMCP 2.0 (`fastmcp` package)
- **APIs**: YouTube Data API v3, Notion API, Google Calendar API
- **Data Processing**: pydantic v2, httpx, python-dateutil
- **Categorization**: Rule-based system with keyword analysis
- **Testing**: pytest with FastMCP built-in client testing
- **Configuration**: python-dotenv for environment management

### Simplified Project Structure

```
src/
├── server.py                  # Main FastMCP server with all MCP tools
├── services/
│   ├── youtube_service.py     # YouTube API operations
│   ├── notion_service.py      # Notion database management
│   ├── calendar_service.py    # Google Calendar integration
│   └── categorizer.py         # Video categorization logic
├── models/
│   ├── video.py              # Pydantic video data models
│   ├── requests.py           # Request/response models for tools
│   └── config.py             # Configuration models
├── utils/
│   ├── text_analyzer.py      # Title/description analysis
│   ├── time_utils.py         # Duration and scheduling utilities
│   └── auth.py               # API authentication helpers
├── tests/
│   ├── test_server.py        # FastMCP server tests using Client
│   ├── test_services/        # Service unit tests
│   └── fixtures/             # Test data and mocks
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md                 # Setup and usage instructions
```

### FastMCP 2.0 Data Models

#### Video Model

```python
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List, Optional

class Video(BaseModel):
    id: str
    title: str
    channel_name: str
    duration: timedelta
    upload_date: datetime
    added_date: Optional[datetime] = None
    url: str
    thumbnail_url: str
    view_count: int
    category: str
    priority: int = 0
    is_available: bool = True
    topics: List[str] = []
```

#### Tool Request Models

```python
class AnalyzeRequest(BaseModel):
    max_results: Optional[int] = None
    include_stats: bool = True

class CategorizeRequest(BaseModel):
    recategorize: bool = False
    custom_rules: Optional[dict] = None

class ScheduleRequest(BaseModel):
    time_slots: List[str]
    categories: List[str]
    duration_limit: int = 120  # minutes
```

## FastMCP 2.0 Tools Implementation

### Core Server Structure

```python
from fastmcp import FastMCP, Context
from typing import List, Optional
import asyncio

# Create the FastMCP server
mcp = FastMCP(
    name="YouTube Watch Later Cleaner",
    dependencies=["google-api-python-client", "notion-client", "httpx", "pydantic"]
)
```

### MCP Tools (using @mcp.tool decorator)

#### 1. `analyze_watch_later`

```python
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
    await ctx.info("Starting Watch Later analysis...")
    # Implementation here
    return {"total_videos": 247, "categories": {...}, "stats": {...}}
```

#### 2. `cleanup_unavailable`

```python
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
    await ctx.info(f"{'Previewing' if dry_run else 'Executing'} cleanup...")
    # Implementation here
    return {"removed_count": 23, "removed_videos": [...]}
```

#### 3. `categorize_videos`

```python
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
    # Implementation here
    return {"categorized_count": 224, "categories": {...}}
```

#### 4. `create_notion_database`

```python
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
    await ctx.info(f"Creating Notion database: {database_name}")
    # Implementation here
    return {"database_url": "https://...", "videos_exported": 224}
```

#### 5. `schedule_viewing`

```python
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
    await ctx.report_progress(0, len(categories))
    # Implementation here
    return {"events_created": 12, "total_time_scheduled": "8.5 hours"}
```

#### 6. `create_filtered_playlists`

```python
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
    # Implementation here
    return {"playlists_created": [...]}
```

### Resources (using @mcp.resource decorator)

```python
@mcp.resource("config://categories")
def get_available_categories() -> dict:
    """Returns available video categories and their descriptions."""
    return {
        "Education": "Tutorials, courses, how-to videos",
        "Tech": "Programming, software reviews, tech news",
        "Entertainment": "Gaming, comedy, vlogs",
        "Productivity": "Business, self-improvement",
        "Conference": "Talks, presentations, lectures"
    }

@mcp.resource("stats://user/{user_preference}")
def get_user_stats(user_preference: str) -> dict:
    """Returns user statistics for specific preference type."""
    # Implementation here
    return {"preference": user_preference, "data": {...}}
```

### Prompts (using @mcp.prompt decorator)

```python
@mcp.prompt
def categorization_help(video_title: str, channel_name: str) -> str:
    """Generate a prompt for manual video categorization assistance."""
    return f"""
    Help categorize this YouTube video:

    Title: {video_title}
    Channel: {channel_name}

    Suggest the most appropriate category from: Education, Tech, Entertainment, Productivity, Conference

    Consider the title keywords, channel type, and likely content focus.
    """
```

## Configuration Management

### Environment Variables

```python
# .env.example
# YouTube API
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REFRESH_TOKEN=your_refresh_token

# Notion API
NOTION_API_KEY=your_notion_integration_key
NOTION_DATABASE_TEMPLATE_ID=optional_template_id

# Google Calendar API
GOOGLE_CALENDAR_CREDENTIALS_FILE=path/to/credentials.json
GOOGLE_CALENDAR_ID=primary

# FastMCP Server
FASTMCP_LOG_LEVEL=INFO
```

### Configuration Model

```python
from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    youtube_api_key: str
    youtube_client_id: str
    youtube_client_secret: str
    youtube_refresh_token: Optional[str] = None

    notion_api_key: str
    notion_database_template_id: Optional[str] = None

    google_credentials_file: str
    google_calendar_id: str = "primary"

    log_level: str = "INFO"
```

## Testing Strategy with FastMCP 2.0

### Unit Testing with Built-in Client

```python
import pytest
from fastmcp import Client
from src.server import mcp

@pytest.mark.asyncio
async def test_analyze_watch_later():
    async with Client(mcp) as client:
        # Test tool execution
        result = await client.call_tool("analyze_watch_later", {
            "max_results": 10,
            "include_stats": True
        })

        assert result.content[0].text
        data = json.loads(result.content[0].text)
        assert "total_videos" in data
        assert "categories" in data

@pytest.mark.asyncio
async def test_categorization_resource():
    async with Client(mcp) as client:
        # Test resource access
        result = await client.read_resource("config://categories")

        assert result.content[0].text
        categories = json.loads(result.content[0].text)
        assert "Education" in categories
```

### Integration Testing

```python
@pytest.mark.asyncio
async def test_full_workflow():
    async with Client(mcp) as client:
        # 1. Analyze playlist
        analysis = await client.call_tool("analyze_watch_later", {"max_results": 5})

        # 2. Categorize videos
        categorization = await client.call_tool("categorize_videos", {})

        # 3. Create Notion database
        notion_db = await client.call_tool("create_notion_database", {
            "database_name": "Test Watch Later"
        })

        # Verify workflow completion
        assert "database_url" in json.loads(notion_db.content[0].text)
```

## Running the Server

### Development Mode

```bash
# Using FastMCP CLI for development with inspector
fastmcp dev src/server.py

# Direct execution
python src/server.py
```

### Production Mode

```python
# In server.py
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
```

### Claude Desktop Integration

```bash
# Install for Claude Desktop
fastmcp install src/server.py --name "YouTube Watch Later Cleaner"
```

## Error Handling Strategy

### FastMCP Context for Logging

```python
@mcp.tool
async def example_tool(ctx: Context = None) -> dict:
    try:
        await ctx.info("Starting operation...")
        # API call
        result = await some_api_call()
        await ctx.info("Operation completed successfully")
        return result
    except APIQuotaExceeded as e:
        await ctx.error(f"YouTube API quota exceeded: {e}")
        raise
    except Exception as e:
        await ctx.error(f"Unexpected error: {e}")
        raise
```

### Pydantic Validation

```python
from pydantic import BaseModel, validator

class ScheduleRequest(BaseModel):
    time_slots: List[str]
    duration_limit: int = 120

    @validator('duration_limit')
    def validate_duration(cls, v):
        if v <= 0 or v > 480:  # Max 8 hours
            raise ValueError('Duration must be between 1 and 480 minutes')
        return v
```

## Performance Considerations

### Async Operations

- All API calls use `httpx.AsyncClient`
- YouTube API batching for efficiency
- Concurrent processing with `asyncio.gather()`

### Caching Strategy

```python
from functools import lru_cache
import asyncio

@lru_cache(maxsize=100)
def get_category_keywords():
    """Cache categorization keywords"""
    return load_keywords_from_config()

# Async caching for API responses
cache = {}

async def get_video_details_cached(video_id: str):
    if video_id not in cache:
        cache[video_id] = await youtube_service.get_video_details(video_id)
    return cache[video_id]
```

## Dependencies

### Core Dependencies

```python
# requirements.txt
fastmcp>=2.9.0
pydantic>=2.0.0
httpx>=0.24.0
python-dotenv>=1.0.0

# API clients
google-api-python-client>=2.0.0
google-auth>=2.0.0
notion-client>=2.0.0

# Utilities
python-dateutil>=2.8.0
```

### Development Dependencies

```python
# requirements-dev.txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
black>=23.0.0
mypy>=1.0.0
httpx[testing]>=0.24.0
```

## Success Metrics

### Functional Metrics

- Tool execution success rate (>95%)
- Video categorization accuracy (>85%)
- API quota efficiency (minimal YouTube API calls)
- Response time (<30 seconds for 100 videos)

### User Experience Metrics

- Setup simplicity (single command installation)
- Integration reliability with Claude Desktop
- Clear error messages and logging
- Comprehensive progress reporting

## Future Enhancements

### Phase 2 Features

- Machine learning categorization improvements
- Collaborative filtering recommendations
- Watch history analysis integration
- Mobile app notifications

### Advanced Integrations

- Integration with more calendar systems
- Support for additional note-taking apps
- Webhook notifications for completed videos
- Analytics dashboard for viewing patterns

This revised architecture leverages FastMCP 2.0's elegant decorator-based approach, eliminating the complex boilerplate while maintaining all the powerful functionality planned for the YouTube Watch Later cleaner.
