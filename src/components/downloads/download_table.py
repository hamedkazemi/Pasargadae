from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt, pyqtSignal
from src.theme.styles import Styles
from .table.header_checkbox import HeaderCheckBox
from .table.row_checkbox import RowCheckBox
from .table.progress_bar import DownloadProgressBar
from .table.file_type_icon import FileTypeIcon
from .table.context_menu import DownloadContextMenu
from .table.header_context_menu import HeaderContextMenu
from src.repositories.download_repository import DownloadRepository

class SortableTableWidgetItem(QTableWidgetItem):
    def __init__(self, text, sort_key=None):
        super().__init__(text)
        self._sort_key = sort_key if sort_key is not None else text
    
    def __lt__(self, other):
        if isinstance(other, SortableTableWidgetItem):
            return self._sort_key < other._sort_key
        return super().__lt__(other)

class DownloadTable(QTableWidget):
    sortingChanged = pyqtSignal(int, Qt.SortOrder)  # column, order
    
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.repository = DownloadRepository()
        self.context_menu = DownloadContextMenu(self)
        self.header_context_menu = HeaderContextMenu(self)
        self.setup_ui()
        self.setup_context_menus()
        self.setup_sorting()
        self.load_data()
        self.connect_signals()
    
    def setup_ui(self):
        headers = ["", "", "Name", "Size", "Status", "Time Left", 
                  "Last Modified", "Speed"]
        
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # Customize header
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setDefaultSectionSize(150)
        header.setStretchLastSection(True)
        
        # Set column widths
        self.setColumnWidth(0, 40)  # Checkbox
        self.setColumnWidth(1, 30)  # Icon
        
        # Add header checkbox
        self.header_checkbox = HeaderCheckBox(self._is_dark)
        self.header_checkbox.stateChanged.connect(self.toggle_all_checkboxes)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setHorizontalHeaderWidget(0, self.header_checkbox)
        
        self.setStyleSheet(Styles.get_styles(self._is_dark)["TABLE"])
    
    def setup_sorting(self):
        header = self.horizontalHeader()
        header.setSortIndicatorShown(True)
        header.sectionClicked.connect(self.handle_sort)
        self.setSortingEnabled(True)
    
    def handle_sort(self, logical_index):
        if logical_index in [0, 1]:  # Skip checkbox and icon columns
            return
        
        header = self.horizontalHeader()
        current_order = header.sortIndicatorOrder()
        
        # Toggle sort order if clicking the same column
        if header.sortIndicatorSection() == logical_index:
            new_order = Qt.SortOrder.DescendingOrder if current_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
            header.setSortIndicator(logical_index, new_order)
        else:
            # First click on new column, start with ascending
            header.setSortIndicator(logical_index, Qt.SortOrder.AscendingOrder)
        
        self.sortItems(logical_index, header.sortIndicatorOrder())
    
    def setup_context_menus(self):
        # Download context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Header context menu
        header = self.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(self.show_header_context_menu)
    
    def show_context_menu(self, pos):
        row = self.rowAt(pos.y())
        if row >= 0:
            download_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
            self.context_menu.show_for_download(download_id, self.mapToGlobal(pos))
    
    def show_header_context_menu(self, pos):
        self.header_context_menu.show_menu(self.horizontalHeader().mapToGlobal(pos))
    
    def connect_signals(self):
        # Connect context menu signals to handlers
        self.context_menu.signals.openFile.connect(self.handle_open_file)
        self.context_menu.signals.openWith.connect(self.handle_open_with)
        self.context_menu.signals.openFolder.connect(self.handle_open_folder)
        self.context_menu.signals.moveRename.connect(self.handle_move_rename)
        self.context_menu.signals.redownload.connect(self.handle_redownload)
        self.context_menu.signals.resumeDownload.connect(self.handle_resume_download)
        self.context_menu.signals.stopDownload.connect(self.handle_stop_download)
        self.context_menu.signals.refreshAddress.connect(self.handle_refresh_address)
        self.context_menu.signals.addToQueue.connect(self.handle_add_to_queue)
        self.context_menu.signals.deleteFromQueue.connect(self.handle_delete_from_queue)
        self.context_menu.signals.showProperties.connect(self.handle_show_properties)
        
        # Connect header context menu signals
        self.header_context_menu.signals.columnVisibilityChanged.connect(
            self.toggle_column_visibility)
    
    def handle_open_file(self, download_id):
        print(f"Opening file for download {download_id}")
    
    def handle_open_with(self, download_id):
        print(f"Open with dialog for download {download_id}")
    
    def handle_open_folder(self, download_id):
        print(f"Opening folder for download {download_id}")
    
    def handle_move_rename(self, download_id):
        print(f"Move/Rename dialog for download {download_id}")
    
    def handle_redownload(self, download_id):
        print(f"Redownloading {download_id}")
    
    def handle_resume_download(self, download_id):
        print(f"Resuming download {download_id}")
    
    def handle_stop_download(self, download_id):
        print(f"Stopping download {download_id}")
    
    def handle_refresh_address(self, download_id):
        print(f"Refreshing address for download {download_id}")
    
    def handle_add_to_queue(self, download_id):
        print(f"Adding download {download_id} to queue")
    
    def handle_delete_from_queue(self, download_id):
        print(f"Deleting download {download_id} from queue")
    
    def handle_show_properties(self, download_id):
        print(f"Showing properties for download {download_id}")
    
    def toggle_column_visibility(self, column, visible):
        self.setColumnHidden(column, not visible)
    
    def setHorizontalHeaderWidget(self, column, widget):
        self.horizontalHeader().setMinimumSectionSize(widget.sizeHint().width())
        self.setCellWidget(0, column, widget)
    
    def toggle_all_checkboxes(self, checked):
        for row in range(self.rowCount()):
            checkbox = self.cellWidget(row, 0)
            if checkbox and isinstance(checkbox, RowCheckBox):
                checkbox.setChecked(checked)
    
    def load_data(self):
        downloads = self.repository.get_all()
        if not downloads:
            self.repository.add_sample_data()
            downloads = self.repository.get_all()
        
        self.setRowCount(len(downloads))
        for row, download in enumerate(downloads):
            # Store download id
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.UserRole, download.id)
            self.setItem(row, 0, id_item)
            
            # Checkbox
            checkbox = RowCheckBox(self._is_dark)
            self.setCellWidget(row, 0, checkbox)
            
            # File type icon
            self.setItem(row, 1, FileTypeIcon(download.file_type, self._is_dark))
            
            # Name
            name_item = SortableTableWidgetItem(download.name)
            self.setItem(row, 2, name_item)
            
            # Size
            size_item = SortableTableWidgetItem(download.size, self._parse_size(download.size))
            self.setItem(row, 3, size_item)
            
            # Status/Progress
            if download.progress > 0 and download.progress < 100:
                progress = DownloadProgressBar()
                progress.setValue(download.progress)
                self.setCellWidget(row, 4, progress)
            else:
                status_item = SortableTableWidgetItem(download.status)
                self.setItem(row, 4, status_item)
            
            # Time Left
            time_item = SortableTableWidgetItem(download.time_left)
            self.setItem(row, 5, time_item)
            
            # Last Modified
            modified_item = SortableTableWidgetItem(download.last_modified)
            self.setItem(row, 6, modified_item)
            
            # Speed
            speed_item = SortableTableWidgetItem(download.speed, self._parse_speed(download.speed))
            self.setItem(row, 7, speed_item)
    
    def _parse_size(self, size_str):
        """Convert size string to bytes for proper sorting"""
        try:
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
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.header_checkbox.update_style()
        self.setStyleSheet(Styles.get_styles(self._is_dark)["TABLE"])
        
        for row in range(self.rowCount()):
            # Update checkbox
            checkbox = self.cellWidget(row, 0)
            if isinstance(checkbox, RowCheckBox):
                checkbox.update_style()
            
            # Update file type icon
            icon_item = self.item(row, 1)
            if isinstance(icon_item, FileTypeIcon):
                self.setItem(row, 1, FileTypeIcon(icon_item.file_type, is_dark))
