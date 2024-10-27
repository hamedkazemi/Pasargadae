import sqlite3
import json
import os
import tempfile
from .settings_schema import CREATE_SETTINGS_TABLE, DEFAULT_SETTINGS

class SettingsRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.initialize_database()
    
    def initialize_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create settings table
            cursor.execute(CREATE_SETTINGS_TABLE)
            
            # Check if settings exist
            cursor.execute("SELECT COUNT(*) FROM settings")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Initialize with default settings
                default_settings = list(DEFAULT_SETTINGS)
                
                # Set system-specific paths
                downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
                temp_dir = os.path.join(tempfile.gettempdir(), "Pasargadae")
                
                # Add paths to default settings
                default_settings.extend([
                    ("default_download_directory", downloads_dir, "download"),
                    ("temporary_folder", temp_dir, "download"),
                    # Add file category management settings
                    ("file_category_management_documents", 
                     os.path.join(downloads_dir, "Documents"), "download"),
                    ("file_category_management_audio", 
                     os.path.join(downloads_dir, "Audio"), "download"),
                    ("file_category_management_video", 
                     os.path.join(downloads_dir, "Video"), "download"),
                    # Add proxy settings
                    ("proxy_enabled", "false", "connection"),
                    ("proxy_server", "", "connection"),
                    ("proxy_port", "0", "connection"),
                    ("proxy_username", "", "connection"),
                    ("proxy_password", "", "connection")
                ])
                
                # Insert all default settings
                cursor.executemany(
                    "INSERT INTO settings (key, value, category) VALUES (?, ?, ?)",
                    default_settings
                )
                conn.commit()
    
    def get_all_settings(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value, category FROM settings")
            settings = {}
            
            for key, value, category in cursor.fetchall():
                if category not in settings:
                    settings[category] = {}
                
                # Handle nested settings
                if key.startswith("file_category_management_"):
                    if "file_category_management" not in settings["download"]:
                        settings["download"]["file_category_management"] = {}
                    sub_key = key.replace("file_category_management_", "")
                    settings["download"]["file_category_management"][sub_key] = value
                    continue
                elif key.startswith("proxy_"):
                    if "proxy_settings" not in settings["connection"]:
                        settings["connection"]["proxy_settings"] = {
                            "enabled": False,
                            "server_address": "",
                            "port": 0,
                            "authentication": {
                                "username": "",
                                "password": ""
                            }
                        }
                    if key == "proxy_enabled":
                        settings["connection"]["proxy_settings"]["enabled"] = value.lower() == "true"
                    elif key == "proxy_server":
                        settings["connection"]["proxy_settings"]["server_address"] = value
                    elif key == "proxy_port":
                        settings["connection"]["proxy_settings"]["port"] = int(value) if value.isdigit() else 0
                    elif key == "proxy_username":
                        settings["connection"]["proxy_settings"]["authentication"]["username"] = value
                    elif key == "proxy_password":
                        settings["connection"]["proxy_settings"]["authentication"]["password"] = value
                    continue
                
                # Convert string representations to Python objects
                if key in ["file_associations", "file_type_filter"]:
                    value = value.split(",") if value and value != '[]' else []
                elif key in ["blocked_urls", "allowed_urls"]:
                    try:
                        value = json.loads(value) if value and value != '[]' else []
                    except json.JSONDecodeError:
                        value = []
                elif value and value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                elif value and value.isdigit():
                    value = int(value)
                elif not value:  # Handle empty values
                    if key in ["file_associations", "file_type_filter", "blocked_urls", "allowed_urls"]:
                        value = []
                    elif key.endswith("_enabled") or key.startswith("startup_"):
                        value = False
                    elif key.endswith("_limit") or key.endswith("_count"):
                        value = 0
                    else:
                        value = ""
                
                settings[category][key] = value
            
            # Ensure all required settings categories exist
            required_categories = {
                "general", "download", "connection", "scheduler", "speed_limiter",
                "filters", "browser_integration", "advanced_download", "notifications",
                "security", "logging", "integrity_checking"
            }
            
            for category in required_categories:
                if category not in settings:
                    settings[category] = {}
            
            # Ensure file_category_management exists
            if "download" in settings and "file_category_management" not in settings["download"]:
                downloads_dir = settings["download"].get("default_download_directory", 
                                                       os.path.join(os.path.expanduser("~"), "Downloads"))
                settings["download"]["file_category_management"] = {
                    "documents": os.path.join(downloads_dir, "Documents"),
                    "audio": os.path.join(downloads_dir, "Audio"),
                    "video": os.path.join(downloads_dir, "Video")
                }
            
            # Ensure proxy_settings exists
            if "connection" in settings and "proxy_settings" not in settings["connection"]:
                settings["connection"]["proxy_settings"] = {
                    "enabled": False,
                    "server_address": "",
                    "port": 0,
                    "authentication": {
                        "username": "",
                        "password": ""
                    }
                }
            
            return settings
    
    def update_setting(self, key, value, category):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Handle nested settings
            if isinstance(value, dict):
                if key == "file_category_management":
                    for sub_key, sub_value in value.items():
                        full_key = f"file_category_management_{sub_key}"
                        self._update_single_setting(cursor, full_key, sub_value, category)
                elif key == "proxy_settings":
                    self._update_single_setting(cursor, "proxy_enabled", value["enabled"], category)
                    self._update_single_setting(cursor, "proxy_server", value["server_address"], category)
                    self._update_single_setting(cursor, "proxy_port", value["port"], category)
                    self._update_single_setting(cursor, "proxy_username", 
                                             value["authentication"]["username"], category)
                    self._update_single_setting(cursor, "proxy_password", 
                                             value["authentication"]["password"], category)
            else:
                self._update_single_setting(cursor, key, value, category)
            
            conn.commit()
    
    def _update_single_setting(self, cursor, key, value, category):
        # Convert Python objects to string representations
        if isinstance(value, (list, tuple)):
            if all(isinstance(x, str) for x in value):
                value = ",".join(value)
            else:
                value = json.dumps(list(value))
        elif isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, (int, float)):
            value = str(value)
        elif value is None:
            value = ""
        
        # Delete existing setting if it exists
        cursor.execute("DELETE FROM settings WHERE key = ?", (key,))
        
        # Insert new setting
        cursor.execute(
            """
            INSERT INTO settings (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (key, value, category)
        )
    
    def update_settings(self, settings):
        for category, category_settings in settings.items():
            for key, value in category_settings.items():
                self.update_setting(key, value, category)
