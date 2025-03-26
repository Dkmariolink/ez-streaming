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
                              QMessageBox, QFileDialog, QInputDialog)
from PySide6.QtCore import Qt, Signal, QSize, QTimer
from PySide6.QtGui import QIcon, QPixmap, QBrush, QColor

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
    
        # Browse button
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)  # Slightly wider
        self.browse_btn.setMinimumHeight(32)  # Match height of other elements
        self.button_layout.addWidget(self.browse_btn)
    
        # Launch button
        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setFixedWidth(80)  # Slightly wider
        self.launch_btn.setMinimumHeight(32)  # Match height of other elements
        self.button_layout.addWidget(self.launch_btn)
        
        # Close button (initially hidden)
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedWidth(80)  # Slightly wider
        self.close_btn.setMinimumHeight(32)  # Match height of other elements
        self.close_btn.setVisible(False)  # Hidden by default
        self.button_layout.addWidget(self.close_btn)
    
        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setFixedSize(32, 32)  # Square button with increased size
        self.remove_btn.setStyleSheet("font-size: 14px;")  # Larger icon
        self.remove_btn.setToolTip("Remove App")  # Add the correct tooltip
        self.button_layout.addWidget(self.remove_btn)
    
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setFixedWidth(80)  # Wider status label
        self.status_label.setMinimumHeight(32)  # Match height of other elements
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.status_label)
    
        layout.addLayout(self.button_layout, 1)  # Reduced stretch so buttons don't get too separated
    
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
            self.button_layout.setSpacing(12)  # Increased spacing
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
            if hasattr(self, 'process_timer') and self.process_timer.isActive():
                self.process_timer.stop()
            return
        
        try:
            return_code = self.process.poll()
            if return_code is None:
                # Process is running
                self.status_label.setText("Launched")
                self.status_label.setStyleSheet("color: #00C853;")
                self.close_btn.setVisible(True)
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
                
                if hasattr(self, 'process_timer') and self.process_timer.isActive():
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
                
            if hasattr(self, 'process_timer') and self.process_timer.isActive():
                self.process_timer.stop()
    
    def close_program(self):
        """Close the running program"""
        if self.process and self.process.poll() is None:
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
        
        # Disable focus rectangles globally
        self.setStyleSheet("QWidget:focus { outline: none; }")
        
        self.setup_ui()
        self.connect_signals()
        self.load_config()
        
        self.setWindowTitle("EZ Streaming")
        self.setMinimumSize(950, 650)  # Further increased minimum size
        self.resize(1000, 700)  # Set a larger default size
        
        # Set application icon
        self.setup_app_icon()
        
        # Set initial state for delete button
        self.update_delete_button_state()
        
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
        
    def setup_app_icon(self):
        """Set up application icon"""
        icon_path = None
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            if hasattr(sys, '_MEIPASS'):
                # Running from PyInstaller bundle
                base_dir = sys._MEIPASS
            else:
                # Fallback to executable directory
                base_dir = os.path.dirname(sys.executable)
            icon_path = os.path.join(base_dir, "assets", "icon.ico")
        else:
            # Running as script
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(current_dir, "assets", "icon.ico")
            
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
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
        
        self.title_label = QLabel("EZ Streaming")
        self.title_label.setObjectName("title_label")
        header_layout.addWidget(self.title_label)
        
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
                margin: 3px 0;
                padding: 4px;
                min-height: 38px;
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
            
            #title_label {{
                color: {self.accent_color}; 
                font-size: 18pt;
                font-weight: bold;
            }}
            
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
        
        # Get the size hint and add just a small amount of extra height
        size_hint = program_widget.sizeHint()
        item.setSizeHint(QSize(size_hint.width(), size_hint.height() + 4))  # Add minimal extra height
        
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
            
        if profile_name in self.profiles:
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
            
        # Create new profile with one empty program entry
        self.profiles[profile_name] = [{"name": "", "path": ""}]
        self.update_profile_combobox()
        self.profile_combo.setCurrentText(profile_name)
        # Change profile will be triggered by the setCurrentText
        
        # Clear the entry field
        self.new_profile_entry.clear()
        
        # Mark changes as unsaved
        self.changes_made = True
        
        # Show status message
        self.show_status(f"Created new profile: {profile_name}", self.launched_color)
    
    def duplicate_current_profile(self):
        """Duplicate the current profile"""
        current_profile = self.profile_combo.currentText()
        
        # Create a new profile name (Profile 1, Profile 2, etc.)
        counter = 1
        new_profile_name = f"{current_profile} (Copy)"
        while new_profile_name in self.profiles:
            counter += 1
            new_profile_name = f"{current_profile} (Copy {counter})"
        
        # Create a deep copy of the current profile
        self.profiles[new_profile_name] = []
        
        # Handle special case for default profile
        if current_profile == self.default_profile_display_name:
            # Copy from the actual "Default" profile
            for program in self.programs:
                widget = program["widget"]
                self.profiles[new_profile_name].append({
                    "name": widget.get_name(),
                    "path": widget.get_path()
                })
        else:
            # For regular profiles
            for program in self.programs:
                widget = program["widget"]
                self.profiles[new_profile_name].append({
                    "name": widget.get_name(),
                    "path": widget.get_path()
                })
        
        # Update UI
        self.update_profile_combobox()
        self.profile_combo.setCurrentText(new_profile_name)
        # Change profile will be triggered by the setCurrentText
        
        # Mark changes as unsaved - this is what was missing
        self.changes_made = True
        
        # Show status message
        self.show_status(f"Created duplicate profile: {new_profile_name}", self.launched_color)
    
    def rename_current_profile(self):
        """Rename the current profile"""
        current_profile = self.profile_combo.currentText()
        is_default = (current_profile == self.default_profile_display_name)
        
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
            
        if new_name in self.profiles and new_name != current_profile:
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
        
        # Store profile data
        if is_default:
            profile_data = self.profiles["Default"]
        else:
            profile_data = self.profiles[current_profile]
        
        # Rename the profile
        if not is_default:
            del self.profiles[current_profile]
            self.profiles[new_name] = profile_data
            self.current_profile = new_name
            self.show_status(f"Profile renamed to '{new_name}'", self.launched_color)
        else:
            # For Default profile, just change the display name
            self.default_profile_display_name = new_name
            self.show_status(f"Default profile renamed to '{new_name}' (still functions as default)", self.launched_color)
        
        # Update UI
        self.update_profile_combobox()
        
        # Mark as changed
        self.changes_made = True
    
    def delete_current_profile(self):
        """Delete the currently selected profile"""
        current_profile = self.profile_combo.currentText()
        is_default = (current_profile == self.default_profile_display_name)
    
        # Check if this is the default profile
        if is_default:
            self.show_status("Cannot delete the default profile", self.error_color)
            return
    
        # Check for unsaved changes
        if self.changes_made:
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"You have unsaved changes in the profile '{current_profile}'. Do you want to save them before deleting?",
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
            f"Are you sure you want to delete the '{current_profile}' profile?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if result != QMessageBox.StandardButton.Yes:
            return
    
        # Delete the profile
        if current_profile in self.profiles:
            del self.profiles[current_profile]
        
            # Switch to Default profile
            self.current_profile = "Default"
            self.profile_combo.setCurrentText(self.default_profile_display_name)
        
            # Update delete button state
            self.update_delete_button_state()
        
            # Show success message
            self.show_status(f"Profile '{current_profile}' deleted", self.warning_color)
        
            # Save the updated configuration
            self.save_config()
    
    def change_profile(self, profile_name=None):
        """Change to a different profile"""
        if profile_name is None:
            display_name = self.profile_combo.currentText()
            # Convert display name to internal name if needed
            if display_name == self.default_profile_display_name:
                profile_name = "Default"
            else:
                profile_name = display_name
            
        if profile_name != self.current_profile:
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
                    if self.current_profile == "Default":
                        self.profile_combo.setCurrentText(self.default_profile_display_name)
                    else:
                        self.profile_combo.setCurrentText(self.current_profile)
                    return
                elif result == QMessageBox.StandardButton.Yes:
                    self.save_config(False)  # Save without showing confirmation
            
            # Load new profile
            self.current_profile = profile_name
            self.load_profile(profile_name)
            
            # Reset changes flag
            self.changes_made = False

            # Update delete button state
            self.update_delete_button_state()
            
            # Show status message
            if profile_name == "Default":
                self.show_status(f"Switched to profile: {self.default_profile_display_name}", self.launched_color)
            else:
                self.show_status(f"Switched to profile: {profile_name}", self.launched_color)
    
    def update_delete_button_state(self):
        """Update the state of the delete profile button based on current profile"""
        current_profile = self.profile_combo.currentText()
        is_default = (current_profile == self.default_profile_display_name)
        
        self.delete_profile_btn.setEnabled(not is_default)
        
        if is_default:
            self.delete_profile_btn.setToolTip("Cannot remove default profile")
        else:
            self.delete_profile_btn.setToolTip("Remove Profile")
    
    def update_profile_combobox(self):
        """Update the profile selection combobox"""
        self.profile_combo.clear()
        
        # Get sorted profile names, but handle Default specially
        profile_names = sorted(self.profiles.keys())
        
        # Add profiles to combo box, with special handling for Default
        for name in profile_names:
            if name == "Default":
                self.profile_combo.addItem(self.default_profile_display_name)
            else:
                self.profile_combo.addItem(name)
        
        # Set the current profile
        if self.current_profile == "Default":
            self.profile_combo.setCurrentText(self.default_profile_display_name)
        else:
            self.profile_combo.setCurrentText(self.current_profile)
    
    def load_profile(self, profile_name):
        """Load a profile by name"""
        # Clear program list
        self.program_list.clear()
        self.programs = []
    
        # Load profile programs
        if profile_name in self.profiles:
            # Get the program data for this profile
            program_data_list = self.profiles[profile_name]
        
            # If the profile is empty, add one blank entry with delay
            if not program_data_list:
                # Use a timer to delay the creation of the first widget
                QTimer.singleShot(50, lambda: self.add_program(None, None))
            else:
                # Process the program data
                for i, program_data in enumerate(program_data_list):
                    program_path = program_data.get("path", "")
                    name = program_data.get("name", "")
                
                    # For the first item, use a small delay to ensure styling is applied correctly
                    if i == 0:
                        QTimer.singleShot(50, lambda p=program_path, n=name: 
                            self._add_with_process_check(n, p))
                    else:
                        self._add_with_process_check(name, program_path)
        
            # Update Close All button state
            QTimer.singleShot(100, self.update_close_all_button)
    
    # Helper method to add program and check process status
    def _add_with_process_check(self, name, path):
        program_widget = self.add_program(name, path)
        
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
            self.profiles = config.get("profiles", {"Default": [{"name": "", "path": ""}]})
            self.current_profile = config.get("current_profile", "Default")
            self.default_profile_display_name = config.get("default_profile_display_name", "Default")
        else:
            # Initialize with default profile containing one empty entry
            self.profiles = {"Default": [{"name": "", "path": ""}]}
            self.default_profile_display_name = "Default"
            
        # Ensure Default profile exists
        if "Default" not in self.profiles:
            self.profiles["Default"] = [{"name": "", "path": ""}]
            
        # Mark that we're doing initial loading (don't mark changes)
        self.is_initial_loading = True
        
        # Update UI
        self.update_profile_combobox()
        if self.current_profile == "Default":
            self.profile_combo.setCurrentText(self.default_profile_display_name)
        else:
            self.profile_combo.setCurrentText(self.current_profile)
        
        self.load_profile(self.current_profile)
        
        # Reset changes flag since we just loaded
        self.changes_made = False
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Check for running programs
        running_programs = []
        for program in self.programs:
            widget = program["widget"]
            if hasattr(widget, 'process') and widget.process and widget.process.poll() is None:
                running_programs.append(widget.get_name() or "Unnamed program")
        
        # Warn if programs are running
        if running_programs:
            result = QMessageBox.question(
                self,
                "Programs Still Running",
                f"The following programs are still running:\n\n{', '.join(running_programs)}\n\nDo you want to exit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if result != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
        
        # Check for unsaved changes
        if self.changes_made:
            result = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"You have unsaved changes in the profile '{self.current_profile}'. Do you want to save them before closing?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            
            if result == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
            elif result == QMessageBox.StandardButton.Yes:
                self.save_config(False)
        
        event.accept()