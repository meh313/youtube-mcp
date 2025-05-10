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
pip install .  # or use 'uv pip install' if you use uv
# Or install directly from pyproject.toml:
# pip install -e .
# or
# uv pip install -e .
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
    "keywords": ["n8n", "AI chatbot", "..."],
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

### Integration with Other MCP Clients

To integrate this MCP server with any other MCP-compatible client:
1. Ensure the server is running and accessible (default: `http://localhost:8000`).
2. In your MCP client's configuration, add a tool entry pointing to the MCP endpoint:
   ```json
   "youtube": {
     "url": "http://localhost:8000/mcp"
   }
   ```
   - Replace `localhost` with your server's address if running remotely.
   - The endpoint `/mcp` exposes the YouTube info tool for all MCP clients.
3. Restart or reload your MCP client as needed. The YouTube tool should now be available for use.

Refer to your specific MCP client's documentation for details on configuring external tools.

## License

MIT License

Copyright (c) 2025 meh313

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
