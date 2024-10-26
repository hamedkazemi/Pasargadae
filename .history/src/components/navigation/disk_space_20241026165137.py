from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
from src.theme.styles import Styles

class DiskSpace(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("diskSpace")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Disk space title
        self.disk_label = QLabel("Disk Space")
        self.disk_label.setObjectName("diskTitle")
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setValue(90)
        self.progress.setStyleSheet(Styles.PROGRESS)
        
        # Path label
        self.path_label = QLabel("C:/Downloads")
        self.path_label.setObjectName("diskPath")
        
        # Disk cleaner button
        self.cleaner_btn = QPushButton("Disk Cleaner")
        self.cleaner_btn.setObjectName("diskCleaner")
        
        layout.addWidget(self.disk_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.path_label)
        layout.addWidget(self.cleaner_btn)
        
        self.setStyleSheet(Styles.DISK_SPACE)
