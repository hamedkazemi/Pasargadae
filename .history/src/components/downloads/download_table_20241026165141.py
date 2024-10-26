from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QProgressBar, QHeaderView
from PyQt6.QtCore import Qt
from src.theme.styles import Styles

class DownloadProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(Styles.PROGRESS)
        self.setTextVisible(False)

class DownloadTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        headers = ["", "Name", "Size", "Status", "Time Left", 
                  "Last Modified", "Speed"]
        
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        
        # Customize header
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setDefaultSectionSize(150)
        header.setStretchLastSection(True)
        
        self.setStyleSheet(Styles.TABLE)
