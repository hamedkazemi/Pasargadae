from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QWidget,
    QProgressBar, QHBoxLayout, QPushButton,
    QHeaderView, QMenu, QStyle
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from typing import Optional, Dict, List
import os
from ...models.download import Download, DownloadStatus
from ...utils.icon_provider import IconProvider
from ...theme.styles import Styles

class DownloadTableWidget(QTableWidget):
    # Signals
    download_action = pyqtSignal(str, str)  # (action, download_id)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_dark = True
        self.downloads = {}  # id -> Download
        self.setup_ui()
    
    def setup_ui(self):
        # Set columns
        columns = [
            "Name", "Status", "Progress", "Speed", 
            "Size", "Remaining", "Actions"
        ]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)
        
        # Set column widths
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Name
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)    # Status
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)    # Progress
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)    # Speed
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)    # Size
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)    # Remaining
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)    # Actions
        
        header.setDefaultSectionSize(100)
        header.resizeSection(2, 150)  # Progress bar needs more space
        
        # Style
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.verticalHeader().hide()
        
        # Context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # Apply initial theme
        self.apply_theme()
    
    def apply_theme(self):
        styles = Styles.get_styles(self._is_dark)
        self.setStyleSheet(styles["TABLE"])
    
    def update_theme(self, is_dark: bool):
        """Update the theme of the table."""
        self._is_dark = is_dark
        self.apply_theme()
        
        # Update action buttons
        for row in range(self.rowCount()):
            actions_widget = self.cellWidget(row, 6)
            if actions_widget:
                for button in actions_widget.findChildren(QPushButton):
                    icon_name = button.property("icon_name")
                    if icon_name:
                        button.setIcon(IconProvider.get_icon(icon_name, is_dark))
    
    def add_download(self, download: Download):
        """Add or update a download in the table."""
        if download.id in self.downloads:
            self.update_download(download)
            return
        
        self.downloads[download.id] = download
        row = self.rowCount()
        self.insertRow(row)
        
        # Name
        name_item = QTableWidgetItem(os.path.basename(download.save_path))
        name_item.setData(Qt.ItemDataRole.UserRole, download.id)
        self.setItem(row, 0, name_item)
        
        # Status
        status_item = QTableWidgetItem(download.status.value.title())
        self.setItem(row, 1, status_item)
        
        # Progress
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(int(download.progress))
        self.setCellWidget(row, 2, progress_bar)
        
        # Speed
        speed_item = QTableWidgetItem(self.format_speed(download.speed))
        self.setItem(row, 3, speed_item)
        
        # Size
        size_item = QTableWidgetItem(self.format_size(download.total_size))
        self.setItem(row, 4, size_item)
        
        # Remaining
        remaining_item = QTableWidgetItem("")  # Will be updated
        self.setItem(row, 5, remaining_item)
        
        # Actions
        actions_widget = self.create_actions_widget(download)
        self.setCellWidget(row, 6, actions_widget)
    
    def update_download(self, download: Download):
        """Update an existing download in the table."""
        row = self.find_download_row(download.id)
        if row is None:
            return
        
        # Update status
        self.item(row, 1).setText(download.status.value.title())
        
        # Update progress
        progress_bar = self.cellWidget(row, 2)
        progress_bar.setValue(int(download.progress))
        
        # Update speed
        self.item(row, 3).setText(self.format_speed(download.speed))
        
        # Update size
        self.item(row, 4).setText(self.format_size(download.total_size))
        
        # Update remaining
        if download.speed > 0 and download.total_size:
            remaining = (download.total_size - download.downloaded_size) / download.speed
            self.item(row, 5).setText(self.format_time(remaining))
        else:
            self.item(row, 5).setText("")
        
        # Update actions
        self.cellWidget(row, 6).update_buttons(download)
    
    def remove_download(self, download_id: str):
        """Remove a download from the table."""
        row = self.find_download_row(download_id)
        if row is not None:
            self.removeRow(row)
            del self.downloads[download_id]
    
    def find_download_row(self, download_id: str) -> Optional[int]:
        """Find the row index for a download ID."""
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item.data(Qt.ItemDataRole.UserRole) == download_id:
                return row
        return None
    
    def create_actions_widget(self, download: Download) -> QWidget:
        """Create the actions widget for a download."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Start/Pause button
        start_pause_btn = QPushButton()
        start_pause_btn.setFixedSize(24, 24)
        start_pause_btn.clicked.connect(
            lambda: self.download_action.emit(
                "pause" if download.status == DownloadStatus.DOWNLOADING else "resume",
                download.id
            )
        )
        
        # Stop button
        stop_btn = QPushButton()
        stop_btn.setFixedSize(24, 24)
        stop_btn.setIcon(IconProvider.get_icon("stop", self._is_dark))
        stop_btn.setProperty("icon_name", "stop")
        stop_btn.clicked.connect(
            lambda: self.download_action.emit("stop", download.id)
        )
        
        layout.addWidget(start_pause_btn)
        layout.addWidget(stop_btn)
        
        # Update initial button states
        widget.update_buttons = lambda d: self.update_action_buttons(
            start_pause_btn, stop_btn, d
        )
        widget.update_buttons(download)
        
        return widget
    
    def update_action_buttons(self, start_pause_btn: QPushButton, 
                            stop_btn: QPushButton, download: Download):
        """Update action button states based on download status."""
        if download.status == DownloadStatus.DOWNLOADING:
            start_pause_btn.setIcon(IconProvider.get_icon("pause", self._is_dark))
            start_pause_btn.setProperty("icon_name", "pause")
            start_pause_btn.setEnabled(True)
            stop_btn.setEnabled(True)
        elif download.status == DownloadStatus.PAUSED:
            start_pause_btn.setIcon(IconProvider.get_icon("resume", self._is_dark))
            start_pause_btn.setProperty("icon_name", "resume")
            start_pause_btn.setEnabled(True)
            stop_btn.setEnabled(True)
        elif download.status == DownloadStatus.QUEUED:
            start_pause_btn.setIcon(IconProvider.get_icon("resume", self._is_dark))
            start_pause_btn.setProperty("icon_name", "resume")
            start_pause_btn.setEnabled(True)
            stop_btn.setEnabled(True)
        elif download.status == DownloadStatus.COMPLETED:
            start_pause_btn.setEnabled(False)
            stop_btn.setEnabled(False)
        else:  # ERROR or other states
            start_pause_btn.setIcon(IconProvider.get_icon("resume", self._is_dark))
            start_pause_btn.setProperty("icon_name", "resume")
            start_pause_btn.setEnabled(True)
            stop_btn.setEnabled(True)
    
    def show_context_menu(self, position):
        """Show context menu for download actions."""
        item = self.itemAt(position)
        if not item:
            return
        
        row = item.row()
        download_id = self.item(row, 0).data(Qt.ItemDataRole.UserRole)
        download = self.downloads[download_id]
        
        menu = QMenu(self)
        
        # Add actions based on download status
        if download.status == DownloadStatus.DOWNLOADING:
            menu.addAction("Pause", lambda: self.download_action.emit("pause", download_id))
        elif download.status in [DownloadStatus.PAUSED, DownloadStatus.ERROR]:
            menu.addAction("Resume", lambda: self.download_action.emit("resume", download_id))
        
        menu.addAction("Stop", lambda: self.download_action.emit("stop", download_id))
        menu.addSeparator()
        menu.addAction("Remove", lambda: self.download_action.emit("remove", download_id))
        
        # Show menu
        menu.exec(self.viewport().mapToGlobal(position))
    
    @staticmethod
    def format_size(size: Optional[int]) -> str:
        """Format size in bytes to human readable string."""
        if size is None:
            return "Unknown"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    @staticmethod
    def format_speed(speed: float) -> str:
        """Format speed in bytes/second to human readable string."""
        if speed == 0:
            return ""
        return f"{DownloadTableWidget.format_size(speed)}/s"
    
    @staticmethod
    def format_time(seconds: float) -> str:
        """Format time in seconds to human readable string."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds/60)}m {int(seconds%60)}s"
        else:
            hours = int(seconds/3600)
            minutes = int((seconds%3600)/60)
            return f"{hours}h {minutes}m"
