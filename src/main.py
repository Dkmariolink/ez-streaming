#!/usr/bin/env python3
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
Entry point for the application
"""

# Add the current directory to the path so we can import modules
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Main entry point for EZ Streaming application"""
    # Check if we should use the Qt version (default) or Tkinter version
    use_tkinter = "--tkinter" in sys.argv or "-tk" in sys.argv
    
    if use_tkinter:
        # Use Tkinter version
        from app import StreamerApp
        app = StreamerApp()
        app.run()
    else:
        # DPI settings MUST be set before importing Qt modules
        # Set QT environment variables
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" 
        os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
        os.environ["QT_FONT_DPI"] = "96"
        
        # Import PySide6 modules after environment variables are set
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QGuiApplication
        
        # Set high DPI policy before creating any application instance
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            
        # Now create the application
        from PySide6.QtWidgets import QApplication
        from app_qt import StreamerApp
        
        app = QApplication(sys.argv)
        window = StreamerApp()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()