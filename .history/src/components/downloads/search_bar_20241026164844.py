from PyQt6.QtWidgets import QLineEdit

class SearchBar(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setPlaceholderText("Search in the List")
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border-radius: 4px;
                background-color: #2A2A2A;
                color: white;
            }
        """)
