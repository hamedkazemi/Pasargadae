from PyQt6.QtWidgets import QToolBar, QToolButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class ActionToolbar(QToolBar):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setMovable(False)
        self.setStyleSheet(Styles.get_styles()["TOOLBAR"])
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
                btn.setIcon(IconProvider.get_icon(icon, self._is_dark))
                btn.setToolTip(name)
                btn.setIconSize(QSize(24, 24))
                self.addWidget(btn)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        # Recreate all buttons with new theme
        while self.actions():
            self.removeAction(self.actions()[0])
        self.setup_actions()
