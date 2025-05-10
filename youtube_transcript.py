from youtube_transcript_api import YouTubeTranscriptApi
import sys
import yt_dlp
import json

def get_best_thumbnail(thumbnails):
    # Prefer maxresdefault.jpg, then hqdefault.jpg, then the first available
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
        return {"error": f"Transcript Error: {e}"}

if __name__ == "__main__":
    # Example usage: python script.py VIDEO_ID [LANGUAGE]
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python script.py VIDEO_ID [LANGUAGE]"}))
        sys.exit(1)
    video_id = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'
    metadata = get_video_metadata_yt_dlp(video_id)
    transcript = get_transcript(video_id, language)
    output = {"metadata": metadata, "transcript": transcript}
    print(json.dumps(output, ensure_ascii=False, indent=2))