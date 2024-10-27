from PyQt6.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout,
    QScrollArea, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import os

from .modal_window import ModalWindow
from .settings.general_tab import GeneralSettingsTab
from .settings.download_tab import DownloadSettingsTab
from .settings.connection_tab import ConnectionSettingsTab
from .settings.scheduler_tab import SchedulerSettingsTab
from .settings.speed_limiter_tab import SpeedLimiterTab
from .settings.filters_tab import FiltersTab
from .settings.browser_tab import BrowserTab
from .settings.advanced_tab import AdvancedSettingsTab
from .settings.notifications_tab import NotificationsTab
from .settings.security_tab import SecurityTab
from .settings.logging_tab import LoggingTab
from .settings.integrity_tab import IntegrityTab

from src.settings.manager import SettingsManager

class SettingsModal(ModalWindow):
    def __init__(self, parent=None):
        super().__init__(parent, title="Settings", width=800, height=600)
        self._is_dark = getattr(parent, '_is_dark', True)
        
        try:
            # Initialize settings manager with absolute path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            settings_dir = os.path.join(base_dir, 'settings')
            os.makedirs(settings_dir, exist_ok=True)
            settings_file = os.path.join(settings_dir, 'settings.json')
            
            self.settings_manager = SettingsManager(settings_file)
            self.settings = self.settings_manager.get_all_settings()
            
            self.setup_settings_ui()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Settings Error",
                f"Failed to initialize settings:\n{str(e)}"
            )
            self.close()
    
    def setup_settings_ui(self):
        # Create main content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.tab_widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Add tabs
        self.tabs = [
            ("General", GeneralSettingsTab(self.settings)),
            ("Downloads", DownloadSettingsTab(self.settings)),
            ("Connection", ConnectionSettingsTab(self.settings)),
            ("Speed", SpeedLimiterTab(self.settings)),
            ("Filters", FiltersTab(self.settings)),
            ("Browser", BrowserTab(self.settings)),
            ("Advanced", AdvancedSettingsTab(self.settings)),
            ("Notifications", NotificationsTab(self.settings)),
            ("Security", SecurityTab(self.settings)),
            ("Logging", LoggingTab(self.settings)),
            ("Integrity", IntegrityTab(self.settings))
        ]
        
        for title, tab in self.tabs:
            self.tab_widget.addTab(tab, title)
        
        content_layout.addWidget(scroll)
        
        # Set content
        self.set_content(content_widget)
        
        # Add action buttons
        self.add_action_button("Cancel", self.close)
        self.add_action_button("Save", self.save_settings, True)
        
        self.setStyleSheet(self.get_settings_style())
    
    def save_settings(self):
        try:
            # Save settings from each tab
            for _, tab in self.tabs:
                tab.save_settings()
            
            # Update settings file
            if not self.settings_manager.update_settings(self.settings):
                raise Exception("Failed to update settings")
            
            if not self.settings_manager.save_settings():
                raise Exception("Failed to save settings to file")
            
            # Notify parent of settings change if method exists
            parent_widget = self.parentWidget()
            if parent_widget and hasattr(parent_widget, 'update_settings'):
                parent_widget.update_settings(self.settings)
            
            self.close()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Saving Settings",
                f"An error occurred while saving settings:\n{str(e)}"
            )
    
    def get_settings_style(self):
        bg_color = "#15161A" if self._is_dark else "#FFFFFF"
        text_color = "#FFFFFF" if self._is_dark else "#212121"
        border_color = "#26272B" if self._is_dark else "#E0E0E0"
        
        return f"""
            QTabWidget::pane {{
                border: none;
                background-color: {bg_color};
            }}
            
            QTabBar::tab {{
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                color: {text_color};
                background-color: {bg_color};
                border: 1px solid {border_color};
            }}
            
            QTabBar::tab:selected {{
                background-color: #2196F3;
                color: white;
                border: none;
            }}
            
            QLabel#sectionTitle {{
                font-weight: bold;
                font-size: 14px;
                padding-top: 10px;
                color: {text_color};
            }}
            
            QLabel {{
                color: {text_color};
            }}
            
            QLineEdit, QComboBox, QSpinBox {{
                padding: 5px;
                border: 1px solid {border_color};
                border-radius: 4px;
                min-width: 200px;
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QPushButton {{
                padding: 5px 10px;
                border-radius: 4px;
            }}
            
            QCheckBox {{
                color: {text_color};
            }}
            
            QScrollArea {{
                border: none;
                background-color: {bg_color};
            }}
            
            QWidget {{
                background-color: {bg_color};
            }}
            
            QMessageBox {{
                background-color: {bg_color};
                color: {text_color};
            }}
            
            QMessageBox QPushButton {{
                min-width: 80px;
                padding: 5px 15px;
            }}
            
            QMessageBox QPushButton:default {{
                background-color: #2196F3;
                color: white;
                border: none;
            }}
            
            QMessageBox QPushButton:hover {{
                background-color: #1976D2;
            }}
        """
