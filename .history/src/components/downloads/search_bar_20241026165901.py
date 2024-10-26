from PyQt6.QtWidgets import QLineEdit
from src.theme.styles import Styles

class SearchBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search in the List")
        self.setStyleSheet(Styles.get_styles()["SEARCH"])
        self.setMinimumHeight(36)
