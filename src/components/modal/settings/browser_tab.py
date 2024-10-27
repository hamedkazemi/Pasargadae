from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCheckBox, QPushButton,
    QLineEdit, QDialog
)
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QKeySequence
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class HotkeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Hotkey")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(
            "Press the key combination you want to use.\n"
            "Press Esc to cancel."
        )
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instructions)
        
        # Current key display
        self.key_label = QLabel("Press a key...")
        self.key_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.key_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: rgba(128, 128, 128, 0.1);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.key_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        self.ok_btn = QPushButton("OK")
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.ok_btn)
        
        layout.addLayout(button_layout)
        
        self.key_sequence = None
        self.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Escape:
                self.reject()
                return True
            
            modifiers = event.modifiers()
            self.key_sequence = QKeySequence(key | int(modifiers))
            self.key_label.setText(self.key_sequence.toString())
            self.ok_btn.setEnabled(True)
            return True
        return super().eventFilter(obj, event)

class HotkeyWidget(QWidget):
    def __init__(self, initial_key: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.key_edit = QLineEdit(initial_key)
        self.key_edit.setReadOnly(True)
        
        set_btn = QPushButton("Set")
        set_btn.clicked.connect(self.show_hotkey_dialog)
        
        layout.addWidget(self.key_edit)
        layout.addWidget(set_btn)
    
    def show_hotkey_dialog(self):
        dialog = HotkeyDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.key_sequence:
            self.key_edit.setText(dialog.key_sequence.toString())
    
    def get_hotkey(self) -> str:
        return self.key_edit.text()

class BrowserTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "browser_integration", parent)
    
    def _setup_ui(self):
        # Browser Extensions Section
        browser_section = self.add_section("Browser Integration")
        
        browsers = [
            ("Chrome", "chrome"),
            ("Firefox", "firefox"),
            ("Edge", "edge")
        ]
        
        enabled_browsers = self.get_nested_setting("enabled_browsers", default=[])
        self.browser_checkboxes = {}
        
        for name, icon_key in browsers:
            checkbox = QCheckBox()
            checkbox.setChecked(name in enabled_browsers)
            
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
            icon_label = QLabel()
            icon_label.setPixmap(IconProvider.get_icon(icon_key).pixmap(24, 24))
            layout.addWidget(icon_label)
            layout.addWidget(QLabel(name))
            layout.addStretch()
            layout.addWidget(checkbox)
            
            self.browser_checkboxes[name] = checkbox
            browser_section.addWidget(container)
        
        # URL Sniffer Section
        sniffer_section = self.add_section("URL Sniffer")
        
        self.url_sniffer = QCheckBox()
        self.url_sniffer.setChecked(
            self.get_nested_setting("url_sniffer", default=True)
        )
        self.add_field(
            sniffer_section,
            "Enable URL Sniffer:",
            self.url_sniffer,
            "Automatically detect downloadable links from web pages"
        )
        
        # Hotkeys Section
        hotkeys_section = self.add_section("Hotkeys")
        
        self.bypass_hotkey = HotkeyWidget(
            self.get_nested_setting("hotkeys", "bypass_capture", default="Alt")
        )
        self.add_field(
            hotkeys_section,
            "Bypass Capture:",
            self.bypass_hotkey,
            "Key combination to temporarily disable URL capture"
        )
        
        self.force_hotkey = HotkeyWidget(
            self.get_nested_setting("hotkeys", "force_capture", default="Ctrl")
        )
        self.add_field(
            hotkeys_section,
            "Force Capture:",
            self.force_hotkey,
            "Key combination to force URL capture"
        )
    
    def save_settings(self):
        enabled_browsers = [
            name for name, checkbox in self.browser_checkboxes.items()
            if checkbox.isChecked()
        ]
        self.set_nested_setting(enabled_browsers, "enabled_browsers")
        
        self.set_nested_setting(self.url_sniffer.isChecked(), "url_sniffer")
        
        hotkeys = {
            "bypass_capture": self.bypass_hotkey.get_hotkey(),
            "force_capture": self.force_hotkey.get_hotkey()
        }
        self.set_nested_setting(hotkeys, "hotkeys")
