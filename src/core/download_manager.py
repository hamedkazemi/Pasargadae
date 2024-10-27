from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
from datetime import datetime
import os
from .download_worker import DownloadWorker
from ..models.download import Download, DownloadStatus
from ..repositories.download_repository import DownloadRepository
from .queue_manager import QueueManager
from .scheduler import Scheduler
from src.utils.logger import Logger

class DownloadManager:
    def __init__(self, settings: dict):
        Logger.debug("Initializing DownloadManager")
        self.settings = settings
        self.downloads: Dict[str, Download] = {}
        self.workers: Dict[str, DownloadWorker] = {}
        self.repository = DownloadRepository()
        self.queue_manager = QueueManager(self)
        self.scheduler = Scheduler(self)
        
        # Load settings
        self.max_concurrent = settings["connection"]["max_active_downloads"]
        self.default_directory = settings["download"]["default_download_directory"]
        self.temp_directory = settings["download"]["temporary_folder"]
        
        # Create necessary directories
        os.makedirs(self.default_directory, exist_ok=True)
        os.makedirs(self.temp_directory, exist_ok=True)
        Logger.info(f"DownloadManager initialized with directories: default={self.default_directory}, temp={self.temp_directory}")
    
    async def add_download(self, url: str, save_path: Optional[str] = None, 
                         queue: str = "regular") -> Download:
        """Add a new download to the queue."""
        Logger.info(f"Adding new download: url={url}, save_path={save_path}, queue={queue}")
        # Use default directory if save_path not provided
        if not save_path:
            filename = url.split('/')[-1]
            save_path = os.path.join(self.default_directory, filename)
            Logger.debug(f"Using default save path: {save_path}")
        
        # Create download object
        download = Download(
            url=url,
            save_path=save_path,
            status=DownloadStatus.QUEUED,
            queue=queue,
            created_at=datetime.now()
        )
        
        # Save to database
        download_id = await self.repository.add(download)
        download.id = download_id
        Logger.debug(f"Download saved to database with ID: {download_id}")
        
        # Add to queue
        self.queue_manager.add_to_queue(download, queue)
        Logger.debug(f"Download added to queue: {queue}")
        
        # Store in memory
        self.downloads[download_id] = download
        
        return download
    
    async def start_download(self, download_id: str):
        """Start a specific download."""
        Logger.info(f"Starting download: {download_id}")
        if download_id in self.workers:
            Logger.debug(f"Download {download_id} already has a worker")
            return
        
        download = self.downloads[download_id]
        if len(self.workers) >= self.max_concurrent:
            download.status = DownloadStatus.QUEUED
            await self.repository.update(download)
            Logger.debug(f"Download {download_id} queued (max concurrent reached)")
            return
        
        # Create worker with current settings
        worker = DownloadWorker(download, self.settings)
        self.workers[download_id] = worker
        Logger.debug(f"Created worker for download {download_id}")
        
        # Start download with progress callback
        download.status = DownloadStatus.DOWNLOADING
        await self.repository.update(download)
        
        asyncio.create_task(worker.start(
            progress_callback=lambda p: self._handle_progress(download_id, p)
        ))
        Logger.info(f"Download {download_id} started")
    
    async def pause_download(self, download_id: str):
        """Pause a specific download."""
        Logger.info(f"Pausing download: {download_id}")
        if download_id not in self.workers:
            return
        
        worker = self.workers[download_id]
        await worker.pause()
        
        download = self.downloads[download_id]
        download.status = DownloadStatus.PAUSED
        await self.repository.update(download)
        Logger.debug(f"Download {download_id} paused")
    
    async def resume_download(self, download_id: str):
        """Resume a paused download."""
        Logger.info(f"Resuming download: {download_id}")
        if download_id not in self.workers:
            await self.start_download(download_id)
            return
        
        worker = self.workers[download_id]
        await worker.resume()
        
        download = self.downloads[download_id]
        download.status = DownloadStatus.DOWNLOADING
        await self.repository.update(download)
        Logger.debug(f"Download {download_id} resumed")
    
    async def cancel_download(self, download_id: str):
        """Cancel and remove a download."""
        Logger.info(f"Canceling download: {download_id}")
        if download_id in self.workers:
            worker = self.workers[download_id]
            await worker.stop()
            del self.workers[download_id]
            Logger.debug(f"Stopped worker for download {download_id}")
        
        if download_id in self.downloads:
            await self.repository.delete(download_id)
            del self.downloads[download_id]
            Logger.debug(f"Deleted download {download_id}")
    
    async def schedule_download(self, url: str, save_path: str, 
                              schedule_time: datetime) -> Download:
        """Schedule a download for later."""
        Logger.info(f"Scheduling download: url={url}, save_path={save_path}, time={schedule_time}")
        download = Download(
            url=url,
            save_path=save_path,
            status=DownloadStatus.SCHEDULED,
            scheduled_time=schedule_time,
            created_at=datetime.now()
        )
        
        # Save to database
        download_id = await self.repository.add(download)
        download.id = download_id
        Logger.debug(f"Scheduled download saved to database with ID: {download_id}")
        
        # Store in memory
        self.downloads[download_id] = download
        
        # Add to scheduler
        self.scheduler.schedule_download(download)
        Logger.debug(f"Download {download_id} added to scheduler")
        
        return download
    
    async def _handle_progress(self, download_id: str, progress: dict):
        """Handle progress updates from workers."""
        if download_id not in self.downloads:
            return
        
        download = self.downloads[download_id]
        download.progress = progress["downloaded"] / progress["total"] * 100
        download.speed = progress["speed"]
        download.downloaded_size = progress["downloaded"]
        download.total_size = progress["total"]
        
        # Update in database
        await self.repository.update(download)
        Logger.debug(f"Updated progress for download {download_id}: {download.progress:.1f}%")
        
        # Log event
        await self.repository.add_event(
            download_id,
            "progress_update",
            progress
        )
    
    async def load_downloads(self):
        """Load all downloads from database."""
        Logger.info("Loading downloads from database")
        downloads = await self.repository.get_all()
        for download in downloads:
            self.downloads[download.id] = download
            
            # Resume active downloads
            if download.status == DownloadStatus.DOWNLOADING:
                await self.start_download(download.id)
                Logger.debug(f"Resumed active download: {download.id}")
            # Add queued downloads back to queue
            elif download.status == DownloadStatus.QUEUED:
                self.queue_manager.add_to_queue(download, download.queue)
                Logger.debug(f"Re-queued download: {download.id}")
            # Re-schedule scheduled downloads
            elif download.status == DownloadStatus.SCHEDULED:
                self.scheduler.schedule_download(download)
                Logger.debug(f"Re-scheduled download: {download.id}")
        Logger.info(f"Loaded {len(downloads)} downloads")
