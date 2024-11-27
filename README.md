# YouTube Mix Downloader

A Python library for downloading videos from YouTube Mix playlists.

## Requirements

### Python Dependencies
```bash
pip install selenium>=4.0.0 webdriver-manager>=3.8.0 yt-dlp>=2023.0.0
```

### System Requirements

#### FFmpeg Installation

**Windows:**
```bash
winget install FFmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### Browser Requirements
- Google Chrome or Chromium browser
- ChromeDriver (automatically installed by webdriver-manager)

### Development Requirements
```bash
pip install build twine pytest black isort mypy
```

## Installation

```bash
pip install youtube_mix_dl
```

## Usage

```python
from youtube_mix_dl import YoutubeMixDownloader

# Initialize the downloader
downloader = YoutubeMixDownloader(output_path="downloads")

# Define a progress callback (optional)
def progress_callback(message):
    print(message)

# Create downloader with callback
downloader = YoutubeMixDownloader(
    output_path="downloads",
    progress_callback=progress_callback
)

# Download a mix
mix_url = "https://www.youtube.com/watch?v=..."
num_videos = 25
successful_downloads = downloader.download_mix(mix_url, num_videos)

print(f"Downloaded {successful_downloads} videos successfully")
```

## Features

- Download videos from YouTube Mix playlists
- Clean YouTube URLs automatically
- Progress tracking and callbacks
- High-quality video and audio
- Automatic merging of video and audio streams
- Error handling and retry mechanism

## Troubleshooting

### Common Issues

1. **No Sound in Downloaded Videos**
   - Make sure FFmpeg is properly installed
   - Check if FFmpeg is in your system PATH

2. **ChromeDriver Issues**
   - Ensure Chrome/Chromium is installed
   - Update Chrome to the latest version
   - Let webdriver-manager handle ChromeDriver installation

3. **Permission Issues**
   - On Linux/macOS, ensure proper permissions for the output directory
   - Run with appropriate user privileges

### Checking Dependencies

Verify FFmpeg installation:
```bash
ffmpeg -version
```

Verify Chrome installation:
```bash
google-chrome --version  # Linux
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version  # macOS
reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version  # Windows
```

## Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/youtube_mix_dl.git
cd youtube_mix_dl
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install development dependencies
```bash
pip install build twine pytest black isort mypy
```

4. Install the package in editable mode
```bash
pip install -e .
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black . && isort .`
6. Submit a pull request

## License

MIT License