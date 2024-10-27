from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QCheckBox,
    QTimeEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QTime
from .base_tab import SettingsTab

class TimeGrid(QWidget):
    def __init__(self, schedule: dict = None, parent=None):
        super().__init__(parent)
        self.schedule = schedule or {}
        
        layout = QGridLayout(self)
        layout.setSpacing(1)
        
        # Create header row (hours)
        for hour in range(24):
            label = QLabel(f"{hour:02d}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, 0, hour + 1)
        
        # Create days rows
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.cells = {}
        
        for row, day in enumerate(days, 1):
            # Add day label
            label = QLabel(day)
            layout.addWidget(label, row, 0)
            
            # Add checkboxes for each hour
            for hour in range(24):
                cell = QCheckBox()
                cell.setFixedSize(20, 20)
                if day in self.schedule and hour in self.schedule[day]:
                    cell.setChecked(True)
                layout.addWidget(cell, row, hour + 1)
                self.cells[(day, hour)] = cell
        
        self.setStyleSheet("""
            QLabel {
                padding: 2px 5px;
            }
            QCheckBox {
                background-color: rgba(128, 128, 128, 0.1);
                border-radius: 3px;
            }
            QCheckBox:checked {
                background-color: #2196F3;
            }
        """)
    
    def get_schedule(self) -> dict:
        schedule = {}
        for (day, hour), cell in self.cells.items():
            if cell.isChecked():
                if day not in schedule:
                    schedule[day] = []
                schedule[day].append(hour)
        return schedule

class SpeedLimiterTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "speed_limiter", parent)
    
    def _setup_ui(self):
        # Enable Speed Limiter Section
        enable_section = self.add_section("Speed Limiter")
        
        self.enable_limiter = QCheckBox()
        self.enable_limiter.setChecked(
            self.get_nested_setting("enabled", default=True)
        )
        self.add_field(
            enable_section,
            "Enable Speed Limiter:",
            self.enable_limiter,
            "Limit download speed to conserve bandwidth"
        )
        
        # Speed Limit Settings
        speed_section = self.add_section("Speed Settings")
        
        self.speed_limit = QSpinBox()
        self.speed_limit.setRange(1, 10000)
        self.speed_limit.setSuffix(" KB/s")
        current_speed = self.get_nested_setting("max_speed", default="500 KB/s")
        self.speed_limit.setValue(int(current_speed.split()[0]))
        self.add_field(
            speed_section,
            "Speed Limit:",
            self.speed_limit,
            "Maximum download speed in kilobytes per second"
        )
        
        # Time-Specific Settings
        time_section = self.add_section("Time-Specific Limits")
        
        time_widget = QWidget()
        time_layout = QHBoxLayout(time_widget)
        time_layout.setContentsMargins(0, 0, 0, 0)
        
        # Start time
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime.fromString(
            self.get_nested_setting("time_specific_limiter", "start_time", default="08:00"),
            "HH:mm"
        ))
        self.add_field(
            time_layout,
            "Start Time:",
            self.start_time
        )
        
        # End time
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime.fromString(
            self.get_nested_setting("time_specific_limiter", "end_time", default="18:00"),
            "HH:mm"
        ))
        self.add_field(
            time_layout,
            "End Time:",
            self.end_time
        )
        
        time_section.addWidget(time_widget)
        
        # Schedule Grid
        schedule_section = self.add_section("Weekly Schedule")
        self.schedule_grid = TimeGrid(
            self.get_nested_setting("schedule", default={})
        )
        schedule_section.addWidget(self.schedule_grid)
        
        # Update enabled states
        self.enable_limiter.stateChanged.connect(self.update_fields_enabled)
        self.update_fields_enabled(self.enable_limiter.isChecked())
    
    def update_fields_enabled(self, enabled: bool):
        self.speed_limit.setEnabled(enabled)
        self.start_time.setEnabled(enabled)
        self.end_time.setEnabled(enabled)
        self.schedule_grid.setEnabled(enabled)
    
    def save_settings(self):
        self.set_nested_setting(self.enable_limiter.isChecked(), "enabled")
        self.set_nested_setting(f"{self.speed_limit.value()} KB/s", "max_speed")
        
        time_specific = {
            "start_time": self.start_time.time().toString("HH:mm"),
            "end_time": self.end_time.time().toString("HH:mm")
        }
        self.set_nested_setting(time_specific, "time_specific_limiter")
        
        self.set_nested_setting(self.schedule_grid.get_schedule(), "schedule")
