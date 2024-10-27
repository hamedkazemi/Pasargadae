from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QApplication, QCheckBox,
    QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from .modal_window import ModalWindow
from src.utils.icon_provider import IconProvider
from src.core.download_manager import DownloadManager
from src.settings.manager import SettingsManager
from src.utils.async_helper import AsyncHelper
from src.utils.logger import Logger
from src.settings.schema import FileCategoryManagement
from src.models.download import Download, DownloadStatus
from pySmartDL import SmartDL
import os
import mimetypes
from urllib.parse import urlparse
import asyncio

class DownloadInfoWidget(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setup_ui()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)
        
        # File info
        layout.addWidget(QLabel("File Name:"), 0, 0)
        self.file_name_label = QLabel()
        layout.addWidget(self.file_name_label, 0, 1)
        
        layout.addWidget(QLabel("Size:"), 1, 0)
        self.size_label = QLabel()
        layout.addWidget(self.size_label, 1, 1)
        
        layout.addWidget(QLabel("Category:"), 2, 0)
        self.category_label = QLabel()
        layout.addWidget(self.category_label, 2, 1)
        
        # Style labels
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                if widget.text().endswith(':'):
                    widget.setStyleSheet("color: #9BA1A6;")  # Secondary text color
    
    def update_info(self, file_name="", size="", category=""):
        self.file_name_label.setText(file_name)
        self.size_label.setText(size)
        self.category_label.setText(category)

class DownloadModal(ModalWindow):
    def __init__(self, parent=None, download_manager=None, settings_manager=None):
        Logger.debug("Initializing DownloadModal")
        super().__init__(
            parent=parent,
            title="Add New Download",
            width=500,
            height=300
        )
        
        # Initialize managers with defaults if not provided
        self.download_manager = download_manager or DownloadManager({
            "connection": {"max_active_downloads": 4},
            "download": {
                "default_download_directory": os.path.expanduser("~/Downloads"),
                "temporary_folder": os.path.join(os.path.expanduser("~"), ".pasargadae", "temp")
            },
            "advanced_download": {
                "chunk_count": 4,
                "timeout_seconds": 30,
                "retry_limit": 3
            },
            "integrity_checking": {
                "hash_verification": True,
                "checksum_algorithm": "MD5"
            },
            "speed_limiter": {
                "enabled": False,
                "max_speed": "500 KB/s"
            }
        })
        self.settings_manager = settings_manager or SettingsManager(
            os.path.join(os.path.expanduser("~"), ".pasargadae", "settings.json")
        )
        Logger.debug("Managers initialized")
        
        # Create async helper
        self.async_helper = AsyncHelper(self)
        self.async_helper.finished.connect(self._on_async_finished)
        self.async_helper.error.connect(self._on_async_error)
        
        # Create content widget
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(10)
        
        # URL input section
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL or paste from clipboard")
        self.preview_btn = QPushButton("Preview")
        self.preview_btn.setFixedWidth(80)
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.preview_btn)
        layout.addLayout(url_layout)
        
        # Download info section
        self.info_widget = DownloadInfoWidget(parent=self)
        layout.addWidget(self.info_widget)
        
        # Options section
        options_layout = QVBoxLayout()
        self.remember_path_cb = QCheckBox("Remember this path for category")
        options_layout.addWidget(self.remember_path_cb)
        layout.addLayout(options_layout)
        
        # Add stretch to push everything up
        layout.addStretch()
        
        # Set the content
        self.set_content(content)
        
        # Add action buttons
        self.add_action_button("Cancel", self.close)
        self.start_btn = self.add_action_button("Start Download", self._start_download_clicked, primary=True)
        self.start_btn.setEnabled(False)  # Disable until URL is valid
        
        # Connect signals
        self.url_input.textChanged.connect(self.on_url_changed)
        self.preview_btn.clicked.connect(self._preview_clicked)
        
        # Load URL from clipboard if available
        self.load_from_clipboard()

        # Store preview info
        self._preview_info = None
        
        Logger.debug("DownloadModal initialized")
    
    def load_from_clipboard(self):
        Logger.debug("Loading URL from clipboard")
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text and (text.startswith('http://') or text.startswith('https://')):
            Logger.info(f"Found URL in clipboard: {text}")
            self.url_input.setText(text)
            self._preview_clicked()
    
    def on_url_changed(self, text):
        Logger.debug(f"URL changed: {text}")
        is_valid = text.startswith('http://') or text.startswith('https://')
        self.preview_btn.setEnabled(is_valid)
        self.start_btn.setEnabled(is_valid)
    
    def _get_file_category(self, mime_type: str) -> str:
        """Determine file category based on MIME type."""
        Logger.debug(f"Getting category for MIME type: {mime_type}")
        if mime_type.startswith('video/'):
            return "video"
        elif mime_type.startswith('audio/'):
            return "audio"
        elif mime_type.startswith('image/'):
            return "image"
        elif mime_type.startswith('text/'):
            return "documents"
        elif mime_type in ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed']:
            return "documents"
        elif mime_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return "documents"
        else:
            return "other"
    
    def _get_category_display_name(self, category: str) -> str:
        """Get display name for category."""
        return category.title()
    
    def _format_size(self, size_in_bytes: int) -> str:
        """Format file size to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.1f} PB"
    
    def _get_save_path(self, file_name: str, category: str) -> str:
        """Get save path based on category and settings."""
        Logger.debug(f"Getting save path for file: {file_name}, category: {category}")
        
        # Get category management settings
        download_settings = self.settings_manager.get_setting("download", None)
        if not download_settings:
            Logger.warning("No download settings found, using default directory")
            return os.path.join(self.download_manager.default_directory, file_name)
        
        file_category_management = download_settings.get("file_category_management")
        if not isinstance(file_category_management, FileCategoryManagement):
            Logger.debug("Creating new FileCategoryManagement instance")
            file_category_management = FileCategoryManagement()
        
        if category in ["video", "audio", "documents"]:
            # Use category-specific path if available
            base_dir = getattr(file_category_management, category)
            Logger.debug(f"Using category-specific path: {base_dir}")
        else:
            # Fall back to default directory
            base_dir = self.download_manager.default_directory
            Logger.debug(f"Using default directory: {base_dir}")
        
        # Create directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        return os.path.join(base_dir, file_name)
    
    def _preview_clicked(self):
        """Handle preview button click."""
        Logger.debug("Preview button clicked")
        try:
            self.async_helper.run_async(self.preview_download())
        except Exception as e:
            Logger.exception("Error starting preview")
            self._on_async_error(e)
    
    def _start_download_clicked(self):
        """Handle start download button click."""
        Logger.debug("Start download button clicked")
        try:
            self.async_helper.run_async(self.start_download())
        except Exception as e:
            Logger.exception("Error starting download")
            self._on_async_error(e)
    
    def _on_async_finished(self, result):
        """Handle async operation completion."""
        Logger.debug(f"Async operation completed: {result}")
        try:
            if isinstance(result, dict) and 'action' in result:
                if result['action'] == 'preview':
                    self.info_widget.update_info(
                        file_name=result['file_name'],
                        size=result['size'],
                        category=result['category']
                    )
                elif result['action'] == 'start':
                    self.close()
        except Exception as e:
            Logger.exception("Error handling async completion")
            self._on_async_error(e)
    
    def _on_async_error(self, error):
        """Handle async operation error."""
        Logger.error(f"Async operation failed: {error}")
        if isinstance(error, Exception):
            self.info_widget.update_info(
                file_name=f"Error: {str(error)}",
                size="Unknown",
                category="Error"
            )
    
    
    async def preview_download(self):
        """Preview download information."""
        url = self.url_input.text()
        if not url:
            Logger.warning("No URL provided for preview")
            return
        
        Logger.info(f"Previewing download for URL: {url}")
        try:
            # Initialize SmartDL to get file info
            temp_file = os.path.join(self.download_manager.temp_directory, "preview_temp")
            Logger.debug(f"Using temp file: {temp_file}")
            
            # Create SmartDL object
            obj = SmartDL(url, temp_file, progress_bar=False)
            Logger.debug("SmartDL object created")
            
            # Start download in non-blocking mode to get info
            obj.start(blocking=False)
            Logger.debug("SmartDL started in non-blocking mode")
            
            # Wait briefly for file info
            await asyncio.sleep(1)
            
            # Get file info
            file_name = os.path.basename(urlparse(url).path) or "unnamed_file"
            file_size = obj.get_dl_size()
            Logger.debug(f"File info: name={file_name}, size={file_size}")
            
            # Stop the download since we only needed info
            obj.stop()
            Logger.debug("SmartDL stopped")
            
            # Clean up temp file if it was created
            if os.path.exists(temp_file):
                os.remove(temp_file)
                Logger.debug("Temp file removed")
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                mime_type = 'application/octet-stream'
            Logger.debug(f"MIME type: {mime_type}")
            
            # Get category
            category = self._get_file_category(mime_type)
            Logger.debug(f"Category: {category}")
            
            # Store preview info for later use
            self._preview_info = {
                'file_name': file_name,
                'size': file_size,
                'mime_type': mime_type,
                'category': category
            }
            
            result = {
                'action': 'preview',
                'file_name': file_name,
                'size': self._format_size(file_size),
                'category': self._get_category_display_name(category)
            }
            Logger.debug(f"Preview completed: {result}")
            return result
            
        except Exception as e:
            Logger.exception("Error previewing download")
            raise Exception(f"Error previewing file: {str(e)}")
    
    async def start_download(self):
        """Start the download process."""
        url = self.url_input.text()
        if not url or not self._preview_info:
            Logger.warning("Cannot start download: missing URL or preview info")
            return
        
        Logger.info(f"Starting download for URL: {url}")
        try:
            # Get save path based on category
            save_path = self._get_save_path(
                self._preview_info['file_name'],
                self._preview_info['category']
            )
            Logger.debug(f"Save path: {save_path}")
            
            # Create download object
            download = Download(
                url=url,
                save_path=save_path,
                status=DownloadStatus.QUEUED,
                total_size=self._preview_info['size']
            )
            Logger.debug("Download object created")
            
            # Add download to manager
            download = await self.download_manager.add_download(
                url=url,
                save_path=save_path
            )
            Logger.info(f"Download added with ID: {download.id}")
            
            # Start download
            await self.download_manager.start_download(download.id)
            Logger.info(f"Download started: {download.id}")
            
            # Remember path if checkbox is checked
            if self.remember_path_cb.isChecked():
                category = self._preview_info['category']
                if category in ["video", "audio", "documents"]:
                    # Get current settings
                    download_settings = self.settings_manager.get_setting("download", {})
                    file_category_management = download_settings.get("file_category_management", FileCategoryManagement())
                    
                    # Update category path
                    setattr(file_category_management, category, os.path.dirname(save_path))
                    download_settings["file_category_management"] = file_category_management
                    
                    # Save settings
                    self.settings_manager.set_setting("download", "file_category_management", file_category_management)
                    self.settings_manager.save_settings()
                    Logger.info(f"Updated category path for {category}: {save_path}")
            
            return {'action': 'start'}
            
        except Exception as e:
            Logger.exception("Error starting download")
            raise Exception(f"Error starting download: {str(e)}")
        self.preview_btn.clicked.connect(self._preview_clicked)
        
        # Load URL from clipboard if available
        self.load_from_clipboard()

        # Store preview info
        self._preview_info = None
        
        Logger.debug("DownloadModal initialized")
    
    def load_from_clipboard(self):
        Logger.debug("Loading URL from clipboard")
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text and (text.startswith('http://') or text.startswith('https://')):
            Logger.info(f"Found URL in clipboard: {text}")
            self.url_input.setText(text)
            self._preview_clicked()
    
    def on_url_changed(self, text):
        Logger.debug(f"URL changed: {text}")
        is_valid = text.startswith('http://') or text.startswith('https://')
        self.preview_btn.setEnabled(is_valid)
        self.start_btn.setEnabled(is_valid)
    
    def _get_file_category(self, mime_type: str) -> str:
        """Determine file category based on MIME type."""
        Logger.debug(f"Getting category for MIME type: {mime_type}")
        if mime_type.startswith('video/'):
            return "video"
        elif mime_type.startswith('audio/'):
            return "audio"
        elif mime_type.startswith('image/'):
            return "image"
        elif mime_type.startswith('text/'):
            return "documents"
        elif mime_type in ['application/zip', 'application/x-rar-compressed', 'application/x-7z-compressed']:
            return "documents"
        elif mime_type in ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return "documents"
        else:
            return "other"
    
    def _get_category_display_name(self, category: str) -> str:
        """Get display name for category."""
        return category.title()
    
    def _format_size(self, size_in_bytes: int) -> str:
        """Format file size to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024:
                return f"{size_in_bytes:.1f} {unit}"
            size_in_bytes /= 1024
        return f"{size_in_bytes:.1f} PB"
    
    def _get_save_path(self, file_name: str, category: str) -> str:
        """Get save path based on category and settings."""
        Logger.debug(f"Getting save path for file: {file_name}, category: {category}")
        
        # Get category management settings
        download_settings = self.settings_manager.get_setting("download", None)
        if not download_settings:
            Logger.warning("No download settings found, using default directory")
            return os.path.join(self.download_manager.default_directory, file_name)
        
        file_category_management = download_settings.get("file_category_management")
        if not isinstance(file_category_management, FileCategoryManagement):
            Logger.debug("Creating new FileCategoryManagement instance")
            file_category_management = FileCategoryManagement()
        
        if category in ["video", "audio", "documents"]:
            # Use category-specific path if available
            base_dir = getattr(file_category_management, category)
            Logger.debug(f"Using category-specific path: {base_dir}")
        else:
            # Fall back to default directory
            base_dir = self.download_manager.default_directory
            Logger.debug(f"Using default directory: {base_dir}")
        
        # Create directory if it doesn't exist
        os.makedirs(base_dir, exist_ok=True)
        
        return os.path.join(base_dir, file_name)
    
    def _preview_clicked(self):
        """Handle preview button click."""
        Logger.debug("Preview button clicked")
        try:
            self.async_helper.run_async(self.preview_download())
        except Exception as e:
            Logger.exception("Error starting preview")
            self._on_async_error(e)
    
    def _start_download_clicked(self):
        """Handle start download button click."""
        Logger.debug("Start download button clicked")
        try:
            self.async_helper.run_async(self.start_download())
        except Exception as e:
            Logger.exception("Error starting download")
            self._on_async_error(e)
    
    def _on_async_finished(self, result):
        """Handle async operation completion."""
        Logger.debug(f"Async operation completed: {result}")
        try:
            if isinstance(result, dict) and 'action' in result:
                if result['action'] == 'preview':
                    self.info_widget.update_info(
                        file_name=result['file_name'],
                        size=result['size'],
                        category=result['category']
                    )
                elif result['action'] == 'start':
                    self.close()
        except Exception as e:
            Logger.exception("Error handling async completion")
            self._on_async_error(e)
    
    def _on_async_error(self, error):
        """Handle async operation error."""
        Logger.error(f"Async operation failed: {error}")
        if isinstance(error, Exception):
            self.info_widget.update_info(
                file_name=f"Error: {str(error)}",
                size="Unknown",
                category="Error"
            )
    
    
    async def preview_download(self):
        """Preview download information."""
        url = self.url_input.text()
        if not url:
            Logger.warning("No URL provided for preview")
            return
        
        Logger.info(f"Previewing download for URL: {url}")
        try:
            # Initialize SmartDL to get file info
            temp_file = os.path.join(self.download_manager.temp_directory, "preview_temp")
            Logger.debug(f"Using temp file: {temp_file}")
            
            # Create SmartDL object
            obj = SmartDL(url, temp_file, progress_bar=False)
            Logger.debug("SmartDL object created")
            
            # Start download in non-blocking mode to get info
            obj.start(blocking=False)
            Logger.debug("SmartDL started in non-blocking mode")
            
            # Wait briefly for file info
            await asyncio.sleep(1)
            
            # Get file info
            file_name = os.path.basename(urlparse(url).path) or "unnamed_file"
            file_size = obj.get_dl_size()
            Logger.debug(f"File info: name={file_name}, size={file_size}")
            
            # Stop the download since we only needed info
            obj.stop()
            Logger.debug("SmartDL stopped")
            
            # Clean up temp file if it was created
            if os.path.exists(temp_file):
                os.remove(temp_file)
                Logger.debug("Temp file removed")
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                mime_type = 'application/octet-stream'
            Logger.debug(f"MIME type: {mime_type}")
            
            # Get category
            category = self._get_file_category(mime_type)
            Logger.debug(f"Category: {category}")
            
            # Store preview info for later use
            self._preview_info = {
                'file_name': file_name,
                'size': file_size,
                'mime_type': mime_type,
                'category': category
            }
            
            result = {
                'action': 'preview',
                'file_name': file_name,
                'size': self._format_size(file_size),
                'category': self._get_category_display_name(category)
            }
            Logger.debug(f"Preview completed: {result}")
            return result
            
        except Exception as e:
            Logger.exception("Error previewing download")
            raise Exception(f"Error previewing file: {str(e)}")
    
    async def start_download(self):
        """Start the download process."""
        url = self.url_input.text()
        if not url or not self._preview_info:
            Logger.warning("Cannot start download: missing URL or preview info")
            return
        
        Logger.info(f"Starting download for URL: {url}")
        try:
            # Get save path based on category
            save_path = self._get_save_path(
                self._preview_info['file_name'],
                self._preview_info['category']
            )
            Logger.debug(f"Save path: {save_path}")
            
            # Create download object
            download = Download(
                url=url,
                save_path=save_path,
                status=DownloadStatus.QUEUED,
                total_size=self._preview_info['size']
            )
            Logger.debug("Download object created")
            
            # Add download to manager
            download = await self.download_manager.add_download(
                url=url,
                save_path=save_path
            )
            Logger.info(f"Download added with ID: {download.id}")
            
            # Start download
            await self.download_manager.start_download(download.id)
            Logger.info(f"Download started: {download.id}")
            
            # Remember path if checkbox is checked
            if self.remember_path_cb.isChecked():
                category = self._preview_info['category']
                if category in ["video", "audio", "documents"]:
                    # Get current settings
                    download_settings = self.settings_manager.get_setting("download", {})
                    file_category_management = download_settings.get("file_category_management", FileCategoryManagement())
                    
                    # Update category path
                    setattr(file_category_management, category, os.path.dirname(save_path))
                    download_settings["file_category_management"] = file_category_management
                    
                    # Save settings
                    self.settings_manager.set_setting("download", "file_category_management", file_category_management)
                    self.settings_manager.save_settings()
                    Logger.info(f"Updated category path for {category}: {save_path}")
            
            return {'action': 'start'}
            
        except Exception as e:
            Logger.exception("Error starting download")
            raise Exception(f"Error starting download: {str(e)}")
