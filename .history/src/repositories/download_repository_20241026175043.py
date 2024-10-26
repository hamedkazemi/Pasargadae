from src.database.connection import DatabaseConnection
from src.models.download import Download

class DownloadRepository:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all(self):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM downloads ORDER BY created_at DESC")
            return [Download.from_db(row) for row in cursor.fetchall()]
    
    def add(self, download: Download):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO downloads (name, file_type, size, status, progress, 
                                    time_left, last_modified, speed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, download.to_db_tuple())
            conn.commit()
            return cursor.lastrowid
    
    def update(self, download: Download):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE downloads 
                SET name=?, file_type=?, size=?, status=?, progress=?,
                    time_left=?, last_modified=?, speed=?
                WHERE id=?
            """, download.to_db_tuple() + (download.id,))
            conn.commit()
    
    def delete(self, download_id: int):
        with self.db as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM downloads WHERE id=?", (download_id,))
            conn.commit()
    
    def add_sample_data(self):
        samples = [
            Download(
                name="UIUXMonster",
                file_type="image",
                size="745 KB",
                status="Complete",
                progress=100,
                time_left="0 Sec",
                last_modified="2023/08/09",
                speed="3MB/s"
            ),
            Download(
                name="2pacCover",
                file_type="music",
                size="3.00 MB",
                status="In Progress",
                progress=80,
                time_left="0 Sec",
                last_modified="2023/08/09",
                speed="2MB/s"
            ),
            Download(
                name="Document",
                file_type="document",
                size="2 MB",
                status="In Progress",
                progress=50,
                time_left="5 Min",
                last_modified="2023/08/09",
                speed="4MB/s"
            )
        ]
        
        for sample in samples:
            self.add(sample)
