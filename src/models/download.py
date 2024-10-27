from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class DownloadStatus(Enum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"
    SCHEDULED = "scheduled"

@dataclass
class Download:
    url: str
    save_path: str
    status: DownloadStatus = DownloadStatus.QUEUED
    progress: float = 0.0
    speed: float = 0.0
    downloaded_size: int = 0
    total_size: Optional[int] = None
    queue: str = "regular"
    error: Optional[str] = None
    expected_hash: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
    id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert download to dictionary for storage."""
        return {
            "id": self.id,
            "url": self.url,
            "save_path": self.save_path,
            "status": self.status.value,
            "progress": self.progress,
            "speed": self.speed,
            "downloaded_size": self.downloaded_size,
            "total_size": self.total_size,
            "queue": self.queue,
            "error": self.error,
            "expected_hash": self.expected_hash,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Download':
        """Create download from dictionary."""
        # Convert string status to enum
        status = DownloadStatus(data["status"])
        
        # Convert ISO format strings to datetime
        created_at = datetime.fromisoformat(data["created_at"])
        completed_at = datetime.fromisoformat(data["completed_at"]) if data["completed_at"] else None
        scheduled_time = datetime.fromisoformat(data["scheduled_time"]) if data["scheduled_time"] else None
        
        return cls(
            id=data["id"],
            url=data["url"],
            save_path=data["save_path"],
            status=status,
            progress=data["progress"],
            speed=data["speed"],
            downloaded_size=data["downloaded_size"],
            total_size=data["total_size"],
            queue=data["queue"],
            error=data["error"],
            expected_hash=data["expected_hash"],
            scheduled_time=scheduled_time,
            created_at=created_at,
            completed_at=completed_at
        )
