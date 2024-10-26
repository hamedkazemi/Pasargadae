from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal
from src.utils.icon_provider import IconProvider

class WindowControls(QWidget):
    minimizeClicked = pyqtSignal()
    closeClicked = pyqtSignal()
    
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(8)
        
        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(IconProvider.get_icon("minimize", self._is_dark))
        self.minimize_btn.clicked.connect(self.minimizeClicked)
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(IconProvider.get_icon("close", self._is_dark))
        self.close_btn.clicked.connect(self.closeClicked)
        
        # Add buttons to layout
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.close_btn)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 8px;
                padding: 4px;
                margin: 2px 2px;
                width: 24px;
                height: 24px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            QPushButton#close_btn:hover {
                background: #E81123;
            }
        """)
        
        self.minimize_btn.setObjectName("minimize_btn")
        self.close_btn.setObjectName("close_btn")
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.minimize_btn.setIcon(IconProvider.get_icon("minimize", self._is_dark))
        self.close_btn.setIcon(IconProvider.get_icon("close", self._is_dark))
