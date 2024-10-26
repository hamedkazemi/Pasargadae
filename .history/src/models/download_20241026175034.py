from dataclasses import dataclass
from datetime import datetime

@dataclass
class Download:
    id: int = None
    name: str = ""
    file_type: str = ""
    size: str = ""
    status: str = ""
    progress: int = 0
    time_left: str = ""
    last_modified: str = ""
    speed: str = ""
    created_at: datetime = None
    
    @staticmethod
    def from_db(row):
        return Download(
            id=row[0],
            name=row[1],
            file_type=row[2],
            size=row[3],
            status=row[4],
            progress=row[5],
            time_left=row[6],
            last_modified=row[7],
            speed=row[8],
            created_at=datetime.fromisoformat(row[9]) if row[9] else None
        )
    
    def to_db_tuple(self):
        return (
            self.name,
            self.file_type,
            self.size,
            self.status,
            self.progress,
            self.time_left,
            self.last_modified,
            self.speed
        )
