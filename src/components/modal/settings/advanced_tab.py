from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, 
    QCheckBox, QSpinBox, QComboBox
)
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class DynamicSpinBox(QWidget):
    def __init__(self, checkbox_text: str, initial_checked: bool, 
                 initial_value: int, min_value: int = 1, max_value: int = 100,
                 suffix: str = "", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.checkbox = QCheckBox(checkbox_text)
        self.checkbox.setChecked(initial_checked)
        
        self.spinbox = QSpinBox()
        self.spinbox.setEnabled(initial_checked)
        self.spinbox.setValue(initial_value)
        self.spinbox.setRange(min_value, max_value)
        if suffix:
            self.spinbox.setSuffix(suffix)
        
        self.checkbox.stateChanged.connect(self.spinbox.setEnabled)
        
        layout.addWidget(self.checkbox)
        layout.addWidget(self.spinbox)
        layout.addStretch()
    
    def get_value(self) -> tuple[bool, int]:
        return self.checkbox.isChecked(), self.spinbox.value()

class IconToggle(QWidget):
    def __init__(self, text: str, icon_enabled: str, icon_disabled: str, 
                 initial_state: bool, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.icon_label = QLabel()
        self.checkbox = QCheckBox(text)
        self.checkbox.setChecked(initial_state)
        
        self.icon_enabled = IconProvider.get_icon(icon_enabled)
        self.icon_disabled = IconProvider.get_icon(icon_disabled)
        self.update_icon(initial_state)
        
        self.checkbox.stateChanged.connect(self.update_icon)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.checkbox)
        layout.addStretch()
    
    def update_icon(self, state: int):
        icon = self.icon_enabled if state else self.icon_disabled
        self.icon_label.setPixmap(icon.pixmap(24, 24))
    
    def isChecked(self) -> bool:
        return self.checkbox.isChecked()

class AdvancedSettingsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "advanced_download", parent)
    
    def _setup_ui(self):
        # Download Capabilities Section
        capabilities_section = self.add_section("Download Capabilities")
        
        # Resume capability
        self.resume_toggle = IconToggle(
            "Enable Auto-Resume",
            "resume",  # Icon when enabled
            "stop",    # Icon when disabled
            self.get_nested_setting("resume_capability", default=True)
        )
        capabilities_section.addWidget(self.resume_toggle)
        
        # Chunk downloading
        self.chunk_widget = DynamicSpinBox(
            "Enable Chunk Downloading",
            self.get_nested_setting("chunk_downloading", default=True),
            4,  # Default chunks
            1, 16,  # Range
            " chunks",  # Suffix
            self
        )
        self.add_field(
            capabilities_section,
            "Chunk Settings:",
            self.chunk_widget,
            "Download files in multiple chunks for better performance"
        )
        
        # Retry Settings Section
        retry_section = self.add_section("Retry Settings")
        
        # Retry limit
        self.retry_limit = QSpinBox()
        self.retry_limit.setRange(0, 10)
        self.retry_limit.setValue(
            self.get_nested_setting("retry_limit", default=5)
        )
        self.add_field(
            retry_section,
            "Retry Limit:",
            self.retry_limit,
            "Number of times to retry failed downloads"
        )
        
        # Timeout Settings Section
        timeout_section = self.add_section("Timeout Settings")
        
        # Connection timeout
        self.conn_timeout = QSpinBox()
        self.conn_timeout.setRange(5, 120)
        self.conn_timeout.setSuffix(" seconds")
        self.conn_timeout.setValue(
            self.get_nested_setting("timeout_seconds", default=30)
        )
        self.add_field(
            timeout_section,
            "Connection Timeout:",
            self.conn_timeout,
            "Time to wait for connection establishment"
        )
        
        # Attempt timeout
        self.attempt_timeout = QSpinBox()
        self.attempt_timeout.setRange(30, 600)
        self.attempt_timeout.setSuffix(" seconds")
        self.attempt_timeout.setValue(
            self.get_nested_setting("attempt_timeout", default=60)
        )
        self.add_field(
            timeout_section,
            "Attempt Timeout:",
            self.attempt_timeout,
            "Time to wait for download attempt"
        )
        
        # Redirect Settings Section
        redirect_section = self.add_section("Redirect Settings")
        
        # Redirect handling
        self.redirect_combo = QComboBox()
        self.redirect_combo.addItems([
            "Automatic",
            "Manual",
            "Disabled"
        ])
        self.redirect_combo.setCurrentText(
            self.get_nested_setting("redirect_handling", default="automatic").title()
        )
        self.add_field(
            redirect_section,
            "Redirect Handling:",
            self.redirect_combo,
            "How to handle URL redirects"
        )
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
            }
            
            QSpinBox, QComboBox {
                min-width: 150px;
                padding: 4px;
                border: 1px solid palette(mid);
                border-radius: 4px;
            }
            
            QCheckBox {
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
    
    def save_settings(self):
        chunk_enabled, chunk_count = self.chunk_widget.get_value()
        
        self.set_nested_setting(self.resume_toggle.isChecked(), "resume_capability")
        self.set_nested_setting(chunk_enabled, "chunk_downloading")
        self.set_nested_setting(chunk_count, "chunk_count")
        self.set_nested_setting(self.retry_limit.value(), "retry_limit")
        self.set_nested_setting(self.conn_timeout.value(), "timeout_seconds")
        self.set_nested_setting(self.attempt_timeout.value(), "attempt_timeout")
        self.set_nested_setting(
            self.redirect_combo.currentText().lower(),
            "redirect_handling"
        )
