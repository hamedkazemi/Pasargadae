from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.components.downloads.download_table import DownloadTable
from src.components.downloads.search_bar import SearchContainer
from src.theme.styles import Styles

class DownloadPanel(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Add search bar
        self.search_bar = SearchContainer(self._is_dark)
        layout.addWidget(self.search_bar)
        
        # Add download table
        self.download_table = DownloadTable(self._is_dark)
        layout.addWidget(self.download_table)
        
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["WINDOW"])
    
    def update_theme(self, is_dark):
        """Update theme for all child widgets"""
        self._is_dark = is_dark
        self.search_bar.update_theme(is_dark)
        self.download_table.update_theme(is_dark)
        self.apply_theme()
