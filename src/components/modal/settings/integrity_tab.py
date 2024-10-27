from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, 
    QCheckBox, QComboBox, QPushButton,
    QLineEdit
)
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class HashPreviewWidget(QWidget):
    def __init__(self, hash_type: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Hash display
        self.hash_display = QLineEdit()
        self.hash_display.setReadOnly(True)
        self.hash_display.setPlaceholderText(f"Sample {hash_type} hash will appear here")
        
        # Preview button
        preview_btn = QPushButton()
        preview_btn.setIcon(IconProvider.get_icon("check"))
        preview_btn.setFixedSize(28, 28)
        preview_btn.clicked.connect(self.show_preview)
        
        layout.addWidget(self.hash_display)
        layout.addWidget(preview_btn)
    
    def show_preview(self):
        # Show a sample hash based on the algorithm
        sample_hashes = {
            "MD5": "d41d8cd98f00b204e9800998ecf8427e",
            "SHA-1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "SHA-256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "SHA-512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce"
        }
        self.hash_display.setText(sample_hashes.get(self.parent().hash_algo.currentText(), ""))

class IntegrityTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "integrity_checking", parent)
    
    def _setup_ui(self):
        # Hash Verification Section
        hash_section = self.add_section("Hash Verification")
        
        self.hash_enabled = QCheckBox()
        self.hash_enabled.setChecked(
            self.get_nested_setting("hash_verification", default=True)
        )
        self.add_field(
            hash_section,
            "Enable Verification:",
            self.hash_enabled,
            "Verify file integrity using hash checksums"
        )
        
        # Algorithm selection
        self.hash_algo = QComboBox()
        self.hash_algo.addItems([
            "MD5",
            "SHA-1",
            "SHA-256",
            "SHA-512"
        ])
        self.hash_algo.setCurrentText(
            self.get_nested_setting("checksum_algorithm", default="MD5")
        )
        self.hash_algo.currentTextChanged.connect(self.update_hash_preview)
        self.add_field(
            hash_section,
            "Hash Algorithm:",
            self.hash_algo,
            "Select the hash algorithm to use for verification"
        )
        
        # Hash preview
        self.hash_preview = HashPreviewWidget(self.hash_algo.currentText())
        self.add_field(
            hash_section,
            "Preview:",
            self.hash_preview,
            "Preview of the selected hash algorithm"
        )
        
        # Verification Settings Section
        verify_section = self.add_section("Verification Settings")
        
        # Verification mode
        self.verify_mode = QComboBox()
        self.verify_mode.addItems([
            "Auto-Verify",
            "Manual",
            "Ask Each Time"
        ])
        self.verify_mode.setCurrentText(
            self.get_nested_setting("verification_mode", default="Auto-Verify")
        )
        self.add_field(
            verify_section,
            "Verification Mode:",
            self.verify_mode,
            "Choose when to perform integrity checks"
        )
        
        # Help text
        help_text = QLabel(
            "Hash verification helps ensure downloaded files haven't been "
            "corrupted or tampered with during transfer. The process compares "
            "the file's hash checksum with the expected value."
        )
        help_text.setWordWrap(True)
        help_text.setStyleSheet("color: gray;")
        verify_section.addWidget(help_text)
        
        # Update enabled states
        self.hash_enabled.stateChanged.connect(self.update_fields_enabled)
        self.update_fields_enabled(self.hash_enabled.isChecked())
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
            }
            
            QLineEdit, QComboBox {
                padding: 4px;
                border: 1px solid palette(mid);
                border-radius: 4px;
                min-width: 200px;
            }
            
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.1);
            }
            
            QCheckBox {
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
    
    def update_fields_enabled(self, enabled: bool):
        self.hash_algo.setEnabled(enabled)
        self.hash_preview.setEnabled(enabled)
        self.verify_mode.setEnabled(enabled)
    
    def update_hash_preview(self, algorithm: str):
        self.hash_preview.show_preview()
    
    def save_settings(self):
        self.set_nested_setting(self.hash_enabled.isChecked(), "hash_verification")
        self.set_nested_setting(self.hash_algo.currentText(), "checksum_algorithm")
        self.set_nested_setting(
            self.verify_mode.currentText().lower().replace("-", "_"),
            "verification_mode"
        )
