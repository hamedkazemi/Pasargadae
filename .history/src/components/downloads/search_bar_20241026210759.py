from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QStyle
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class SearchBar(QLineEdit):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search downloads...")
        self.setClearButtonEnabled(True)
        
        # Add search icon
        search_action = self.addAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView), QLineEdit.ActionPosition.LeadingPosition)
        
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["SEARCH"])
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        self.apply_theme()
