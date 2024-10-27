import json
import os
from typing import Optional, Any, Dict
from .schema import Settings
import tempfile

class SettingsManager:
    def __init__(self, settings_file: str):
        """Initialize the settings manager with a settings file path."""
        self.settings_file = settings_file
        self.settings: Settings = self._load_settings()
    
    def _load_settings(self) -> Settings:
        """Load settings from file or create default settings."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                return Settings.parse_obj(data)
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        # Return default settings if loading fails
        return Settings()
    
    def save_settings(self) -> bool:
        """Save current settings to file."""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            # Save settings
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings.dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, category: str, key: str, default: Any = None) -> Any:
        """Get a setting value by category and key."""
        try:
            category_dict = getattr(self.settings, category)
            return category_dict.get(key, default)
        except AttributeError:
            return default
    
    def set_setting(self, category: str, key: str, value: Any) -> bool:
        """Set a setting value by category and key."""
        try:
            category_dict = getattr(self.settings, category)
            category_dict[key] = value
            return True
        except AttributeError:
            return False
    
    def get_all_settings(self) -> Dict:
        """Get all settings as a dictionary."""
        return self.settings.dict()
    
    def update_settings(self, settings: Dict) -> bool:
        """Update settings from a dictionary."""
        try:
            self.settings = Settings.parse_obj(settings)
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        self.settings = Settings()
    
    def migrate_settings(self, old_settings: Dict) -> None:
        """Migrate settings from an old format to the current format."""
        try:
            # Create new settings with defaults
            new_settings = Settings()
            
            # Update with old settings where possible
            for category in old_settings:
                if hasattr(new_settings, category):
                    category_dict = getattr(new_settings, category)
                    for key, value in old_settings[category].items():
                        if key in category_dict:
                            category_dict[key] = value
            
            self.settings = new_settings
        except Exception as e:
            print(f"Error migrating settings: {e}")
            # Keep default settings if migration fails
            self.settings = Settings()
