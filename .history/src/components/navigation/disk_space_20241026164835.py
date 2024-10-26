from PyQt6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel

class DiskSpace(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.disk_label = QLabel("Disk Space")
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        self.progress.setValue(90)
        
        self.path_label = QLabel("C:/Downloads")
        self.cleaner_label = QLabel("Disk Cleaner")
        self.cleaner_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                          stop:0 #2196F3, stop:1 #9C27B0);
                padding: 8px;
                border-radius: 4px;
                color: white;
            }
        """)
        
        layout.addWidget(self.disk_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.path_label)
        layout.addWidget(self.cleaner_label)
