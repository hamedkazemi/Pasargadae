from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, 
    QCheckBox, QComboBox, QPushButton,
    QLineEdit
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
import os
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class SoundPreviewWidget(QWidget):
    def __init__(self, sound_name: str, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.combo = QComboBox()
        self.combo.addItems([
            "Default",
            "Ding",
            "Chime",
            "Alert",
            "Custom..."
        ])
        self.combo.setCurrentText(sound_name)
        
        self.preview_btn = QPushButton()
        self.preview_btn.setIcon(IconProvider.get_icon("music"))
        self.preview_btn.setFixedSize(28, 28)
        self.preview_btn.clicked.connect(self.play_sound)
        
        layout.addWidget(self.combo)
        layout.addWidget(self.preview_btn)
        
        # Sound effect player
        self.sound = QSoundEffect()
    
    def play_sound(self):
        sound_name = self.combo.currentText()
        if sound_name != "Custom...":
            # In a real app, you would load the actual sound file
            sound_path = os.path.join("assets", "sounds", f"{sound_name.lower()}.wav")
            self.sound.setSource(QUrl.fromLocalFile(sound_path))
            self.sound.play()
    
    def get_sound(self) -> str:
        return self.combo.currentText()

class NotificationsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "notifications", parent)
    
    def _setup_ui(self):
        # Visual Notifications Section
        visual_section = self.add_section("Visual Notifications")
        
        self.visual_notify = QCheckBox()
        self.visual_notify.setChecked(
            self.get_nested_setting("visual_notifications", default=True)
        )
        self.add_field(
            visual_section,
            "Enable Pop-ups:",
            self.visual_notify,
            "Show pop-up notifications for download events"
        )
        
        # Preview image
        preview = QLabel()
        preview.setPixmap(IconProvider.get_icon("notifications").pixmap(200, 100))
        preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        visual_section.addWidget(preview)
        
        # Sound Alerts Section
        sound_section = self.add_section("Sound Alerts")
        
        self.sound_enabled = QCheckBox()
        self.sound_enabled.setChecked(
            self.get_nested_setting("sound_alerts", default=True)
        )
        self.add_field(
            sound_section,
            "Enable Sounds:",
            self.sound_enabled,
            "Play sounds for download events"
        )
        
        # Sound settings for different events
        events = {
            "Start": "Default",
            "Complete": "Chime",
            "Error": "Alert"
        }
        
        self.sound_widgets = {}
        for event, default_sound in events.items():
            widget = SoundPreviewWidget(
                self.get_nested_setting("sounds", event.lower(), default=default_sound)
            )
            self.add_field(
                sound_section,
                f"{event} Sound:",
                widget,
                f"Sound to play when download {event.lower()}s"
            )
            self.sound_widgets[event.lower()] = widget
        
        # Email Notifications Section
        email_section = self.add_section("Email Notifications")
        
        self.email_enabled = QCheckBox()
        self.email_enabled.setChecked(
            self.get_nested_setting("email_notifications", default=False)
        )
        self.add_field(
            email_section,
            "Enable Email:",
            self.email_enabled,
            "Send email notifications for download events"
        )
        
        # Email settings
        self.email_address = QLineEdit(
            self.get_nested_setting("email_address", default="")
        )
        self.email_address.setPlaceholderText("Enter email address")
        self.add_field(
            email_section,
            "Email Address:",
            self.email_address,
            "Address to send notifications to"
        )
        
        # Update enabled states
        self.sound_enabled.stateChanged.connect(self.update_sound_enabled)
        self.email_enabled.stateChanged.connect(self.email_address.setEnabled)
        
        self.update_sound_enabled(self.sound_enabled.isChecked())
        self.email_address.setEnabled(self.email_enabled.isChecked())
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
            }
            
            QLineEdit, QComboBox {
                min-width: 200px;
                padding: 4px;
                border: 1px solid palette(mid);
                border-radius: 4px;
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
    
    def update_sound_enabled(self, enabled: bool):
        for widget in self.sound_widgets.values():
            widget.setEnabled(enabled)
    
    def save_settings(self):
        self.set_nested_setting(self.visual_notify.isChecked(), "visual_notifications")
        self.set_nested_setting(self.sound_enabled.isChecked(), "sound_alerts")
        
        sounds = {
            event: widget.get_sound()
            for event, widget in self.sound_widgets.items()
        }
        self.set_nested_setting(sounds, "sounds")
        
        self.set_nested_setting(self.email_enabled.isChecked(), "email_notifications")
        self.set_nested_setting(self.email_address.text(), "email_address")
