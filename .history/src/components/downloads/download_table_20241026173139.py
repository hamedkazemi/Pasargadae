from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem, QProgressBar, 
                                    QHeaderView, QMenu, QCheckBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class DownloadProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setTextVisible(False)
        self.setFixedHeight(4)

class FileTypeIcon(QTableWidgetItem):
    def __init__(self, file_type, is_dark=True):
        super().__init__()
        icon_map = {
            'image': 'image',
            'music': 'music',
            'video': 'video',
            'document': 'document',
            'program': 'options',
            'archive': 'document'
        }
        icon_name = icon_map.get(file_type, 'document')
        self.setIcon(IconProvider.get_icon(icon_name, is_dark))

class DownloadTable(QTableWidget):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setup_ui()
        self.setup_context_menu()
        self.add_sample_data()
    
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
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Checkbox column
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # Icon column
        header.setDefaultSectionSize(150)
        header.setStretchLastSection(True)
        
        # Set column widths
        self.setColumnWidth(0, 30)  # Checkbox
        self.setColumnWidth(1, 30)  # Icon
        
        self.setStyleSheet(Styles.get_styles()["TABLE"])
    
    def setup_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.addAction("Open")
        menu.addAction("Open With")
        menu.addAction("Open Folder")
        menu.addSeparator()
        menu.addAction("Move/Rename")
        menu.addAction("Redownload")
        menu.addSeparator()
        menu.addAction("Resume Download")
        menu.addAction("Stop Download")
        menu.addAction("Refresh Download Address")
        menu.addSeparator()
        menu.addAction("Add to queue")
        menu.addAction("Delete from Queue")
        menu.addSeparator()
        menu.addAction("Properties")
        
        menu.exec(self.mapToGlobal(pos))
    
    def add_sample_data(self):
        sample_data = [
            ("UIUXMonster", "image", "745 KB", "Complete", "0 Sec", "2023/08/09", "3MB/s"),
            ("2pacCover", "music", "3.00 MB", "80%", "0 Sec", "2023/08/09", "2MB/s"),
            ("Document", "document", "2 MB", "50%", "5 Min", "2023/08/09", "4MB/s"),
            ("Better.Call.Saul", "video", "2.5 GB", "0%", "0 Sec", "Today", "0MB/s"),
            ("Call.Of.Duty", "program", "12.00 MB", "Paused", "0 Sec", "Today", "0MB/s"),
            ("Mima.exe", "program", "32 MB", "Complete", "0 Sec", "2023/08/09", "5MB/s"),
        ]
        
        self.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            # Checkbox
            checkbox = QCheckBox()
            self.setCellWidget(row, 0, checkbox)
            
            # File type icon
            self.setItem(row, 1, FileTypeIcon(data[1], self._is_dark))
            
            # Name
            name_item = QTableWidgetItem(data[0])
            self.setItem(row, 2, name_item)
            
            # Size
            size_item = QTableWidgetItem(data[2])
            self.setItem(row, 3, size_item)
            
            # Status/Progress
            if data[3].endswith("%"):
                progress = DownloadProgressBar()
                progress.setValue(int(data[3][:-1]))
                self.setCellWidget(row, 4, progress)
            else:
                status_item = QTableWidgetItem(data[3])
                self.setItem(row, 4, status_item)
            
            # Time Left
            time_item = QTableWidgetItem(data[4])
            self.setItem(row, 5, time_item)
            
            # Last Modified
            modified_item = QTableWidgetItem(data[5])
            self.setItem(row, 6, modified_item)
            
            # Speed
            speed_item = QTableWidgetItem(data[6])
            self.setItem(row, 7, speed_item)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        # Update all file type icons
        for row in range(self.rowCount()):
            icon_item = self.item(row, 1)
            if isinstance(icon_item, FileTypeIcon):
                file_type = icon_item.data(Qt.ItemDataRole.UserRole)
                self.setItem(row, 1, FileTypeIcon(file_type, is_dark))
