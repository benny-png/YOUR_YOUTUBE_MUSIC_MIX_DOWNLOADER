from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import yt_dlp
from typing import List, Optional, Callable
from .utils import clean_youtube_url

class YoutubeMixDownloader:
    """A class to download videos from YouTube Mix playlists"""
    
    def __init__(self, output_path: str = "downloads", progress_callback: Optional[Callable] = None):
        """
        Initialize the YouTube Mix Downloader
        
        Args:
            output_path (str): Directory to save downloaded videos
            progress_callback (callable): Optional callback for progress updates
        """
        self.output_path = output_path
        self.progress_callback = progress_callback
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Chrome webdriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def get_mix_videos(self, mix_url: str, num_videos: int = 25) -> List[str]:
        """
        Extract video URLs from YouTube Mix
        
        Args:
            mix_url (str): URL of the YouTube Mix
            num_videos (int): Number of videos to extract
            
        Returns:
            List[str]: List of video URLs
        """
        driver = self._setup_driver()
        video_urls = []
        
        try:
            if self.progress_callback:
                self.progress_callback("Loading playlist page...")
            driver.get(mix_url)
            time.sleep(3)
            
            while len(video_urls) < num_videos:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(2)
                
                items = driver.find_elements(By.CSS_SELECTOR, 
                    "a.yt-simple-endpoint.style-scope.ytd-playlist-panel-video-renderer")
                
                for item in items:
                    href = item.get_attribute("href")
                    if href and "watch?v=" in href:
                        clean_url = clean_youtube_url(href)
                        if clean_url not in video_urls:
                            video_urls.append(clean_url)
                
                video_urls = list(dict.fromkeys(video_urls))
                if self.progress_callback:
                    self.progress_callback(f"Found {len(video_urls)} videos...")
                
                if len(video_urls) >= num_videos:
                    break
                    
        finally:
            driver.quit()
        
        return video_urls[:num_videos]
    
    def download_video(self, url: str) -> bool:
        """
        Download a single video
        
        Args:
            url (str): Video URL to download
            
        Returns:
            bool: True if download was successful
        """
        try:
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(self.output_path, '%(title)s.%(ext)s'),
                'ignoreerrors': True,
                'no_warnings': False,
                'quiet': False,
                'progress': True,
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }
            
            if self.progress_callback:
                ydl_opts['progress_hooks'] = [
                    lambda d: self.progress_callback(
                        f"Downloading: {d.get('_percent_str', '0%')} of {d.get('_total_bytes_str', 'Unknown')}"
                    ) if d['status'] == 'downloading' else None
                ]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if info:
                    if self.progress_callback:
                        self.progress_callback(f"Successfully downloaded: {info.get('title', 'Unknown title')}")
                    return True
                return False

        except Exception as e:
            if self.progress_callback:
                self.progress_callback(f"Error downloading video: {str(e)}")
            return False
    
    def download_mix(self, mix_url: str, num_videos: int = 25) -> int:
        """
        Download videos from a YouTube Mix playlist
        
        Args:
            mix_url (str): URL of the YouTube Mix
            num_videos (int): Number of videos to download
            
        Returns:
            int: Number of successfully downloaded videos
        """
        if self.progress_callback:
            self.progress_callback("Starting YouTube Mix downloader...")
            
        video_urls = self.get_mix_videos(mix_url, num_videos)
        successful_downloads = 0
        
        for index, video_url in enumerate(video_urls, 1):
            if self.progress_callback:
                self.progress_callback(f"[{index}/{len(video_urls)}] Processing video...")
            if self.download_video(video_url):
                successful_downloads += 1
            time.sleep(1)
        
        if self.progress_callback:
            self.progress_callback(f"Download complete! Successfully downloaded {successful_downloads} videos.")
            
        return successful_downloads