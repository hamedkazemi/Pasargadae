from typing import Dict, Optional
from datetime import datetime
import asyncio
from ..models.download import Download

class Scheduler:
    def __init__(self, download_manager):
        self.download_manager = download_manager
        self.scheduled_downloads: Dict[str, Download] = {}
        self.schedule_tasks: Dict[str, asyncio.Task] = {}
    
    def schedule_download(self, download: Download):
        """Schedule a download for later."""
        if not download.scheduled_time:
            return
        
        self.scheduled_downloads[download.id] = download
        
        # Calculate delay until scheduled time
        now = datetime.now()
        delay = (download.scheduled_time - now).total_seconds()
        
        if delay > 0:
            # Create task to start download at scheduled time
            task = asyncio.create_task(self._schedule_task(download.id, delay))
            self.schedule_tasks[download.id] = task
    
    async def _schedule_task(self, download_id: str, delay: float):
        """Task that waits for scheduled time and starts download."""
        try:
            await asyncio.sleep(delay)
            
            # Start download if it still exists
            if download_id in self.scheduled_downloads:
                download = self.scheduled_downloads[download_id]
                await self.download_manager.start_download(download_id)
                
                # Cleanup
                del self.scheduled_downloads[download_id]
                del self.schedule_tasks[download_id]
                
        except asyncio.CancelledError:
            # Handle cancellation
            if download_id in self.scheduled_downloads:
                del self.scheduled_downloads[download_id]
            if download_id in self.schedule_tasks:
                del self.schedule_tasks[download_id]
    
    def cancel_scheduled_download(self, download_id: str):
        """Cancel a scheduled download."""
        if download_id in self.schedule_tasks:
            task = self.schedule_tasks[download_id]
            task.cancel()
            del self.schedule_tasks[download_id]
        
        if download_id in self.scheduled_downloads:
            del self.scheduled_downloads[download_id]
    
    def get_scheduled_downloads(self) -> Dict[str, Download]:
        """Get all scheduled downloads."""
        return self.scheduled_downloads.copy()
    
    def reschedule_download(self, download_id: str, new_time: datetime):
        """Reschedule a download for a different time."""
        if download_id not in self.scheduled_downloads:
            return
        
        # Cancel existing schedule
        self.cancel_scheduled_download(download_id)
        
        # Update scheduled time
        download = self.scheduled_downloads[download_id]
        download.scheduled_time = new_time
        
        # Create new schedule
        self.schedule_download(download)
