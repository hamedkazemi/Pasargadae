from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, pyqtSignal

class ThemeSwitcher(QPushButton):
    themeChanged = pyqtSignal(bool)  # True for dark mode, False for light mode
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = True
        self.setup_ui()
        
    def setup_ui(self):
        self.setFixedSize(32, 32)
        self.setIconSize(QSize(20, 20))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_icon()
        self.clicked.connect(self.toggle_theme)
        
        # Style
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 16px;
                padding: 4px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
    
    def toggle_theme(self):
        self._is_dark = not self._is_dark
        self.update_icon()
        self.themeChanged.emit(self._is_dark)
    
    def update_icon(self):
        icon_name = "dark_mode" if self._is_dark else "light_mode"
        self.setIcon(QIcon(f"src/assets/icons/{icon_name}.svg"))
        self.setToolTip("Switch to Light Mode" if self._is_dark else "Switch to Dark Mode")
