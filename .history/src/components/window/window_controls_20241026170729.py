from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal

class WindowControls(QWidget):
    minimizeClicked = pyqtSignal()
    closeClicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 10, 0)
        layout.setSpacing(8)
        
        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon("src/assets/icons/minimize.svg"))
        self.minimize_btn.clicked.connect(self.minimizeClicked)
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("src/assets/icons/close.svg"))
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
