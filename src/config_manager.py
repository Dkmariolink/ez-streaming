# Copyright 2025 Dkmariolink (thedkmariolink@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
                config_data = json.load(f)

            # --- Check if loaded data is a dictionary ---
            if not isinstance(config_data, dict):
                print(f"Warning: Configuration file {self.config_path} does not contain a valid JSON object. Using defaults.")
                return {} # Return empty dict if not a dict

            # --- Add default values for new keys if missing ---
            
            # Global setting
            if 'show_low_delay_warning' not in config_data:
                config_data['show_low_delay_warning'] = True
                
            # Profile structure validation and migration
            if 'profiles' in config_data:
                for profile_name, profile_content in config_data['profiles'].items():
                    # Ensure profile_content is a dictionary
                    if not isinstance(profile_content, dict):
                        # Attempt to migrate from old list format if possible
                        if isinstance(profile_content, list):
                            print(f"Migrating profile '{profile_name}' from list to dict format.")
                            profile_content = {
                                "launch_delay": 5, # Assign default delay
                                "programs": profile_content # Keep the existing list
                            }
                            config_data['profiles'][profile_name] = profile_content
                        else:
                            # Cannot migrate, reset to default structure
                            print(f"Warning: Profile '{profile_name}' has unexpected format. Resetting.")
                            profile_content = {"launch_delay": 5, "programs": []}
                            config_data['profiles'][profile_name] = profile_content

                    # Ensure 'launch_delay' exists
                    if 'launch_delay' not in profile_content:
                        profile_content['launch_delay'] = 5

                    # Ensure 'programs' list exists
                    if 'programs' not in profile_content or not isinstance(profile_content['programs'], list):
                        profile_content['programs'] = []

                    # Process programs within the profile
                    programs_list = profile_content['programs']
                    for program_entry in programs_list:
                        # Ensure program_entry is a dictionary
                        if not isinstance(program_entry, dict):
                            # Skip invalid program entries
                            print(f"Warning: Invalid program entry found in profile '{profile_name}'. Skipping.")
                            continue 

                        # --- Migrate from 'app_delay' to 'use_custom_delay'/'custom_delay_value' ---
                        if 'app_delay' in program_entry:
                            old_delay = program_entry.pop('app_delay') # Remove old key
                            if old_delay is not None and isinstance(old_delay, int) and old_delay >= 0:
                                program_entry['use_custom_delay'] = True
                                program_entry['custom_delay_value'] = old_delay
                            else: # Includes -1 or invalid types
                                program_entry['use_custom_delay'] = False
                                program_entry['custom_delay_value'] = 0
                        else:
                            # Set defaults if neither old nor new keys exist
                            if 'use_custom_delay' not in program_entry:
                                program_entry['use_custom_delay'] = False
                            if 'custom_delay_value' not in program_entry:
                                program_entry['custom_delay_value'] = 0
                        # --- End Migration ---

            return config_data
            # --- End of structure validation and migration ---
            
        except Exception as e:
            error_msg = f"Error loading configuration: {str(e)}"
            print(error_msg)
            messagebox.showerror("Configuration Error", 
                               f"Could not load configuration file.\n\n{error_msg}\n\nDefault settings will be used.")
            return {}
