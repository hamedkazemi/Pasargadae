import os
import tempfile
from typing import Dict, List, Union, Optional
from pydantic import BaseModel, Field

class ProxyAuth(BaseModel):
    username: str = ""
    password: str = ""

class ProxySettings(BaseModel):
    enabled: bool = False
    server_address: str = ""
    port: int = 0
    authentication: ProxyAuth = Field(default_factory=ProxyAuth)

class FileCategoryManagement(BaseModel):
    documents: str = Field(default_factory=lambda: os.path.join(os.path.expanduser("~"), "Downloads", "Documents"))
    audio: str = Field(default_factory=lambda: os.path.join(os.path.expanduser("~"), "Downloads", "Audio"))
    video: str = Field(default_factory=lambda: os.path.join(os.path.expanduser("~"), "Downloads", "Video"))

class QueueSettings(BaseModel):
    start_time: str = "00:00"
    stop_time: str = "23:59"
    limit_active_downloads: int = 2
    post_download_action: str = "none"

class SchedulerQueues(BaseModel):
    high_priority: QueueSettings = Field(default_factory=lambda: QueueSettings(
        start_time="02:00",
        stop_time="06:00",
        limit_active_downloads=3,
        post_download_action="shutdown"
    ))
    regular: QueueSettings = Field(default_factory=lambda: QueueSettings(
        start_time="00:00",
        stop_time="23:59",
        limit_active_downloads=2,
        post_download_action="none"
    ))

class TimeSpecificLimiter(BaseModel):
    start_time: str = "08:00"
    end_time: str = "18:00"

class URLFilter(BaseModel):
    blocked: List[str] = Field(default_factory=list)
    allowed: List[str] = Field(default_factory=list)

class FileSizeFilter(BaseModel):
    min_size_mb: int = 0
    max_size_mb: int = 2048

class BrowserHotkeys(BaseModel):
    bypass_capture: str = "Alt"
    force_capture: str = "Ctrl"

class Settings(BaseModel):
    # General Settings
    general: Dict[str, Union[bool, str, List[str]]] = Field(default_factory=lambda: {
        "startup_with_system": True,
        "user_interface_language": "English",
        "notifications_enabled": True,
        "file_associations": [".exe", ".zip", ".pdf"]
    })

    # Download Settings
    download: Dict[str, Union[str, FileCategoryManagement]] = Field(default_factory=lambda: {
        "default_download_directory": os.path.join(os.path.expanduser("~"), "Downloads"),
        "temporary_folder": os.path.join(tempfile.gettempdir(), "Pasargadae"),
        "file_category_management": FileCategoryManagement(),
        "file_naming": "append_numbers_for_duplicates"
    })

    # Connection Settings
    connection: Dict[str, Union[str, int, ProxySettings]] = Field(default_factory=lambda: {
        "connection_type": "high-speed",
        "max_simultaneous_connections": 8,
        "max_active_downloads": 4,
        "proxy_settings": ProxySettings()
    })

    # Scheduler Settings
    scheduler: Dict[str, SchedulerQueues] = Field(default_factory=lambda: {
        "queues": SchedulerQueues()
    })

    # Speed Limiter Settings
    speed_limiter: Dict[str, Union[bool, str, TimeSpecificLimiter]] = Field(default_factory=lambda: {
        "enabled": True,
        "max_speed": "500 KB/s",
        "time_specific_limiter": TimeSpecificLimiter()
    })

    # Filter Settings
    filters: Dict[str, Union[List[str], URLFilter, FileSizeFilter]] = Field(default_factory=lambda: {
        "file_type_filter": [".mp4", ".jpg", ".pdf"],
        "url_filter": URLFilter(),
        "file_size_filter": FileSizeFilter()
    })

    # Browser Integration Settings
    browser_integration: Dict[str, Union[List[str], bool, BrowserHotkeys]] = Field(default_factory=lambda: {
        "enabled_browsers": ["Chrome", "Firefox", "Edge"],
        "url_sniffer": True,
        "hotkeys": BrowserHotkeys()
    })

    # Advanced Download Settings
    advanced_download: Dict[str, Union[bool, int, str]] = Field(default_factory=lambda: {
        "resume_capability": True,
        "chunk_downloading": True,
        "retry_limit": 5,
        "timeout_seconds": 30,
        "redirect_handling": "automatic"
    })

    # Notification Settings
    notifications: Dict[str, Union[bool, str]] = Field(default_factory=lambda: {
        "visual_notifications": True,
        "sound_alerts": True,
        "email_notifications": False,
        "email_address": ""
    })

    # Security Settings
    security: Dict[str, Union[bool, str]] = Field(default_factory=lambda: {
        "antivirus_scanning": True,
        "custom_commands": "",
        "pre_scan_command": "",
        "post_scan_command": ""
    })

    # Logging Settings
    logging: Dict[str, Union[bool, int]] = Field(default_factory=lambda: {
        "download_log": True,
        "history_management_days": 30,
        "clear_data_on_exit": False
    })

    # Integrity Settings
    integrity_checking: Dict[str, Union[bool, str]] = Field(default_factory=lambda: {
        "hash_verification": True,
        "checksum_algorithm": "MD5",
        "verification_mode": "auto_verify"
    })
