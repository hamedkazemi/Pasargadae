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
    
    -- Additional metadata
    filename TEXT,
    mime_type TEXT,
    category TEXT,
    
    -- Settings used for this download
    chunks INTEGER,
    speed_limit INTEGER,
    verify_hash BOOLEAN,
    hash_algorithm TEXT,
    resume_support BOOLEAN,
    
    -- Post-processing
    post_process_command TEXT,
    post_process_status TEXT,
    
    -- Security
    virus_scanned BOOLEAN DEFAULT FALSE,
    virus_scan_result TEXT,
    
    -- Integrity
    integrity_checked BOOLEAN DEFAULT FALSE,
    integrity_result TEXT,
    
    -- Browser info
    referrer TEXT,
    user_agent TEXT,
    
    -- Queue info
    queue_position INTEGER,
    priority INTEGER DEFAULT 0
);

-- Index for faster queue processing
CREATE INDEX IF NOT EXISTS idx_downloads_queue 
ON downloads(queue, status, priority);

-- Index for status filtering
CREATE INDEX IF NOT EXISTS idx_downloads_status
ON downloads(status);

-- Index for scheduled downloads
CREATE INDEX IF NOT EXISTS idx_downloads_scheduled
ON downloads(scheduled_time)
WHERE scheduled_time IS NOT NULL;
"""

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
);

-- Index for faster part lookup
CREATE INDEX IF NOT EXISTS idx_download_parts
ON download_parts(download_id, part_number);
"""

CREATE_DOWNLOAD_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS download_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    download_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_data TEXT,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (download_id) REFERENCES downloads(id)
);

-- Index for event lookup
CREATE INDEX IF NOT EXISTS idx_download_events
ON download_events(download_id, created_at);
"""
