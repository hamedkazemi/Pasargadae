from PyQt6.QtWidgets import QLineEdit, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPalette, QColor
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider
from src.theme.colors import Colors

class SearchContainer(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.search_bar = SearchBar(is_dark, self)
        self.setup_ui()
    
    def setup_ui(self):
        # Enable background filling
        self.setAutoFillBackground(True)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search_bar)
        
        # Set fixed height for proper background visibility
        self.setFixedHeight(36)
        self.setObjectName("search_container")
        
        # Set initial background color
        self.update_background()
        self.apply_theme()
    
    def update_background(self):
        palette = self.palette()
        colors = Colors.Dark if self._is_dark else Colors.Light
        color = QColor(colors.SURFACE_LIGHT)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Window, color)
        palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, color)
        self.setPalette(palette)
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["SEARCH"])
        self.update_background()
        
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()

class SearchBar(QLineEdit):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search downloads...")
        self.setClearButtonEnabled(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Add custom search icon
        search_icon = IconProvider.get_icon('search')
        search_action = self.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
        
        # Set size policy to fill the container
        self.setFixedHeight(36)
