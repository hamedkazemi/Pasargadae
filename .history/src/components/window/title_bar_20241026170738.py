from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from src.components.menu.menu_bar import MenuBar
from src.components.theme.theme_switcher import ThemeSwitcher
from .window_controls import WindowControls

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(10)
        
        # Logo and title
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("src/assets/icons/logo.svg").pixmap(24, 24))
        
        title_label = QLabel("Pasargadae")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding-right: 20px;
            }
        """)
        
        # Menu bar
        self.menu_bar = MenuBar(self.parent)
        
        # Theme switcher
        self.theme_switcher = ThemeSwitcher(self.parent)
        
        # Window controls
        self.window_controls = WindowControls()
        self.window_controls.minimizeClicked.connect(self.parent.showMinimized)
        self.window_controls.closeClicked.connect(self.parent.close)
        
        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addWidget(self.menu_bar)
        layout.addStretch()
        layout.addWidget(self.theme_switcher)
        layout.addWidget(self.window_controls)
    
    def apply_theme(self, styles):
        self.menu_bar.setStyleSheet(styles["MENU"])
    
    @property
    def theme_changed(self):
        return self.theme_switcher.themeChanged
