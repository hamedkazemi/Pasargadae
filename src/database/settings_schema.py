CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

DEFAULT_SETTINGS = [
    # General Settings
    ("startup_with_system", "true", "general"),
    ("user_interface_language", "English", "general"),
    ("notifications_enabled", "true", "general"),
    ("file_associations", '".exe,.zip,.pdf"', "general"),
    ("start_notification", "true", "general"),
    ("completion_notification", "true", "general"),
    ("error_notification", "true", "general"),
    
    # Download Settings
    ("default_download_directory", "", "download"),  # Set programmatically
    ("temporary_folder", "", "download"),  # Set programmatically
    ("file_naming", "append_numbers", "download"),
    
    # Connection Settings
    ("connection_type", "high-speed", "connection"),
    ("max_simultaneous_connections", "8", "connection"),
    ("max_active_downloads", "4", "connection"),
    ("proxy_enabled", "false", "connection"),
    ("proxy_server", "", "connection"),
    ("proxy_port", "0", "connection"),
    ("proxy_username", "", "connection"),
    ("proxy_password", "", "connection"),
    
    # Scheduler Settings
    ("high_priority_start", "02:00", "scheduler"),
    ("high_priority_stop", "06:00", "scheduler"),
    ("high_priority_limit", "3", "scheduler"),
    ("high_priority_action", "shutdown", "scheduler"),
    ("regular_start", "00:00", "scheduler"),
    ("regular_stop", "23:59", "scheduler"),
    ("regular_limit", "2", "scheduler"),
    ("regular_action", "none", "scheduler"),
    
    # Speed Limiter
    ("speed_limit_enabled", "true", "speed"),
    ("max_speed", "500", "speed"),
    ("time_specific_start", "08:00", "speed"),
    ("time_specific_end", "18:00", "speed"),
    
    # File Type and URL Filters
    ("file_type_filter", '".mp4,.jpg,.pdf"', "filters"),
    ("blocked_urls", '["example.com"]', "filters"),
    ("allowed_urls", '["trusted.com"]', "filters"),
    ("min_size_mb", "0", "filters"),
    ("max_size_mb", "2048", "filters"),
    
    # Browser Integration
    ("browser_chrome", "true", "browser"),
    ("browser_firefox", "true", "browser"),
    ("browser_edge", "true", "browser"),
    ("url_sniffer", "true", "browser"),
    ("bypass_capture_hotkey", "Alt", "browser"),
    ("force_capture_hotkey", "Ctrl", "browser"),
    
    # Advanced Download
    ("resume_capability", "true", "advanced"),
    ("chunk_downloading", "true", "advanced"),
    ("retry_limit", "5", "advanced"),
    ("timeout_seconds", "30", "advanced"),
    ("redirect_handling", "automatic", "advanced"),
    
    # Notifications
    ("visual_notifications", "true", "notifications"),
    ("sound_alerts", "true", "notifications"),
    ("email_notifications", "false", "notifications"),
    ("email_address", "", "notifications"),
    
    # Security
    ("antivirus_scanning", "true", "security"),
    ("custom_commands", "", "security"),
    
    # Logging
    ("download_log", "true", "logging"),
    ("history_management_days", "30", "logging"),
    ("clear_data_on_exit", "false", "logging"),
    
    # Integrity
    ("hash_verification", "true", "integrity"),
    ("checksum_algorithm", "MD5", "integrity")
]
