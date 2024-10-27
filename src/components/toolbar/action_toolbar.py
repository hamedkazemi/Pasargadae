from PyQt6.QtWidgets import QToolBar, QToolButton, QWidget
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize
from src.theme.styles import Styles
from src.utils.icon_provider import IconProvider
from src.theme.colors import Colors
from src.components.modal.download_modal import DownloadModal
from src.components.modal.settings_modal import SettingsModal
from src.utils.logger import Logger

class ToolbarSeparator(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setFixedSize(2, 24)
        self.update_style()
    
    def update_style(self):
        colors = Colors.Dark if self._is_dark else Colors.Light
        color = colors.TEXT_SECONDARY
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                margin: 6px 8px;
                border-radius: 1px;
                opacity: 0.2;
            }}
        """)

class ActionToolbar(QToolBar):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self._buttons = []  # Store buttons for theme updates
        self._separators = []  # Store separators for theme updates
        self.setMovable(False)
        self.setup_ui()
        self.update_theme(is_dark)
    
    def setup_ui(self):
        actions = [
            ("Add URL", "add_url", self.show_download_modal),
            None,  # Separator
            ("Resume", "resume", None),
            ("Stop", "stop", None),
            ("Stop All", "stop", None),
            None,  # Separator
            ("Delete", "delete", None),
            ("Options", "options", self.show_settings_modal),
            ("Queues", "queue", None),
            ("Schedule", "schedule", None),
            ("Share", "share", None)
        ]
        
        # Clear existing buttons and separators
        self._buttons.clear()
        self._separators.clear()
        while self.actions():
            self.removeAction(self.actions()[0])
        
        spacer = QWidget()
        spacer.setFixedWidth(5)
        self.addWidget(spacer)
        
        for action in actions:
            if action is None:
                separator = ToolbarSeparator(self._is_dark)
                self._separators.append(separator)
                self.addWidget(separator)
            else:
                name, icon, callback = action
                btn = QToolButton()
                btn.setIcon(IconProvider.get_icon(icon, self._is_dark))
                btn.setToolTip(name)
                btn.setIconSize(QSize(24, 24))
                if callback:
                    btn.clicked.connect(callback)
                self._buttons.append((btn, icon))  # Store button and icon name
                self.addWidget(btn)
    
    def show_download_modal(self):
        Logger.debug("Opening download modal")
        try:
            # Get main window
            main_window = self.window()
            
            # Create modal with the main window as parent and pass managers
            modal = DownloadModal(
                parent=main_window,
                download_manager=main_window.download_manager,
                settings_manager=main_window.settings_manager
            )
            modal.exec()
        except Exception as e:
            Logger.error(f"Error showing download modal: {e}")
    
    def show_settings_modal(self):
        # Create modal with the main window as parent
        modal = SettingsModal(self.window())
        # Ensure modal stays on top and is independent
        modal.setWindowModality(Qt.WindowModality.ApplicationModal)
        modal.exec()
    
    def update_theme(self, is_dark):
        self._is_dark = is_dark
        colors = Colors.Dark if self._is_dark else Colors.Light
        
        # Update toolbar style
        self.setStyleSheet(f"""
            QToolBar {{
                background-color: {colors.SURFACE};
                border: none;
                padding: 5px;
                spacing: 5px;
            }}
            QToolButton {{
                background-color: transparent;
                color: {colors.TEXT_PRIMARY};
                border: none;
                border-radius: 4px;
                padding: 5px;
                icon-size: 20px;
            }}
            QToolButton:hover {{
                background-color: rgba(128, 128, 128, 0.1);
            }}
            QToolButton:pressed {{
                background-color: rgba(128, 128, 128, 0.15);
            }}
        """)
        
        # Update icons for all buttons
        for btn, icon_name in self._buttons:
            btn.setIcon(IconProvider.get_icon(icon_name, self._is_dark))
        
        # Update separators
        for separator in self._separators:
            separator.update_style()
