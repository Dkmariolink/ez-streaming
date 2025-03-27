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
Main application module containing the core UI and functionality (Qt version)
"""

import os
import sys
import subprocess
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QComboBox, QPushButton, 
                              QLineEdit, QListWidget, QListWidgetItem, QFrame,
                               QMessageBox, QFileDialog, QInputDialog, QGraphicsOpacityEffect) # Added QGraphicsOpacityEffect
from PySide6.QtCore import Qt, Signal, QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, QEvent # Added QEvent
from PySide6.QtGui import QIcon, QPixmap, QBrush, QColor, QFont, QFontDatabase

from config_manager import ConfigManager

class ProgramWidget(QWidget):
    """Widget representing a single program in the list"""
    
    removed = Signal(object)  # Signal when program is removed
    data_changed = Signal()   # Signal when data changes
    
    def __init__(self, name=None, path=None, parent=None):
        super().__init__(parent)
        # Ensure name and path are strings, not booleans or other types
        self.name = str(name) if name not in (None, False, "") else ""
        self.path = str(path) if path not in (None, False, "") else ""
        self.process = None
        self.process_timer = None
        
        self.setup_ui()
        self.connect_signals()
        
        # Install event filter on line edits for row selection
        self.name_edit.installEventFilter(self)
        self.path_edit.installEventFilter(self)
        
    def eventFilter(self, watched, event):
        """Filter events for line edits to trigger row selection."""
        if watched in (self.name_edit, self.path_edit) and event.type() == QEvent.Type.MouseButtonPress:
            # Find the main window and the list widget
            app_window = self.window()
            if isinstance(app_window, StreamerApp):
                list_widget = app_window.program_list
                # Find the QListWidgetItem associated with this ProgramWidget
                for i in range(list_widget.count()):
                    item = list_widget.item(i)
                    widget = list_widget.itemWidget(item)
                    if widget == self:
                        list_widget.setCurrentItem(item)
                        break
        # Pass the event along
        return super().eventFilter(watched, event)

    def setup_ui(self):
        """Create and arrange widgets"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)  # Reduced vertical margins
        layout.setSpacing(10)  # Maintain horizontal spacing
    
        # Drag handle - increase width and add more padding
        self.drag_handle = QLabel("≡")
        self.drag_handle.setStyleSheet("color: #AAAAAA; font-size: 18px;")
        self.drag_handle.setFixedWidth(30)  # Wider drag handle
        self.drag_handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
        layout.addWidget(self.drag_handle)
    
        # Program name - set stretch factor to 2
        self.name_edit = QLineEdit(self.name)
        self.name_edit.setPlaceholderText("App Name")
        self.name_edit.setMinimumWidth(200)
        self.name_edit.setMinimumHeight(30)
        self.name_edit.setStyleSheet("padding: 2px 8px; color: #FFFFFF; background-color: #2E2E2E;")
        self.name_edit.setClearButtonEnabled(True)
        layout.addWidget(self.name_edit, 2)  # Stretch factor of 2
    
        # Program path - set stretch factor to 3
        self.path_edit = QLineEdit(self.path)
        self.path_edit.setPlaceholderText("Program Path")
        self.path_edit.setMinimumWidth(350)  # Increased minimum width
        self.path_edit.setMinimumHeight(30)  # Set minimum height to prevent text clipping
        self.path_edit.setStyleSheet("padding: 2px 8px;")  # Add internal padding
        self.path_edit.setClearButtonEnabled(True)
        layout.addWidget(self.path_edit, 3)  # Stretch factor of 3
    
        # Button layout with consistent sizing
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(8)  # Default spacing between buttons

        # Common button style - ensure consistent appearance
        button_style = """
            QPushButton {
                background-color: #772CE8;
                color: #FFFFFF;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #9146FF;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #AAAAAA;
        }
    """
    
        # Browse button
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)  # Slightly wider
        self.browse_btn.setMinimumHeight(32)  # Match height of other elements
        self.browse_btn.setStyleSheet(button_style)
        self.button_layout.addWidget(self.browse_btn)
    
        # Launch button
        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setFixedWidth(80)  # Slightly wider
        self.launch_btn.setMinimumHeight(32)  # Match height of other elements
        self.launch_btn.setStyleSheet(button_style)
        self.button_layout.addWidget(self.launch_btn)
        
        # Close button (initially hidden)
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedWidth(80)  # Slightly wider
        self.close_btn.setMinimumHeight(32)  # Match height of other elements
        self.close_btn.setStyleSheet(button_style)
        self.close_btn.setVisible(False)  # Hidden by default
        self.close_btn.setToolTip("Close App") # Add tooltip here
        self.button_layout.addWidget(self.close_btn)
    
        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setFixedSize(32, 32)  # Square button with increased size
        self.remove_btn.setStyleSheet(button_style + "font-size: 14px;")  # Larger icon
        self.remove_btn.setToolTip("Remove App")  # Add the correct tooltip
        self.button_layout.addWidget(self.remove_btn)
    
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setFixedWidth(80)  # Wider status label
        self.status_label.setMinimumHeight(32)  # Match height of other elements
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.status_label)
    
        layout.addLayout(self.button_layout, 0)  # Remove stretch, let line edits expand
    
        self.setLayout(layout)
        
    def connect_signals(self):
        """Connect widget signals to slots"""
        self.browse_btn.clicked.connect(self.browse_for_program)
        self.launch_btn.clicked.connect(self.launch_program)
        self.remove_btn.clicked.connect(self.remove_program)
        self.close_btn.clicked.connect(self.close_program)  # Connect close button
        self.name_edit.textChanged.connect(self.on_data_changed)
        self.path_edit.textChanged.connect(self.on_data_changed)
        
    def browse_for_program(self):
        """Open file browser to select program"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Program",
            "",
            "Executables (*.exe);;All Files (*.*)"
        )
        
        if file_path:
            self.path_edit.setText(file_path)
    
    def launch_program(self):
        """Launch the program"""
        path = self.path_edit.text()
        
        # Check if path is provided
        if not path:
            # Signal to the main window to show a warning
            app_window = self.window()
            app_window.show_status("Cannot launch: No program path provided", app_window.warning_color)
            return None
        
        # Check if path exists
        if not os.path.exists(path):
            app_window = self.window()
            app_window.show_status(f"Error: Program path does not exist: {path}", app_window.error_color)
            return None
            
        try:
            # Update status
            self.status_label.setText("Launching...")
            self.status_label.setStyleSheet("color: #9146FF;")
            QApplication.processEvents()
            
            # Extract directory from path
            program_dir = os.path.dirname(path)
            
            # Launch the program
            self.process = subprocess.Popen([path], cwd=program_dir)
            
            # Create a timer for monitoring this process
            self.process_timer = QTimer(self)
            self.process_timer.timeout.connect(self.check_process_status)
            self.process_timer.start(500)  # Check every 500ms
            
            # Show the close button when a program is launched
            self.close_btn.setVisible(True)
            self.adjust_layout_for_close_button()
            
            # Track process globally in the main window
            app_window = self.window()
            app_window.track_process(path, self.process)
            
            return self.process
            
        except Exception as e:
            self.status_label.setText("Error")
            self.status_label.setStyleSheet("color: #FF5252;")
            app_window = self.window()
            app_window.show_status(f"Error launching program: {str(e)}", app_window.error_color)
            return None
    
    def adjust_layout_for_close_button(self):
        """Adjust the widget layout when the close button appears/disappears"""
        if self.close_btn.isVisible():
            # Increase spacing in the button layout
            self.button_layout.setSpacing(16)  # Increased spacing
        else:
            # Reset spacing to default
            self.button_layout.setSpacing(8)  # Default spacing
            
    def check_process_status(self):
        """Check the status of the launched process"""
        if not hasattr(self, 'process') or self.process is None:
            # No process to monitor
            self.reset_status()
            self.close_btn.setVisible(False)
            self.adjust_layout_for_close_button()
            if hasattr(self, 'process_timer') and self.process_timer is not None and self.process_timer.isActive():
                self.process_timer.stop()
            return
        
        try:
            return_code = self.process.poll()
            if return_code is None:
                # Process is running
                self.status_label.setText("Launched")
                self.status_label.setStyleSheet("color: #00C853;")
                self.close_btn.setVisible(True)
                self.adjust_layout_for_close_button()
            else:
                # Process has exited
                self.reset_status()
                self.process = None
                self.close_btn.setVisible(False)
                self.adjust_layout_for_close_button()
                
                # Untrack globally
                path = self.path_edit.text()
                if path:
                    app_window = self.window()
                    app_window.untrack_process(path)
                
                if hasattr(self, 'process_timer') and self.process_timer is not None and self.process_timer.isActive():
                    self.process_timer.stop()
        except Exception:
            # In case of any error, reset the status
            self.reset_status()
            self.process = None
            self.close_btn.setVisible(False)
            self.adjust_layout_for_close_button()
            
            # Untrack globally
            path = self.path_edit.text()
            if path:
                app_window = self.window()
                app_window.untrack_process(path)
                
            if hasattr(self, 'process_timer') and self.process_timer is not None and self.process_timer.isActive():
                self.process_timer.stop()
    
    def close_program(self):
        """Close the running program"""
        if hasattr(self, 'process') and self.process and self.process.poll() is None:
            path = self.path_edit.text()
            
            try:
                # Try to terminate gracefully first
                self.process.terminate()
                
                # Give it a moment to close
                for i in range(5):  # Try for about 0.5 seconds
                    if self.process.poll() is not None:
                        break
                    QApplication.processEvents()
                    time.sleep(0.1)
                    
                # If it's still running, force kill
                if self.process.poll() is None:
                    # On Windows, use the taskkill /F command for more forceful termination
                    if sys.platform == "win32":
                        try:
                            # Get the process ID
                            pid = self.process.pid
                            # Use taskkill /F to force terminate
                            subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                                          stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL)
                        except Exception:
                            # Fallback to kill if taskkill fails
                            self.process.kill()
                    else:
                        # On other platforms just use kill
                        self.process.kill()
                
                # Update UI
                self.reset_status()
                self.close_btn.setVisible(False)
                self.adjust_layout_for_close_button()
                
                # Untrack process globally
                app_window = self.window()
                app_window.untrack_process(path)
                
                # Show status
                app_name = self.get_name()
                app_window.show_status(f"Closed {app_name}", app_window.warning_color)
                
            except Exception as e:
                app_window = self.window()
                app_window.show_status(f"Error closing program: {str(e)}", app_window.error_color)
    
    def remove_program(self):
        """Request removal of this program"""
        # Get app name and path
        app_name = self.get_name()
        app_path = self.get_path()
    
        # Skip confirmation for blank/default entries
        if not app_path and not app_name:
            # Directly remove without confirmation
            self.removed.emit(self)
            return
    
        # Use app_name if available, otherwise use a generic name
        display_name = app_name if app_name else "this app"
        
        # For non-blank entries, show confirmation
        result = QMessageBox.question(
            self,
            "Confirm Removal",
            f"Remove {display_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
    
        if result == QMessageBox.StandardButton.Yes:
            self.removed.emit(self)
    
    def get_name(self):
        """Get the program name or a default value"""
        name = self.name_edit.text()
        if not name and self.path_edit.text():
            return os.path.basename(self.path_edit.text())
        return name or ""
    
    def get_path(self):
        """Get the program path"""
        return self.path_edit.text()
    
    def on_data_changed(self):
        """Handle changes to program data"""
        self.data_changed.emit()
    
    def reset_status(self):
        """Reset status to Ready"""
        # Force update the UI immediately
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("color: white;")
        QApplication.processEvents()


class StreamerApp(QMainWindow):
    """Main application window for EZ Streaming"""
    
    def __init__(self):
        super().__init__()
        self.programs = []
        self.config_manager = ConfigManager()
        self.current_profile = "Default"
        self.profiles = {"Default": []}
        self.changes_made = False
        self.is_initial_loading = True
        self.default_profile_display_name = "Default"  # Display name for Default profile
        self.running_processes = {}  # Store dictionary of running processes: {path: process_object}
        self.summer_blaster_font = None # Initialize font attribute
        self.title_opacity_effect = None # For animation
        self.title_animation = None # For animation
        
        # Disable focus rectangles globally
        self.setStyleSheet("QWidget:focus { outline: none; }")
        
        self.setup_ui()
        self.connect_signals()
        self.load_config()
        
        self.setWindowTitle("EZ Streaming")
        self.setMinimumSize(950, 650)  # Further increased minimum size
        self.resize(1000, 700)  # Set a larger default size
        
        # Set application icon and font 
        self.setup_app_icon_and_font()
        
        # Set initial state for delete and rename buttons
        self.update_delete_button_state()
        self.update_rename_button_state() 
        
        self.is_initial_loading = False
        
    def track_process(self, path, process):
        """Add a process to the global tracking dictionary"""
        self.running_processes[path] = process
        # Update the Close All button
        self.update_close_all_button()

    def untrack_process(self, path):
        """Remove a process from the global tracking dictionary"""
        if path in self.running_processes:
            del self.running_processes[path]
        # Update the Close All button
        self.update_close_all_button()

    # Helper function to find asset paths correctly
    def find_asset_path(self, asset_name):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            if hasattr(sys, '_MEIPASS'):
                # Running from PyInstaller bundle
                base_dir = sys._MEIPASS
            else:
                # Fallback to executable directory
                base_dir = os.path.dirname(sys.executable)
            asset_path = os.path.join(base_dir, "assets", asset_name)
        else:
            # Running as script
            # Assuming src is one level down from project root where assets is
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir) # Go up one level from src
            asset_path = os.path.join(base_dir, "assets", asset_name)
        
        print(f"Calculated asset path for {asset_name}: {asset_path}") # Debug print
        return asset_path if os.path.exists(asset_path) else None
        
    def setup_app_icon_and_font(self):
        """Set up application icon and custom font"""
        icon_path = self.find_asset_path("icon.ico")
        font_path = self.find_asset_path(os.path.join("fonts", "SummerBlaster.otf"))
            
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))

        # Print debug info
        print(f"Looking for font at: {font_path}")
        print(f"Font exists: {font_path is not None}")
    
        # Load the font if it exists
        if font_path:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"Font loaded successfully. Available families: {font_families}")
                if font_families:
                    self.summer_blaster_font = font_families[0]
                    print(f"Stored font family '{self.summer_blaster_font}'")
                else:
                     print("Warning: Font loaded but no families found.")
                     self.summer_blaster_font = None # Ensure it's None if loading failed
            else:
                print(f"Failed to load font: {font_path}, error code: {font_id}")
                self.summer_blaster_font = None
        else:
            print(f"Font file not found.")
            self.summer_blaster_font = None
    
    def setup_ui(self):
        """Set up the user interface"""
        # Apply dark theme with purple accents
        self.setup_styling()
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Increased margins
        main_layout.setSpacing(15)  # Increased spacing
        
        # Application header with title
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center items in the layout

        # --- New Title Area ---
        # Use title.png as a single label
        self.title_image_label = QLabel() # Store as instance variable
        title_logo_path = self.find_asset_path("title.png") 
        if title_logo_path:
            pixmap = QPixmap(title_logo_path)
            # Scale the logo to a height of 80px
            scaled_pixmap = pixmap.scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
            self.title_image_label.setPixmap(scaled_pixmap) 
            self.title_image_label.setFixedSize(scaled_pixmap.size()) # Set size to scaled pixmap

            # Add opacity effect for animation
            self.title_opacity_effect = QGraphicsOpacityEffect(self.title_image_label)
            self.title_image_label.setGraphicsEffect(self.title_opacity_effect)

            # Setup animation using keyframes for smoother pulse
            self.title_animation = QPropertyAnimation(self.title_opacity_effect, b"opacity")
            self.title_animation.setDuration(3000) # Slower duration (3 seconds per full cycle)
            self.title_animation.setLoopCount(-1) # Loop indefinitely
            self.title_animation.setKeyValueAt(0.0, 1.0)   # Fully visible at start
            self.title_animation.setKeyValueAt(0.5, 0.85)  # Dimmed at midpoint
            self.title_animation.setKeyValueAt(1.0, 1.0)   # Fully visible at end
            self.title_animation.start()

        else:
            # Fallback text if title.png not found
            self.title_image_label.setText("EZ Streaming") 
            self.title_image_label.setStyleSheet(f"color: {self.accent_color}; font-size: 24pt; font-weight: bold;")
        
        header_layout.addWidget(self.title_image_label) # Add the single title label
        # --- End New Title Area ---
        
        main_layout.addWidget(header_frame)
        
        # Profile selection area
        profile_frame = QFrame()
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        
        profile_label = QLabel("Current Profile:")
        profile_layout.addWidget(profile_label)
        
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumHeight(32)  # Increased height
        self.profile_combo.setMinimumWidth(220)  # Increased width to accommodate longer profile names
        self.profile_combo.setStyleSheet("padding: 2px 8px;")  # Add internal padding
        profile_layout.addWidget(self.profile_combo)
        
        self.delete_profile_btn = QPushButton("🗑")
        self.delete_profile_btn.setFixedSize(36, 36)  # Square button with increased size
        self.delete_profile_btn.setStyleSheet("font-size: 16px;")  # Larger icon
        self.delete_profile_btn.setToolTip("Remove Profile")
        profile_layout.addWidget(self.delete_profile_btn)
        
        # Add rename profile button
        rename_profile_btn = QPushButton("✏️")
        rename_profile_btn.setFixedSize(36, 36)  # Square button with increased size
        rename_profile_btn.setStyleSheet("font-size: 16px;")  # Larger icon
        rename_profile_btn.setToolTip("Rename Profile")
        profile_layout.addWidget(rename_profile_btn)
        
        # Add duplicate profile button
        duplicate_profile_btn = QPushButton("📋")
        duplicate_profile_btn.setFixedSize(36, 36)  # Square button with increased size
        duplicate_profile_btn.setStyleSheet("font-size: 16px;")  # Larger icon
        duplicate_profile_btn.setToolTip("Duplicate Profile")
        profile_layout.addWidget(duplicate_profile_btn)
        
        new_profile_label = QLabel("New Profile:")
        new_profile_label.setContentsMargins(15, 0, 5, 0)
        profile_layout.addWidget(new_profile_label)
        
        self.new_profile_entry = QLineEdit()
        self.new_profile_entry.setFixedWidth(200)  # Increased width
        self.new_profile_entry.setMinimumHeight(32)  # Increased height
        self.new_profile_entry.setStyleSheet("padding: 2px 8px;")  # Add internal padding
        profile_layout.addWidget(self.new_profile_entry)
        
        add_profile_btn = QPushButton("+")
        add_profile_btn.setFixedSize(36, 36)  # Square button with increased size
        add_profile_btn.setStyleSheet("font-size: 16px;")  # Larger icon
        add_profile_btn.setToolTip("Add New Profile")
        profile_layout.addWidget(add_profile_btn)
        
        profile_layout.addStretch()
        
        main_layout.addWidget(profile_frame)
        
        # Program list header
        list_header_frame = QFrame()
        list_header_layout = QHBoxLayout(list_header_frame)
        list_header_layout.setContentsMargins(10, 5, 10, 2)  # Reduced bottom margin
        
        # Add empty space for drag handle
        drag_placeholder = QLabel("")
        drag_placeholder.setFixedWidth(24)
        list_header_layout.addWidget(drag_placeholder)
        
        app_name_label = QLabel("App Name")
        app_name_label.setStyleSheet("font-weight: bold;")
        list_header_layout.addWidget(app_name_label, 2)  # Give 2 units of space
        
        path_label = QLabel("Path")
        path_label.setStyleSheet("font-weight: bold;")
        list_header_layout.addWidget(path_label, 3)  # Give 3 units of space
        
        actions_label = QLabel("Actions")
        actions_label.setStyleSheet("font-weight: bold;")
        actions_label.setFixedWidth(230)  # Match the width of all action buttons
        list_header_layout.addWidget(actions_label)
        
        main_layout.addWidget(list_header_frame)
        
        # Programs list widget with drag & drop
        self.program_list = QListWidget()
        self.program_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.program_list.setDefaultDropAction(Qt.MoveAction)
        self.program_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.program_list.setAlternatingRowColors(True)
        self.program_list.setFocusPolicy(Qt.NoFocus)  # Disable focus completely
        self.program_list.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: #2A2A2A;
                border-radius: 4px;
                margin: 5px 0;  /* Increased vertical margin for more spacing */
                padding: 6px;   /* Increased padding */
                min-height: 40px; /* Slightly increased minimum height */
            }
            QListWidget::item:selected {
                background-color: #3D3D3D;
                border: 1px solid #9146FF;
                outline: none;
            }
            QListWidget::item:hover {
                background-color: #333333;
            }
            QListWidget::item:selected:active {
                background-color: #4D4D4D;
                border: 1px solid #9146FF;
                outline: none;
            }
            QListWidget::item:focus {
                outline: none;
                border: 1px solid #9146FF;
            }
        """)
        main_layout.addWidget(self.program_list)
        
        # Status bar
        self.status_label = QLabel("")
        self.status_label.setMinimumHeight(30)  # Ensure visibility
        main_layout.addWidget(self.status_label)
        
        # Action buttons
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 5, 0, 5)
        
        add_btn = QPushButton("Add Program")
        button_layout.addWidget(add_btn)
        
        button_layout.addStretch()
        
        # Add Close All button (initially disabled)
        close_all_btn = QPushButton("Close All")
        close_all_btn.setEnabled(False)  # Disabled until programs are running
        button_layout.addWidget(close_all_btn)
        
        save_btn = QPushButton("Save Profile")
        button_layout.addWidget(save_btn)
        
        launch_all_btn = QPushButton("Launch All")
        button_layout.addWidget(launch_all_btn)
        
        main_layout.addWidget(button_frame)
        
        # Footer with credits
        credit_label = QLabel("Created by Dkmariolink - Free Software")
        credit_label.setStyleSheet("color: #AAAAAA; font-size: 8pt;")
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(credit_label)
        
        # Set the main widget
        self.setCentralWidget(main_widget)
        
        # Store references to buttons
        self.add_btn = add_btn
        self.save_btn = save_btn
        self.launch_all_btn = launch_all_btn
        self.add_profile_btn = add_profile_btn
        self.duplicate_profile_btn = duplicate_profile_btn
        self.close_all_btn = close_all_btn
        self.rename_profile_btn = rename_profile_btn
    
    def setup_styling(self):
        """Set up application styling"""
        # Define colors
        self.bg_color = "#1E1E1E"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#9146FF"  # Twitch purple
        self.button_color = "#772CE8"  # Lighter Twitch purple
        self.ready_color = "#FFFFFF"     # White (same as regular text)
        self.launching_color = "#9146FF" # Purple (same as accent_color)
        self.launched_color = "#00C853"  # Green
        self.error_color = "#FF5252"     # Red
        self.warning_color = "#FFC107"   # Amber - for warnings/notifications
        
        # Disable focus rectangle globally
        self.setStyleSheet("QWidget:focus { outline: none; }")
        
        # Apply stylesheet
        self.setStyleSheet(f"""
            QMainWindow, QWidget, QFrame {{
                background-color: {self.bg_color};
                color: {self.fg_color};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            
            QPushButton {{
                background-color: {self.button_color};
                color: {self.fg_color};
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }}
            
            QPushButton:hover {{
                background-color: {self.accent_color};
            }}
            
            QPushButton:disabled {{
                background-color: #555555;
                color: #AAAAAA;
            }}
            
            QLabel {{
                font-size: 10pt;
            }}
            
            /* Remove specific #title_label styling */
            
            QLineEdit, QComboBox {{
                background-color: #2E2E2E;
                color: {self.fg_color};
                border: 1px solid #444;
                padding: 5px 8px;
                border-radius: 4px;
                font-size: 10pt;
                min-height: 24px;
            }}
            
            QComboBox::drop-down {{
                border: none;
                background: {self.accent_color};
                width: 24px;
            }}
            
            QComboBox::down-arrow {{
                width: 12px;
                height: 12px;
                color: white;
                image: url("data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12'><path fill='white' d='M0 3 L6 9 L12 3 Z'/></svg>");
                margin-right: 6px;
            }}
            
            QComboBox QAbstractItemView {{
                background-color: #2E2E2E;
                color: {self.fg_color};
                selection-background-color: {self.accent_color};
            }}
            
            QToolTip {{
                background-color: white;
                color: black;
                border: 1px solid #AAAAAA;
                padding: 4px;
                font-size: 9pt; 
            }}
        """)
    
    def connect_signals(self):
        """Connect UI signals to slots"""
        self.add_btn.clicked.connect(self.add_program)
        self.save_btn.clicked.connect(lambda: self.save_config(True))
        self.launch_all_btn.clicked.connect(self.launch_all)
        self.close_all_btn.clicked.connect(self.close_all)
        self.add_profile_btn.clicked.connect(self.new_profile_from_entry)
        self.delete_profile_btn.clicked.connect(self.delete_current_profile)
        self.duplicate_profile_btn.clicked.connect(self.duplicate_current_profile)
        self.rename_profile_btn.clicked.connect(self.rename_current_profile)
        self.profile_combo.currentTextChanged.connect(self.change_profile)
        self.new_profile_entry.returnPressed.connect(self.new_profile_from_entry)
        
        # Track program list reordering
        self.program_list.model().rowsMoved.connect(self.on_programs_reordered)
        
        # Set up drag tracking
        self.program_list.itemSelectionChanged.connect(self.on_selection_changed)
    
    def on_selection_changed(self):
        """Handle selection changes in the program list"""
        # This helps with highlighting during drag operations
        for i in range(self.program_list.count()):
            item = self.program_list.item(i)
            if item.isSelected():
                item.setBackground(QBrush(QColor("#3D3D3D")))
            else:
                item.setBackground(QBrush(QColor("#2A2A2A")))
    
    def add_program(self, name=None, path=None):
        """Add a new program to the list"""
        # Create the program widget with empty strings for None, False, or empty values
        program_widget = ProgramWidget(name, path)
        
        # Create a list item and set its size
        item = QListWidgetItem(self.program_list)
        
        # Add to program list
        self.program_list.addItem(item)
        
        # Get the size hint and add a bit more extra height to prevent clipping
        size_hint = program_widget.sizeHint()
        item.setSizeHint(QSize(size_hint.width(), size_hint.height() + 12)) # Further increased extra height
        
        self.program_list.setItemWidget(item, program_widget)
        
        # Connect signals
        program_widget.removed.connect(self.remove_program)
        program_widget.data_changed.connect(self.mark_unsaved_changes)
        
        # Store program data
        self.programs.append({
            "widget": program_widget,
            "item": item
        })
        
        # Only mark changes if this isn't during initial loading
        if not self.is_initial_loading and not (name == "" and path == ""):
            self.mark_unsaved_changes()
        
        return program_widget
    
    def remove_program(self, program_widget):
        """Remove a program from the list"""
        # Find the program in the list
        for i, program in enumerate(self.programs):
            if program["widget"] == program_widget:
                # Remove the item from the list widget
                item = program["item"]
                row = self.program_list.row(item)
                self.program_list.takeItem(row)
                
                # Remove from our programs list
                self.programs.pop(i)
                
                # Mark that changes have been made
                self.mark_unsaved_changes()
                
                # Show status message
                app_name = program_widget.get_name()
                if app_name:
                    self.show_status(f"Program '{app_name}' removed. Remember to save your profile.", self.warning_color)
                else:
                    self.show_status("Blank entry removed. Remember to save your profile.", self.warning_color)
            
                break
    
    def launch_all(self):
        """Launch all configured programs with a short delay between each"""
        if not self.programs:
            self.show_status("No programs configured to launch", self.warning_color)
            return
            
        launched = 0
        
        for program in self.programs:
            widget = program["widget"]
            
            # Skip empty entries
            if not widget.get_path():
                continue
                
            process = widget.launch_program()
            
            if process:  # Only count if successfully launched
                launched += 1
            
            # Small delay to prevent system overload
            QApplication.processEvents()
            QTimer.singleShot(500, lambda: None)  # Small delay between launches
            
        # Show launch summary in status bar
        if launched > 0:
            self.show_status(f"Successfully launched {launched} programs", self.launched_color)
        else:
            self.show_status("No programs were launched", self.warning_color)
        
        # Update the Close All button state
        self.update_close_all_button()
    
    def close_all(self):
        """Close all running programs with a slight delay between each"""
        if not self.running_processes:
            self.show_status("No running programs to close", self.warning_color)
            return
        
        # Confirm with the user
        result = QMessageBox.question(
            self,
            "Close All Programs",
            f"Are you sure you want to close all {len(self.running_processes)} running programs?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if result != QMessageBox.StandardButton.Yes:
            return
        
        # Get all paths that have running processes
        paths_to_close = list(self.running_processes.keys())
        closed_count = 0
        
        # Find widgets for each path and close them
        for path in paths_to_close:
            for program in self.programs:
                widget = program["widget"]
                if widget.get_path() == path and widget.process and widget.process.poll() is None:
                    widget.close_program()
                    closed_count += 1
                    QApplication.processEvents()
                    # Add a small delay between closures
                    QTimer.singleShot(300, lambda: None)
                    break
        
        self.show_status(f"Closed {closed_count} programs", self.warning_color)
        # Update button will be handled by untrack_process
    
    def update_close_all_button(self):
        """Enable/disable the Close All button based on running processes"""
        self.close_all_btn.setEnabled(len(self.running_processes) > 0)
    
    def generate_numbered_profile_name(self, base_name):
        """Generate a numbered profile name that doesn't conflict with existing ones"""
        if base_name not in self.profiles:
            return base_name
        
        counter = 1
        while f"{base_name}{counter}" in self.profiles:
            counter += 1
        
        return f"{base_name}{counter}"
    
    def monitor_process(self, program_widget):
        """Monitor a launched process and update status when it exits"""
        # Each widget now handles its own process monitoring with QTimer
        pass
    
    def on_programs_reordered(self, parent, start, end, destination, row):
        """Handle program reordering"""
        # Update our internal programs list to match the QListWidget order
        new_programs = []
        for i in range(self.program_list.count()):
            item = self.program_list.item(i)
            widget = self.program_list.itemWidget(item)
            
            # Find this widget in our original programs list
            for program in self.programs:
                if program["widget"] == widget:
                    new_programs.append(program)
                    break
        
        # Update the programs list
        self.programs = new_programs
        
        # Mark changes
        self.mark_unsaved_changes()
        
        # Show status
        self.show_status("Programs reordered. Remember to save your profile.", self.warning_color)
    
    def new_profile_from_entry(self):
        """Create a new profile from the entry field"""
        profile_name = self.new_profile_entry.text().strip()
        
        if not profile_name:
            self.show_status("Please enter a profile name", self.warning_color)
            return
        
        # Check if name conflicts with an existing profile or the default display name
        original_display_name = self.default_profile_display_name
        
        if profile_name in self.profiles or profile_name == original_display_name:
            # Generate a numbered alternative
            numbered_name = self.generate_numbered_profile_name(profile_name)
            
            # Ask if they want to use the numbered alternative
            result = QMessageBox.question(
                self,
                "Profile Already Exists",
                f"Profile '{profile_name}' already exists. Would you like to create '{numbered_name}' instead?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if result == QMessageBox.StandardButton.Yes:
                profile_name = numbered_name
            else:
                return
        
        # Create new profile with EXACTLY TWO empty program entries for consistency
        self.profiles[profile_name] = [
            {"name": "", "path": ""}, 
            {"name": "", "path": ""}
        ]
        
        # Clear the program list BEFORE loading the new profile to prevent duplication
        # Block signals to prevent double loading
        self.profile_combo.blockSignals(True)

        # Clear the program list BEFORE loading the new profile to prevent duplication
        self.program_list.clear()
        self.programs = []
    
        # Update UI (add item to combobox)
        self.update_profile_combobox()
    
        # Set the internal current profile variable
        self.current_profile = profile_name
    
        # Find and set the index in the combobox without triggering signals
        index = self.profile_combo.findText(profile_name)
        if index != -1:
            self.profile_combo.setCurrentIndex(index)
        
        # Manually load the profile exactly once
        self.load_profile(profile_name)
    
        # Clear the entry field
        self.new_profile_entry.clear()
    
        # Mark changes as unsaved
        self.changes_made = True
    
        # Update button states immediately for the new profile
        self.update_delete_button_state()
        self.update_rename_button_state()

        # Re-enable signals
        self.profile_combo.blockSignals(False)

        # Show status message
        self.show_status(f"Created new profile: {profile_name}", self.launched_color)
    
    def duplicate_current_profile(self):
        """Duplicate the current profile"""
        # Get the internal name of the profile to duplicate
        source_display_name = self.profile_combo.currentText()
        source_internal_name = "Default" if source_display_name == self.default_profile_display_name else source_display_name

        # Create a new profile name (Profile 1, Profile 2, etc.)
        counter = 1
        # Use source_display_name here instead of undefined current_profile
        new_profile_name = f"{source_display_name} (Copy)"
        while new_profile_name in self.profiles:
            counter += 1
            # Use source_display_name here instead of undefined current_profile
            new_profile_name = f"{source_display_name} (Copy {counter})"
        
        # Create a deep copy of the source profile's data directly from self.profiles
        if source_internal_name in self.profiles:
             # Use list comprehension for a clean deep copy of the list of dicts
            source_data = [item.copy() for item in self.profiles[source_internal_name]]
            self.profiles[new_profile_name] = source_data
        else:
             # Fallback if source somehow doesn't exist (shouldn't happen)
            self.profiles[new_profile_name] = []

        # Make sure the duplicated profile has at least 2 entries
        while len(self.profiles[new_profile_name]) < 2:
            self.profiles[new_profile_name].append({"name": "", "path": ""})

        # Block signals for controlled update
        self.profile_combo.blockSignals(True)

        # Clear the program list BEFORE loading the new profile
        self.program_list.clear()
        self.programs = []    
        
        # Update UI (add item to combobox)
        self.update_profile_combobox()
        
        # Set the internal current profile variable
        self.current_profile = new_profile_name
        
        # Find and set the index in the combobox without triggering signals
        index = self.profile_combo.findText(new_profile_name)
        if index != -1:
            self.profile_combo.setCurrentIndex(index)

        # Manually load the profile exactly once
        self.load_profile(new_profile_name)
        
        # Mark changes as unsaved
        self.changes_made = True

        # Update button states immediately for the new profile
        self.update_delete_button_state()
        self.update_rename_button_state()

        # Re-enable signals
        self.profile_combo.blockSignals(False)
        
        # Show status message
        self.show_status(f"Created duplicate profile: {new_profile_name}", self.launched_color)
    
    def rename_current_profile(self):
        """Rename the current profile"""
        current_profile = self.profile_combo.currentText()
        # Remove (default) suffix if present
        if " (default)" in current_profile:
            current_profile = current_profile.replace(" (default)", "")
        
        is_default = (current_profile == self.default_profile_display_name)
        
        # Prevent renaming of default profile
        if is_default:
            self.show_status("Cannot rename the default profile", self.error_color)
            return
    
        # Get new name from user
        new_name, ok = QInputDialog.getText(
            self, 
            "Rename Profile", 
            "Enter new profile name:",
            text=current_profile
        )
        
        # Validate input
        if not ok or not new_name or new_name == current_profile:
            return
        
        # Check if the new name conflicts with existing profiles
        conflicts_with_default = (new_name == "Default" and not is_default)
        conflicts_with_existing = (new_name in self.profiles and new_name != current_profile 
                          and not (is_default and new_name == "Default"))
        
        if conflicts_with_default or conflicts_with_existing:
            # Generate a numbered alternative
            numbered_name = self.generate_numbered_profile_name(new_name)
            
            # Ask if they want to use the numbered alternative
            result = QMessageBox.question(
                self,
                "Profile Already Exists",
                f"Profile '{new_name}' already exists. Would you like to rename to '{numbered_name}' instead?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if result == QMessageBox.StandardButton.Yes:
                new_name = numbered_name
            else:
                return
        
        # Store profile data - always create a deep copy
        if is_default:
            # Make a deep copy of the profile data
            profile_data = [{k: v for k, v in item.items()} for item in self.profiles["Default"]]
            
            # Make sure it has at least two entries
            while len(profile_data) < 2:
                profile_data.append({"name": "", "path": ""})
        else:
            # Make a deep copy of the profile data
            profile_data = [{k: v for k, v in item.items()} for item in self.profiles[current_profile]]
            
            # Make sure it has at least two entries
            while len(profile_data) < 2:
                profile_data.append({"name": "", "path": ""})
        
        # Rename the profile
        if not is_default:
            # For regular profiles, update the key in the dictionary
            del self.profiles[current_profile]
            self.profiles[new_name] = profile_data
            self.current_profile = new_name
            self.show_status(f"Profile renamed to '{new_name}'", self.launched_color)
        else:
            # For Default profile, just change the display name
            self.default_profile_display_name = new_name
            # Ensure Default profile data is preserved
            self.profiles["Default"] = profile_data
            self.show_status(f"Default profile renamed to '{new_name}' (still functions as default)", self.launched_color)
        
        # Update UI
        self.update_profile_combobox()
        
        # Set current profile explicitly to ensure consistency
        if is_default:
            display_name = new_name
            if new_name != "Default":
                display_name = f"{new_name} (default)"
            self.profile_combo.setCurrentText(display_name)
        else:
            self.profile_combo.setCurrentText(new_name)
        
        # Mark as changed
        self.changes_made = True
        
        # Save configuration immediately for consistency
        self.save_config(False)
        
        # Force refresh the program list to ensure consistent display
        self.load_profile(self.current_profile)
    
    def delete_current_profile(self):
        """Delete the currently selected profile"""
        current_profile_display = self.profile_combo.currentText()
        # Get internal name for dictionary key
        current_profile_internal = "Default" if current_profile_display == self.default_profile_display_name else current_profile_display
            
        is_default = (current_profile_internal == "Default")

        # Check if this is the default profile
        if is_default:
            self.show_status("Cannot delete the default profile", self.error_color)
            return

        # Check for unsaved changes
        if self.changes_made:
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"You have unsaved changes in the profile '{current_profile_display}'. Do you want to save them before deleting?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
        
            if result == QMessageBox.StandardButton.Cancel:
                return
            elif result == QMessageBox.StandardButton.Yes:
                self.save_config(False)  # Save without showing confirmation

        # Confirm deletion
        result = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the '{current_profile_display}' profile?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
    
        if result != QMessageBox.StandardButton.Yes:
            return

        # Delete the profile
        if current_profile_internal in self.profiles:
            # Delete from the dictionary FIRST
            del self.profiles[current_profile_internal]

            # Switch internal state to Default profile BEFORE saving
            self.current_profile = "Default"

            # Switch UI to Default profile *before* saving
            self.load_profile("Default")

            # Save the updated configuration immediately 
            self.save_config(False) 

            # Update UI to show the default profile in the combobox (redundant after load_profile, but safe)
            self.update_profile_combobox() 
            
            # Update delete and rename button states for the now-current Default profile
            self.update_delete_button_state() 
            self.update_rename_button_state() 
    
            # Show success message
            self.show_status(f"Profile '{current_profile_display}' deleted", self.warning_color)
    
    def change_profile(self, profile_name=None):
        """Change to a different profile"""
        # If coming from combobox selection
        if profile_name is None:
            display_name = self.profile_combo.currentText()
            
            
            # Convert display name to internal name if needed
            if display_name == self.default_profile_display_name:
                profile_name = "Default"
            else:
                profile_name = display_name
        
        # Check if we're actually changing profiles
        if profile_name == self.current_profile:
            return  # No change needed, prevent duplicate creation
        
        # Check for unsaved changes
        if self.changes_made:
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"You have unsaved changes in the profile '{self.current_profile}'. Do you want to save them before switching?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if result == QMessageBox.StandardButton.Cancel:
                # Revert combobox selection to current profile
                self.update_profile_combobox()  # Reset the combo box
                return
            elif result == QMessageBox.StandardButton.Yes:
                self.save_config(False)  # Save without showing confirmation
        
        # Load new profile
        self.current_profile = profile_name
        self.load_profile(profile_name)
        
        # Reset changes flag
        self.changes_made = False
        
        # Update delete and rename button states
        self.update_delete_button_state()
        self.update_rename_button_state() # Add call here
        
        # Show status message
        if profile_name == "Default":
            self.show_status(f"Switched to profile: {self.default_profile_display_name}", self.launched_color)
        else:
            self.show_status(f"Switched to profile: {profile_name}", self.launched_color)
    
    def update_delete_button_state(self):
        """Update the state of the delete profile button based on current profile"""
        # Check against the internal current_profile name
        is_default = (self.current_profile == "Default")
        
        self.delete_profile_btn.setEnabled(not is_default)
        
        if is_default:
            self.delete_profile_btn.setToolTip("Cannot remove default profile")
        else:
            self.delete_profile_btn.setToolTip("Remove Profile")

    def update_rename_button_state(self):
        """Update the state of the rename profile button based on current profile"""
        # Check against the internal current_profile name
        is_default = (self.current_profile == "Default")

        self.rename_profile_btn.setEnabled(not is_default)

        if is_default:
            self.rename_profile_btn.setToolTip("Cannot rename the default profile")
        else:
            self.rename_profile_btn.setToolTip("Rename Profile")

    def closeEvent(self, event):
        """Handle the window close event, prompting to save if changes were made."""
        if self.changes_made:
            profile_display = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
            
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Unsaved Changes")
            msg_box.setText(f"You have unsaved changes in the profile '{profile_display}'.")
            msg_box.setInformativeText("Do you want to save them before closing?")
            
            save_button = msg_box.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
            dont_save_button = msg_box.addButton("Don't Save", QMessageBox.ButtonRole.DestructiveRole)
            cancel_button = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            
            msg_box.setDefaultButton(cancel_button) # Default to Cancel
            msg_box.setEscapeButton(cancel_button) # Escape key cancels
            
            msg_box.exec()
            
            clicked_button = msg_box.clickedButton()
            
            if clicked_button == save_button:
                self.save_config(False)  # Save without confirmation message
                event.accept()  # Allow closing
            elif clicked_button == dont_save_button:
                event.accept()  # Allow closing without saving
            else: # Cancel button or closing the dialog
                event.ignore()  # Prevent closing
        else:
            event.accept() # No changes, allow closing
    
    def update_profile_combobox(self):
        """Update the profile selection combobox"""
        self.profile_combo.clear()
    
        # Get sorted profile names, but handle Default specially
        profile_names = sorted(self.profiles.keys())
    
        # Add profiles to combo box, with Default handled specially
        for name in profile_names:
            if not name:  # Skip any empty profile names that might exist
                continue
            
            if name == "Default":
                # Remove the (default) suffix completely
                self.profile_combo.addItem(self.default_profile_display_name)
            else:
                self.profile_combo.addItem(name)
    
        # Set the current profile
        if self.current_profile == "Default":
            self.profile_combo.setCurrentText(self.default_profile_display_name)
        else:
            self.profile_combo.setCurrentText(self.current_profile)
    
            # Removed duplicate block that set current text again
    
    def load_profile(self, profile_name):
        """Load a profile by name"""
        # Clear program list
        self.program_list.clear()
        self.programs = []
        
        # Load profile programs
        if profile_name in self.profiles:
            # Get the program data for this profile
            program_data_list = self.profiles[profile_name]
            
            # If the profile is empty or has fewer than 2 entries, ensure exactly 2
            if len(program_data_list) < 2:
                # Update the profile data to have exactly 2 entries
                program_data_list = [{"name": "", "path": ""}, {"name": "", "path": ""}]
                # Update stored data
                self.profiles[profile_name] = program_data_list
            
            # Now load all program entries synchronously
            for program_data in program_data_list:
                program_path = program_data.get("path", "")
                name = program_data.get("name", "")
                # Add directly without timer
                self._add_with_process_check(name, program_path) 
        else:
            # If the profile doesn't exist (unlikely), create it with 2 empty entries
            self.profiles[profile_name] = [{"name": "", "path": ""}, {"name": "", "path": ""}]
            # Add two empty program entries directly
            self._add_with_process_check("", "")
            self._add_with_process_check("", "")
        
        # Update Close All button state immediately
        self.update_close_all_button()
        # Force viewport update after adding items
        self.program_list.viewport().update() 
    
    def _add_with_process_check(self, name, path):
        """Add a program and check if it's a running process"""
        program_widget = self.add_program(name, path)
        
        # --- Explicitly apply button styles to fix first-row issue ---
        button_style = """
            QPushButton {
                background-color: #772CE8;
                color: #FFFFFF;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #9146FF;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #AAAAAA;
            }
        """
        program_widget.browse_btn.setStyleSheet(button_style)
        program_widget.launch_btn.setStyleSheet(button_style)
        program_widget.close_btn.setStyleSheet(button_style)
        # Apply specific style for remove button (includes larger font size)
        program_widget.remove_btn.setStyleSheet(button_style + "font-size: 14px;") 
        
        # --- Explicitly apply QLineEdit styles to fix first-row issue ---
        line_edit_style = "padding: 2px 8px; color: #FFFFFF; background-color: #2E2E2E; border: 1px solid #444; border-radius: 4px;"
        program_widget.name_edit.setStyleSheet(line_edit_style)
        program_widget.path_edit.setStyleSheet(line_edit_style)
        # --- Explicitly apply status label style to fix first-row issue (borderless) ---
        program_widget.status_label.setStyleSheet("background-color: #2A2A2A; color: white; border-radius: 4px;")
        # --- Explicitly apply drag handle style to fix first-row issue (borderless) ---
        program_widget.drag_handle.setStyleSheet("background-color: #2A2A2A; color: #AAAAAA; font-size: 18px; border-radius: 4px;")
        # --- End explicit style application ---

        # Force a style update to ensure consistent styling (Keep this as well, might help other elements)
        item = self.program_list.item(self.program_list.count() - 1) # Get the item just added
        if item:
            item.setBackground(QBrush(QColor("#2A2A2A"))) # Explicitly set background
        if program_widget.style(): # Check if style exists
            program_widget.style().unpolish(program_widget)
            program_widget.style().polish(program_widget)
        program_widget.update() # Request repaint

        QApplication.processEvents() # Process events to help rendering
        
        # Check if this program is in the running processes dictionary
        if path and path in self.running_processes:
            process = self.running_processes[path]
            # Check if it's still running
            if process and process.poll() is None:
                # Update the widget to show it's running
                program_widget.process = process
                program_widget.status_label.setText("Launched")
                program_widget.status_label.setStyleSheet("color: #00C853;")
                program_widget.close_btn.setVisible(True)
                program_widget.adjust_layout_for_close_button()
                
                # Start monitoring
                program_widget.process_timer = QTimer(program_widget)
                program_widget.process_timer.timeout.connect(program_widget.check_process_status)
                program_widget.process_timer.start(500)  # Check every 500ms
    
    def mark_unsaved_changes(self):
        """Mark that unsaved changes have been made"""
        if not self.is_initial_loading:
            self.changes_made = True
            self.show_status("Changes made. Remember to save your profile.", self.warning_color)
    
    def show_status(self, message, color=None, duration=5000):
        """Show a message in the status bar that auto-clears after duration"""
        if color is None:
            color = self.fg_color
            
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")
        
        # Cancel any previous timer to avoid override
        if hasattr(self, '_status_timer') and self._status_timer is not None:
            self._status_timer.stop()
        
        # Create and store a reference to the timer
        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self.clear_status)
        self._status_timer.start(duration)
    
    def clear_status(self):
        """Clear the status message"""
        self.status_label.setText("")
    
    def save_config(self, show_confirmation=False):
        """Save the current configuration"""
        # Build the configuration to save
        profile_data = []
        for program in self.programs:
            widget = program["widget"]
            profile_data.append({
                "name": widget.get_name(),
                "path": widget.get_path()
            })
        
        # Ensure current_profile exists before saving
        if self.current_profile not in self.profiles:
             # If current profile somehow got deleted, default to "Default"
             # This might happen in edge cases during deletion/switching
             print(f"Warning: Current profile '{self.current_profile}' not found in profiles dict. Saving to 'Default'.")
             self.current_profile = "Default"
             # Ensure Default exists
             if "Default" not in self.profiles:
                 self.profiles["Default"] = [] # Create if missing

        self.profiles[self.current_profile] = profile_data
        
        config = {
            "profiles": self.profiles,
            "current_profile": self.current_profile,
            "default_profile_display_name": self.default_profile_display_name
        }
        
        success = self.config_manager.save_config(config)
        
        # Reset the changes flag
        self.changes_made = False
        
        # Show confirmation with status message
        if success:
            if show_confirmation:
                profile_name = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
                self.show_status(f"Profile '{profile_name}' saved successfully.", self.launched_color)
        else:
            self.show_status("Failed to save profile.", self.error_color)
    
    def load_config(self):
        """Load the saved configuration"""
        config = self.config_manager.load_config()
        
        if config:
            self.profiles = config.get("profiles", {"Default": [{"name": "", "path": ""}, {"name": "", "path": ""}]})
            self.current_profile = config.get("current_profile", "Default")
            # Ensure loaded current_profile actually exists in profiles, else default
            if self.current_profile not in self.profiles:
                print(f"Warning: Loaded current_profile '{self.current_profile}' not found. Defaulting to 'Default'.")
                self.current_profile = "Default"
            self.default_profile_display_name = config.get("default_profile_display_name", "Default")
        else:
            # Initialize with default profile containing TWO empty entries
            self.profiles = {"Default": [{"name": "", "path": ""}, {"name": "", "path": ""}]}
            self.default_profile_display_name = "Default"
            self.current_profile = "Default" # Ensure current is set
            
        # Ensure Default profile exists with correct number of entries
        if "Default" not in self.profiles:
            self.profiles["Default"] = [{"name": "", "path": ""}, {"name": "", "path": ""}]
        elif not self.profiles["Default"]:
            # If Default exists but is empty, add two entries
            self.profiles["Default"] = [{"name": "", "path": ""}, {"name": "", "path": ""}]
        elif len(self.profiles["Default"]) < 2:
            # If default has fewer than 2 entries, add entries until it has 2
            while len(self.profiles["Default"]) < 2:
                self.profiles["Default"].append({"name": "", "path": ""})
            
        # Mark that we're doing initial loading (don't mark changes)
        self.is_initial_loading = True
        
        # Update UI
        self.update_profile_combobox()
        
        # Load the current profile
        self.load_profile(self.current_profile)
        
        # Reset changes flag since we just loaded
        self.changes_made = False
        
        # Force delete and rename button state update
        self.update_delete_button_state()
        self.update_rename_button_state() # Add call
