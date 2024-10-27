import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from src.components.main_window import MainWindow
from src.database.migrations import MigrationManager
import asyncio

async def init_database():
    """Initialize database with migrations."""
    migration_manager = MigrationManager("downloads.db")
    await migration_manager.apply_migrations()

def main():
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Run database migrations
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(init_database())
    finally:
        loop.close()
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
