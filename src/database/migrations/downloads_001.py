"""Initial downloads schema migration"""

CREATE_DOWNLOADS_TABLE = """
CREATE TABLE IF NOT EXISTS downloads (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    save_path TEXT NOT NULL,
    status TEXT NOT NULL,
    progress REAL DEFAULT 0.0,
    speed REAL DEFAULT 0.0,
    downloaded_size INTEGER DEFAULT 0,
    total_size INTEGER,
    queue TEXT DEFAULT 'regular',
    error TEXT,
    expected_hash TEXT,
    scheduled_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    filename TEXT,
    mime_type TEXT,
    category TEXT,
    chunks INTEGER,
    speed_limit INTEGER,
    verify_hash BOOLEAN,
    hash_algorithm TEXT,
    resume_support BOOLEAN,
    post_process_command TEXT,
    post_process_status TEXT,
    virus_scanned BOOLEAN DEFAULT FALSE,
    virus_scan_result TEXT,
    integrity_checked BOOLEAN DEFAULT FALSE,
    integrity_result TEXT,
    referrer TEXT,
    user_agent TEXT,
    queue_position INTEGER,
    priority INTEGER DEFAULT 0
)"""

CREATE_DOWNLOAD_PARTS_TABLE = """
CREATE TABLE IF NOT EXISTS download_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    download_id TEXT NOT NULL,
    part_number INTEGER NOT NULL,
    start_byte INTEGER NOT NULL,
    end_byte INTEGER NOT NULL,
    downloaded_size INTEGER DEFAULT 0,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    FOREIGN KEY (download_id) REFERENCES downloads(id)
)"""

CREATE_DOWNLOAD_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS download_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    download_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_data TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (download_id) REFERENCES downloads(id)
)"""

# Define indexes separately
DOWNLOADS_INDEXES = [
    """CREATE INDEX IF NOT EXISTS idx_downloads_queue 
       ON downloads(queue, status, priority)""",
    """CREATE INDEX IF NOT EXISTS idx_downloads_status
       ON downloads(status)""",
    """CREATE INDEX IF NOT EXISTS idx_downloads_scheduled
       ON downloads(scheduled_time)
       WHERE scheduled_time IS NOT NULL"""
]

DOWNLOAD_PARTS_INDEXES = [
    """CREATE INDEX IF NOT EXISTS idx_download_parts
       ON download_parts(download_id, part_number)"""
]

DOWNLOAD_EVENTS_INDEXES = [
    """CREATE INDEX IF NOT EXISTS idx_download_events
       ON download_events(download_id, created_at)"""
]

async def up(db):
    """Apply the migration."""
    # First create all tables
    await db.execute(CREATE_DOWNLOADS_TABLE)
    await db.commit()
    
    await db.execute(CREATE_DOWNLOAD_PARTS_TABLE)
    await db.commit()
    
    await db.execute(CREATE_DOWNLOAD_EVENTS_TABLE)
    await db.commit()
    
    # Then create all indexes
    for index in DOWNLOADS_INDEXES:
        await db.execute(index)
        await db.commit()
    
    for index in DOWNLOAD_PARTS_INDEXES:
        await db.execute(index)
        await db.commit()
    
    for index in DOWNLOAD_EVENTS_INDEXES:
        await db.execute(index)
        await db.commit()

async def down(db):
    """Revert the migration."""
    await db.execute("DROP TABLE IF EXISTS download_events")
    await db.commit()
    
    await db.execute("DROP TABLE IF EXISTS download_parts")
    await db.commit()
    
    await db.execute("DROP TABLE IF EXISTS downloads")
    await db.commit()
