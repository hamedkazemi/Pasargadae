from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QComboBox,
    QFileDialog
)
from .base_tab import SettingsTab
from src.utils.icon_provider import IconProvider

class CategoryWidget(QWidget):
    def __init__(self, category: str, path: str, icon_name: str, parent=None):
        super().__init__(parent)
        self.category = category
        self.path = path
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(IconProvider.get_icon(icon_name).pixmap(24, 24))
        layout.addWidget(icon_label)
        
        # Category name
        name_label = QLabel(category.title())
        name_label.setMinimumWidth(100)
        layout.addWidget(name_label)
        
        # Path
        self.path_edit = QLineEdit(path)
        self.path_edit.setReadOnly(True)
        layout.addWidget(self.path_edit)
        
        # Browse button
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_path)
        layout.addWidget(browse_btn)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_category)
        layout.addWidget(edit_btn)
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(128, 128, 128, 0.1);
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: transparent;
                border: 1px solid rgba(128, 128, 128, 0.3);
                border-radius: 3px;
                padding: 3px 10px;
            }
            QPushButton:hover {
                background-color: rgba(128, 128, 128, 0.1);
            }
        """)
    
    def browse_path(self):
        path = QFileDialog.getExistingDirectory(
            self, f"Select {self.category.title()} Directory"
        )
        if path:
            self.path_edit.setText(path)
    
    def edit_category(self):
        # TODO: Implement category editing dialog
        pass
    
    def get_path(self) -> str:
        return self.path_edit.text()

class DownloadSettingsTab(SettingsTab):
    def __init__(self, settings: dict, parent=None):
        super().__init__(settings, "download", parent)
    
    def _setup_ui(self):
        # Download Paths Section
        paths_section = self.add_section("Download Paths")
        
        # Default download directory
        download_widget, self.download_path = self.create_browse_widget(
            self.get_nested_setting("default_download_directory"),
            self.browse_download_path
        )
        self.add_field(
            paths_section,
            "Default Download Directory:",
            download_widget,
            "Choose where downloaded files will be saved by default"
        )
        
        # Temporary folder
        temp_widget, self.temp_path = self.create_browse_widget(
            self.get_nested_setting("temporary_folder"),
            self.browse_temp_path
        )
        self.add_field(
            paths_section,
            "Temporary Folder:",
            temp_widget,
            "Location for temporary files during download"
        )
        
        # File Categories Section
        categories_section = self.add_section("File Categories")
        
        self.categories = {}
        category_icons = {
            "documents": "document",
            "audio": "music",
            "video": "video"
        }
        
        category_management = self.get_nested_setting("file_category_management", default={})
        for category, icon in category_icons.items():
            path = category_management.get(category, "")
            category_widget = CategoryWidget(category, path, icon, self)
            self.categories[category] = category_widget
            categories_section.addWidget(category_widget)
        
        # File Naming Section
        naming_section = self.add_section("File Naming")
        
        self.naming_combo = QComboBox()
        self.naming_combo.addItems([
            "Append Numbers",
            "Overwrite",
            "Ask",
            "Skip"
        ])
        current_naming = self.get_nested_setting("file_naming", default="append_numbers")
        self.naming_combo.setCurrentText(current_naming.replace("_", " ").title())
        self.add_field(
            naming_section,
            "Duplicate Files:",
            self.naming_combo,
            "Choose how to handle duplicate file names"
        )
    
    def browse_download_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        if path:
            self.download_path.setText(path)
    
    def browse_temp_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Temporary Directory")
        if path:
            self.temp_path.setText(path)
    
    def save_settings(self):
        self.set_nested_setting(self.download_path.text(), "default_download_directory")
        self.set_nested_setting(self.temp_path.text(), "temporary_folder")
        
        # Save category management settings
        category_settings = {
            category: widget.get_path()
            for category, widget in self.categories.items()
        }
        self.set_nested_setting(category_settings, "file_category_management")
        
        # Save file naming settings
        self.set_nested_setting(
            self.naming_combo.currentText().lower().replace(" ", "_"),
            "file_naming"
        )
