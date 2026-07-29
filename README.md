# FLA Downloader

A modern YouTube video and playlist downloader with a dark-themed GUI built with Python, tkinter, and yt-dlp.

## Features

- Download videos from YouTube
- Download entire playlists
- Multiple quality options: 4K, 1080p, 720p, 480p, 360p, or best available
- Multiple formats: MP4, MP3 (audio only), WEBM, MKV
- Custom destination folder selection
- Progress tracking with speed and ETA
- Modern dark theme UI

## Requirements

- Python 3.7+
- yt-dlp
- ffmpeg (required for merging video/audio or converting to MP3)

## Installation

1. Install Python from [python.org](https://www.python.org/)

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Install ffmpeg (required for video processing):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or via chocolatey: `choco install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or your distro's package manager

## Usage

Run the application:
```bash
python youtube-downloader/youtube_downloader.py
```

Or simply double-click the file if Python is associated with .py files.

## License

For personal use only.

