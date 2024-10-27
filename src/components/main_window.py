from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from qframelesswindow import FramelessMainWindow, StandardTitleBar
from src.components.window.title_bar import TitleBar
from PyQt6.QtCore import Qt
from src.components.toolbar.action_toolbar import ActionToolbar
from src.components.downloads.download_table import DownloadTableWidget
from src.components.downloads.search_bar import SearchContainer
from src.components.navigation.navigation_panel import NavigationPanel
from src.theme.styles import Styles
from src.core.download_manager import DownloadManager
from src.settings.manager import SettingsManager
import os
from src.utils.logger import Logger

class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self._is_dark = True
        self.setWindowTitle("Pasargadae")
        self.setMinimumSize(1000, 600)
        
        # Initialize managers
        self.settings_manager = SettingsManager(
            os.path.join(os.path.expanduser("~"), ".pasargadae", "settings.json")
        )
        self.download_manager = DownloadManager(self.settings_manager.get_all_settings())
        Logger.debug("Managers initialized in MainWindow")
        
        # Create main container
        self.container = QWidget()
        self.container.setObjectName("centralWidget")

        self.setCentralWidget(self.container)  # FramelessWindow uses setWidget instead of setCentralWidget
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout for container
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Add custom title bar
        self.title_bar = TitleBar(self)
        self.setTitleBar(self.title_bar)  # Set custom title bar
        self.title_bar.theme_changed.connect(self.on_theme_changed)

        # Add toolbar
        self.toolbar = ActionToolbar(self._is_dark)
        
        # Create main content layout
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(10)
        
        # Add navigation panel
        self.navigation_panel = NavigationPanel(self._is_dark)
        content_layout.addWidget(self.navigation_panel)
        
        # Create downloads area
        downloads_container = QWidget()
        downloads_layout = QVBoxLayout(downloads_container)
        downloads_layout.setContentsMargins(0, 0, 0, 0)
        downloads_layout.setSpacing(10)
        
        # Add search bar
        self.search_bar = SearchContainer(self._is_dark)
        downloads_layout.addWidget(self.search_bar)
        
        # Add download table
        self.download_table = DownloadTableWidget()
        downloads_layout.addWidget(self.download_table)
        
        content_layout.addWidget(downloads_container)
        
        # Add widgets to main layout
        layout.addWidget(self.title_bar)
        layout.addWidget(self.toolbar)
        layout.addLayout(content_layout)
        
        # Connect signals
        self.search_bar.searchTextChanged.connect(self.filter_downloads)
        
        # Apply theme
        self.apply_theme(self._is_dark)
    
    def filter_downloads(self, search_text: str):
        """Filter downloads based on search text."""
        for row in range(self.download_table.rowCount()):
            item = self.download_table.item(row, 0)  # Name column
            should_show = not search_text or search_text.lower() in item.text().lower()
            self.download_table.setRowHidden(row, not should_show)
    
    def on_theme_changed(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme(is_dark)
    
    def apply_theme(self, is_dark):
        styles = Styles.get_styles(is_dark)
        self.setStyleSheet(styles["WINDOW"])
        self.toolbar.update_theme(is_dark)
        self.navigation_panel.update_theme(is_dark)
        self.search_bar.update_theme(is_dark)
        self.download_table.update_theme(is_dark)
    
    def add_download(self, download):
        """Add a new download."""
        self.download_table.add_download(download)
    
    def update_download(self, download):
        """Update an existing download."""
        self.download_table.update_download(download)
    
    def remove_download(self, download_id: str):
        """Remove a download."""
        self.download_table.remove_download(download_id)
