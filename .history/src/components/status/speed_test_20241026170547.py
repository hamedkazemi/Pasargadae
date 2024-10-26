from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from src.theme.colors import Colors

class SpeedTestWidget(QFrame):
    def __init__(self, is_dark=True):
        super().__init__()
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        speed_label = QLabel("Speed Test:")
        download_label = QLabel("↓ 10.55 MB/s")
        upload_label = QLabel("↑ 6.30 MB/s")
        
        colors = Colors.Dark if self._is_dark else Colors.Light
        style = f"""
            QLabel {{
                color: {colors.TEXT_SECONDARY};
                font-size: 12px;
            }}
        """
        
        for label in [speed_label, download_label, upload_label]:
            label.setStyleSheet(style)
        
        layout.addWidget(speed_label)
        layout.addWidget(download_label)
        layout.addWidget(upload_label)
        layout.addStretch()
