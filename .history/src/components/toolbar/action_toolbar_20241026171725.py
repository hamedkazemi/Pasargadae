from PyQt6.QtWidgets import QToolBar, QToolButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider

class ActionToolbar(QToolBar):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self._buttons = []  # Store buttons for theme updates
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
        
        # Clear existing buttons
        self._buttons.clear()
        while self.actions():
            self.removeAction(self.actions()[0])
        
        for action in actions:
            if action is None:
                self.addSeparator()
            else:
                name, icon = action
                btn = QToolButton()
                btn.setIcon(IconProvider.get_icon(icon, self._is_dark))
                btn.setToolTip(name)
                btn.setIconSize(QSize(24, 24))
                self._buttons.append((btn, icon))  # Store button and icon name
                self.addWidget(btn)
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        # Update icons for all buttons
        for btn, icon_name in self._buttons:
            btn.setIcon(IconProvider.get_icon(icon_name, self._is_dark))
