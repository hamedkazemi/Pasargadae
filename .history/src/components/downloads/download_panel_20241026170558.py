from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .download_table import DownloadTable
from .search_bar import SearchBar
from src.components.status.speed_test import SpeedTestWidget

class DownloadPanel(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_bar = SearchBar()
        self.download_table = DownloadTable()
        self.speed_test = SpeedTestWidget(self._is_dark)
        
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.download_table)
        self.layout.addWidget(self.speed_test)
    
    def apply_theme(self, styles, is_dark):
        self._is_dark = is_dark
        self.search_bar.setStyleSheet(styles["SEARCH"])
        self.download_table.setStyleSheet(styles["TABLE"])
        
        # Update speed test widget
        self.speed_test.setParent(None)
        self.speed_test = SpeedTestWidget(self._is_dark)
        self.layout.addWidget(self.speed_test)
