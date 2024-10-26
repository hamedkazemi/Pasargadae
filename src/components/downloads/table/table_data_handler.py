from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
from src.repositories.download_repository import DownloadRepository
from .row_checkbox import RowCheckBox
from .progress_bar import DownloadProgressBar
from .file_type_icon import FileTypeIcon

class SortableTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, sort_key=None):
        super().__init__(str(text) if text is not None else "")
        self._sort_key = sort_key if sort_key is not None else text
    
    def __lt__(self, other):
        if isinstance(other, SortableTableWidgetItem):
            return self._sort_key < other._sort_key
        return super().__lt__(other)

class TableDataHandler:
    def __init__(self):
        self.repository = DownloadRepository()
        self._all_downloads = []
    
    def load_data(self):
        self._all_downloads = self.repository.get_all()
        if not self._all_downloads:
            self.repository.add_sample_data()
            self._all_downloads = self.repository.get_all()
        return self._all_downloads
    
    def filter_downloads(self, search_text):
        """Filter downloads based on search text"""
        if not search_text:
            return self._all_downloads
        
        search_text = search_text.lower()
        return [
            download for download in self._all_downloads
            if self._matches_search(download, search_text)
        ]
    
    def _matches_search(self, download, search_text):
        """Check if download matches search text"""
        return search_text in download.name.lower()
    
    def create_table_items(self, download, is_dark):
        """Create table items for a download"""
        items = {}
        
        # Store download id
        id_item = QTableWidgetItem()
        id_item.setData(Qt.ItemDataRole.UserRole, download.id)
        items['id'] = id_item
        
        # Checkbox
        items['checkbox'] = RowCheckBox(is_dark)
        
        # File type icon
        items['icon'] = FileTypeIcon(download.file_type, is_dark)
        
        # Name
        items['name'] = SortableTableWidgetItem(download.name)
        
        # Size
        items['size'] = SortableTableWidgetItem(
            download.size, 
            self._parse_size(download.size)
        )
        
        # Status/Progress
        if download.progress > 0 and download.progress < 100:
            progress = DownloadProgressBar()
            progress.setValue(download.progress)
            items['status'] = progress
        else:
            items['status'] = SortableTableWidgetItem(download.status)
        
        # Time Left
        items['time_left'] = SortableTableWidgetItem(download.time_left)
        
        # Last Modified
        items['modified'] = SortableTableWidgetItem(download.last_modified)
        
        # Speed
        items['speed'] = SortableTableWidgetItem(
            download.speed, 
            self._parse_speed(download.speed)
        )
        
        return items
    
    def _parse_size(self, size_str):
        """Convert size string to bytes for proper sorting"""
        try:
            if not size_str:
                return 0
            number = float(''.join(filter(str.isdigit, size_str)))
            if 'GB' in size_str:
                return number * 1024 * 1024 * 1024
            elif 'MB' in size_str:
                return number * 1024 * 1024
            elif 'KB' in size_str:
                return number * 1024
            return number
        except:
            return 0
    
    def _parse_speed(self, speed_str):
        """Convert speed string to bytes/s for proper sorting"""
        try:
            if not speed_str:
                return 0
            number = float(''.join(filter(str.isdigit, speed_str)))
            if 'GB/s' in speed_str:
                return number * 1024 * 1024 * 1024
            elif 'MB/s' in speed_str:
                return number * 1024 * 1024
            elif 'KB/s' in speed_str:
                return number * 1024
            return number
        except:
            return 0
