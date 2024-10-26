from PyQt6.QtWidgets import QLineEdit, QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider
from src.theme.colors import Colors

class SearchContainer(QFrame):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 8, 0)
        layout.setSpacing(4)
        
        # Create search icon
        self.search_icon = QLabel(self)
        self.search_icon.setFixedSize(16, 16)
        layout.addWidget(self.search_icon)
        
        # Create search bar
        self.search_bar = SearchBar(self._is_dark, self)
        layout.addWidget(self.search_bar)
        
        # Set fixed height
        self.setFixedHeight(36)
        self.search_bar.setFixedHeight(36)
        
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["SEARCH"])
        self.update_icon()
        
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
    
    def update_icon(self):
        colors = Colors.Dark if self._is_dark else Colors.Light
        icon = IconProvider.get_icon('search', color=colors.ICON_COLOR)
        self.search_icon.setPixmap(icon.pixmap(16, 16))

class SearchBar(QLineEdit):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search downloads...")
        self.setClearButtonEnabled(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
