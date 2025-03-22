import subprocess
import os
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Use /tmp for downloads (Render allows this)
DOWNLOAD_FOLDER = "/tmp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.get("/download")
def download_video(url: str, format: str = Query("mp4", enum=["mp3", "mp4"])):
    output_path = f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s"
    
    command = ["yt-dlp", "-o", output_path, url]

    if format == "mp3":
        command.extend(["-f", "bestaudio", "--extract-audio", "--audio-format", "mp3"])
    else:
        command.extend(["-f", "bestvideo+bestaudio/best"])
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return {"status": "success", "message": "Download completed!", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

@app.get("/")
def root():
    return {"message": "YouTube Downloader Backend is Running!"}
