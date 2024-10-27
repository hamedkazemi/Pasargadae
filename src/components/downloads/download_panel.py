from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .download_table import DownloadTableWidget
from .search_bar import SearchBar

class DownloadPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Search bar
        self.search_bar = SearchBar()
        layout.addWidget(self.search_bar)
        
        # Download table
        self.download_table = DownloadTableWidget()
        layout.addWidget(self.download_table)
        
        # Connect signals
        #self.search_bar.searchTextChanged.connect(self.filter_downloads)
    
    def filter_downloads(self, search_text: str):
        """Filter downloads based on search text."""
        for row in range(self.download_table.rowCount()):
            item = self.download_table.item(row, 0)  # Name column
            should_show = not search_text or search_text.lower() in item.text().lower()
            self.download_table.setRowHidden(row, not should_show)
    
    def add_download(self, download):
        """Add a new download to the table."""
        self.download_table.add_download(download)
    
    def update_download(self, download):
        """Update an existing download in the table."""
        self.download_table.update_download(download)
    
    def remove_download(self, download_id: str):
        """Remove a download from the table."""
        self.download_table.remove_download(download_id)
        
        
    def update_theme(is_dark):
        print("theme should update here")    
