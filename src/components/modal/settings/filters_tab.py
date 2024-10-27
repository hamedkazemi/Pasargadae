from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem, QSpinBox
)
from PyQt6.QtCore import Qt
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class URLListWidget(QWidget):
    def __init__(self, urls: list[str], parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add new URL controls
        add_layout = QHBoxLayout()
        self.new_url_input = QLineEdit()
        self.new_url_input.setPlaceholderText("Enter URL (e.g., example.com)")
        
        self.add_button = QPushButton()
        self.add_button.setIcon(IconProvider.get_icon("add_url"))
        self.add_button.setFixedSize(28, 28)
        self.add_button.clicked.connect(self.add_url)
        
        add_layout.addWidget(self.new_url_input)
        add_layout.addWidget(self.add_button)
        
        layout.addLayout(add_layout)
        
        # URL list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # Add initial URLs
        for url in urls:
            self.add_list_item(url)
        
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: rgba(128, 128, 128, 0.1);
            }
        """)
    
    def add_url(self):
        url = self.new_url_input.text().strip()
        if url and not self.item_exists(url):
            self.add_list_item(url)
            self.new_url_input.clear()
    
    def add_list_item(self, url: str):
        item = QListWidgetItem(url)
        
        # Create item widget with delete button
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # URL label
        label = QLabel(url)
        layout.addWidget(label)
        
        # Delete button
        delete_btn = QPushButton()
        delete_btn.setIcon(IconProvider.get_icon("delete"))
        delete_btn.setFixedSize(24, 24)
        delete_btn.clicked.connect(lambda: self.remove_item(item))
        
        layout.addStretch()
        layout.addWidget(delete_btn)
        
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item_widget)
    
    def item_exists(self, url: str) -> bool:
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).text() == url:
                return True
        return False
    
    def remove_item(self, item: QListWidgetItem):
        self.list_widget.takeItem(self.list_widget.row(item))
    
    def get_urls(self) -> list[str]:
        return [self.list_widget.item(i).text() 
                for i in range(self.list_widget.count())]

class FiltersTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "filters", parent)
    
    def _setup_ui(self):
        # File Type Filter Section
        file_type_section = self.add_section("File Type Filter")
        
        self.file_types = URLListWidget(
            self.get_nested_setting("file_type_filter", default=[])
        )
        file_type_section.addWidget(self.file_types)
        
        # URL Filter Section
        url_section = self.add_section("URL Filter")
        
        # Blocked URLs
        blocked_label = QLabel("Blocked URLs")
        blocked_label.setObjectName("subsectionTitle")
        url_section.addWidget(blocked_label)
        
        self.blocked_urls = URLListWidget(
            self.get_nested_setting("url_filter", "blocked", default=[])
        )
        url_section.addWidget(self.blocked_urls)
        
        # Allowed URLs
        allowed_label = QLabel("Allowed URLs")
        allowed_label.setObjectName("subsectionTitle")
        url_section.addWidget(allowed_label)
        
        self.allowed_urls = URLListWidget(
            self.get_nested_setting("url_filter", "allowed", default=[])
        )
        url_section.addWidget(self.allowed_urls)
        
        # File Size Filter Section
        size_section = self.add_section("File Size Filter")
        
        # Min size
        self.min_size = QSpinBox()
        self.min_size.setRange(0, 100000)
        self.min_size.setSuffix(" MB")
        self.min_size.setValue(
            self.get_nested_setting("file_size_filter", "min_size_mb", default=0)
        )
        self.add_field(
            size_section,
            "Minimum Size:",
            self.min_size,
            "Minimum file size to download (0 for no limit)"
        )
        
        # Max size
        self.max_size = QSpinBox()
        self.max_size.setRange(0, 100000)
        self.max_size.setSuffix(" MB")
        self.max_size.setValue(
            self.get_nested_setting("file_size_filter", "max_size_mb", default=2048)
        )
        self.add_field(
            size_section,
            "Maximum Size:",
            self.max_size,
            "Maximum file size to download (0 for no limit)"
        )
        
        self.setStyleSheet("""
            QLabel#subsectionTitle {
                font-weight: bold;
                color: #666;
                margin-top: 10px;
            }
            
            QListWidget {
                border: 1px solid palette(mid);
                border-radius: 4px;
                padding: 5px;
            }
            
            QListWidget::item {
                padding: 5px;
                border-radius: 4px;
            }
            
            QListWidget::item:hover {
                background-color: rgba(128, 128, 128, 0.1);
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
    
    def save_settings(self):
        self.set_nested_setting(self.file_types.get_urls(), "file_type_filter")
        
        url_filter = {
            "blocked": self.blocked_urls.get_urls(),
            "allowed": self.allowed_urls.get_urls()
        }
        self.set_nested_setting(url_filter, "url_filter")
        
        file_size_filter = {
            "min_size_mb": self.min_size.value(),
            "max_size_mb": self.max_size.value()
        }
        self.set_nested_setting(file_size_filter, "file_size_filter")
