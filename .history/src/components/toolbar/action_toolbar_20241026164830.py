from PyQt6.QtWidgets import QToolBar
from PyQt6.QtGui import QAction

class ActionToolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(False)
        self.setup_actions()
    
    def setup_actions(self):
        actions = [
            ("Add URL", None),
            None,  # Separator
            ("Resume", None),
            ("Stop", None),
            ("Stop All", None),
            None,  # Separator
            ("Delete", None),
            ("Options", None),
            ("Queues", None),
            ("Schedule", None),
            ("Share", None)
        ]
        
        for action in actions:
            if action is None:
                self.addSeparator()
            else:
                name, icon = action
                self.addAction(QAction(name, self))
