from PyQt6.QtWidgets import QMenu, QAction
from PyQt6.QtCore import pyqtSignal, QObject

class HeaderContextMenuSignals(QObject):
    columnVisibilityChanged = pyqtSignal(int, bool)  # column index, visible

class HeaderContextMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = HeaderContextMenuSignals()
        self.column_actions = {}
        
        # Default column names and their visibility
        self.columns = {
            0: ("Checkbox", True),
            1: ("Icon", True),
            2: ("Name", True),
            3: ("Size", True),
            4: ("Status", True),
            5: ("Time Left", True),
            6: ("Last Modified", True),
            7: ("Speed", True)
        }
        
        self.setup_menu()
    
    def setup_menu(self):
        self.addSection("Show/Hide Columns")
        
        for col_idx, (name, visible) in self.columns.items():
            if col_idx in [0, 1, 2]:  # Always show checkbox, icon, and name
                continue
                
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(visible)
            action.toggled.connect(lambda checked, idx=col_idx: 
                self.signals.columnVisibilityChanged.emit(idx, checked))
            self.addAction(action)
            self.column_actions[col_idx] = action
    
    def update_column_state(self, column, visible):
        if column in self.column_actions:
            self.column_actions[column].setChecked(visible)
    
    def show_menu(self, pos):
        self.exec(pos)
