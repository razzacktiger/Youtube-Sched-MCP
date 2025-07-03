# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Watch Later Cleaner is a FastMCP 2.0 server that transforms chaotic YouTube "Watch Later" playlists into organized, actionable viewing systems. It provides tools for analyzing, categorizing, cleaning, and exporting video data to external services like Notion and Google Calendar.

## Architecture

### Core Framework
- **FastMCP 2.0**: Modern MCP server using decorator-based tools (`@mcp.tool`)
- **Single server file**: `src/server.py` contains all tool definitions with implementation delegates
- **Modular design**: Implementation logic separated into focused modules:
  - `youtube_api.py`: YouTube Data API interactions
  - `categorizer.py`: Video categorization logic  
  - `exporters.py`: Notion and Calendar integrations
  - `utils.py`: Shared utilities and configuration

### Tool Architecture
- **8 main tools**: From basic hello_world to complex analyze_watch_later
- **2 resources**: Configuration categories and server stats
- **2 prompts**: User assistance for categorization and scheduling
- **Async-first**: All tools use async/await with Context logging support

## Development Commands

### Setup and Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools

# Setup environment
cp env.example .env  # Add your API keys
```

### Development Server
```bash
# Run basic server (console output)
python src/server.py

# Run with FastMCP Inspector (recommended for development)
fastmcp dev src/server.py

# Install for Claude Desktop
fastmcp install src/server.py
```

### Testing and Quality
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src

# Format code
black src/

# Type checking
mypy src/

# Run all quality checks
black src/ && mypy src/ && pytest
```

### API Testing
```bash
# Test YouTube API without quotas
MOCK_YOUTUBE_API=true python src/server.py

# Test with debug logging
DEBUG=true python src/server.py

# Test specific functions
python debug_youtube.py
python test_youtube.py
```

## Key Implementation Patterns

### FastMCP 2.0 Tool Structure
```python
@mcp.tool
async def tool_name(
    param: type,
    optional_param: Optional[type] = None,
    ctx: Context = None
) -> return_type:
    """Tool description for MCP schema generation."""
    return await implementation_function(param, optional_param, ctx)
```

### Error Handling Strategy
- **API quotas**: Use mock implementations during development (`MOCK_YOUTUBE_API=true`)
- **Missing credentials**: Graceful degradation with clear error messages
- **Network issues**: Retry logic with exponential backoff in API calls
- **Rate limiting**: Respect YouTube API quotas with batching

### Configuration Management
- **Environment variables**: API keys and settings in `.env` file
- **API configuration**: Centralized in `utils.get_api_config()`
- **Categories**: Default video categories in `utils.get_default_categories()`
- **Resource endpoints**: Expose configuration via MCP resources

## Current Implementation Status

### Complete (✅)
- FastMCP 2.0 server foundation
- Project structure and dependencies
- Environment setup and basic tools
- Testing framework setup

### In Progress (🚧)
- YouTube Data API integration (`src/youtube_api.py`)
- Video categorization system (`src/categorizer.py`)
- External service integrations (`src/exporters.py`)

### Planned (⏳)
- OAuth authentication for private playlists
- Advanced ML-based categorization
- Calendar conflict detection
- Bulk playlist management

## External Dependencies

### Required APIs
- **YouTube Data API v3**: Core functionality for playlist access
- **Notion API**: Optional for database exports
- **Google Calendar API**: Optional for scheduling features

### Python Dependencies
- `fastmcp>=2.9.0`: Core MCP server framework
- `google-api-python-client`: YouTube API client
- `notion-client`: Notion API integration
- `httpx`: Async HTTP client
- `pydantic>=2.0.0`: Data validation and schemas

## Development Workflow

### Adding New Tools
1. Add tool definition with `@mcp.tool` decorator in `src/server.py`
2. Implement logic in appropriate module (`youtube_api.py`, `categorizer.py`, etc.)
3. Add comprehensive tests in `tests/`
4. Test manually with `fastmcp dev src/server.py`
5. Update documentation and type hints

### API Integration Guidelines
- **Batch operations**: Minimize API calls by batching requests
- **Error handling**: Always handle API quotas and network errors
- **Async patterns**: Use `httpx.AsyncClient` for all HTTP operations
- **Context logging**: Use `ctx.info()` and `ctx.report_progress()` for user feedback

### Testing Strategy
- **Unit tests**: Individual function testing with mocked APIs
- **Integration tests**: End-to-end workflow testing with real APIs
- **Mock mode**: `MOCK_YOUTUBE_API=true` for quota-free development
- **Manual testing**: FastMCP Inspector for interactive tool testing

## File Structure Context

```
src/
├── server.py           # Main FastMCP server with tool definitions
├── youtube_api.py      # YouTube Data API implementation
├── categorizer.py      # Video categorization logic
├── exporters.py        # Notion/Calendar export functionality
├── utils.py           # Shared utilities and configuration
└── __init__.py        # Package initialization

tests/                  # Test suite
requirements*.txt       # Dependency management
.env                   # API keys and configuration (gitignored)
TASK.md               # Development roadmap and task tracking
```

## Important Notes

- **Never commit API keys**: Always use `.env` file for sensitive credentials
- **Respect API quotas**: YouTube Data API has daily limits - use mock mode during development
- **FastMCP Context**: Always include `ctx: Context = None` parameter for proper logging
- **Async consistency**: All tools should be async for optimal performance
- **Error messages**: Provide clear, actionable error messages to users