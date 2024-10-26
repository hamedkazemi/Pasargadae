from PyQt6.QtWidgets import QWidget, QHBoxLayout
from src.components.menu.menu_bar import MenuBar
from src.components.theme.theme_switcher import ThemeSwitcher

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Menu bar
        self.menu_bar = MenuBar(self.parent)
        
        # Theme switcher
        self.theme_switcher = ThemeSwitcher(self.parent)
        self.menu_bar.setCornerWidget(self.theme_switcher)
        
        layout.addWidget(self.menu_bar)
    
    def apply_theme(self, styles):
        self.menu_bar.setStyleSheet(styles["MENU"])
    
    @property
    def theme_changed(self):
        return self.theme_switcher.themeChanged
