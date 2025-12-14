from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI(title="YouTube Downloader API")

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/youtube")
def youtube(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL required")

    ydl_opts = {
        "quiet": True,
        "skip_download": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    mp4, mp3 = [], []

    for f in info.get("formats", []):
        if f.get("ext") == "mp4" and f.get("vcodec") != "none":
            mp4.append({
                "quality": f.get("format_note"),
                "resolution": f.get("resolution"),
                "size": f.get("filesize"),
                "url": f.get("url")
            })

        if f.get("vcodec") == "none" and f.get("acodec") != "none":
            mp3.append({
                "abr": f.get("abr"),
                "size": f.get("filesize"),
                "url": f.get("url")
            })

    return {
        "status": "success",
        "video": {
            "title": info.get("title"),
            "duration": info.get("duration"),
            "views": info.get("view_count"),
            "channel": info.get("uploader"),
            "thumbnail": info.get("thumbnail")
        },
        "mp4": mp4[:5],
        "mp3": mp3[:5]
  }
