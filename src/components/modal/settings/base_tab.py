from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QCheckBox, QComboBox,
    QSpinBox, QPushButton
)
from PyQt6.QtCore import Qt
from typing import Any, Dict, Optional

class SettingsTab(QWidget):
    def __init__(self, settings: Dict[str, Any], category: str, parent=None):
        """
        Base class for settings tabs.
        
        Args:
            settings: The complete settings dictionary
            category: The category this tab handles (e.g., 'general', 'download')
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings = settings
        self.category = category
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self._setup_ui()
    
    def _setup_ui(self):
        """Override this method in subclasses to setup the UI"""
        pass
    
    def save_settings(self):
        """Override this method in subclasses to save settings"""
        pass

    def add_section(self, title: str) -> QVBoxLayout:
        """Add a new section with a title"""
        label = QLabel(title)
        label.setObjectName("sectionTitle")
        self.layout.addWidget(label)
        
        section = QWidget()
        section_layout = QVBoxLayout(section)
        section_layout.setSpacing(10)
        section_layout.setContentsMargins(10, 5, 10, 15)
        self.layout.addWidget(section)
        return section_layout

    def add_field(self, layout: QVBoxLayout, label_text: str, 
                 widget: QWidget, tooltip: Optional[str] = None) -> QWidget:
        """Add a field with a label to the given layout"""
        field_widget = QWidget()
        field_layout = QHBoxLayout(field_widget)
        field_layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        if tooltip:
            label.setToolTip(tooltip)
            widget.setToolTip(tooltip)
        
        field_layout.addWidget(label)
        field_layout.addWidget(widget)
        
        layout.addWidget(field_widget)
        return widget

    def create_browse_widget(self, initial_path: str = "", 
                           callback: Optional[callable] = None) -> tuple[QWidget, QLineEdit]:
        """Create a widget with a text field and browse button"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        text_field = QLineEdit(initial_path)
        text_field.setReadOnly(True)
        
        browse_btn = QPushButton("Browse")
        if callback:
            browse_btn.clicked.connect(callback)
        
        layout.addWidget(text_field)
        layout.addWidget(browse_btn)
        
        return container, text_field
    
    def get_nested_setting(self, *keys: str, default: Any = None) -> Any:
        """
        Get a nested setting value safely.
        
        Example:
            get_nested_setting('proxy_settings', 'authentication', 'username')
        """
        value = self.settings[self.category]
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set_nested_setting(self, value: Any, *keys: str) -> None:
        """
        Set a nested setting value safely.
        
        Example:
            set_nested_setting('new_username', 'proxy_settings', 'authentication', 'username')
        """
        target = self.settings[self.category]
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        target[keys[-1]] = value
