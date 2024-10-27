from typing import Optional, Callable, Dict, Any
import asyncio
from datetime import datetime
import os
from pySmartDL import SmartDL
from functools import partial
import hashlib
from ..models.download import Download, DownloadStatus
from src.utils.logger import Logger

class DownloadWorker:
    def __init__(self, download: Download, settings: dict):
        Logger.debug(f"Initializing DownloadWorker for download {download.id}")
        self.download = download
        self.settings = settings
        self.obj: Optional[SmartDL] = None
        self.progress_callback: Optional[Callable] = None
        self._stop_event = asyncio.Event()
        self._paused = False
        
        # Get settings
        self.chunk_size = settings["advanced_download"].get("chunk_count", 4)
        self.verify_hash = settings["integrity_checking"].get("hash_verification", True)
        self.hash_algo = settings["integrity_checking"].get("checksum_algorithm", "MD5")
        self.timeout = settings["advanced_download"].get("timeout_seconds", 30)
        
        # Speed limit from settings
        speed_limit = settings["speed_limiter"].get("max_speed", "500 KB/s")
        try:
            self.speed_limit = int(speed_limit.split()[0]) * 1024  # Convert KB/s to B/s
        except (ValueError, IndexError):
            self.speed_limit = 500 * 1024  # Default to 500 KB/s
        
        Logger.debug(f"Worker initialized with settings: chunks={self.chunk_size}, "
                    f"verify_hash={self.verify_hash}, timeout={self.timeout}, "
                    f"speed_limit={self.speed_limit}")
    
    async def start(self, progress_callback: Optional[Callable] = None):
        """Start the download."""
        Logger.info(f"Starting download {self.download.id}: {self.download.url}")
        self.progress_callback = progress_callback
        self._stop_event.clear()
        self._paused = False
        
        try:
            # Create download directory if it doesn't exist
            os.makedirs(os.path.dirname(self.download.save_path), exist_ok=True)
            Logger.debug(f"Created directory: {os.path.dirname(self.download.save_path)}")
            
            # Initialize SmartDL
            self.obj = SmartDL(
                self.download.url,
                self.download.save_path,
                progress_bar=False,  # We'll handle progress ourselves
                fix_urls=True,
                threads=self.chunk_size,
                timeout=self.timeout
            )
            
            # Set speed limit if enabled
            if self.settings["speed_limiter"]["enabled"]:
                self.obj.limit_speed = self.speed_limit
                Logger.debug(f"Speed limit set to {self.speed_limit} B/s")
            
            # Start download in thread pool
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self._download_with_progress
            )
            
            # Verify hash if enabled
            if self.verify_hash and self.download.expected_hash:
                Logger.debug("Verifying file hash")
                if not await self._verify_hash():
                    self.download.status = DownloadStatus.ERROR
                    self.download.error = "Hash verification failed"
                    Logger.error("Hash verification failed")
                    return
                Logger.debug("Hash verification successful")
            
            self.download.status = DownloadStatus.COMPLETED
            self.download.completed_at = datetime.now()
            Logger.info(f"Download {self.download.id} completed successfully")
            
        except Exception as e:
            self.download.status = DownloadStatus.ERROR
            self.download.error = str(e)
            Logger.error(f"Download {self.download.id} failed: {str(e)}")
    
    def _download_with_progress(self):
        """Run the download with progress updates."""
        Logger.debug(f"Starting download process for {self.download.id}")
        self.obj.start(blocking=False)
        
        while not self.obj.isFinished():
            if self._stop_event.is_set():
                self.obj.pause()
                Logger.debug(f"Download {self.download.id} stopped")
                break
            
            if self._paused:
                if not self.obj.isPaused():
                    self.obj.pause()
                    Logger.debug(f"Download {self.download.id} paused")
                continue
            elif self.obj.isPaused():
                self.obj.unpause()
                Logger.debug(f"Download {self.download.id} unpaused")
            
            if self.progress_callback:
                progress = {
                    "downloaded": self.obj.get_dl_size(),
                    "total": self.obj.get_final_filesize(),
                    "speed": self.obj.get_speed(),
                    "eta": self.obj.get_eta()
                }
                Logger.debug(f"Download {self.download.id} progress: "
                           f"{progress['downloaded']}/{progress['total']} bytes, "
                           f"speed: {progress['speed']} B/s")
                asyncio.run_coroutine_threadsafe(
                    self.progress_callback(progress),
                    asyncio.get_event_loop()
                )
            
            # Sleep briefly to avoid high CPU usage
            asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))
    
    async def pause(self):
        """Pause the download."""
        Logger.info(f"Pausing download {self.download.id}")
        self._paused = True
        self.download.status = DownloadStatus.PAUSED
    
    async def resume(self):
        """Resume the download."""
        Logger.info(f"Resuming download {self.download.id}")
        self._paused = False
        self.download.status = DownloadStatus.DOWNLOADING
    
    async def stop(self):
        """Stop the download."""
        Logger.info(f"Stopping download {self.download.id}")
        self._stop_event.set()
        if self.obj:
            # Run stop in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.obj.stop
            )
    
    async def _verify_hash(self) -> bool:
        """Verify the downloaded file's hash."""
        Logger.debug(f"Verifying hash for download {self.download.id}")
        if not os.path.exists(self.download.save_path):
            Logger.error(f"File not found: {self.download.save_path}")
            return False
        
        # Get hash algorithm
        hash_func = getattr(hashlib, self.hash_algo.lower(), None)
        if not hash_func:
            Logger.error(f"Unsupported hash algorithm: {self.hash_algo}")
            return False
        
        # Calculate file hash
        hasher = hash_func()
        with open(self.download.save_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        calculated_hash = hasher.hexdigest()
        Logger.debug(f"Calculated hash: {calculated_hash}")
        Logger.debug(f"Expected hash: {self.download.expected_hash}")
        return calculated_hash.lower() == self.download.expected_hash.lower()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current download status."""
        if not self.obj:
            return {
                "status": self.download.status,
                "progress": 0,
                "speed": 0,
                "eta": 0
            }
        
        status = {
            "status": self.download.status,
            "progress": self.obj.get_progress() * 100,
            "speed": self.obj.get_speed(),
            "eta": self.obj.get_eta()
        }
        Logger.debug(f"Download {self.download.id} status: {status}")
        return status
