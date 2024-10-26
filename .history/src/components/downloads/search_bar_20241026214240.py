from PyQt6.QtWidgets import QLineEdit, QFrame, QHBoxLayout
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
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
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
        self.search_bar.update_icons()
        
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()

class SearchBar(QLineEdit):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self._search_action = None
        self._clear_action = None
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search downloads...")
        self.setClearButtonEnabled(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.update_icons()
    
    def update_icons(self):
        # Update search icon
        if self._search_action:
            self.removeAction(self._search_action)
        
        colors = Colors.Dark if self._is_dark else Colors.Light
        search_icon = IconProvider.get_icon('search', color=colors.ICON_COLOR)
        self._search_action = self.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
        
        # Update clear button icon
        if self._clear_action:
            self.removeAction(self._clear_action)
        
        close_icon = IconProvider.get_icon('close', color=colors.ICON_COLOR)
        self._clear_action = self.addAction(close_icon, QLineEdit.ActionPosition.TrailingPosition)
        self._clear_action.triggered.connect(self.clear)
