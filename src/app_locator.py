# EZ Streaming
# Copyright (C) 2025 Dkmariolink <thedkmariolink@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
App Locator Module - Finds common streaming applications on the system
"""

import os
import platform
import winreg
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import re

class AppLocator:
    """Handles locating common streaming applications on the system"""
    
    def __init__(self):
        self.system = platform.system()
        self._init_app_definitions()
    
    def _init_app_definitions(self):
        """Initialize the definitions of common streaming apps and their locations"""
        # Define common apps with their possible names, registry keys, and common paths
        self.app_definitions = {
            'obs': {
                'display_name': 'OBS Studio',
                'executable_names': ['obs64.exe', 'obs32.exe', 'obs.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\OBS Studio'),
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\OBS Studio'),
                ],
                'common_paths': [
                    r'C:\Program Files\obs-studio\bin\64bit',
                    r'C:\Program Files\obs-studio\bin\32bit',
                    r'C:\Program Files (x86)\obs-studio\bin\64bit',
                    r'C:\Program Files (x86)\obs-studio\bin\32bit',
                ]
            },
            'streamlabs': {
                'display_name': 'Streamlabs Desktop',
                'executable_names': ['Streamlabs OBS.exe', 'Streamlabs Desktop.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Streamlabs Desktop'),
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Streamlabs Desktop'),
                ],
                'common_paths': [
                    r'C:\Program Files\Streamlabs Desktop',
                    r'C:\Program Files (x86)\Streamlabs Desktop',
                ]
            },
            'discord': {
                'display_name': 'Discord',
                'executable_names': ['Discord.exe', 'DiscordPTB.exe', 'DiscordCanary.exe'],
                'registry_keys': [
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Discord'),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Discord'),
                ],
                'common_paths': [
                    os.path.expandvars(r'%LOCALAPPDATA%\Discord'),
                    os.path.expandvars(r'%LOCALAPPDATA%\DiscordPTB'),
                    os.path.expandvars(r'%LOCALAPPDATA%\DiscordCanary'),
                ]
            },
            'spotify': {
                'display_name': 'Spotify',
                'executable_names': ['Spotify.exe'],
                'registry_keys': [
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Spotify'),
                ],
                'common_paths': [
                    os.path.expandvars(r'%APPDATA%\Spotify'),
                    r'C:\Program Files\Spotify',
                    r'C:\Program Files (x86)\Spotify',
                ]
            },
            'steam': {
                'display_name': 'Steam',
                'executable_names': ['steam.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Valve\Steam'),
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Valve\Steam'),
                ],
                'common_paths': [
                    r'C:\Program Files\Steam',
                    r'C:\Program Files (x86)\Steam',
                ]
            },
            'epic': {
                'display_name': 'Epic Games Launcher',
                'executable_names': ['EpicGamesLauncher.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\EpicGames\Unreal Engine'),
                ],
                'common_paths': [
                    r'C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64',
                    r'C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win32',
                    r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64',
                    r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32',
                    r'D:\Epic Games\Launcher\Portal\Binaries\Win64',
                    r'D:\Epic Games\Launcher\Portal\Binaries\Win32',
                ]
            },
            'chrome': {
                'display_name': 'Google Chrome',
                'executable_names': ['chrome.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Google\Chrome'),
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Google\Chrome'),
                ],
                'common_paths': [
                    r'C:\Program Files\Google\Chrome\Application',
                    r'C:\Program Files (x86)\Google\Chrome\Application',
                ]
            },
            'firefox': {
                'display_name': 'Mozilla Firefox',
                'executable_names': ['firefox.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Mozilla\Mozilla Firefox'),
                    (winreg.HKEY_CURRENT_USER, r'SOFTWARE\Mozilla\Mozilla Firefox'),
                ],
                'common_paths': [
                    r'C:\Program Files\Mozilla Firefox',
                    r'C:\Program Files (x86)\Mozilla Firefox',
                ]
            },
            'voicemeeter': {
                'display_name': 'VoiceMeeter',
                'executable_names': ['voicemeeter.exe', 'voicemeeterpro.exe', 'voicemeeter8.exe'],
                'registry_keys': [
                    (winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\VB-Audio\Voicemeeter'),
                ],
                'common_paths': [
                    r'C:\Program Files\VB\Voicemeeter',
                    r'C:\Program Files (x86)\VB\Voicemeeter',
                ]
            },
            'nvidia_broadcast': {
                'display_name': 'NVIDIA Broadcast',
                'executable_names': ['NVIDIA Broadcast.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\NVIDIA Corporation\NVIDIA Broadcast',
                ]
            },
            'elgato_stream_deck': {
                'display_name': 'Elgato Stream Deck',
                'executable_names': ['Stream Deck.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Elgato\StreamDeck',
                    r'C:\Program Files (x86)\Elgato\StreamDeck',
                ]
            },
            'vtube_studio': {
                'display_name': 'VTube Studio',
                'executable_names': ['VTube Studio.exe', 'VTubeStudio.exe', 'VTS.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\VTube Studio',
                    r'C:\Program Files (x86)\VTube Studio',
                    # Steam paths will be searched automatically
                ]
            },
            'mixitup': {
                'display_name': 'Mix It Up',
                'executable_names': ['MixItUp.exe', 'Mix It Up.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Mix It Up',
                    r'C:\Program Files (x86)\Mix It Up',
                    os.path.expandvars(r'%LOCALAPPDATA%\MixItUp'),
                ]
            },
            'streamelements': {
                'display_name': 'StreamElements OBS.Live',
                'executable_names': ['StreamElements.exe', 'obs64.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\StreamElements OBS.Live',
                    r'C:\Program Files (x86)\StreamElements OBS.Live',
                ]
            },
            'twitch_studio': {
                'display_name': 'Twitch Studio',
                'executable_names': ['Twitch Studio.exe', 'TwitchStudio.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Twitch Studio',
                    r'C:\Program Files (x86)\Twitch Studio',
                ]
            },
            'xsplit': {
                'display_name': 'XSplit Broadcaster',
                'executable_names': ['XSplit.Core.exe', 'XSplitBroadcaster.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\XSplit\Broadcaster',
                    r'C:\Program Files (x86)\XSplit\Broadcaster',
                ]
            },
            'nvidia_shadowplay': {
                'display_name': 'NVIDIA ShadowPlay',
                'executable_names': ['NVIDIA Share.exe', 'nvcontainer.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience',
                    r'C:\Program Files (x86)\NVIDIA Corporation\NVIDIA GeForce Experience',
                ]
            },
            'streamlabs_chatbot': {
                'display_name': 'Streamlabs Chatbot',
                'executable_names': ['Streamlabs Chatbot.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Streamlabs Chatbot',
                    r'C:\Program Files (x86)\Streamlabs Chatbot',
                    os.path.expandvars(r'%APPDATA%\Streamlabs Chatbot'),
                ]
            },
            'touch_portal': {
                'display_name': 'Touch Portal',
                'executable_names': ['TouchPortal.exe', 'Touch Portal.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Touch Portal',
                    r'C:\Program Files (x86)\Touch Portal',
                ]
            },
            'loupedeck': {
                'display_name': 'Loupedeck',
                'executable_names': ['Loupedeck.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Loupedeck\Loupedeck2',
                    r'C:\Program Files (x86)\Loupedeck\Loupedeck2',
                ]
            },
            'restream': {
                'display_name': 'Restream',
                'executable_names': ['Restream.exe', 'Restream Chat.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Restream',
                    r'C:\Program Files (x86)\Restream',
                    os.path.expandvars(r'%LOCALAPPDATA%\Restream'),
                ]
            },
            'snap_camera': {
                'display_name': 'Snap Camera',
                'executable_names': ['Snap Camera.exe', 'SnapCamera.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Snap Inc\Snap Camera',
                    r'C:\Program Files (x86)\Snap Inc\Snap Camera',
                ]
            },
            'crowd_control': {
                'display_name': 'Crowd Control',
                'executable_names': ['CrowdControl.exe', 'Crowd Control.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Crowd Control',
                    r'C:\Program Files (x86)\Crowd Control',
                    os.path.expandvars(r'%LOCALAPPDATA%\CrowdControl'),
                ]
            },
            'dixper': {
                'display_name': 'Dixper',
                'executable_names': ['Dixper.exe'],
                'registry_keys': [],
                'common_paths': [
                    r'C:\Program Files\Dixper',
                    r'C:\Program Files (x86)\Dixper',
                    os.path.expandvars(r'%LOCALAPPDATA%\Dixper'),
                ]
            }
        }
        
        # Add aliases for smart matching
        self.app_aliases = {
            'obs studio': 'obs',
            'streamlabs obs': 'streamlabs',
            'slobs': 'streamlabs',
            'google chrome': 'chrome',
            'mozilla firefox': 'firefox',
            'epic games': 'epic',
            'epicgames': 'epic',
            'nvidia': 'nvidia_broadcast',
            'broadcast': 'nvidia_broadcast',
            'elgato': 'elgato_stream_deck',
            'stream deck': 'elgato_stream_deck',
            'streamdeck': 'elgato_stream_deck',
            'voice meeter': 'voicemeeter',
            'voicemeter': 'voicemeeter',
            'vtube': 'vtube_studio',
            'vtuber studio': 'vtube_studio',
            'v tube studio': 'vtube_studio',
            'vts': 'vtube_studio',
            'mix it up': 'mixitup',
            'mixitup bot': 'mixitup',
            'streamelements obs': 'streamelements',
            'obs.live': 'streamelements',
            'obs live': 'streamelements',
            'twitch': 'twitch_studio',
            'xsplit': 'xsplit',
            'broadcaster': 'xsplit',
            'shadowplay': 'nvidia_shadowplay',
            'nvidia share': 'nvidia_shadowplay',
            'geforce experience': 'nvidia_shadowplay',
            'chatbot': 'streamlabs_chatbot',
            'streamlabs bot': 'streamlabs_chatbot',
            'touch portal': 'touch_portal',
            'touchportal': 'touch_portal',
            'loupedeck': 'loupedeck',
            'restream': 'restream',
            'restream chat': 'restream',
            'snap camera': 'snap_camera',
            'snapcamera': 'snap_camera',
            'snap': 'snap_camera',
            'crowd control': 'crowd_control',
            'crowdcontrol': 'crowd_control',
            'dixper': 'dixper',
        }
    
    def _normalize_app_name(self, app_name: str) -> str:
        """Normalize app name for matching"""
        normalized = app_name.lower().strip()
        # Remove common suffixes
        for suffix in ['.exe', ' app', ' application']:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()
        return normalized
    
    def _find_app_key(self, app_name: str) -> Optional[str]:
        """Find the app key from user input using smart matching"""
        normalized = self._normalize_app_name(app_name)
        
        # Direct match
        if normalized in self.app_definitions:
            return normalized
        
        # Alias match
        if normalized in self.app_aliases:
            return self.app_aliases[normalized]
        
        # Partial match on app keys
        for key in self.app_definitions:
            if key in normalized or normalized in key:
                return key
        
        # Partial match on display names
        for key, info in self.app_definitions.items():
            display_lower = info['display_name'].lower()
            if normalized in display_lower or display_lower in normalized:
                return key
        
        # Fuzzy match - check if any word matches
        words = normalized.split()
        for word in words:
            if len(word) >= 3:  # Skip very short words
                for key in self.app_definitions:
                    if word in key:
                        return key
        
        return None
    
    def _search_registry(self, app_info: Dict) -> Optional[str]:
        """Search Windows registry for app installation path"""
        if self.system != 'Windows':
            return None
        
        for root_key, sub_key in app_info['registry_keys']:
            try:
                with winreg.OpenKey(root_key, sub_key) as key:
                    # Try common value names for install paths
                    for value_name in ['InstallLocation', 'Install_Dir', 'Path', 'InstallPath', '']:
                        try:
                            value, _ = winreg.QueryValueEx(key, value_name)
                            if value and os.path.exists(value):
                                # Check if executable exists in this directory
                                for exe_name in app_info['executable_names']:
                                    exe_path = os.path.join(value, exe_name)
                                    if os.path.exists(exe_path):
                                        return exe_path
                                    # Check bin subdirectories
                                    for subdir in ['bin', 'bin64', 'bin\\64bit']:
                                        exe_path = os.path.join(value, subdir, exe_name)
                                        if os.path.exists(exe_path):
                                            return exe_path
                        except WindowsError:
                            continue
            except WindowsError:
                continue
        
        return None
    
    def _search_common_paths(self, app_info: Dict) -> Optional[str]:
        """Search common installation paths for the app"""
        for path in app_info['common_paths']:
            # Expand environment variables
            expanded_path = os.path.expandvars(path)
            
            # For Discord-like apps, we need to find the latest version directory
            if 'Discord' in app_info['display_name'] and os.path.exists(expanded_path):
                # Look for app-x.x.x directories
                import re
                version_pattern = re.compile(r'app-\d+\.\d+\.\d+')
                try:
                    subdirs = [d for d in os.listdir(expanded_path) if version_pattern.match(d)]
                    if subdirs:
                        # Get the latest version
                        subdirs.sort(reverse=True)
                        for exe_name in app_info['executable_names']:
                            exe_path = os.path.join(expanded_path, subdirs[0], exe_name)
                            if os.path.exists(exe_path):
                                return exe_path
                except OSError:
                    pass
            
            # Standard check
            if os.path.exists(expanded_path):
                for exe_name in app_info['executable_names']:
                    exe_path = os.path.join(expanded_path, exe_name)
                    if os.path.exists(exe_path):
                        return exe_path
        
        return None
    
    def _search_general_exe(self, exe_name: str) -> Optional[str]:
        """Search for any .exe file in common directories"""
        # Ensure we have .exe extension
        if not exe_name.lower().endswith('.exe'):
            exe_name = exe_name + '.exe'
        
        # Common directories to search
        search_dirs = [
            # System directories (usually in PATH)
            'C:\\Windows\\system32',
            'C:\\Windows',
            
            # Program directories
            os.environ.get('ProgramFiles', 'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', 'C:\\Program Files (x86)'),
            os.environ.get('ProgramW6432', 'C:\\Program Files'),
            
            # User directories
            os.path.expandvars('%LOCALAPPDATA%'),
            os.path.expandvars('%APPDATA%'),
            os.path.expandvars('%LOCALAPPDATA%\\Microsoft\\WindowsApps'),  # Windows Store apps
            
            # Common install locations
            'C:\\',
            'D:\\',
        ]
        
        # Add PATH directories
        path_env = os.environ.get('PATH', '')
        if path_env:
            path_dirs = path_env.split(os.pathsep)
            # Add unique PATH directories that aren't already in our list
            for path_dir in path_dirs:
                if path_dir and path_dir not in search_dirs:
                    search_dirs.append(path_dir)
        
        checked_paths = []
        
        for base_dir in search_dirs:
            if not os.path.exists(base_dir):
                continue
                
            # Direct check in base directory
            direct_path = os.path.join(base_dir, exe_name)
            if os.path.exists(direct_path) and os.path.isfile(direct_path):
                return direct_path
            
            # For Program Files directories, search one level deep
            if 'Program Files' in base_dir:
                try:
                    for item in os.listdir(base_dir):
                        item_path = os.path.join(base_dir, item)
                        if os.path.isdir(item_path):
                            # Check in the subdirectory
                            exe_path = os.path.join(item_path, exe_name)
                            if os.path.exists(exe_path) and os.path.isfile(exe_path):
                                return exe_path
                            
                            # Also check common bin subdirectories
                            for bin_dir in ['bin', 'bin64', 'bin32', 'bin\\64bit', 'bin\\32bit']:
                                bin_exe_path = os.path.join(item_path, bin_dir, exe_name)
                                if os.path.exists(bin_exe_path) and os.path.isfile(bin_exe_path):
                                    return bin_exe_path
                except (OSError, PermissionError):
                    # Skip directories we can't read
                    continue
        
        return None
    
    def _search_steam_apps(self, app_name: str) -> Optional[str]:
        """Search for apps in Steam directories"""
        # Common Steam installation paths
        steam_paths = [
            r'C:\Program Files\Steam',
            r'C:\Program Files (x86)\Steam',
            r'D:\Steam',
            r'E:\Steam',
        ]
        
        # Try to find Steam path from registry
        if self.system == 'Windows':
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\Valve\Steam') as key:
                    steam_path, _ = winreg.QueryValueEx(key, 'InstallPath')
                    if steam_path and steam_path not in steam_paths:
                        steam_paths.insert(0, steam_path)
            except:
                pass
        
        # Normalize app name for searching
        search_name = app_name.lower().replace(' ', '').replace('-', '').replace('_', '')
        
        for steam_path in steam_paths:
            if not os.path.exists(steam_path):
                continue
            
            # Check steamapps/common directory
            common_path = os.path.join(steam_path, 'steamapps', 'common')
            if os.path.exists(common_path):
                try:
                    for game_folder in os.listdir(common_path):
                        # Fuzzy match folder name
                        folder_normalized = game_folder.lower().replace(' ', '').replace('-', '').replace('_', '')
                        if search_name in folder_normalized or folder_normalized in search_name:
                            game_path = os.path.join(common_path, game_folder)
                            
                            # Look for common executable patterns
                            exe_patterns = [
                                f"{app_name}.exe",
                                f"{app_name.replace(' ', '')}.exe",
                                f"{app_name.replace(' ', '_')}.exe",
                                f"{app_name.replace(' ', '-')}.exe",
                                f"{game_folder}.exe",
                            ]
                            
                            for pattern in exe_patterns:
                                # Direct file check
                                exe_path = os.path.join(game_path, pattern)
                                if os.path.exists(exe_path):
                                    return exe_path
                                
                                # Check in bin subdirectories
                                for subdir in ['bin', 'Bin', 'x64', 'x86', 'Binaries', 'Win64', 'Win32']:
                                    exe_path = os.path.join(game_path, subdir, pattern)
                                    if os.path.exists(exe_path):
                                        return exe_path
                            
                            # If no direct match, look for any .exe that matches
                            for file in os.listdir(game_path):
                                if file.endswith('.exe') and not file.startswith('unins'):
                                    file_normalized = file.lower().replace(' ', '').replace('-', '').replace('_', '')
                                    if search_name in file_normalized:
                                        return os.path.join(game_path, file)
                                    
                            # Check one level deep
                            for subdir in os.listdir(game_path):
                                subdir_path = os.path.join(game_path, subdir)
                                if os.path.isdir(subdir_path):
                                    try:
                                        for file in os.listdir(subdir_path):
                                            if file.endswith('.exe') and not file.startswith('unins'):
                                                file_normalized = file.lower().replace(' ', '').replace('-', '').replace('_', '')
                                                if search_name in file_normalized:
                                                    return os.path.join(subdir_path, file)
                                    except:
                                        continue
                except:
                    continue
        
        return None
    
    def _get_available_apps(self, search_query: str = None) -> List[str]:
        """Get list of available apps, optionally filtered by similarity to search query"""
        all_apps = []
        
        # Add all predefined apps
        for app_info in self.app_definitions.values():
            all_apps.append(app_info['display_name'])
        
        # If no search query, return all apps
        if not search_query:
            return sorted(all_apps)
        
        # Filter by similarity
        search_lower = search_query.lower()
        search_normalized = search_lower.replace(' ', '').replace('-', '').replace('_', '')
        
        similar_apps = []
        for app in all_apps:
            app_lower = app.lower()
            app_normalized = app_lower.replace(' ', '').replace('-', '').replace('_', '')
            
            # Check various similarity conditions
            if (search_lower in app_lower or 
                app_lower in search_lower or
                search_normalized in app_normalized or
                app_normalized in search_normalized or
                any(word in app_lower for word in search_lower.split()) or
                any(word in search_lower for word in app_lower.split() if len(word) > 2)):
                similar_apps.append(app)
        
        # If no similar apps found, return all apps
        if not similar_apps:
            similar_apps = all_apps
        
        return sorted(similar_apps)
    
    def locate_app(self, app_name: str) -> Tuple[Optional[str], str, List[str]]:
        """
        Locate an app by name.
        
        Returns:
            - Path to executable (if found)
            - Display name of the app
            - List of locations checked (for error feedback)
        """
        locations_checked = []
        
        # Find the app key
        app_key = self._find_app_key(app_name)
        if app_key:
            # Found in predefined apps
            app_info = self.app_definitions[app_key]
            display_name = app_info['display_name']
            
            # Try registry first (most reliable)
            if self.system == 'Windows':
                locations_checked.append("Windows Registry")
                path = self._search_registry(app_info)
                if path:
                    return path, display_name, locations_checked
            
            # Try common paths
            locations_checked.append("Common installation directories")
            path = self._search_common_paths(app_info)
            if path:
                return path, display_name, locations_checked
            
            # Try Steam search for this specific app
            locations_checked.append("Steam directories")
            # Use display name for better matching in Steam folders
            path = self._search_steam_apps(display_name)
            if not path:
                # Also try with original query
                path = self._search_steam_apps(app_name)
            if path:
                return path, display_name, locations_checked
            
            # Add specific paths checked for transparency
            for common_path in app_info['common_paths']:
                expanded = os.path.expandvars(common_path)
                if expanded not in locations_checked:
                    locations_checked.append(expanded)
        
        # If not found in predefined apps or not found at all, try Steam search
        locations_checked.append("Steam directories")
        path = self._search_steam_apps(app_name)
        if path:
            # Extract a clean display name from the path
            display_name = os.path.splitext(os.path.basename(path))[0]
            return path, display_name, locations_checked
        
        # Try general .exe search
        locations_checked.append("General executable search")
        path = self._search_general_exe(app_name)
        if path:
            # Extract a clean display name from the path
            display_name = os.path.splitext(os.path.basename(path))[0]
            return path, display_name, locations_checked
        
        # Not found anywhere - return available apps instead of locations
        available_apps = self._get_available_apps(app_name)
        return None, app_name, available_apps
