"""
EZ Streaming - A simple launcher for streaming applications
Configuration management module for saving and loading settings
"""

import os
import json
import sys
import tkinter.messagebox as messagebox

class ConfigManager:
    """Handles saving and loading of application configuration"""
    
    def __init__(self):
        """Initialize the configuration manager"""
        self.config_dir = self._get_config_dir()
        self.config_path = os.path.join(self.config_dir, "ez_streaming_config.json")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
    
    def _get_config_dir(self):
        """Get the appropriate configuration directory for the platform"""
        if sys.platform == "win32":
            # Windows - always use AppData
            return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "EZStreaming")
        elif sys.platform == "darwin":
            # macOS
            return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "EZStreaming")
        else:
            # Linux/Unix
            return os.path.join(os.path.expanduser("~"), ".config", "ezstreaming")
    
    def save_config(self, config_data):
        """Save configuration data to file"""
        try:
            print(f"Saving configuration to: {self.config_path}")
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2)
            print(f"Configuration saved successfully")
            return True
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            return False
    
    def load_config(self):
        """
        Load configuration data from file
        
        Returns:
            dict: Configuration data, or empty dict if file doesn't exist
        """
        if not os.path.exists(self.config_path):
            return {}
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            error_msg = f"Error loading configuration: {str(e)}"
            print(error_msg)
            messagebox.showerror("Configuration Error", 
                               f"Could not load configuration file.\n\n{error_msg}\n\nDefault settings will be used.")
            return {}