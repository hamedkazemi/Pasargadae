from PyQt6.QtWidgets import QLineEdit, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class SearchContainer(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.search_bar = SearchBar(is_dark, self)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.search_bar)
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["SEARCH_CONTAINER"])
        self.search_bar.apply_theme()
    
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
        
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["SEARCH"])
