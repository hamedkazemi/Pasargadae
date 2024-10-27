from typing import Dict, List, Optional
from collections import defaultdict
from ..models.download import Download

class QueueManager:
    def __init__(self, download_manager):
        self.download_manager = download_manager
        self.queues = defaultdict(list)  # Queue name -> List[Download]
    
    def add_to_queue(self, download: Download, queue_name: str = "regular"):
        """Add a download to a specific queue."""
        self.queues[queue_name].append(download)
    
    async def process_queue(self):
        """Process downloads in queues based on priority."""
        # First try high priority queue
        if await self._process_queue_items("high_priority"):
            return
        
        # Then try regular queue
        await self._process_queue_items("regular")
    
    async def _process_queue_items(self, queue_name: str) -> bool:
        """Process items in a specific queue. Returns True if started a download."""
        queue = self.queues.get(queue_name, [])
        if not queue:
            return False
        
        # Check if we can start more downloads
        active_count = len(self.download_manager.active_downloads)
        if active_count >= self.download_manager.max_concurrent:
            return False
        
        # Get next download from queue
        download = queue[0]
        queue.pop(0)
        
        # Start the download
        await self.download_manager.start_download(download.id)
        return True
    
    def get_queue_status(self, queue_name: str) -> dict:
        """Get status information about a queue."""
        queue = self.queues.get(queue_name, [])
        return {
            "name": queue_name,
            "count": len(queue),
            "active": sum(1 for d in queue if d.status == "downloading"),
            "waiting": sum(1 for d in queue if d.status == "queued")
        }
    
    def reorder_queue(self, queue_name: str, download_id: str, new_position: int):
        """Move a download to a new position in its queue."""
        queue = self.queues.get(queue_name, [])
        if not queue:
            return
        
        # Find download in queue
        download_index = next(
            (i for i, d in enumerate(queue) if d.id == download_id), 
            None
        )
        if download_index is None:
            return
        
        # Move download to new position
        download = queue.pop(download_index)
        queue.insert(min(new_position, len(queue)), download)
    
    def move_to_queue(self, download_id: str, from_queue: str, to_queue: str):
        """Move a download from one queue to another."""
        from_queue_list = self.queues.get(from_queue, [])
        if not from_queue_list:
            return
        
        # Find and remove download from old queue
        download = next(
            (d for d in from_queue_list if d.id == download_id),
            None
        )
        if download is None:
            return
        
        from_queue_list.remove(download)
        
        # Add to new queue
        self.add_to_queue(download, to_queue)
