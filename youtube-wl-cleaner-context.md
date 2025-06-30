# YouTube Watch Later Cleaner - MCP Server Context

## Problem Statement

YouTube's "Watch Later" feature becomes an unmanageable graveyard of hundreds of videos that users add impulsively but never watch. Common issues include:
- No organization or categorization system
- Deleted/private videos cluttering the list
- No way to schedule viewing time
- Difficulty finding specific content types
- Mix of educational and entertainment content without separation
- No insights into total time commitment

## Solution Overview

An MCP server that connects YouTube, Notion, and Google Calendar to transform the chaotic Watch Later list into an organized, actionable viewing system with smart categorization, scheduling, and progress tracking.

## Core Functionality

### 1. Analysis & Cleanup
- Fetch entire Watch Later playlist via YouTube API
- Identify and remove deleted/private/unavailable videos
- Extract comprehensive metadata for each video
- Calculate total watch time and statistics

### 2. Smart Categorization
- Auto-categorize videos based on:
  - Title keywords (tutorial, vlog, review, etc.)
  - Channel type and history
  - Video duration patterns
  - Upload date and relevance
- Categories: Education, Entertainment, Tutorials, Productivity, Conference Talks, etc.

### 3. Organization & Export
- Create structured Notion database with all video information
- Group related videos (series, similar topics)
- Prioritize based on user preferences and video engagement
- Generate playlists for specific purposes

### 4. Scheduling & Planning
- Create viewing schedules based on available time slots
- Add calendar events for learning sessions
- Match video duration to available time windows
- Separate work-appropriate vs leisure content

## Data Flow

```
1. User Request → MCP Server authenticates with YouTube
2. YouTube API → Fetch Watch Later playlist data
3. Process each video:
   - Check availability status
   - Extract metadata (title, duration, channel, stats)
   - Categorize using keyword/pattern matching
   - Calculate priority score
4. Generate organized structure:
   - Remove unavailable videos
   - Group by category and priority
   - Create viewing schedule
5. Export to external tools:
   - Notion: Create/update video database
   - Calendar: Add viewing sessions
   - YouTube: Create filtered playlists
6. Return summary report to user
```

## Key Data Points Per Video

- Video ID and URL
- Title and channel name
- Duration and upload date
- Date added to Watch Later
- Category (auto-detected)
- Priority level
- Availability status
- View count and engagement metrics
- Detected topics/tags

## Example Interactions

### Basic Cleanup Request
**Input:** "Clean up my YouTube Watch Later list"

**Output:**
- Summary: 247 total videos → 224 active (23 deleted removed)
- Categorization breakdown with hours per category
- Notion database created with all videos organized
- Option to create viewing schedule

### Filtered Learning Plan
**Input:** "Find all React tutorials under 30 minutes from the last 3 months and create a weekend study plan"

**Output:**
- 12 matching videos found (4.5 hours total)
- Weekend schedule created with specific time slots
- Calendar events added with reminder
- Notion page with notes template for each video

### Bulk Management
**Input:** "Archive videos older than 6 months except from favorite channels, remove anything over 3 hours"

**Output:**
- 89 videos archived to separate playlist
- 18 videos kept from favorite channels
- 7 long videos removed
- Watch Later reduced from 247 to 141 videos

## Advanced Features

### Pattern Detection
- Identify video series and proper viewing order
- Find duplicate content across channels
- Detect user preferences from watching history

### Time Optimization
- Match video length to available time slots
- Create "lunch break" vs "deep learning" sessions
- Suggest best times based on video type

### Progress Tracking
- Mark videos as watched
- Track completion of learning paths
- Generate weekly viewing reports

## Success Criteria

- User can quickly find specific types of content
- Total watch time is visible and manageable
- Videos are scheduled realistically
- Deleted content is automatically cleaned
- Organization persists in external tools (Notion/Calendar)

## User Benefits

1. **Time Awareness**: Know exactly how much content you've saved
2. **Intentional Viewing**: Videos scheduled when you'll actually watch them
3. **Learning Paths**: Educational content organized progressively
4. **Clean List**: No more scrolling past deleted videos
5. **External Organization**: Your system lives beyond YouTube