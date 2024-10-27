import json
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import aiosqlite
from ..models.download import Download, DownloadStatus

class DownloadRepository:
    def __init__(self, db_path: str = "downloads.db"):
        self.db_path = db_path
    
    async def add(self, download: Download) -> str:
        """Add a new download to the database."""
        if not download.id:
            download.id = str(uuid.uuid4())
        
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO downloads (
                    id, url, save_path, status, progress, speed,
                    downloaded_size, total_size, queue, error,
                    expected_hash, scheduled_time, created_at,
                    completed_at, filename, category
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                download.id, download.url, download.save_path,
                download.status.value, download.progress, download.speed,
                download.downloaded_size, download.total_size,
                download.queue, download.error, download.expected_hash,
                download.scheduled_time, download.created_at,
                download.completed_at,
                download.url.split('/')[-1],  # filename
                None  # category
            ))
            await db.commit()
        
        return download.id
    
    async def update(self, download: Download):
        """Update an existing download."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE downloads SET
                    status = ?, progress = ?, speed = ?,
                    downloaded_size = ?, total_size = ?,
                    queue = ?, error = ?, completed_at = ?
                WHERE id = ?
            """, (
                download.status.value, download.progress, download.speed,
                download.downloaded_size, download.total_size,
                download.queue, download.error, download.completed_at,
                download.id
            ))
            await db.commit()
    
    async def get(self, download_id: str) -> Optional[Download]:
        """Get a download by ID."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT * FROM downloads WHERE id = ?",
                (download_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return self._row_to_download(row)
        return None
    
    async def get_all(self, status: Optional[DownloadStatus] = None) -> List[Download]:
        """Get all downloads, optionally filtered by status."""
        async with aiosqlite.connect(self.db_path) as db:
            if status:
                async with db.execute(
                    "SELECT * FROM downloads WHERE status = ? ORDER BY created_at DESC",
                    (status.value,)
                ) as cursor:
                    rows = await cursor.fetchall()
            else:
                async with db.execute(
                    "SELECT * FROM downloads ORDER BY created_at DESC"
                ) as cursor:
                    rows = await cursor.fetchall()
            
            return [self._row_to_download(row) for row in rows]
    
    async def get_queue(self, queue_name: str) -> List[Download]:
        """Get all downloads in a specific queue."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """
                SELECT * FROM downloads 
                WHERE queue = ? AND status IN ('queued', 'scheduled')
                ORDER BY priority DESC, created_at ASC
                """,
                (queue_name,)
            ) as cursor:
                rows = await cursor.fetchall()
            
            return [self._row_to_download(row) for row in rows]
    
    async def delete(self, download_id: str):
        """Delete a download and its related data."""
        async with aiosqlite.connect(self.db_path) as db:
            # Delete download parts
            await db.execute(
                "DELETE FROM download_parts WHERE download_id = ?",
                (download_id,)
            )
            
            # Delete download events
            await db.execute(
                "DELETE FROM download_events WHERE download_id = ?",
                (download_id,)
            )
            
            # Delete the download
            await db.execute(
                "DELETE FROM downloads WHERE id = ?",
                (download_id,)
            )
            
            await db.commit()
    
    async def add_event(self, download_id: str, event_type: str, 
                       event_data: Optional[Dict[str, Any]] = None):
        """Add an event for a download."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO download_events (
                    download_id, event_type, event_data, created_at
                ) VALUES (?, ?, ?, ?)
            """, (
                download_id,
                event_type,
                json.dumps(event_data) if event_data else None,
                datetime.now()
            ))
            await db.commit()
    
    async def get_events(self, download_id: str) -> List[Dict[str, Any]]:
        """Get all events for a download."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                """
                SELECT event_type, event_data, created_at 
                FROM download_events 
                WHERE download_id = ?
                ORDER BY created_at DESC
                """,
                (download_id,)
            ) as cursor:
                rows = await cursor.fetchall()
            
            return [{
                "type": row[0],
                "data": json.loads(row[1]) if row[1] else None,
                "created_at": datetime.fromisoformat(row[2])
            } for row in rows]
    
    def _row_to_download(self, row) -> Download:
        """Convert a database row to a Download object."""
        # Get column names from cursor description
        columns = [
            "id", "url", "save_path", "status", "progress", "speed",
            "downloaded_size", "total_size", "queue", "error",
            "expected_hash", "scheduled_time", "created_at",
            "completed_at", "filename", "category"
        ]
        
        # Create dict from row
        data = dict(zip(columns, row))
        
        # Convert timestamps
        for field in ["scheduled_time", "created_at", "completed_at"]:
            if data[field]:
                data[field] = datetime.fromisoformat(data[field])
        
        return Download.from_dict(data)
