# EZ Streaming
# Copyright (C) 2025 Dkmariolink <thedkmariolink@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
EZ Streaming - A simple launcher for streaming applications
Configuration management module for saving and loading settings
"""

import os
import json
import sys
import tkinter.messagebox as messagebox
from config_models import ProfileConfig, ProgramConfig # Import model classes
from exceptions import ConfigError # Import custom exception

class ConfigManager:
    """Handles saving and loading of application configuration"""

    def __init__(self):
        """Initialize the configuration manager"""
        try:
            self.config_dir = self._get_config_dir()
            self.config_path = os.path.join(self.config_dir, "ez_streaming_config.json")

            # Ensure config directory exists
            os.makedirs(self.config_dir, exist_ok=True)
        except OSError as e:
            # Handle potential errors during directory creation
            error_msg = f"Failed to create configuration directory: {self.config_dir}\nError: {e}"
            print(error_msg)
            messagebox.showerror("Initialization Error", error_msg)
            # Depending on severity, might want to exit or use a fallback path
            raise ConfigError(error_msg) from e # Re-raise as custom exception

    def _get_config_dir(self):
        """Get the appropriate configuration directory for the platform"""
        try:
            if sys.platform == "win32":
                # Windows - always use AppData
                app_data = os.environ.get("APPDATA", None)
                if not app_data:
                    raise ConfigError("APPDATA environment variable not found.")
                return os.path.join(app_data, "EZStreaming")
            elif sys.platform == "darwin":
                # macOS
                home = os.path.expanduser("~")
                return os.path.join(home, "Library", "Application Support", "EZStreaming")
            else:
                # Linux/Unix
                home = os.path.expanduser("~")
                return os.path.join(home, ".config", "ezstreaming")
        except Exception as e:
            raise ConfigError(f"Could not determine configuration directory: {e}") from e

    def save_config(self, config_data):
        """
        Save configuration data to file.
        Expects config_data['profiles'] to be a dict of {name: ProfileConfig object}.
        Raises ConfigError on failure.
        """
        try:
            print(f"Saving configuration to: {self.config_path}")

            # Prepare data for serialization
            serializable_config = {
                "current_profile": config_data.get("current_profile", "Default"),
                "default_profile_display_name": config_data.get("default_profile_display_name", "Default"),
                "show_low_delay_warning": config_data.get("show_low_delay_warning", True),
                "profiles": {}
            }

            profiles_to_save = config_data.get("profiles", {})
            for name, profile_obj in profiles_to_save.items():
                if isinstance(profile_obj, ProfileConfig):
                    serializable_config["profiles"][name] = profile_obj.to_dict()
                else:
                    # Should not happen if app logic is correct, but handle gracefully
                    print(f"Warning: Profile '{name}' is not a ProfileConfig object during save. Skipping.")


            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(serializable_config, f, indent=2)
            print(f"Configuration saved successfully")
            return True
        except (IOError, TypeError, json.JSONEncodeError) as e:
            error_msg = f"Error saving configuration to {self.config_path}: {e}"
            print(error_msg)
            # Optionally show messagebox here or let the caller handle ConfigError
            # messagebox.showerror("Save Error", f"Failed to save configuration:\n{e}")
            raise ConfigError(error_msg) from e
        except Exception as e: # Catch any other unexpected errors
            error_msg = f"Unexpected error saving configuration: {e}"
            print(error_msg)
            raise ConfigError(error_msg) from e


    def load_config(self):
        """
        Load configuration data from file.

        Returns:
            dict: Configuration data with profiles converted to ProfileConfig objects.
                  Returns an empty dict with a default profile if file doesn't exist.
        Raises:
            ConfigError: If the file exists but cannot be loaded or parsed.
        """
        if not os.path.exists(self.config_path):
            print("Config file not found. Returning default config structure.")
            # Return a structure with a default profile object
            default_profile = ProfileConfig(name="Default")
            while len(default_profile.programs) < 2:
                default_profile.programs.append(ProgramConfig())
            return {
                "current_profile": "Default",
                "default_profile_display_name": "Default",
                "show_low_delay_warning": True,
                "profiles": {"Default": default_profile}
            }

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            # --- Basic validation ---
            if not isinstance(loaded_data, dict):
                raise ConfigError(f"Configuration file {self.config_path} does not contain a valid JSON object.")

            # --- Prepare the final config structure ---
            final_config = {
                "current_profile": loaded_data.get("current_profile", "Default"),
                "default_profile_display_name": loaded_data.get("default_profile_display_name", "Default"),
                "show_low_delay_warning": loaded_data.get("show_low_delay_warning", True),
                "profiles": {} # This will hold ProfileConfig objects
            }

            # --- Load and convert profiles ---
            loaded_profiles_dict = loaded_data.get("profiles", {})
            if not isinstance(loaded_profiles_dict, dict):
                 print(f"Warning: 'profiles' key in config is not a dictionary. Resetting profiles.")
                 loaded_profiles_dict = {}

            for profile_name, profile_data in loaded_profiles_dict.items():
                if not isinstance(profile_data, dict):
                    print(f"Warning: Data for profile '{profile_name}' is not a dictionary. Skipping.")
                    continue
                try:
                    # Use ProfileConfig.from_dict to create the object
                    # This handles internal structure validation and defaults (like min 2 programs)
                    profile_obj = ProfileConfig.from_dict(profile_name, profile_data)
                    final_config["profiles"][profile_name] = profile_obj
                except Exception as e:
                    # Catch errors during individual profile processing
                    print(f"Error processing profile '{profile_name}': {e}. Skipping.")
                    # Optionally raise ConfigError here if one bad profile should invalidate all
                    # raise ConfigError(f"Error processing profile '{profile_name}': {e}") from e

            # --- Ensure Default profile exists ---
            if "Default" not in final_config["profiles"]:
                 print("Default profile not found in config, creating one.")
                 # Create a default ProfileConfig object
                 default_profile = ProfileConfig(name="Default")
                 while len(default_profile.programs) < 2:
                     default_profile.programs.append(ProgramConfig())
                 final_config["profiles"]["Default"] = default_profile


            # Ensure current_profile actually exists in the loaded profiles
            if final_config["current_profile"] not in final_config["profiles"]:
                print(f"Warning: Loaded current_profile '{final_config['current_profile']}' not found. Defaulting to 'Default'.")
                final_config["current_profile"] = "Default"


            print(f"Configuration loaded successfully from {self.config_path}")
            return final_config

        except json.JSONDecodeError as e:
            error_msg = f"Error decoding JSON from configuration file: {str(e)}"
            print(error_msg)
            # Show error and raise ConfigError
            messagebox.showerror("Configuration Error",
                               f"Could not load configuration file (invalid JSON).\n\n{error_msg}\n\nPlease check or delete the file. Default settings will be used for now.")
            raise ConfigError(error_msg) from e
        except (IOError, OSError) as e:
             error_msg = f"Error reading configuration file {self.config_path}: {e}"
             print(error_msg)
             messagebox.showerror("Configuration Error",
                                f"Could not read configuration file.\n\n{error_msg}\n\nDefault settings will be used for now.")
             raise ConfigError(error_msg) from e
        except Exception as e: # Catch any other unexpected errors during loading/processing
            error_msg = f"Unexpected error loading configuration: {e}"
            print(error_msg)
            messagebox.showerror("Configuration Error",
                               f"Could not load configuration file.\n\n{error_msg}\n\nDefault settings will be used for now.")
            raise ConfigError(error_msg) from e
