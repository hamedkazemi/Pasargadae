from PyQt6.QtWidgets import QToolBar, QToolButton
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt
from src.theme.styles import Styles

class ActionToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setStyleSheet(Styles.TOOLBAR)
        self.setup_actions()
    
    def setup_actions(self):
        actions = [
            ("Add URL", "add_url"),
            None,  # Separator
            ("Resume", "resume"),
            ("Stop", "stop"),
            ("Stop All", "stop"),
            None,  # Separator
            ("Delete", "delete"),
            ("Options", "options"),
            ("Queues", "queue"),
            ("Schedule", "schedule"),
            ("Share", "share")
        ]
        
        for action in actions:
            if action is None:
                self.addSeparator()
            else:
                name, icon = action
                btn = QToolButton()
                btn.setIcon(QIcon(f"src/assets/icons/{icon}.svg"))
                btn.setToolTip(name)
                btn.setIconSize(Qt.QSize(24, 24))
                self.addWidget(btn)
