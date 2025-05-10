from fastapi import FastAPI, Query
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from fastapi_mcp import FastApiMCP

app = FastAPI()

def get_best_thumbnail(thumbnails):
    for thumb in thumbnails or []:
        if "maxresdefault.jpg" in thumb["url"]:
            return thumb["url"]
    for thumb in thumbnails or []:
        if "hqdefault.jpg" in thumb["url"]:
            return thumb["url"]
    if thumbnails:
        return thumbnails[0]["url"]
    return None

def get_video_metadata_yt_dlp(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            thumbnails = info.get("thumbnails")
            return {
                "title": info.get("title"),
                "description": info.get("description"),
                "author": info.get("uploader"),
                "publish_date": info.get("upload_date"),
                "length": info.get("duration"),
                "views": info.get("view_count"),
                "keywords": info.get("tags"),
                "channel_url": info.get("channel_url"),
                "thumbnail": get_best_thumbnail(thumbnails),
            }
    except Exception as e:
        return {"error": f"Metadata Error: {e}"}

def get_transcript(video_id, language='en'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        return "\n".join([entry['text'] for entry in transcript])
    except Exception as e:
        # If the requested language is 'en', try 'ar' as a fallback
        error_message = str(e)
        if language == 'en' and (
            'No transcripts were found for any of the requested language codes' in error_message or
            'Could not retrieve a transcript' in error_message
        ):
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ar'])
                return "\n".join([entry['text'] for entry in transcript])
            except Exception as e2:
                return {"error": f"Transcript Error: {e2}"}
        return {"error": f"Transcript Error: {e}"}

@app.get("/youtube-info")
def youtube_info(video_id: str = Query(...), language: str = Query('en')):
    metadata = get_video_metadata_yt_dlp(video_id)
    transcript = get_transcript(video_id, language)
    return {"metadata": metadata, "transcript": transcript}

# Create the MCP server and mount it
mcp = FastApiMCP(
    app,
    name="YouTube Info MCP",
    description="Fetch YouTube video metadata and transcripts",
    # base_url="http://localhost:8000"  # Use your actual base URL if different
)
mcp.mount()
