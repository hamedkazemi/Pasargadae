from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtCore import Qt
from src.theme.styles import Styles
from .table.header_checkbox import HeaderCheckBox
from .table.row_checkbox import RowCheckBox
from .table.progress_bar import DownloadProgressBar
from .table.file_type_icon import FileTypeIcon
from .table.context_menu import DownloadContextMenu
from src.repositories.download_repository import DownloadRepository

class DownloadTable(QTableWidget):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.repository = DownloadRepository()
        self.context_menu = DownloadContextMenu(self)
        self.setup_ui()
        self.setup_context_menu()
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
        
        self.setStyleSheet(Styles.get_styles()["TABLE"])
    
    def setHorizontalHeaderWidget(self, column, widget):
        self.horizontalHeader().setMinimumSectionSize(widget.sizeHint().width())
        self.setCellWidget(0, column, widget)
    
    def toggle_all_checkboxes(self, checked):
        for row in range(self.rowCount()):
            checkbox = self.cellWidget(row, 0)
            if checkbox and isinstance(checkbox, RowCheckBox):
                checkbox.setChecked(checked)
    
    def setup_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos):
        row = self.rowAt(pos.y())
        if row >= 0:
            download_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
            self.context_menu.show_for_download(download_id, self.mapToGlobal(pos))
    
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
            name_item = QTableWidgetItem(download.name)
            self.setItem(row, 2, name_item)
            
            # Size
            size_item = QTableWidgetItem(download.size)
            self.setItem(row, 3, size_item)
            
            # Status/Progress
            if download.progress > 0 and download.progress < 100:
                progress = DownloadProgressBar()
                progress.setValue(download.progress)
                self.setCellWidget(row, 4, progress)
            else:
                status_item = QTableWidgetItem(download.status)
                self.setItem(row, 4, status_item)
            
            # Time Left
            time_item = QTableWidgetItem(download.time_left)
            self.setItem(row, 5, time_item)
            
            # Last Modified
            modified_item = QTableWidgetItem(download.last_modified)
            self.setItem(row, 6, modified_item)
            
            # Speed
            speed_item = QTableWidgetItem(download.speed)
            self.setItem(row, 7, speed_item)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.header_checkbox.update_style()
        
        for row in range(self.rowCount()):
            # Update checkbox
            checkbox = self.cellWidget(row, 0)
            if isinstance(checkbox, RowCheckBox):
                checkbox.update_style()
            
            # Update file type icon
            icon_item = self.item(row, 1)
            if isinstance(icon_item, FileTypeIcon):
                self.setItem(row, 1, FileTypeIcon(icon_item.file_type, is_dark))