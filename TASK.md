# YouTube Watch Later Cleaner - Task Management (Revised for FastMCP 2.0)

## Project Status: 🚀 Planning Complete - Ready to Start (FastMCP 2.0)

**Last Updated**: December 27, 2024  
**Current Phase**: Phase 1 - Foundation Setup  
**Priority**: High - Simplified FastMCP 2.0 implementation

**Major Revision**: Updated to use FastMCP 2.0 architecture - significantly simpler implementation with decorator-based approach!

---

## Overview of Changes

✅ **Simplified Architecture**: Single `server.py` file with decorator-based tools instead of complex multi-module structure  
✅ **Built-in Testing**: FastMCP 2.0 provides built-in client for testing - no need for complex test setup  
✅ **Modern Dependencies**: Using `fastmcp>=2.9.0`, `pydantic>=2.0.0`, `httpx` instead of older libraries  
✅ **Fewer Files**: Reduced from 40+ files to ~15 files total  
✅ **Estimated Time**: Reduced from 65-85 hours to **7-12 hours** (FastMCP 2.0 simplified)

---

## Phase 1: Foundation & Core Setup

### Task 1.1: Project Structure & Environment Setup ✅ **COMPLETE**

**Priority**: Critical Path | **Estimated Time**: 1-2 hours | **Dependencies**: None | **Completed**: Dec 27, 2024

- [x] Create simplified project directory structure
- [x] Set up virtual environment with `fastmcp>=2.9.0`
- [x] Create requirements.txt with FastMCP 2.0 dependencies
- [x] Create env.example file with API credentials template
- [x] Set up basic FastMCP server file (`src/server.py`) - **8 tools, 2 resources working!**
- [x] Test basic FastMCP server with hello world tool - **✅ SERVER RUNNING**
- [x] Create README.md with setup instructions

**Files to Create**:

- `src/server.py` (main FastMCP server)
- `requirements.txt`
- `requirements-dev.txt`
- `.env.example`
- `README.md`
- `.gitignore`

**Verification**:

```bash
fastmcp dev src/server.py  # Should open MCP Inspector
```

---

### Task 1.2: API Keys Setup ⏳

**Priority**: Critical Path | **Estimated Time**: 30 minutes | **Dependencies**: Task 1.1

- [x] Copy `env.example` to `.env` ✅
- [x] Get YouTube Data API key from Google Console
- [x] Add YouTube API key to `.env` file
- [x] Test server with real API key (no warnings)
- [x] Optional: Get Notion API key for export features

**Steps**:

1. Go to [Google Developers Console](https://console.developers.google.com/)
2. Create project → Enable YouTube Data API v3 → Create API Key
3. Add to `.env`: `YOUTUBE_API_KEY=your_actual_key_here`
4. Restart server - should see ✅ instead of ⚠️

---

### Task 1.3: Implement YouTube API Integration ⏳

**Priority**: Critical Path | **Estimated Time**: 2-3 hours | **Dependencies**: Task 1.2

- [ ] Add real YouTube API client to `src/server.py`
- [ ] Implement `analyze_watch_later` tool with actual API calls
- [ ] Implement `cleanup_unavailable` tool to remove deleted videos
- [ ] Add simple video categorization by keyword matching
- [ ] Test with real Watch Later playlist
- [ ] Handle API errors gracefully

**Implementation**: Keep everything in single `server.py` file using FastMCP 2.0 patterns

---

### Task 1.4: Add Export Features ⏳

**Priority**: High | **Estimated Time**: 2-3 hours | **Dependencies**: Task 1.3

- [ ] Implement `create_filtered_playlists` tool
- [ ] Add basic `create_notion_database` tool (optional - needs Notion API key)
- [ ] Implement `schedule_viewing` tool with time-based suggestions
- [ ] Add CSV export as backup option
- [ ] Test complete workflow end-to-end

**Focus**: Simple, working features rather than complex architecture

---

## Phase 2: Testing and Polish

### Task 2.1: Testing and Documentation ⏳

**Priority**: Medium | **Estimated Time**: 2-3 hours | **Dependencies**: Task 1.4

- [ ] Create basic unit tests for core functions
- [ ] Add integration test with real YouTube API
- [ ] Update README.md with usage examples
- [ ] Add error handling documentation
- [ ] Test with large playlists (performance)

**Files to Create**:

- `tests/test_server.py`
- Update `README.md` with examples
- `conftest.py`

---

## Optional Tasks (Future Enhancements)

### Task 2.2: Enhanced Features ⏳

**Priority**: Low | **Estimated Time**: 3-5 hours | **Dependencies**: Task 2.1

- [ ] Add advanced categorization with ML/AI
- [ ] Implement smart playlist recommendations
- [ ] Add calendar integration with Google Calendar API
- [ ] Create web UI for non-technical users
- [ ] Add video thumbnail and preview support

**Note**: These are optional enhancements - core functionality works without them!

---

## Discovered During Work

_(Tasks discovered during implementation will be added here)_

---

## Completed Tasks ✅

_(Completed tasks will be moved here with completion date)_

---

## Notes and Decisions (FastMCP 2.0)

### Key Architectural Changes:

- **Built-in Testing**: Use `Client(mcp)` for in-memory testing
- **Modern Dependencies**: FastMCP 2.0, pydantic v2, httpx
- **Simplified Structure**: No complex MCP protocol handling needed

### FastMCP 2.0 Advantages:

- **Decorator-based**: `@mcp.tool`, `@mcp.resource`, `@mcp.prompt`
- **Built-in Context**: `ctx: Context` parameter for logging and progress
- **Automatic Schema**: Generated from type hints and docstrings
- **Testing Built-in**: Client class for testing without external processes
- **CLI Integration**: `fastmcp dev` and `fastmcp install` commands

### API Integration Strategy:

- YouTube API batching to minimize quota usage
- Notion API bulk operations for performance
- Google Calendar conflict detection and smart scheduling
- All async operations using `httpx.AsyncClient`

### Testing Strategy:

```python
# In-memory testing with FastMCP Client
async with Client(mcp) as client:
    result = await client.call_tool("analyze_watch_later", {...})
    assert "total_videos" in json.loads(result.content[0].text)
```

---

## Development Guidelines

### FastMCP 2.0 Best Practices:

1. Use `@mcp.tool` for all server-side functions
2. Add `ctx: Context = None` parameter for logging and progress
3. Use pydantic models for complex inputs
4. Test with `Client(mcp)` for fast iteration
5. Use `fastmcp dev` for development with inspector

### Definition of Done:

- [ ] Tool works with real API calls
- [ ] Tested manually in MCP Inspector
- [ ] Basic error handling included
- [ ] README updated with usage example

### **Estimated Total Time: 7-12 hours** (Reduced from 65-85 hours!)

### **Target Completion: 1-2 weeks** (part-time development)

---

## Quick Start Commands

```bash
# 1. Setup
pip install -r requirements.txt
cp .env.example .env  # Add your YouTube API key

# 2. Development
fastmcp dev src/server.py  # Opens MCP Inspector

# 3. Test tools manually in the inspector
# 4. Ready to use!
```

The FastMCP 2.0 approach dramatically simplifies the implementation while maintaining all the powerful functionality!
