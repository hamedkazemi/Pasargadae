from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QSpinBox, QComboBox,
    QLineEdit, QPushButton, QCheckBox,
    QFrame
)
from PyQt6.QtCore import Qt
from .base_tab import SettingsTab

class ExpandableSection(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.expanded = False
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        self.toggle = QCheckBox(title)
        self.toggle.stateChanged.connect(self.on_toggle)
        header_layout.addWidget(self.toggle)
        
        layout.addWidget(header)
        
        # Content
        self.content = QWidget()
        self.content.hide()
        layout.addWidget(self.content)
        
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 10, 10, 10)
    
    def on_toggle(self, state: int):
        self.expanded = bool(state)
        self.content.setVisible(self.expanded)
    
    def add_widget(self, widget: QWidget):
        self.content_layout.addWidget(widget)
    
    def isChecked(self) -> bool:
        return self.toggle.isChecked()

class ConnectionSettingsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "connection", parent)
    
    def _setup_ui(self):
        # Connection Type Section
        connection_section = self.add_section("Connection Settings")
        
        # Connection type dropdown
        self.connection_type = QComboBox()
        self.connection_type.addItems([
            "High-Speed",
            "DSL",
            "4G",
            "Dial-up"
        ])
        self.connection_type.setCurrentText(
            self.get_nested_setting("connection_type", default="high-speed")
                .replace("-", " ").title()
        )
        self.add_field(
            connection_section,
            "Connection Type:",
            self.connection_type,
            "Select your connection type to optimize download performance"
        )
        
        # Max connections spinbox
        self.max_connections = QSpinBox()
        self.max_connections.setRange(1, 16)
        self.max_connections.setValue(
            self.get_nested_setting("max_simultaneous_connections", default=8)
        )
        self.add_field(
            connection_section,
            "Max Simultaneous Connections:",
            self.max_connections,
            "Maximum number of connections per download"
        )
        
        # Max downloads spinbox
        self.max_downloads = QSpinBox()
        self.max_downloads.setRange(1, 10)
        self.max_downloads.setValue(
            self.get_nested_setting("max_active_downloads", default=4)
        )
        self.add_field(
            connection_section,
            "Max Active Downloads:",
            self.max_downloads,
            "Maximum number of downloads running at once"
        )
        
        # Proxy Settings Section
        proxy_section = self.add_section("Proxy Settings")
        
        self.proxy_settings = ExpandableSection("Enable Proxy")
        proxy_section.addWidget(self.proxy_settings)
        
        # Server address
        self.proxy_server = QLineEdit(
            self.get_nested_setting("proxy_settings", "server_address", default="")
        )
        self.proxy_settings.add_widget(
            self.add_field(
                QVBoxLayout(),
                "Server Address:",
                self.proxy_server,
                "Enter proxy server address (e.g., proxy.example.com)"
            ).parent()
        )
        
        # Port
        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(0, 65535)
        self.proxy_port.setValue(
            self.get_nested_setting("proxy_settings", "port", default=0)
        )
        self.proxy_settings.add_widget(
            self.add_field(
                QVBoxLayout(),
                "Port:",
                self.proxy_port,
                "Enter proxy server port"
            ).parent()
        )
        
        # Authentication
        auth_widget = QWidget()
        auth_layout = QHBoxLayout(auth_widget)
        auth_layout.setContentsMargins(0, 0, 0, 0)
        
        self.proxy_username = QLineEdit(
            self.get_nested_setting("proxy_settings", "authentication", "username", default="")
        )
        self.proxy_password = QLineEdit(
            self.get_nested_setting("proxy_settings", "authentication", "password", default="")
        )
        self.proxy_password.setEchoMode(QLineEdit.EchoMode.Password)
        
        auth_layout.addWidget(QLabel("Username:"))
        auth_layout.addWidget(self.proxy_username)
        auth_layout.addWidget(QLabel("Password:"))
        auth_layout.addWidget(self.proxy_password)
        
        self.proxy_settings.add_widget(auth_widget)
        
        # Test connection button
        test_btn = QPushButton("Test Connection")
        test_btn.clicked.connect(self.test_proxy_connection)
        self.proxy_settings.add_widget(test_btn)
        
        # Set initial proxy state
        self.proxy_settings.toggle.setChecked(
            self.get_nested_setting("proxy_settings", "enabled", default=False)
        )
    
    def test_proxy_connection(self):
        # TODO: Implement proxy connection testing
        pass
    
    def save_settings(self):
        self.set_nested_setting(
            self.connection_type.currentText().lower().replace(" ", "-"),
            "connection_type"
        )
        self.set_nested_setting(
            self.max_connections.value(),
            "max_simultaneous_connections"
        )
        self.set_nested_setting(
            self.max_downloads.value(),
            "max_active_downloads"
        )
        
        # Save proxy settings
        proxy_settings = {
            "enabled": self.proxy_settings.isChecked(),
            "server_address": self.proxy_server.text(),
            "port": self.proxy_port.value(),
            "authentication": {
                "username": self.proxy_username.text(),
                "password": self.proxy_password.text()
            }
        }
        self.set_nested_setting(proxy_settings, "proxy_settings")
