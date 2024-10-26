from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt
from src.theme.styles import Styles

class DiskSpace(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        self.setObjectName("diskSpace")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Title
        self.title_label = QLabel("Disk Space")
        self.title_label.setObjectName("diskTitle")
        
        # Path
        self.path_label = QLabel("/home/downloads")
        self.path_label.setObjectName("diskPath")
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setValue(65)  # Example value
        
        # Space info
        self.space_label = QLabel("650.3 GB free of 1 TB")
        self.space_label.setObjectName("diskPath")
        
        # Cleaner button
        self.cleaner_btn = QPushButton("Clean Downloads")
        self.cleaner_btn.setObjectName("diskCleaner")
        
        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.path_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.space_label)
        layout.addWidget(self.cleaner_btn)
        
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["DISK_SPACE"])
        self.progress_bar.setStyleSheet(styles["PROGRESS"])
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
