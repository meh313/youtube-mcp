# YouTube MCP Server

A FastAPI-based MCP server that provides YouTube video metadata and transcripts as a tool for Cursor and other MCP clients.

## Features
- Fetches video title, description, author, publish date, view count, tags, and best thumbnail.
- Retrieves transcript in English or falls back to Arabic if English is not available.
- Exposes a single `/youtube-info` endpoint as an MCP tool.
- Robust error handling for both metadata and transcript retrieval.

## Requirements
- Python 3.10+
- See `pyproject.toml` for dependencies (uses FastAPI, yt-dlp, youtube-transcript-api, fastapi-mcp, etc.)

## Installation

```bash
# Clone the repository
git clone https://github.com/meh313/youtube-mcp.git
cd youtube-mcp

# (Recommended) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt  # or use 'uv pip install -r requirements.txt' if you use uv
# Or use pyproject.toml with pip or uv
```

## Usage

```bash
uvicorn main:app --reload
```

Then access the API at:
```
http://localhost:8000/youtube-info?video_id=YOUR_VIDEO_ID
```

### Example Request
```
GET /youtube-info?video_id=l6TrXxqSzrE
```

### Example Response
```json
{
  "metadata": {
    "title": "Create an AI Chat Bot in n8n in 60 Seconds or Less!",
    "description": "...",
    "author": "Kris Torrington",
    "publish_date": "20250505",
    "length": 91,
    "views": 25,
    "keywords": ["n8n", "AI chatbot", ...],
    "channel_url": "https://www.youtube.com/channel/UCUevUDRxTDJCoG1KxQveXag",
    "thumbnail": "https://i.ytimg.com/vi/l6TrXxqSzrE/maxresdefault.jpg"
  },
  "transcript": "Hi everyone. I'm going to show you how..."
}
```

## MCP Integration

To use this server as a tool in Cursor:
1. Make sure the server is running (`uvicorn main:app --reload`).
2. Add the following to your `.cursor/mcp.json`:
   ```json
   "youtube": {
     "url": "http://localhost:8000/mcp"
   }
   ```
3. Restart Cursor. The `/youtube-info` tool will be available in the tool list.

## License

MIT
