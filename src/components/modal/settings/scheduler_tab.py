from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QComboBox,
    QPushButton, QTimeEdit, QFrame
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QColor
from .base_tab import SettingsTab

class QueueCard(QWidget):
    def __init__(self, queue_settings: dict, accent_color: str, parent=None):
        super().__init__(parent)
        self.accent_color = QColor(accent_color)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Time settings
        time_widget = QWidget()
        time_layout = QHBoxLayout(time_widget)
        time_layout.setContentsMargins(0, 0, 0, 0)
        
        # Start time
        start_label = QLabel("Start Time:")
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime.fromString(queue_settings["start_time"], "HH:mm"))
        self.start_time.setDisplayFormat("hh:mm AP")
        
        # Stop time
        stop_label = QLabel("Stop Time:")
        self.stop_time = QTimeEdit()
        self.stop_time.setTime(QTime.fromString(queue_settings["stop_time"], "HH:mm"))
        self.stop_time.setDisplayFormat("hh:mm AP")
        
        time_layout.addWidget(start_label)
        time_layout.addWidget(self.start_time)
        time_layout.addWidget(stop_label)
        time_layout.addWidget(self.stop_time)
        
        layout.addWidget(time_widget)
        
        # Download limit
        limit_widget = QWidget()
        limit_layout = QHBoxLayout(limit_widget)
        limit_layout.setContentsMargins(0, 0, 0, 0)
        
        limit_label = QLabel("Active Downloads Limit:")
        self.limit_spin = QSpinBox()
        self.limit_spin.setRange(1, 10)
        self.limit_spin.setValue(queue_settings["limit_active_downloads"])
        
        limit_layout.addWidget(limit_label)
        limit_layout.addWidget(self.limit_spin)
        limit_layout.addStretch()
        
        layout.addWidget(limit_widget)
        
        # Post-download action
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(0, 0, 0, 0)
        
        action_label = QLabel("Post-Download Action:")
        self.action_combo = QComboBox()
        self.action_combo.addItems([
            "None",
            "Shutdown",
            "Sleep",
            "Hibernate",
            "Disconnect Internet"
        ])
        self.action_combo.setCurrentText(queue_settings["post_download_action"].title())
        
        action_layout.addWidget(action_label)
        action_layout.addWidget(self.action_combo)
        action_layout.addStretch()
        
        layout.addWidget(action_widget)
        
        # Styling
        self.setStyleSheet(f"""
            QWidget {{
                background-color: rgba({self.accent_color.red()}, 
                                     {self.accent_color.green()}, 
                                     {self.accent_color.blue()}, 
                                     0.1);
                border-radius: 8px;
            }}
            QTimeEdit, QSpinBox, QComboBox {{
                background-color: palette(base);
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 4px;
                min-width: 100px;
            }}
        """)
    
    def get_settings(self) -> dict:
        return {
            "start_time": self.start_time.time().toString("HH:mm"),
            "stop_time": self.stop_time.time().toString("HH:mm"),
            "limit_active_downloads": self.limit_spin.value(),
            "post_download_action": self.action_combo.currentText().lower()
        }

class SchedulerSettingsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "scheduler", parent)
    
    def _setup_ui(self):
        # Queue Management Section
        queue_section = self.add_section("Queue Management")
        
        # High Priority Queue
        high_priority_settings = self.get_nested_setting("queues", "high_priority")
        self.high_priority_queue = QueueCard(
            high_priority_settings,
            "#E91E63",  # Pink accent
            self
        )
        queue_section.addWidget(self.high_priority_queue)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        queue_section.addWidget(separator)
        
        # Regular Queue
        regular_settings = self.get_nested_setting("queues", "regular")
        self.regular_queue = QueueCard(
            regular_settings,
            "#2196F3",  # Blue accent
            self
        )
        queue_section.addWidget(self.regular_queue)
    
    def save_settings(self):
        queues = {
            "high_priority": self.high_priority_queue.get_settings(),
            "regular": self.regular_queue.get_settings()
        }
        self.set_nested_setting(queues, "queues")
