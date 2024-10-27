"""Initial settings schema migration"""

CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)"""

CREATE_SETTINGS_INDEXES = [
    """CREATE INDEX IF NOT EXISTS idx_settings_category 
       ON settings(category)"""
]

async def up(db):
    """Apply the migration."""
    # First create table
    await db.execute(CREATE_SETTINGS_TABLE)
    await db.commit()
    
    # Then create indexes
    for index in CREATE_SETTINGS_INDEXES:
        await db.execute(index)
        await db.commit()

async def down(db):
    """Revert the migration."""
    await db.execute("DROP TABLE IF EXISTS settings")
    await db.commit()
