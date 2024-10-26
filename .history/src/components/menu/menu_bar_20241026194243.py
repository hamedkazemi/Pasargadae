from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtCore import Qt
from src.theme.styles import Styles

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = True
        self.setup_menus()
        self.apply_theme()  # Apply theme on initialization
    
    def setup_menus(self):
        # File menu
        file_menu = QMenu("File", self)
        file_menu.addAction("Add URL")
        file_menu.addAction("Add Batch URLs")
        file_menu.addSeparator()
        file_menu.addAction("Import")
        file_menu.addAction("Export")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        self.addMenu(file_menu)
        
        # Downloads menu
        downloads_menu = QMenu("Downloads", self)
        downloads_menu.addAction("Start All")
        downloads_menu.addAction("Pause All")
        downloads_menu.addAction("Stop All")
        downloads_menu.addSeparator()
        downloads_menu.addAction("Remove All")
        downloads_menu.addAction("Remove Completed")
        self.addMenu(downloads_menu)
        
        # View menu
        view_menu = QMenu("View", self)
        view_menu.addAction("Show Categories")
        view_menu.addAction("Show Toolbar")
        view_menu.addAction("Show Status Bar")
        self.addMenu(view_menu)
        
        # Help menu
        help_menu = QMenu("Help", self)
        help_menu.addAction("Documentation")
        help_menu.addAction("Check for Updates")
        help_menu.addSeparator()
        help_menu.addAction("About")
        self.addMenu(help_menu)
    
    def apply_theme(self):
        """Apply theme styles"""
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["MENU"])
        
        # Apply styles to submenus
        for action in self.actions():
            menu = action.menu()
            if menu:
                menu.setStyleSheet(styles["MENU"])
    
    def update_theme(self, is_dark):
        """Update theme for menu and all submenus"""
        self._is_dark = is_dark
        self.apply_theme()
