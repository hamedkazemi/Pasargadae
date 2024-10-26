from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, 
                                    QTableWidgetItem, QLineEdit, QHBoxLayout,
                                    QPushButton)
from PyQt6.QtCore import Qt

class DownloadList(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QVBoxLayout()
        title_label = QLineEdit("Downloads")
        title_label.setReadOnly(True)
        title_label.setStyleSheet("QLineEdit { border: none; font-size: 24px; }")
        subtitle_label = QLineEdit("Manage your downloads")
        subtitle_label.setReadOnly(True)
        subtitle_label.setStyleSheet("QLineEdit { border: none; color: gray; }")
        
        # Search bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search downloads")
        
        # Filter buttons
        filter_layout = QHBoxLayout()
        filters = ["All", "Active", "Paused", "Completed"]
        for filter_text in filters:
            btn = QPushButton(filter_text)
            filter_layout.addWidget(btn)
        filter_layout.addStretch()
        
        # Downloads table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Size", "Progress", "Speed", "ETA", "Actions"])
        
        # Add all widgets to main layout
        layout.addLayout(header_layout)
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        layout.addWidget(search_bar)
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
