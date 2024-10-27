from importlib import import_module
from pathlib import Path
import aiosqlite
import sqlite3
import os

class MigrationManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self):
        """Create migrations table if it doesn't exist."""
        # Use sqlite3 for sync initialization
        with sqlite3.connect(self.db_path) as db:
            db.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db.commit()
    
    async def get_applied_migrations(self) -> set:
        """Get list of applied migrations."""
        db = await aiosqlite.connect(self.db_path)
        try:
            async with db.execute("SELECT name FROM migrations") as cursor:
                rows = await cursor.fetchall()
                return {row[0] for row in rows}
        finally:
            await db.close()
    
    async def apply_migrations(self):
        """Apply all pending migrations."""
        # Get list of migration files
        migrations_dir = Path(__file__).parent
        migration_files = sorted([
            f for f in os.listdir(migrations_dir)
            if f.endswith('.py') and f != '__init__.py'
        ])
        
        # Get already applied migrations
        applied = await self.get_applied_migrations()
        
        db = await aiosqlite.connect(self.db_path)
        try:
            for file in migration_files:
                name = file[:-3]  # Remove .py extension
                if name not in applied:
                    # Import and run migration
                    module = import_module(f'.{name}', package='src.database.migrations')
                    await module.up(db)
                    
                    # Mark as applied
                    await db.execute(
                        "INSERT INTO migrations (name) VALUES (?)",
                        (name,)
                    )
                    await db.commit()
        finally:
            await db.close()
    
    async def revert_migration(self, name: str):
        """Revert a specific migration."""
        db = await aiosqlite.connect(self.db_path)
        try:
            # Import and run down migration
            module = import_module(f'.{name}', package='src.database.migrations')
            await module.down(db)
            
            # Remove from applied migrations
            await db.execute(
                "DELETE FROM migrations WHERE name = ?",
                (name,)
            )
            await db.commit()
        finally:
            await db.close()
