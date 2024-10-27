from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QCheckBox, QSpinBox,
    QPushButton, QDialog, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class LogViewerDialog(QDialog):
    def __init__(self, log_type: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"{log_type} Viewer")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Log display
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        # Button row
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton()
        refresh_btn.setIcon(IconProvider.get_icon("resume"))
        refresh_btn.setFixedSize(28, 28)
        refresh_btn.clicked.connect(self.refresh_logs)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Load initial logs
        self.refresh_logs()
        
        self.setStyleSheet("""
            QTextEdit {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 4px;
            }
            
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 4px;
            }
            
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.1);
            }
        """)
    
    def refresh_logs(self):
        # TODO: Implement actual log loading
        self.log_text.setText("Sample log content would appear here...")

class ClearDataDialog(QDialog):
    def __init__(self, data_type: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Clear Data")
        
        layout = QVBoxLayout(self)
        
        # Warning icon
        icon_label = QLabel()
        icon_label.setPixmap(IconProvider.get_icon("delete").pixmap(32, 32))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # Warning message
        msg = QLabel(
            f"Are you sure you want to clear {data_type}?\n"
            "This action cannot be undone."
        )
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet("background-color: #dc3545; color: white;")
        clear_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
                margin: 10px;
            }
            
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                border: none;
            }
            
            QPushButton:hover {
                opacity: 0.9;
            }
        """)

class LoggingTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "logging", parent)
    
    def _setup_ui(self):
        # Download Log Section
        log_section = self.add_section("Download Log")
        
        log_widget = QWidget()
        log_layout = QHBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        
        self.enable_log = QCheckBox()
        self.enable_log.setChecked(
            self.get_nested_setting("download_log", default=True)
        )
        
        view_log_btn = QPushButton()
        view_log_btn.setIcon(IconProvider.get_icon("document"))
        view_log_btn.setFixedSize(28, 28)
        view_log_btn.clicked.connect(lambda: self.view_logs("Download"))
        
        log_layout.addWidget(self.enable_log)
        log_layout.addWidget(view_log_btn)
        log_layout.addStretch()
        
        self.add_field(
            log_section,
            "Enable Logging:",
            log_widget,
            "Keep a detailed log of all download activities"
        )
        
        # History Management Section
        history_section = self.add_section("History Management")
        
        self.history_days = QSpinBox()
        self.history_days.setRange(1, 365)
        self.history_days.setValue(
            self.get_nested_setting("history_management_days", default=30)
        )
        self.history_days.setSuffix(" days")
        self.add_field(
            history_section,
            "Keep History For:",
            self.history_days,
            "Number of days to keep download history"
        )
        
        # Clear Data Section
        clear_section = self.add_section("Clear Data")
        
        # Clear buttons
        clear_layout = QHBoxLayout()
        
        clear_logs_btn = QPushButton("Clear Logs")
        clear_logs_btn.clicked.connect(lambda: self.clear_data("logs"))
        
        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.clicked.connect(lambda: self.clear_data("history"))
        
        clear_temp_btn = QPushButton("Clear Temporary Data")
        clear_temp_btn.clicked.connect(lambda: self.clear_data("temporary data"))
        
        clear_layout.addWidget(clear_logs_btn)
        clear_layout.addWidget(clear_history_btn)
        clear_layout.addWidget(clear_temp_btn)
        
        clear_widget = QWidget()
        clear_widget.setLayout(clear_layout)
        clear_section.addWidget(clear_widget)
        
        self.setStyleSheet("""
            QLabel {
                color: palette(text);
            }
            
            QSpinBox {
                padding: 4px;
                border: 1px solid palette(mid);
                border-radius: 4px;
                min-width: 100px;
            }
            
            QPushButton {
                padding: 6px 12px;
                border-radius: 4px;
                border: 1px solid palette(mid);
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
    
    def view_logs(self, log_type: str):
        dialog = LogViewerDialog(log_type, self)
        dialog.exec()
    
    def clear_data(self, data_type: str):
        dialog = ClearDataDialog(data_type, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # TODO: Implement actual data clearing
            QMessageBox.information(
                self,
                "Data Cleared",
                f"{data_type.title()} have been cleared successfully."
            )
    
    def save_settings(self):
        self.set_nested_setting(self.enable_log.isChecked(), "download_log")
        self.set_nested_setting(self.history_days.value(), "history_management_days")
        self.set_nested_setting(False, "clear_data_on_exit")
