from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QWidget, QLabel,
    QVBoxLayout, QListWidget, QPushButton,
    QHBoxLayout, QLineEdit, QListWidgetItem
)
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class FileTypeList(QWidget):
    def __init__(self, file_types: list[str], parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # File type list
        self.list_widget = QListWidget()
        
        # Add new type controls
        add_layout = QHBoxLayout()
        self.new_type_input = QLineEdit()
        self.new_type_input.setPlaceholderText("Enter file type (e.g., .pdf)")
        
        self.add_button = QPushButton()
        self.add_button.setIcon(IconProvider.get_icon("add_url"))
        self.add_button.setFixedSize(28, 28)
        self.add_button.clicked.connect(self.add_file_type)
        
        add_layout.addWidget(self.new_type_input)
        add_layout.addWidget(self.add_button)
        
        layout.addLayout(add_layout)
        layout.addWidget(self.list_widget)
        
        # Add initial items
        for file_type in file_types:
            self.add_list_item(file_type)
        
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
    
    def add_file_type(self):
        file_type = self.new_type_input.text().strip()
        if file_type:
            if not file_type.startswith('.'):
                file_type = '.' + file_type
            if not self.item_exists(file_type):
                self.add_list_item(file_type)
                self.new_type_input.clear()
    
    def add_list_item(self, file_type: str):
        item = QListWidgetItem(file_type)
        
        # Create item widget with delete button
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(IconProvider.get_icon("document").pixmap(16, 16))
        layout.addWidget(icon_label)
        
        # File type label
        label = QLabel(file_type)
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
    
    def item_exists(self, file_type: str) -> bool:
        for i in range(self.list_widget.count()):
            if self.list_widget.item(i).text() == file_type:
                return True
        return False
    
    def remove_item(self, item: QListWidgetItem):
        self.list_widget.takeItem(self.list_widget.row(item))
    
    def get_file_types(self) -> list[str]:
        return [self.list_widget.item(i).text() 
                for i in range(self.list_widget.count())]

class GeneralSettingsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "general", parent)
    
    def _setup_ui(self):
        # System Integration Section
        system_section = self.add_section("System Integration")
        
        self.startup_checkbox = self.add_field(
            system_section,
            "Start with System:",
            QCheckBox(),
            "Launch application automatically when system starts"
        )
        self.startup_checkbox.setChecked(
            self.get_nested_setting("startup_with_system", default=True)
        )
        
        # Language Section
        language_section = self.add_section("Language")
        
        languages = ["English", "Spanish", "French", "German"]
        self.language_combo = self.add_field(
            language_section,
            "Interface Language:",
            QComboBox(),
            "Select the language for the user interface"
        )
        self.language_combo.addItems(languages)
        self.language_combo.setCurrentText(
            self.get_nested_setting("user_interface_language", default="English")
        )
        
        # Notifications Section
        notif_section = self.add_section("Notifications")
        
        self.notifications_checkbox = self.add_field(
            notif_section,
            "Enable Notifications:",
            QCheckBox(),
            "Show notifications for download events"
        )
        self.notifications_checkbox.setChecked(
            self.get_nested_setting("notifications_enabled", default=True)
        )
        
        # File Associations Section
        file_section = self.add_section("File Associations")
        
        self.file_types = FileTypeList(
            self.get_nested_setting("file_associations", default=[".exe", ".zip", ".pdf"])
        )
        file_section.addWidget(self.file_types)
    
    def save_settings(self):
        self.set_nested_setting(self.startup_checkbox.isChecked(), "startup_with_system")
        self.set_nested_setting(self.language_combo.currentText(), "user_interface_language")
        self.set_nested_setting(self.notifications_checkbox.isChecked(), "notifications_enabled")
        self.set_nested_setting(self.file_types.get_file_types(), "file_associations")
