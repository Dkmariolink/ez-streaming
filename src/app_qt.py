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
import functools # Added for QTimer lambda issue
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QLabel, QComboBox, QPushButton, 
                              QLineEdit, QListWidget, QListWidgetItem, QFrame,
                              QMessageBox, QFileDialog, QInputDialog, QGraphicsOpacityEffect,
                              QSpinBox, QCheckBox)
from PySide6.QtCore import Qt, Signal, QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, QEvent
from PySide6.QtGui import QIcon, QPixmap, QBrush, QColor, QFont, QFontDatabase

from config_manager import ConfigManager

class ProgramWidget(QWidget):
    """Widget representing a single program in the list"""
    
    removed = Signal(object)  # Signal when program is removed
    data_changed = Signal()   # Signal when data changes
    
    def __init__(self, name=None, path=None, use_custom_delay=False, custom_delay_value=0, parent=None): # Updated delay params
        super().__init__(parent)
        # Ensure name and path are strings, not booleans or other types
        self.name = str(name) if name not in (None, False, "") else ""
        self.path = str(path) if path not in (None, False, "") else ""
        self.use_custom_delay = bool(use_custom_delay) # Store custom delay flag
        # Ensure initial value is reasonable, default to 5 if custom is used but value is 0
        self.custom_delay_value = int(custom_delay_value) if custom_delay_value is not None else 0 
        if self.use_custom_delay and self.custom_delay_value == 0:
            self.custom_delay_value = 5 # Set default to 5 if enabled with 0
            
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
        # Increase bottom margin slightly to prevent clipping
        layout.setContentsMargins(10, 8, 10, 10) 
        layout.setSpacing(10)
    
        # Drag handle
        self.drag_handle = QLabel("≡")
        self.drag_handle.setStyleSheet("color: #AAAAAA; font-size: 18px;")
        self.drag_handle.setFixedWidth(30)
        self.drag_handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
        layout.addWidget(self.drag_handle)
    
        # Program name
        self.name_edit = QLineEdit(self.name)
        self.name_edit.setPlaceholderText("App Name")
        self.name_edit.setMinimumWidth(150) # Reduced min width
        self.name_edit.setMinimumHeight(30)
        self.name_edit.setStyleSheet("padding: 2px 8px; color: #FFFFFF; background-color: #2E2E2E;")
        self.name_edit.setClearButtonEnabled(True)
        layout.addWidget(self.name_edit, 2) # Stretch factor 2
    
        # Program path
        self.path_edit = QLineEdit(self.path)
        self.path_edit.setPlaceholderText("Program Path")
        self.path_edit.setMinimumWidth(250) # Reduced min width
        self.path_edit.setMinimumHeight(30)
        self.path_edit.setStyleSheet("padding: 2px 8px;")
        self.path_edit.setClearButtonEnabled(True)
        # Define button_style earlier as browse_btn needs it now
        button_style = """
            QPushButton {
                background-color: #772CE8; color: #FFFFFF; border: none;
                padding: 6px 12px; border-radius: 4px;
                font-weight: bold; font-size: 10pt;
            }
            QPushButton:hover { background-color: #9146FF; }
            QPushButton:disabled { background-color: #555555; color: #AAAAAA; }
        """

        # Create browse_btn here but add it to the main layout later
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.setMinimumHeight(32)
        self.browse_btn.setStyleSheet(button_style)

        # Add Browse button and Path entry to main layout
        layout.addWidget(self.browse_btn)
        layout.addWidget(self.path_edit, 3) # Add path entry after browse

        # --- Custom Delay Checkbox and Spinbox ---
        self.custom_delay_checkbox = QCheckBox("Custom Delay")
        self.custom_delay_checkbox.setChecked(self.use_custom_delay)
        self.custom_delay_checkbox.setToolTip("Enable to set a specific delay for this app, overriding the profile default.")
        layout.addWidget(self.custom_delay_checkbox)

        self.custom_delay_spinbox = QSpinBox()
        self.custom_delay_spinbox.setRange(0, 60) # 0-60 seconds
        self.custom_delay_spinbox.setValue(self.custom_delay_value) # Set initial value
        self.custom_delay_spinbox.setFixedWidth(45) # Reduced width again
        self.custom_delay_spinbox.setMinimumHeight(32) # Match button height
        self.custom_delay_spinbox.setToolTip("Delay before launching this app (seconds).")
        self.custom_delay_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.custom_delay_spinbox.setVisible(self.use_custom_delay) # Hide if not checked initially
        self.custom_delay_spinbox.setEnabled(self.use_custom_delay) # Enable based on checkbox
        # Set strong focus policy to help with spinbox buttons
        self.custom_delay_spinbox.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Initially hide the spinbox, visibility controlled by checkbox state and update_delay_ui_state
        self.custom_delay_spinbox.setVisible(self.use_custom_delay)
        
        # --- Custom Arrow Buttons for Custom Delay ---
        self.custom_up_btn = QPushButton("▲")
        self.custom_down_btn = QPushButton("▼")
        self.custom_up_btn.setObjectName("ArrowButton") # Use same style as profile arrows
        self.custom_down_btn.setObjectName("ArrowButton")
        self.custom_up_btn.setFixedSize(20, 14) # Adjusted size
        self.custom_down_btn.setFixedSize(20, 14) # Adjusted size
        self.custom_up_btn.setToolTip("Increase Custom Delay")
        self.custom_down_btn.setToolTip("Decrease Custom Delay")

        custom_spin_button_layout = QVBoxLayout()
        custom_spin_button_layout.setSpacing(4) # Set spacing to 4px
        custom_spin_button_layout.setContentsMargins(0,0,0,0)
        custom_spin_button_layout.addWidget(self.custom_up_btn)
        custom_spin_button_layout.addWidget(self.custom_down_btn)

        custom_spin_container_layout = QHBoxLayout()
        custom_spin_container_layout.setSpacing(0)
        custom_spin_container_layout.setContentsMargins(0,0,0,0)
        custom_spin_container_layout.addWidget(self.custom_delay_spinbox)
        custom_spin_container_layout.addLayout(custom_spin_button_layout)
        # --- End Custom Arrow Buttons ---

        layout.addLayout(custom_spin_container_layout) # Add container with spinbox + buttons
        # --- End Custom Delay UI ---
    
        # Button layout
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(8)
        # self.button_layout.setContentsMargins(0, 0, 0, 2) # Removed margin from here

        # button_style defined earlier
    
        # self.browse_btn created earlier and added to main layout
        # self.button_layout.addWidget(self.browse_btn) # Removed from button_layout
    
        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setFixedWidth(80)
        self.launch_btn.setMinimumHeight(32)
        self.launch_btn.setStyleSheet(button_style)
        self.button_layout.addWidget(self.launch_btn)
        
        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedWidth(80)
        self.close_btn.setMinimumHeight(32)
        self.close_btn.setStyleSheet(button_style)
        self.close_btn.setVisible(False)
        self.close_btn.setToolTip("Close App")
        self.button_layout.addWidget(self.close_btn)
    
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setFixedSize(32, 32)
        self.remove_btn.setStyleSheet(button_style + "font-size: 14px;")
        self.remove_btn.setToolTip("Remove App")
        self.button_layout.addWidget(self.remove_btn)
    
        self.status_label = QLabel("Ready")
        self.status_label.setFixedWidth(80)
        self.status_label.setMinimumHeight(32)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.status_label)
    
        layout.addLayout(self.button_layout) # Add button layout
        layout.addStretch(1) # Add stretch factor at the end
    
        self.setLayout(layout)

    def update_delay_ui_state(self, is_first_item: bool, first_app_path_valid: bool):
        """Enable/disable delay controls based on position, first app validity, and current path validity."""
        current_path = self.get_path()
        current_path_valid = bool(current_path and os.path.exists(current_path))

        # Determine if delay *could* be enabled based on rules
        can_potentially_enable_delay = not is_first_item and first_app_path_valid and current_path_valid

        # Enable checkbox only if delay is potentially possible
        self.custom_delay_checkbox.setEnabled(can_potentially_enable_delay)

        # Enable spinbox/buttons only if checkbox is checked AND delay is potentially possible
        can_enable_spinbox = self.use_custom_delay and can_potentially_enable_delay
        self.custom_delay_spinbox.setEnabled(can_enable_spinbox)
        self.custom_up_btn.setEnabled(can_enable_spinbox)
        self.custom_down_btn.setEnabled(can_enable_spinbox)

        # Show spinbox/buttons only if checkbox is checked AND delay is potentially possible
        # (We still show disabled controls if checkbox is checked but path is invalid, for clarity)
        show_custom_controls = self.use_custom_delay and not is_first_item and first_app_path_valid
        self.custom_delay_spinbox.setVisible(show_custom_controls)
        self.custom_up_btn.setVisible(show_custom_controls)
        self.custom_down_btn.setVisible(show_custom_controls)


        # Update checkbox text color and tooltips based on enabled state
        checkbox_style = "background-color: transparent; color: {color}; border-radius: 4px;"
        tooltip_checkbox = ""
        tooltip_spinbox = ""
        tooltip_buttons = "" # Tooltip for buttons when disabled

        if can_potentially_enable_delay:
            checkbox_color = "#FFFFFF" # Enabled color
            tooltip_checkbox = "Enable to set a specific delay for this app, overriding the profile default."
            tooltip_spinbox = "Delay before launching this app (seconds)."
            tooltip_buttons = "" # Use default button tooltips
        elif is_first_item:
            checkbox_color = "#AAAAAA" # Disabled color
            tooltip_checkbox = "Delay is not applicable for the first app in the sequence."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox
        elif not first_app_path_valid: # Not first item, but first app path is invalid
            checkbox_color = "#AAAAAA" # Disabled color
            tooltip_checkbox = "Delay requires the first app to have a valid path."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox
        else: # Not first item, first app valid, but *this* path is invalid
            checkbox_color = "#AAAAAA" # Disabled color
            tooltip_checkbox = "Delay requires a valid program path in this row."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox

        self.custom_delay_checkbox.setStyleSheet(checkbox_style.format(color=checkbox_color))
        self.custom_delay_checkbox.setToolTip(tooltip_checkbox)
        self.custom_delay_spinbox.setToolTip(tooltip_spinbox)
        # Also update tooltips for custom buttons if they are disabled for a specific reason
        self.custom_up_btn.setToolTip(tooltip_buttons if tooltip_buttons else "Increase Custom Delay")
        self.custom_down_btn.setToolTip(tooltip_buttons if tooltip_buttons else "Decrease Custom Delay")


    def connect_signals(self):
        """Connect widget signals to slots"""
        self.browse_btn.clicked.connect(self.browse_for_program)
        self.launch_btn.clicked.connect(self.launch_program) # Individual launch remains immediate
        self.remove_btn.clicked.connect(self.remove_program)
        self.close_btn.clicked.connect(self.close_program)
        self.name_edit.textChanged.connect(self.on_data_changed)
        self.path_edit.textChanged.connect(self.on_data_changed)
        self.custom_delay_checkbox.stateChanged.connect(self.on_custom_delay_toggled)
        self.custom_delay_spinbox.valueChanged.connect(self.on_custom_delay_value_changed)
        # Connect custom arrow buttons
        self.custom_up_btn.clicked.connect(lambda: self.custom_delay_spinbox.stepBy(1))
        self.custom_down_btn.clicked.connect(lambda: self.custom_delay_spinbox.stepBy(-1))
        
    def on_custom_delay_toggled(self, state):
        """Handle checkbox state changes"""
        is_checked = (state == Qt.CheckState.Checked.value)
        self.use_custom_delay = is_checked
        # Show/hide spinbox AND custom buttons based on checkbox state
        # (Visibility/Enablement based on row index is handled in update_delay_ui_state)
        self.custom_delay_spinbox.setVisible(is_checked) 
        self.custom_up_btn.setVisible(is_checked)
        self.custom_down_btn.setVisible(is_checked)
        self.custom_delay_spinbox.setEnabled(is_checked) 
        self.custom_up_btn.setEnabled(is_checked)
        self.custom_down_btn.setEnabled(is_checked)

        if is_checked and self.custom_delay_spinbox.value() == 0: # Set default value to 5 only if enabling and current is 0
            self.custom_delay_spinbox.setValue(5)
            self.custom_delay_value = 5 # Update internal value too
        elif not is_checked:
             # Keep last value when unchecking, just disable/hide
             pass 
        self.on_data_changed()

    def on_custom_delay_value_changed(self, value):
        """Handle changes to the custom delay spinbox value"""
        self.custom_delay_value = value
        # Add warning check here
        app_window = self.window()
        if isinstance(app_window, StreamerApp):
             if 0 < value < 5 and app_window.show_low_delay_warning:
                 app_window.show_low_delay_warning_message()
        self.on_data_changed()
        
    def browse_for_program(self):
        """Open file browser to select program"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Program", "", "Executables (*.exe);;All Files (*.*)"
        )
        if file_path: 
            self.path_edit.setText(file_path)
            # Auto-populate name if empty
            if not self.name_edit.text():
                base_name = os.path.basename(file_path)
                app_name, _ = os.path.splitext(base_name)
                self.name_edit.setText(app_name)
    
    def launch_program(self):
        """Launch the program (immediately, no delay here)"""
        path = self.path_edit.text()
        app_window = self.window() # Get window ref
        if not path:
            app_window.show_status("Cannot launch: No program path provided", app_window.warning_color)
            return None
        if not os.path.exists(path):
            app_window.show_status(f"Error: Program path does not exist: {path}", app_window.error_color)
            return None
        try:
            self.status_label.setText("Launching...")
            self.status_label.setStyleSheet("background-color: transparent; color: #9146FF;") # Added transparent bg
            QApplication.processEvents()
            program_dir = os.path.dirname(path)
            self.process = subprocess.Popen([path], cwd=program_dir)
            self.process_timer = QTimer(self)
            self.process_timer.timeout.connect(self.check_process_status)
            self.process_timer.start(500)
            self.close_btn.setVisible(True)
            app_window.track_process(path, self.process)
            return self.process
        except Exception as e:
            self.status_label.setText("Error"); self.status_label.setStyleSheet("color: #FF5252;")
            app_window.show_status(f"Error launching program: {str(e)}", app_window.error_color)
            return None
            
    def check_process_status(self):
        """Check the status of the launched process"""
        if not hasattr(self, 'process') or self.process is None:
            self.reset_status(); self.close_btn.setVisible(False)
            if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()
            return
        try:
            return_code = self.process.poll()
            if return_code is None:
                self.status_label.setText("Launched"); self.status_label.setStyleSheet("background-color: transparent; color: #00C853;") # Added transparent bg
                self.close_btn.setVisible(True)
            else:
                self.reset_status(); self.process = None; self.close_btn.setVisible(False)
                path = self.path_edit.text()
                if path: self.window().untrack_process(path)
                if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()
        except Exception:
            self.reset_status(); self.process = None; self.close_btn.setVisible(False)
            path = self.path_edit.text()
            if path: self.window().untrack_process(path)
            if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()
    
    def close_program(self):
        """Close the running program after confirmation"""
        if hasattr(self, 'process') and self.process and self.process.poll() is None:
            path = self.path_edit.text(); app_window = self.window()
            app_name = self.get_name() or "this app"

            # Add confirmation dialog
            result = QMessageBox.question(self, "Confirm Close", f"Are you sure you want to close {app_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if result != QMessageBox.StandardButton.Yes:
                return # User cancelled

            try:
                self.process.terminate()
                for _ in range(5): # Wait up to 0.5s
                    if self.process.poll() is not None: break
                    QApplication.processEvents(); time.sleep(0.1)
                if self.process.poll() is None: # Force kill if needed
                    if sys.platform == "win32":
                        try: subprocess.run(['taskkill', '/F', '/PID', str(self.process.pid)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except Exception: self.process.kill() # Fallback
                    else: self.process.kill()
                self.reset_status(); self.close_btn.setVisible(False)
                app_window.untrack_process(path)
                app_name = self.get_name()
                app_window.show_status(f"Closed {app_name}", app_window.warning_color)
            except Exception as e:
                app_window.show_status(f"Error closing program: {str(e)}", app_window.error_color)
    
    def remove_program(self):
        """Request removal of this program"""
        app_name = self.get_name(); app_path = self.get_path()
        if not app_path and not app_name: self.removed.emit(self); return
        display_name = app_name if app_name else "this app"
        result = QMessageBox.question(self, "Confirm Removal", f"Remove {display_name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result == QMessageBox.StandardButton.Yes: self.removed.emit(self)
    
    def get_name(self):
        name = self.name_edit.text()
        return os.path.basename(self.path_edit.text()) if not name and self.path_edit.text() else (name or "")
    
    def get_path(self): return self.path_edit.text()
    def on_data_changed(self): 
        self.data_changed.emit()
        # Trigger UI refresh for all rows when any row's data changes
        app_window = self.window()
        if isinstance(app_window, StreamerApp):
            app_window._refresh_delay_ui_states()
    def reset_status(self):
        self.status_label.setText("Ready"); self.status_label.setStyleSheet("background-color: transparent; color: white;") # Added transparent bg
        QApplication.processEvents()

class StreamerApp(QMainWindow):
    """Main application window for EZ Streaming"""
    
    def __init__(self):
        super().__init__()
        self.programs = [] # Holds {"widget": ProgramWidget, "item": QListWidgetItem}
        self.config_manager = ConfigManager()
        self.current_profile = "Default"
        self.profiles = {"Default": {"launch_delay": 5, "programs": []}} # Ensure dict structure
        self.changes_made = False
        self.is_initial_loading = True
        self.default_profile_display_name = "Default"
        self.running_processes = {}
        self.summer_blaster_font = None
        self.title_opacity_effect = None
        self.title_animation = None
        self.show_low_delay_warning = True
        self._launch_queue = [] # For QTimer launch sequence
        self._current_launch_index = 0 # For QTimer launch sequence
        self._countdown_timer = None # Timer for countdown display
        self._countdown_end_time = 0 # Target time for countdown end
        
        self.setStyleSheet("QWidget:focus { outline: none; }")
        
        self.setup_ui()
        self.connect_signals()
        self.load_config()
        
        self.setWindowTitle("EZ Streaming")
        self.setMinimumSize(1100, 700)
        self.resize(1150, 750)
        
        self.setup_app_icon_and_font()
        self.update_delete_button_state()
        self.update_rename_button_state() 
        
        self.is_initial_loading = False
        
    def track_process(self, path, process):
        self.running_processes[path] = process
        self.update_close_all_button()

    def untrack_process(self, path):
        if path in self.running_processes:
            del self.running_processes[path]
        self.update_close_all_button()

    def find_asset_path(self, asset_name):
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
            asset_path = os.path.join(base_dir, "assets", asset_name)
        else:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.dirname(current_dir)
            asset_path = os.path.join(base_dir, "assets", asset_name)
        
        print(f"Calculated asset path for {asset_name}: {asset_path}")
        return asset_path if os.path.exists(asset_path) else None
        
    def setup_app_icon_and_font(self):
        icon_path = self.find_asset_path("icon.ico")
        font_path = self.find_asset_path(os.path.join("fonts", "SummerBlaster.otf"))
            
        if icon_path: self.setWindowIcon(QIcon(icon_path))
        if font_path:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families: self.summer_blaster_font = font_families[0]
                else: print("Warning: Font loaded but no families found.")
            else: print(f"Failed to load font: {font_path}")
        else: print(f"Font file not found.")
    
    def setup_ui(self):
        self.setup_styling()
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # --- Header ---
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_image_label = QLabel()
        title_logo_path = self.find_asset_path("title.png") 
        if title_logo_path:
            pixmap = QPixmap(title_logo_path).scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
            self.title_image_label.setPixmap(pixmap) 
            self.title_image_label.setFixedSize(pixmap.size())
            self.title_opacity_effect = QGraphicsOpacityEffect(self.title_image_label)
            self.title_image_label.setGraphicsEffect(self.title_opacity_effect)
            self.title_animation = QPropertyAnimation(self.title_opacity_effect, b"opacity")
            self.title_animation.setDuration(3000)
            self.title_animation.setLoopCount(-1)
            self.title_animation.setKeyValueAt(0.0, 1.0); self.title_animation.setKeyValueAt(0.5, 0.85); self.title_animation.setKeyValueAt(1.0, 1.0)
            self.title_animation.start()
        else:
            self.title_image_label.setText("EZ Streaming") 
            self.title_image_label.setStyleSheet(f"color: {self.accent_color}; font-size: 24pt; font-weight: bold;")
        header_layout.addWidget(self.title_image_label)
        main_layout.addWidget(header_frame)
        
        # --- Profile Area ---
        profile_frame = QFrame()
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.addWidget(QLabel("Current Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumHeight(32); self.profile_combo.setMinimumWidth(220); self.profile_combo.setStyleSheet("padding: 2px 8px;")
        profile_layout.addWidget(self.profile_combo)
        self.delete_profile_btn = QPushButton("🗑"); self.delete_profile_btn.setFixedSize(36, 36); self.delete_profile_btn.setStyleSheet("font-size: 16px;"); self.delete_profile_btn.setToolTip("Remove Profile")
        profile_layout.addWidget(self.delete_profile_btn)
        self.rename_profile_btn = QPushButton("✏️"); self.rename_profile_btn.setFixedSize(36, 36); self.rename_profile_btn.setStyleSheet("font-size: 16px;"); self.rename_profile_btn.setToolTip("Rename Profile")
        profile_layout.addWidget(self.rename_profile_btn)
        self.duplicate_profile_btn = QPushButton("📋"); self.duplicate_profile_btn.setFixedSize(36, 36); self.duplicate_profile_btn.setStyleSheet("font-size: 16px;"); self.duplicate_profile_btn.setToolTip("Copy Profile")
        profile_layout.addWidget(self.duplicate_profile_btn)
        profile_layout.addWidget(QLabel("New Profile:"), 0, Qt.AlignmentFlag.AlignRight) # Align right
        self.new_profile_entry = QLineEdit(); self.new_profile_entry.setFixedWidth(200); self.new_profile_entry.setMinimumHeight(32); self.new_profile_entry.setStyleSheet("padding: 2px 8px;")
        profile_layout.addWidget(self.new_profile_entry)
        self.add_profile_btn = QPushButton("+"); self.add_profile_btn.setFixedSize(36, 36); self.add_profile_btn.setStyleSheet("font-size: 16px;"); self.add_profile_btn.setToolTip("Add New Profile")
        profile_layout.addWidget(self.add_profile_btn)
        profile_layout.addStretch(1) # Add stretch before delay
        self.profile_delay_label = QLabel("Launch Delay (s):"); self.profile_delay_label.setContentsMargins(15, 0, 5, 0)
        profile_layout.addWidget(self.profile_delay_label)
        self.profile_delay_spinbox = QSpinBox()
        self.profile_delay_spinbox.setRange(0, 60); self.profile_delay_spinbox.setValue(5)
        self.profile_delay_spinbox.setFixedWidth(45) # Reduced width as buttons are separate
        self.profile_delay_spinbox.setMinimumHeight(32)
        self.profile_delay_spinbox.setToolTip("Default delay between launching apps (seconds).")
        self.profile_delay_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_delay_spinbox.setObjectName("ProfileDelaySpinBox") # Keep object name

        # --- Custom Arrow Buttons for Profile Delay ---
        self.profile_up_btn = QPushButton("▲")
        self.profile_down_btn = QPushButton("▼")
        self.profile_up_btn.setObjectName("ProfileUpArrow") # Specific name
        self.profile_down_btn.setObjectName("ProfileDownArrow") # Specific name
        # Adjust size for better vertical alignment
        self.profile_up_btn.setFixedSize(20, 17)
        self.profile_down_btn.setFixedSize(20, 17)
        self.profile_up_btn.setToolTip("Increase Delay")
        self.profile_down_btn.setToolTip("Decrease Delay")

        spin_button_layout = QVBoxLayout()
        spin_button_layout.setSpacing(0) # Ensure buttons touch
        spin_button_layout.setContentsMargins(0,0,0,0)
        spin_button_layout.addWidget(self.profile_up_btn)
        spin_button_layout.addWidget(self.profile_down_btn)

        spin_container_layout = QHBoxLayout()
        spin_container_layout.setSpacing(0)
        spin_container_layout.setContentsMargins(0,0,0,0)
        spin_container_layout.addWidget(self.profile_delay_spinbox)
        spin_container_layout.addLayout(spin_button_layout)
        # --- End Custom Arrow Buttons ---

        profile_layout.addLayout(spin_container_layout) # Add the container layout
        main_layout.addWidget(profile_frame)
        
        # --- List Header ---
        list_header_frame = QFrame()
        list_header_layout = QHBoxLayout(list_header_frame)
        list_header_layout.setContentsMargins(10, 5, 10, 2)
        drag_placeholder = QLabel(""); drag_placeholder.setFixedWidth(24)
        list_header_layout.addWidget(drag_placeholder)
        app_name_label = QLabel("App Name"); app_name_label.setStyleSheet("font-weight: bold;")
        list_header_layout.addWidget(app_name_label, 2)
        path_label = QLabel("Path"); path_label.setStyleSheet("font-weight: bold;")
        list_header_layout.addWidget(path_label, 3)
        actions_label = QLabel("Actions"); actions_label.setStyleSheet("font-weight: bold;")
        # Removed fixed width, rely on layout stretch
        list_header_layout.addWidget(actions_label) 
        list_header_layout.addStretch(1) # Add stretch to header
        main_layout.addWidget(list_header_frame)
        
        # --- Program List ---
        self.program_list = QListWidget()
        self.program_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.program_list.setDefaultDropAction(Qt.MoveAction)
        self.program_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.program_list.setAlternatingRowColors(True)
        self.program_list.setFocusPolicy(Qt.NoFocus)
        self.program_list.setStyleSheet("""
            QListWidget { background-color: #1E1E1E; border: none; outline: none; }
            QListWidget::item { background-color: #2A2A2A; border-radius: 4px; margin: 5px 0; padding: 6px; min-height: 40px; }
            QListWidget::item:selected { background-color: #3D3D3D; border: 1px solid #9146FF; outline: none; }
            QListWidget::item:hover { background-color: #333333; }
            QListWidget::item:selected:active { background-color: #4D4D4D; border: 1px solid #9146FF; outline: none; }
            QListWidget::item:focus { outline: none; border: 1px solid #9146FF; }
        """)
        main_layout.addWidget(self.program_list)
        
        # --- Status Bar ---
        self.status_label = QLabel(""); self.status_label.setMinimumHeight(30)
        main_layout.addWidget(self.status_label)
        
        # --- Action Buttons ---
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 5, 0, 5)
        self.add_btn = QPushButton("Add Program"); button_layout.addWidget(self.add_btn)
        button_layout.addStretch()
        self.close_all_btn = QPushButton("Close All"); self.close_all_btn.setEnabled(False)
        button_layout.addWidget(self.close_all_btn)
        self.save_btn = QPushButton("Save Profile"); button_layout.addWidget(self.save_btn)
        self.launch_all_btn = QPushButton("Launch All"); button_layout.addWidget(self.launch_all_btn)
        main_layout.addWidget(button_frame)
        
        # --- Footer ---
        credit_label = QLabel("Created by Dkmariolink - Free Software")
        credit_label.setStyleSheet("color: #AAAAAA; font-size: 8pt;")
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(credit_label)
        
        self.setCentralWidget(main_widget)
    
    def setup_styling(self):
        self.bg_color = "#1E1E1E"; self.fg_color = "#FFFFFF"; self.accent_color = "#9146FF"; self.button_color = "#772CE8"
        self.ready_color = "#FFFFFF"; self.launching_color = "#9146FF"; self.launched_color = "#00C853"
        self.error_color = "#FF5252"; self.warning_color = "#FFC107"
        self.setStyleSheet(f"""
            QMainWindow, QWidget, QFrame {{ background-color: {self.bg_color}; color: {self.fg_color}; font-family: 'Segoe UI', Arial, sans-serif; }}
            QPushButton {{ background-color: {self.button_color}; color: {self.fg_color}; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 10pt; }}
            QPushButton:hover {{ background-color: {self.accent_color}; }}
            QPushButton:disabled {{ background-color: #555555; color: #AAAAAA; }}
            QLabel {{ font-size: 10pt; }}
            QLineEdit, QComboBox {{ background-color: #2E2E2E; color: {self.fg_color}; border: 1px solid #444; padding: 5px 8px; border-radius: 4px; font-size: 10pt; min-height: 24px; }}
            QSpinBox {{ font-size: 10pt; min-height: 24px; border: 1px solid #444; background-color: #2E2E2E; border-radius: 4px; padding: 1px; }} /* Added minimal padding back */
            QCheckBox {{ font-size: 10pt; }} /* Style checkbox */
            /* Hide default spin box buttons */
            QSpinBox::up-button {{ width: 0px; border: none; }}
            QSpinBox::down-button {{ width: 0px; border: none; }}
            /* Style custom arrow buttons */
            QPushButton#ArrowButton, QPushButton#ProfileUpArrow, QPushButton#ProfileDownArrow {{ 
                background-color: #3E3E3E; 
                color: white;
                border: 1px solid #444; 
                padding: 1px 2px; /* Adjust padding */
                font-size: 7pt; 
                border-radius: 3px; /* Rounded corners */
                margin: 0px; /* Ensure no extra margin */
            }}
            QPushButton#ArrowButton:hover, QPushButton#ProfileUpArrow:hover, QPushButton#ProfileDownArrow:hover {{ 
                background-color: #4E4E4E; 
                border: 1px solid {self.accent_color}; 
            }}
            /* Specific border removal/rounding for touching buttons */
            QPushButton#ProfileUpArrow {{ border-bottom-left-radius: 0px; border-bottom-right-radius: 0px; border-bottom: none; }} /* Keep top corners rounded */
            QPushButton#ProfileDownArrow {{ border-top-left-radius: 0px; border-top-right-radius: 0px; border-top: none; }} /* Keep bottom corners rounded */
            QPushButton#ProfileUpArrow:hover {{ border-bottom: none; }} /* Keep border consistent on hover */
            QPushButton#ProfileDownArrow:hover {{ border-top: none; }} /* Keep border consistent on hover */

            QComboBox::drop-down {{ border: none; background: {self.accent_color}; width: 24px; }}
            QComboBox::down-arrow {{ width: 12px; height: 12px; color: white; image: url("data:image/svg+xml;charset=utf-8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12'><path fill='white' d='M0 3 L6 9 L12 3 Z'/></svg>"); margin-right: 6px; }}
            QComboBox QAbstractItemView {{ background-color: #2E2E2E; color: {self.fg_color}; selection-background-color: {self.accent_color}; }}
            QToolTip {{ background-color: white; color: black; border: 1px solid #AAAAAA; padding: 4px; font-size: 9pt; }}
        """)
    
    def connect_signals(self):
        self.add_btn.clicked.connect(self.add_program)
        self.save_btn.clicked.connect(lambda: self.save_config(True))
        self.launch_all_btn.clicked.connect(self.start_launch_sequence) # Changed to start sequence
        self.close_all_btn.clicked.connect(self.close_all)
        self.add_profile_btn.clicked.connect(self.new_profile_from_entry)
        self.delete_profile_btn.clicked.connect(self.delete_current_profile)
        self.duplicate_profile_btn.clicked.connect(self.duplicate_current_profile)
        self.rename_profile_btn.clicked.connect(self.rename_current_profile)
        self.profile_combo.currentTextChanged.connect(self.change_profile)
        self.profile_delay_spinbox.valueChanged.connect(self.on_profile_delay_changed)
        self.new_profile_entry.returnPressed.connect(self.new_profile_from_entry)
        self.program_list.model().rowsMoved.connect(self.on_programs_reordered)
        self.program_list.itemSelectionChanged.connect(self.on_selection_changed)
        # Connect custom profile delay buttons
        self.profile_up_btn.clicked.connect(lambda: self.profile_delay_spinbox.stepBy(1))
        self.profile_down_btn.clicked.connect(lambda: self.profile_delay_spinbox.stepBy(-1))
    
    def on_selection_changed(self):
        for i in range(self.program_list.count()):
            item = self.program_list.item(i)
            item.setBackground(QBrush(QColor("#3D3D3D")) if item.isSelected() else QBrush(QColor("#2A2A2A")))

    def on_profile_delay_changed(self, value):
        profile = self.profiles.get(self.current_profile)
        if isinstance(profile, dict):
            profile['launch_delay'] = value
            self.mark_unsaved_changes()
            if 0 < value < 5 and self.show_low_delay_warning:
                self.show_low_delay_warning_message()
    
    def add_program(self, name=None, path=None, use_custom_delay=False, custom_delay_value=0):
        program_widget = ProgramWidget(name, path, use_custom_delay, custom_delay_value)
        item = QListWidgetItem(self.program_list)
        self.program_list.addItem(item)
        size_hint = program_widget.sizeHint()
        # Increase height slightly more to prevent clipping, adjust 14/16 as needed
        item.setSizeHint(QSize(size_hint.width(), size_hint.height() + 14)) 
        self.program_list.setItemWidget(item, program_widget)
        program_widget.removed.connect(self.remove_program)
        program_widget.data_changed.connect(self.mark_unsaved_changes)
        self.programs.append({"widget": program_widget, "item": item})

        # Apply styles using the helper for manually added rows too
        self._apply_styles_to_widget(program_widget)

        if not self.is_initial_loading and not (name == "" and path == ""):
            self.mark_unsaved_changes()

        # Add layout updates after adding
        self.program_list.viewport().update()
        QApplication.processEvents()
        self._refresh_delay_ui_states() # Update delay states after adding

        return program_widget

    def remove_program(self, program_widget):
        for i, program in enumerate(self.programs):
            if program["widget"] == program_widget:
                item = program["item"]
                row = self.program_list.row(item)
                self.program_list.takeItem(row)
                self.programs.pop(i)
                self.mark_unsaved_changes()
                app_name = program_widget.get_name()
                status_msg = f"Program '{app_name}' removed." if app_name else "Blank entry removed."
                self.show_status(status_msg + " Remember to save your profile.", self.warning_color)
                self._refresh_delay_ui_states() # Update delay states after removal
                break

    def show_low_delay_warning_message(self):
        msg_box = QMessageBox(self); msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Low Launch Delay")
        msg_box.setText("Setting a launch delay below 5 seconds may cause system instability or overload. Proceed with caution.")
        checkbox = QCheckBox("Do not show this warning again"); msg_box.setCheckBox(checkbox)
        msg_box.addButton(QMessageBox.StandardButton.Ok); msg_box.exec()
        if checkbox.isChecked():
            self.show_low_delay_warning = False; self.mark_unsaved_changes()
            print("Low delay warning disabled.")

    # --- Launch All Sequence using QTimer ---
    def start_launch_sequence(self):
        """Initiates the non-blocking launch sequence for all programs."""
        self._launch_queue = [p for p in self.programs if p["widget"].get_path()]
        if not self._launch_queue:
            self.show_status("No programs configured with valid paths to launch", self.warning_color)
            return
        
        self._current_launch_index = 0
        self.launch_all_btn.setEnabled(False) # Disable button during launch
        self._launch_next_app_in_sequence() # Start the sequence

    def _launch_next_app_in_sequence(self):
        """Launches the next app in the queue, applying delay if needed."""
        if self._current_launch_index >= len(self._launch_queue):
            # Sequence finished
            launched_count = len([p for p in self._launch_queue if p["widget"].process])
            if launched_count > 0:
                 self.show_status(f"Successfully launched {launched_count} programs", self.launched_color)
            else:
                 self.show_status("No programs were launched (check paths/errors)", self.warning_color)
            self.update_close_all_button()
            self.launch_all_btn.setEnabled(True) # Re-enable button
            # Ensure countdown timer is stopped if sequence finishes early
            if self._countdown_timer:
                self._countdown_timer.stop()
            return

        program_data = self._launch_queue[self._current_launch_index]
        widget = program_data["widget"]
        
        # Determine effective delay
        profile_dict = self.profiles.get(self.current_profile)
        profile_delay = 5
        if isinstance(profile_dict, dict):
            profile_delay = profile_dict.get('launch_delay', 5)
            
        effective_delay = widget.custom_delay_value if widget.use_custom_delay else profile_delay
        delay_ms = effective_delay * 1000 # Convert s to ms for QTimer

        # --- Apply delay *before* launching (except for the first app) ---
        if self._current_launch_index > 0 and delay_ms > 0:
            # Check for warning
            if 0 < effective_delay < 5 and self.show_low_delay_warning:
                self.show_low_delay_warning_message()
                if not self.show_low_delay_warning: print("Warning disabled during launch.")

            # Start countdown timer
            self._countdown_end_time = time.time() + effective_delay
            if self._countdown_timer: # Stop previous if any
                self._countdown_timer.stop()
            self._countdown_timer = QTimer(self)
            self._countdown_timer.timeout.connect(self._update_countdown_status)
            self._countdown_timer.start(100) # Update ~10 times per second
            self._update_countdown_status() # Show initial time immediately
            # The actual launch will be triggered by _update_countdown_status when timer finishes
        else:
            # No delay needed for the first app or if delay is 0
            print(f"Launching immediately: {widget.get_name()}") # Debug print
            process = widget.launch_program()
            QApplication.processEvents() # Allow UI update
            self._current_launch_index += 1
            # Schedule the *next* step immediately
            QTimer.singleShot(10, self._launch_next_app_in_sequence)

    def _update_countdown_status(self):
        """Updates the status label with remaining time and triggers launch when done."""
        remaining_time = self._countdown_end_time - time.time()

        if remaining_time > 0:
            # Get the name of the next app for the status message
            next_app_name = "next app"
            if self._current_launch_index < len(self._launch_queue):
                 next_app_name = self._launch_queue[self._current_launch_index]["widget"].get_name() or "next app"
            # Update status label - round up seconds
            self.show_status(f"Launching {next_app_name} in {int(remaining_time + 0.99)}s...", self.warning_color, duration=200) # Short duration for status update
        else:
            # Countdown finished
            if self._countdown_timer:
                self._countdown_timer.stop()

            # Get the widget that needs launching NOW
            if self._current_launch_index < len(self._launch_queue):
                program_data = self._launch_queue[self._current_launch_index]
                widget = program_data["widget"]

                # --- Perform the launch action ---
                print(f"Launching after delay: {widget.get_name()}") # Debug print
                process = widget.launch_program()
                QApplication.processEvents() # Allow UI update after launch attempt
                self._current_launch_index += 1

                # Schedule the *next* step immediately after this launch
                QTimer.singleShot(10, self._launch_next_app_in_sequence)
            else:
                 # Should not happen if logic is correct, but safety check
                 print("Error: Countdown finished but index out of bounds.")
                 self.launch_all_btn.setEnabled(True) # Re-enable button
    # --- End Launch All Sequence ---

    def close_all(self):
        if not self.running_processes:
            self.show_status("No running programs to close", self.warning_color); return
        
        result = QMessageBox.question(self, "Close All Programs", 
            f"Are you sure you want to close all {len(self.running_processes)} running programs?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result != QMessageBox.StandardButton.Yes: return
        
        paths_to_close = list(self.running_processes.keys()); closed_count = 0
        for path in paths_to_close:
            for program in self.programs:
                widget = program["widget"]
                if widget.get_path() == path and widget.process and widget.process.poll() is None:
                    widget.close_program(); closed_count += 1
                    QApplication.processEvents()
                    QTimer.singleShot(300, lambda: None) # Small delay between closures
                    break
        self.show_status(f"Closed {closed_count} programs", self.warning_color)
    
    def update_close_all_button(self):
        self.close_all_btn.setEnabled(len(self.running_processes) > 0)
    
    def generate_numbered_profile_name(self, base_name):
        if base_name not in self.profiles: return base_name
        counter = 1
        while f"{base_name}{counter}" in self.profiles: counter += 1
        return f"{base_name}{counter}"
    
    def monitor_process(self, program_widget): pass # Handled by widget timer
    
    def on_programs_reordered(self, parent, start, end, destination, row):
        new_programs = []
        for i in range(self.program_list.count()):
            widget = self.program_list.itemWidget(self.program_list.item(i))
            for program in self.programs:
                if program["widget"] == widget: new_programs.append(program); break
        self.programs = new_programs
        self.mark_unsaved_changes()
        self.show_status("Programs reordered. Remember to save your profile.", self.warning_color)
        self._refresh_delay_ui_states() # Update delay states after reorder

    def _refresh_delay_ui_states(self):
        """Updates the enabled/disabled state of delay controls for all rows."""
        first_app_path_valid = False
        if len(self.programs) > 0:
            first_widget = self.programs[0]["widget"]
            first_path = first_widget.get_path()
            first_app_path_valid = bool(first_path and os.path.exists(first_path))

        for i, program_data in enumerate(self.programs):
            widget = program_data["widget"]
            widget.update_delay_ui_state(is_first_item=(i == 0), first_app_path_valid=first_app_path_valid)

    def new_profile_from_entry(self):
        profile_name = self.new_profile_entry.text().strip()
        if not profile_name: self.show_status("Please enter a profile name", self.warning_color); return
        
        original_display_name = self.default_profile_display_name
        if profile_name in self.profiles or profile_name == original_display_name:
            numbered_name = self.generate_numbered_profile_name(profile_name)
            result = QMessageBox.question(self, "Profile Already Exists",
                f"Profile '{profile_name}' already exists. Create '{numbered_name}' instead?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if result == QMessageBox.StandardButton.Yes: profile_name = numbered_name
            else: return
        
        self.profiles[profile_name] = {
            "launch_delay": 5,
            "programs": [
                {"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0}, 
                {"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0}
            ]
        }
        
        self.profile_combo.blockSignals(True)
        self.program_list.clear(); self.programs = []
        self.update_profile_combobox()
        self.current_profile = profile_name
        index = self.profile_combo.findText(profile_name)
        if index != -1: self.profile_combo.setCurrentIndex(index)
        self.load_profile(profile_name) # Load the new empty profile
        self.new_profile_entry.clear()
        self.changes_made = True # Mark as unsaved
        self.update_delete_button_state(); self.update_rename_button_state()
        self.profile_combo.blockSignals(False)
        self.show_status(f"Created new profile: {profile_name}", self.launched_color)
    
    def duplicate_current_profile(self):
        source_display_name = self.profile_combo.currentText()
        source_internal_name = "Default" if source_display_name == self.default_profile_display_name else source_display_name
        counter = 1; new_profile_name = f"{source_display_name} (Copy)"
        while new_profile_name in self.profiles:
            counter += 1; new_profile_name = f"{source_display_name} (Copy {counter})"
        
        if source_internal_name in self.profiles and isinstance(self.profiles[source_internal_name], dict):
            source_profile = self.profiles[source_internal_name]
            copied_programs = []
            for prog in source_profile.get("programs", []):
                new_prog = prog.copy()
                if 'use_custom_delay' not in new_prog: new_prog['use_custom_delay'] = False
                if 'custom_delay_value' not in new_prog: new_prog['custom_delay_value'] = 0
                if 'app_delay' in new_prog: del new_prog['app_delay']
                copied_programs.append(new_prog)
            copied_delay = source_profile.get("launch_delay", 5)
            self.profiles[new_profile_name] = {"launch_delay": copied_delay, "programs": copied_programs}
        else:
            self.profiles[new_profile_name] = {"launch_delay": 5, "programs": []}

        while len(self.profiles[new_profile_name]["programs"]) < 2:
            self.profiles[new_profile_name]["programs"].append({"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0})

        self.profile_combo.blockSignals(True)
        self.program_list.clear(); self.programs = []    
        self.update_profile_combobox()
        self.current_profile = new_profile_name
        index = self.profile_combo.findText(new_profile_name)
        if index != -1: self.profile_combo.setCurrentIndex(index)
        self.load_profile(new_profile_name)
        self.changes_made = True
        self.update_delete_button_state(); self.update_rename_button_state()
        self.profile_combo.blockSignals(False)
        self.show_status(f"Created duplicate profile: {new_profile_name}", self.launched_color)
    
    def rename_current_profile(self):
        current_profile_display = self.profile_combo.currentText()
        current_profile_internal = "Default" if current_profile_display == self.default_profile_display_name else current_profile_display
        is_default = (current_profile_internal == "Default")
        
        if is_default: self.show_status("Cannot rename the default profile", self.error_color); return
    
        new_name, ok = QInputDialog.getText(self, "Rename Profile", "Enter new profile name:", text=current_profile_internal)
        if not ok or not new_name or new_name == current_profile_internal: return
        
        conflicts_with_default = (new_name == "Default")
        conflicts_with_existing = (new_name in self.profiles and new_name != current_profile_internal)
        
        if conflicts_with_default or conflicts_with_existing:
            numbered_name = self.generate_numbered_profile_name(new_name)
            result = QMessageBox.question(self, "Profile Already Exists",
                f"Profile '{new_name}' already exists. Rename to '{numbered_name}' instead?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if result == QMessageBox.StandardButton.Yes: new_name = numbered_name
            else: return
        
        # Get the profile data dictionary
        profile_dict = self.profiles.pop(current_profile_internal) # Remove old entry
        self.profiles[new_name] = profile_dict # Add with new name
        self.current_profile = new_name
        self.show_status(f"Profile renamed to '{new_name}'", self.launched_color)
        
        self.update_profile_combobox()
        self.profile_combo.setCurrentText(new_name) # Set UI to new name
        self.changes_made = True
        self.save_config(False) # Save immediately
        self.load_profile(self.current_profile) # Refresh list (might be redundant)
        self.update_delete_button_state(); self.update_rename_button_state() # Update buttons for new name
    
    def delete_current_profile(self):
        current_profile_display = self.profile_combo.currentText()
        current_profile_internal = "Default" if current_profile_display == self.default_profile_display_name else current_profile_display
        is_default = (current_profile_internal == "Default")

        if is_default: self.show_status("Cannot delete the default profile", self.error_color); return

        if self.changes_made:
            result = QMessageBox.question(self, "Unsaved Changes",
                f"Save changes in '{current_profile_display}' before deleting?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Cancel)
            if result == QMessageBox.StandardButton.Cancel: return
            elif result == QMessageBox.StandardButton.Yes: self.save_config(False)

        result = QMessageBox.question(self, "Confirm Deletion",
            f"Delete the '{current_profile_display}' profile?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result != QMessageBox.StandardButton.Yes: return

        if current_profile_internal in self.profiles:
            del self.profiles[current_profile_internal]
            self.current_profile = "Default" # Switch internal state first
            self.load_profile("Default") # Load default profile UI
            self.save_config(False) # Save changes
            self.update_profile_combobox() # Update dropdown
            self.update_delete_button_state(); self.update_rename_button_state() 
            self.show_status(f"Profile '{current_profile_display}' deleted", self.warning_color)
    
    def change_profile(self, profile_name=None):
        if profile_name is None:
            display_name = self.profile_combo.currentText()
            profile_name = "Default" if display_name == self.default_profile_display_name else display_name
        
        if profile_name == self.current_profile: return
        
        if self.changes_made:
            current_display = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
            result = QMessageBox.question(self, "Unsaved Changes",
                f"Save changes in '{current_display}' before switching?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Cancel)
            if result == QMessageBox.StandardButton.Cancel:
                # Revert combobox selection
                current_display_index = self.profile_combo.findText(self.default_profile_display_name if self.current_profile == "Default" else self.current_profile)
                if current_display_index != -1:
                    self.profile_combo.blockSignals(True)
                    self.profile_combo.setCurrentIndex(current_display_index)
                    self.profile_combo.blockSignals(False)
                return
            elif result == QMessageBox.StandardButton.Yes:
                self.save_config(False)
        
        self.current_profile = profile_name
        self.load_profile(profile_name)
        self.changes_made = False
        self.update_delete_button_state(); self.update_rename_button_state()
        new_display = self.default_profile_display_name if profile_name == "Default" else profile_name
        self.show_status(f"Switched to profile: {new_display}", self.launched_color)
    
    def update_delete_button_state(self):
        is_default = (self.current_profile == "Default")
        self.delete_profile_btn.setEnabled(not is_default)
        self.delete_profile_btn.setToolTip("Cannot remove default profile" if is_default else "Remove Profile")

    def update_rename_button_state(self):
        is_default = (self.current_profile == "Default")
        self.rename_profile_btn.setEnabled(not is_default)
        self.rename_profile_btn.setToolTip("Cannot rename the default profile" if is_default else "Rename Profile")

    def closeEvent(self, event):
        if self.changes_made:
            profile_display = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
            msg_box = QMessageBox(self); msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Unsaved Changes"); msg_box.setText(f"Unsaved changes in profile '{profile_display}'.")
            msg_box.setInformativeText("Save before closing?"); 
            save_btn = msg_box.addButton("Save", QMessageBox.ButtonRole.AcceptRole)
            dont_save_btn = msg_box.addButton("Don't Save", QMessageBox.ButtonRole.DestructiveRole)
            cancel_btn = msg_box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
            msg_box.setDefaultButton(cancel_btn); msg_box.setEscapeButton(cancel_btn)
            msg_box.exec()
            clicked = msg_box.clickedButton()
            if clicked == save_btn: self.save_config(False); event.accept()
            elif clicked == dont_save_btn: event.accept()
            else: event.ignore()
        else: event.accept()
    
    def update_profile_combobox(self):
        self.profile_combo.blockSignals(True) # Block signals during update
        current_selection = self.profile_combo.currentText() # Store current selection
        self.profile_combo.clear()
        profile_names = sorted(self.profiles.keys())
        for name in profile_names:
            if not name: continue
            display = self.default_profile_display_name if name == "Default" else name
            self.profile_combo.addItem(display)
        
        # Try to restore selection
        target_display = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
        index = self.profile_combo.findText(target_display)
        if index != -1: self.profile_combo.setCurrentIndex(index)
        elif current_selection: # Fallback to previous selection if possible
             index = self.profile_combo.findText(current_selection)
             if index != -1: self.profile_combo.setCurrentIndex(index)

        self.profile_combo.blockSignals(False) # Re-enable signals
    
    def load_profile(self, profile_name):
        self.program_list.clear(); self.programs = []
        
        profile_dict = self.profiles.get(profile_name)
        
        # Ensure profile exists and is a dictionary
        if not isinstance(profile_dict, dict):
             print(f"Warning: Profile '{profile_name}' not found or invalid format. Creating default.")
             profile_dict = { "launch_delay": 5, "programs": [] }
             self.profiles[profile_name] = profile_dict # Add to profiles if it didn't exist

        program_data_list = profile_dict.get("programs", [])
        profile_delay = profile_dict.get("launch_delay", 5)
            
        # Ensure structure and migrate keys
        migrated = False
        while len(program_data_list) < 2:
            program_data_list.append({"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0}); migrated = True
        for prog_data in program_data_list:
            if not isinstance(prog_data, dict): continue # Skip invalid entries
            if 'app_delay' in prog_data: # Migrate from old key
                old_delay = prog_data.pop('app_delay'); migrated = True
                if old_delay is not None and isinstance(old_delay, int) and old_delay >= 0:
                    prog_data['use_custom_delay'] = True; prog_data['custom_delay_value'] = old_delay
                else:
                    prog_data['use_custom_delay'] = False; prog_data['custom_delay_value'] = 0
            else: # Ensure new keys exist
                if 'use_custom_delay' not in prog_data: prog_data['use_custom_delay'] = False; migrated = True
                if 'custom_delay_value' not in prog_data: prog_data['custom_delay_value'] = 0; migrated = True
        
        if migrated: # Update stored data if migration happened
            profile_dict["programs"] = program_data_list 
            
        self.profile_delay_spinbox.setValue(profile_delay)
            
        # Load program entries using new structure
        for program_data in program_data_list:
            if not isinstance(program_data, dict): continue # Skip invalid entries
            program_path = program_data.get("path", "")
            name = program_data.get("name", "")
            use_custom = program_data.get("use_custom_delay", False)
            custom_val = program_data.get("custom_delay_value", 0)
            self._add_with_process_check(name, program_path, use_custom, custom_val)
        
        self.update_close_all_button()
        self.program_list.viewport().update()
        QApplication.processEvents() # Added layout update
        self._refresh_delay_ui_states() # Update delay states after loading profile

    def _apply_styles_to_widget(self, program_widget):
        """Applies consistent styling to a ProgramWidget."""
        # Apply styles explicitly (important for consistency)
        button_style = """QPushButton { background-color: #772CE8; color: #FFFFFF; border: none; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 10pt; } QPushButton:hover { background-color: #9146FF; } QPushButton:disabled { background-color: #555555; color: #AAAAAA; }"""
        program_widget.browse_btn.setStyleSheet(button_style)
        program_widget.launch_btn.setStyleSheet(button_style)
        program_widget.close_btn.setStyleSheet(button_style)
        program_widget.remove_btn.setStyleSheet(button_style + "font-size: 14px;")
        line_edit_style = "padding: 2px 8px; color: #FFFFFF; background-color: #2E2E2E; border: 1px solid #444; border-radius: 4px;"
        program_widget.name_edit.setStyleSheet(line_edit_style)
        program_widget.path_edit.setStyleSheet(line_edit_style)
        # Use background-color: transparent for labels/checkbox to inherit item background
        program_widget.status_label.setStyleSheet("background-color: transparent; color: white; border-radius: 4px;")
        program_widget.drag_handle.setStyleSheet("background-color: transparent; color: #AAAAAA; font-size: 18px; border-radius: 4px;")
        program_widget.custom_delay_checkbox.setStyleSheet("background-color: transparent; color: white; border-radius: 4px;")
        program_widget.custom_delay_spinbox.setStyleSheet("background-color: #2E2E2E; color: white; border: 1px solid #444; border-radius: 4px;")

        # Force style refresh
        # Find the QListWidgetItem containing the ProgramWidget
        list_widget = program_widget.parent()
        item = None
        if isinstance(list_widget, QListWidget): # Check if parent is QListWidget
             for i in range(list_widget.count()):
                 current_item = list_widget.item(i)
                 widget = list_widget.itemWidget(current_item)
                 if widget == program_widget:
                     item = current_item
                     break
        elif isinstance(program_widget.parentWidget(), QListWidgetItem): # Check if parent is the item itself (less common)
             item = program_widget.parentWidget()

        if item: item.setBackground(QBrush(QColor("#2A2A2A"))) # Ensure default background
        if program_widget.style(): program_widget.style().unpolish(program_widget); program_widget.style().polish(program_widget)
        program_widget.update()

    def _add_with_process_check(self, name, path, use_custom_delay, custom_delay_value):
        program_widget = self.add_program(name, path, use_custom_delay, custom_delay_value)

        # Apply styles using the helper
        self._apply_styles_to_widget(program_widget)
        QApplication.processEvents() # Ensure styles apply visually

        # Check if process is already running
        if path and path in self.running_processes:
            process = self.running_processes[path]
            if process and process.poll() is None:
                program_widget.process = process
                program_widget.status_label.setText("Launched"); program_widget.status_label.setStyleSheet("color: #00C853;")
                program_widget.close_btn.setVisible(True)
                program_widget.process_timer = QTimer(program_widget)
                program_widget.process_timer.timeout.connect(program_widget.check_process_status)
                program_widget.process_timer.start(500)
    
    def mark_unsaved_changes(self):
        if not self.is_initial_loading:
            self.changes_made = True
            self.show_status("Changes made. Remember to save your profile.", self.warning_color)
    
    def show_status(self, message, color=None, duration=5000):
        if color is None: color = self.fg_color
        self.status_label.setText(message); self.status_label.setStyleSheet(f"color: {color};")
        if hasattr(self, '_status_timer') and self._status_timer is not None: self._status_timer.stop()
        self._status_timer = QTimer(self); self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self.clear_status); self._status_timer.start(duration)
    
    def clear_status(self): self.status_label.setText("")
    
    def save_config(self, show_confirmation=False):
        program_list_data = []
        for program in self.programs:
            widget = program["widget"]
            program_list_data.append({
                "name": widget.get_name(), "path": widget.get_path(),
                "use_custom_delay": widget.use_custom_delay, 
                "custom_delay_value": widget.custom_delay_value
            })
        
        # Ensure current profile exists and is dict
        if self.current_profile not in self.profiles or not isinstance(self.profiles.get(self.current_profile), dict):
             print(f"Warning: Profile '{self.current_profile}' invalid during save. Saving to 'Default'.")
             self.current_profile = "Default"
             if "Default" not in self.profiles or not isinstance(self.profiles.get("Default"), dict):
                 self.profiles["Default"] = {"launch_delay": 5, "programs": []} 

        # Update profile data
        current_profile_data = self.profiles[self.current_profile]
        current_profile_data["programs"] = program_list_data
        current_profile_data["launch_delay"] = self.profile_delay_spinbox.value()

        config = {
            "profiles": self.profiles,
            "current_profile": self.current_profile,
            "default_profile_display_name": self.default_profile_display_name,
            "show_low_delay_warning": self.show_low_delay_warning
        }
        
        success = self.config_manager.save_config(config)
        self.changes_made = False
        
        if success and show_confirmation:
            profile_name = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
            self.show_status(f"Profile '{profile_name}' saved successfully.", self.launched_color)
        elif not success:
            self.show_status("Failed to save profile.", self.error_color)
    
    def load_config(self):
        config = self.config_manager.load_config() # load_config now handles migration/defaults
        
        if config:
            self.profiles = config.get("profiles", {}) # Default to empty dict
            # --- Add safety check for self.profiles type ---
            if not isinstance(self.profiles, dict):
                print(f"Warning: Loaded 'profiles' data is not a dictionary. Resetting profiles.")
                self.profiles = {"Default": {"launch_delay": 5, "programs": []}}
            # --- End safety check ---
            self.current_profile = config.get("current_profile", "Default")
            self.default_profile_display_name = config.get("default_profile_display_name", "Default")
            self.show_low_delay_warning = config.get("show_low_delay_warning", True)
            
            # Ensure current_profile exists, default to "Default" if not
            if self.current_profile not in self.profiles:
                print(f"Warning: Loaded current_profile '{self.current_profile}' not found. Defaulting.")
                self.current_profile = "Default"
                
        # Ensure Default profile exists *after* loading potentially empty profiles
        if "Default" not in self.profiles or not isinstance(self.profiles["Default"], dict):
             self.profiles["Default"] = {"launch_delay": 5, "programs": [
                 {"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0}, 
                 {"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0}
             ]}
        # Also ensure Default has minimum structure if it exists but is malformed
        else: # Check existing Default profile
            default_profile = self.profiles["Default"]
            if "launch_delay" not in default_profile: 
                 default_profile["launch_delay"] = 5
            if "programs" not in default_profile or not isinstance(default_profile["programs"], list): 
                 default_profile["programs"] = []
        
            # Ensure Default programs list has minimum length and correct keys
            while len(default_profile["programs"]) < 2:
                 default_profile["programs"].append({"name": "", "path": "", "use_custom_delay": False, "custom_delay_value": 0})
            for prog in default_profile["programs"]:
                 if 'use_custom_delay' not in prog: 
                     prog['use_custom_delay'] = False
                 if 'custom_delay_value' not in prog: 
                     prog['custom_delay_value'] = 0
                 if 'app_delay' in prog: 
                     # Clean up old key if present
                     del prog['app_delay'] 

        self.is_initial_loading = True
        self.update_profile_combobox()
        self.load_profile(self.current_profile) # load_profile handles structure check for the loaded one
        self.changes_made = False
        self.update_delete_button_state(); self.update_rename_button_state()
        self.is_initial_loading = False # Set to false after initial load
