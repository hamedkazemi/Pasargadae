from PyQt6.QtWidgets import QCheckBox
from src.theme.colors import Colors

class RowCheckBox(QCheckBox):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.update_style()
    
    def update_style(self):
        colors = Colors.Dark if self._is_dark else Colors.Light
        self.setStyleSheet(f"""
            QCheckBox {{
                spacing: 0px;
            }}
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
                border: 0px solid {colors.TEXT_SECONDARY};
                image: url(src/assets/icons/uncheck.svg);
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
