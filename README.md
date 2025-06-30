# 🎬 YouTube Watch Later Cleaner - FastMCP Server

Transform your chaotic YouTube "Watch Later" list into an organized, actionable viewing system. Built with **FastMCP 2.0** for seamless integration with Claude Desktop and other MCP clients.

## ✨ Features

- **🔍 Smart Analysis**: Analyze your Watch Later playlist with categorization breakdown
- **🧹 Cleanup Tools**: Remove deleted/private videos automatically
- **🏷️ Auto-Categorization**: Intelligent video categorization using title/channel analysis
- **📋 Notion Integration**: Export organized videos to beautiful Notion databases
- **📅 Calendar Scheduling**: Create viewing sessions in Google Calendar
- **🎵 Playlist Creation**: Generate category-based YouTube playlists
- **📊 Progress Tracking**: Monitor viewing progress and statistics

## 🚀 Quick Start

### 1. Installation

```bash
# Clone and navigate to project
cd Youtube-Sched-MCP/

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Setup

1. **Copy environment file**:

   ```bash
   cp env.example .env
   ```

2. **Get YouTube API Key**:

   - Go to [Google Developers Console](https://console.developers.google.com/)
   - Create project → Enable YouTube Data API v3 → Create API Key
   - Add to `.env`: `YOUTUBE_API_KEY=your_key_here`

3. **Get Notion API Key** (optional):
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - Create new internal integration → Copy secret
   - Add to `.env`: `NOTION_API_KEY=your_key_here`

### 3. Test the Server

```bash
# Test basic functionality
python src/server.py

# Open FastMCP Inspector (recommended)
fastmcp dev src/server.py
```

**Expected Output**:

```
🎬 YouTube Watch Later Cleaner - FastMCP Server
==================================================
Server: YouTube Watch Later Cleaner
Tools: 8 available
Resources: 2 available
==================================================
✅ API keys configured
==================================================
🚀 Starting FastMCP server...
   Use 'fastmcp dev src/server.py' for MCP Inspector
   Use 'fastmcp install src/server.py' for Claude Desktop
==================================================
```

### 4. Test Tools

Once the server is running, test these tools:

```json
// Test basic functionality
{
  "tool": "hello_world",
  "arguments": {"name": "YouTube Cleaner"}
}

// Test async functionality
{
  "tool": "test_async",
  "arguments": {"message": "Testing FastMCP setup"}
}

// Test main tool (stub implementation)
{
  "tool": "analyze_watch_later",
  "arguments": {"max_results": 10, "include_stats": true}
}
```

## 🔧 Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

## 📱 Claude Desktop Integration

1. **Install the server**:

   ```bash
   fastmcp install src/server.py
   ```

2. **Or manually add to Claude config**:
   ```json
   {
     "mcpServers": {
       "youtube-cleaner": {
         "command": "python",
         "args": ["/path/to/Youtube-Sched-MCP/src/server.py"],
         "env": {
           "YOUTUBE_API_KEY": "your_key_here",
           "NOTION_API_KEY": "your_key_here"
         }
       }
     }
   }
   ```

## 🛠️ Available Tools

| Tool                        | Status   | Description                   |
| --------------------------- | -------- | ----------------------------- |
| `hello_world`               | ✅ Ready | Test FastMCP setup            |
| `test_async`                | ✅ Ready | Test async functionality      |
| `analyze_watch_later`       | 🚧 Stub  | Analyze Watch Later playlist  |
| `cleanup_unavailable`       | 🚧 Stub  | Remove deleted/private videos |
| `categorize_videos`         | 🚧 Stub  | Auto-categorize videos        |
| `create_notion_database`    | 🚧 Stub  | Export to Notion              |
| `schedule_viewing`          | 🚧 Stub  | Create calendar events        |
| `create_filtered_playlists` | 🚧 Stub  | Generate category playlists   |

**Note**: Stub tools return mock data for testing. Real implementations coming in subsequent tasks.

## 📋 Resources & Prompts

- **`config://categories`**: Available video categories
- **`stats://server`**: Server status and statistics
- **`categorization_help`**: Manual categorization assistance
- **`scheduling_help`**: Optimal viewing schedule suggestions

## 🐛 Troubleshooting

### Common Issues:

1. **"FastMCP not found"**:

   ```bash
   pip install fastmcp>=2.9.0
   ```

2. **"API key not working"**:

   - Check `.env` file exists and keys are correct
   - Verify YouTube API is enabled in Google Console
   - Ensure no extra spaces in API keys

3. **"Import errors"**:

   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. **"Permission denied"**:
   ```bash
   chmod +x src/server.py
   ```

### Debug Mode:

```bash
# Enable debug logging
DEBUG=true python src/server.py

# Enable API mocking (no quotas used)
MOCK_YOUTUBE_API=true python src/server.py
```

## 📖 Next Steps

Once Task 1.1 is complete, continue with:

- **Task 1.2**: Enhanced project structure and basic testing
- **Task 3.1**: YouTube API integration (analyze_watch_later, cleanup_unavailable)
- **Task 3.2**: Categorization system (categorize_videos)
- **Task 3.3**: External integrations (Notion, Calendar, Playlists)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Status**: ✅ Task 1.1 Complete - FastMCP 2.0 foundation ready for development!
