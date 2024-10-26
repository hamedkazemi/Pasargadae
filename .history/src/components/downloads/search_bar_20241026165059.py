from PyQt6.QtWidgets import QLineEdit
from ...theme.styles import Styles

class SearchBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search in the List")
        self.setStyleSheet(Styles.SEARCH)
        self.setMinimumHeight(36)
