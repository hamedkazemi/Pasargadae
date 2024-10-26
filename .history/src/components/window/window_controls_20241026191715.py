from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from src.utils.icon_provider import IconProvider

class WindowControls(QWidget):
    minimizeClicked = pyqtSignal()
    closeClicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._is_dark = True
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Minimize button
        self.minimize_btn = QPushButton()
        self.minimize_btn.setFixedSize(45, 30)
        self.minimize_btn.clicked.connect(self.minimizeClicked.emit)
        self.minimize_btn.setIcon(IconProvider.get_icon("minimize", self._is_dark))
        
        # Close button
        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(45, 30)
        self.close_btn.clicked.connect(self.closeClicked.emit)
        self.close_btn.setIcon(IconProvider.get_icon("close", self._is_dark))
        
        # Add buttons to layout
        layout.addWidget(self.minimize_btn)
        layout.addWidget(self.close_btn)
        
        self.update_style()
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.minimize_btn.setIcon(IconProvider.get_icon("minimize", is_dark))
        self.close_btn.setIcon(IconProvider.get_icon("close", is_dark))
        self.update_style()
    
    def update_style(self):
        base_btn_style = """
            QPushButton {
                background: transparent;
                border: none;
                border-radius: 0px;
                padding: 5px;
            }
        """
        
        minimize_hover = "rgba(255, 255, 255, 0.1)" if self._is_dark else "rgba(0, 0, 0, 0.1)"
        close_hover = "#E81123"
        
        self.minimize_btn.setStyleSheet(base_btn_style + f"""
            QPushButton:hover {{
                background: {minimize_hover};
            }}
        """)
        
        self.close_btn.setStyleSheet(base_btn_style + f"""
            QPushButton:hover {{
                background: {close_hover};
            }}
        """)
