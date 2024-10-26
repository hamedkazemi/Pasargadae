from PyQt6.QtWidgets import QProgressBar
from src.theme.styles import Styles

class DownloadProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setTextVisible(False)
        self.setFixedHeight(4)
        self.setStyleSheet(Styles.get_styles()["PROGRESS"])
