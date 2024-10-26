from PyQt6.QtWidgets import QWidget, QCheckBox, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from src.theme.colors import Colors

class HeaderCheckBox(QWidget):
    stateChanged = pyqtSignal(bool)
    
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 0, 0, 0)
        layout.setSpacing(0)
        
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self._emit_state)
        
        layout.addWidget(self.checkbox)
        self.update_style()
    
    def update_style(self):
        colors = Colors.Dark if self._is_dark else Colors.Light
        self.setStyleSheet(f"""
            QCheckBox {{
                spacing: 0px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {colors.TEXT_SECONDARY};
                border-radius: 4px;
                background: transparent;
            }}
            QCheckBox::indicator:checked {{
                background: {colors.PRIMARY};
                border-color: {colors.PRIMARY};
                image: url(src/assets/icons/check.svg);
            }}
            QCheckBox::indicator:hover {{
                border-color: {colors.PRIMARY};
            }}
        """)
    
    def _emit_state(self, state):
        from PyQt6.QtCore import Qt
        self.stateChanged.emit(state == Qt.CheckState.Checked.value)
