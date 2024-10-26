from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QProgressBar
from PyQt6.QtCore import Qt

class DownloadProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #2A2A2A;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 4px;
            }
        """)

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
        self.setAlternatingRowColors(True)
