CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS downloads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    size TEXT NOT NULL,
    status TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    time_left TEXT,
    last_modified TEXT,
    speed TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
