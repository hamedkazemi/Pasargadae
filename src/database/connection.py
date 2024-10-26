import sqlite3
from pathlib import Path
from .schema import CREATE_TABLES

class DatabaseConnection:
    def __init__(self, db_path="downloads.db"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        if not Path(self.db_path).exists():
            self.create_tables()
    
    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(CREATE_TABLES)
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def __enter__(self):
        self.conn = self.get_connection()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
