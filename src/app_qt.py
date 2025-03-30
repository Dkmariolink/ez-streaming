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
Main application module containing the core UI and functionality (Qt version)
"""

import os
import sys
import subprocess
import time
import functools # Added for QTimer lambda issue
import copy # For deep copying profiles
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                              QHBoxLayout, QLabel, QComboBox, QPushButton,
                              QLineEdit, QListWidget, QListWidgetItem, QFrame,
                              QMessageBox, QFileDialog, QInputDialog, QGraphicsOpacityEffect,
                              QSpinBox, QCheckBox)
from PySide6.QtCore import Qt, Signal, QSize, QTimer, QPropertyAnimation, QEasingCurve, QRect, QEvent
from PySide6.QtGui import QIcon, QPixmap, QBrush, QColor, QFont, QFontDatabase

from config_manager import ConfigManager
from style_manager import StyleManager # Import StyleManager
from process_manager import ProcessManager # Import ProcessManager
from config_models import ProfileConfig, ProgramConfig # Import model classes
from launch_sequence import LaunchSequence # Import LaunchSequence
from exceptions import ProcessError, ConfigError # Import custom exceptions
from event_bus import UIEventBus, STATUS_UPDATE, PROCESS_LIST_CHANGED, LAUNCH_SEQUENCE_STATE_CHANGED # Import Event Bus

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
        # Style applied later via _apply_styles_to_widget
        self.drag_handle.setFixedWidth(30)
        self.drag_handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
        layout.addWidget(self.drag_handle)

        # Program name
        self.name_edit = QLineEdit(self.name)
        self.name_edit.setPlaceholderText("App Name")
        self.name_edit.setMinimumWidth(150) # Reduced min width
        self.name_edit.setMinimumHeight(30)
        # Style applied later via _apply_styles_to_widget
        self.name_edit.setClearButtonEnabled(True)
        layout.addWidget(self.name_edit, 2) # Stretch factor 2

        # Program path
        self.path_edit = QLineEdit(self.path)
        self.path_edit.setPlaceholderText("Program Path")
        self.path_edit.setMinimumWidth(250) # Reduced min width
        self.path_edit.setMinimumHeight(30)
        # Style applied later via _apply_styles_to_widget
        self.path_edit.setClearButtonEnabled(True)

        # Create browse_btn here but add it to the main layout later
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.setMinimumHeight(32)
        # Style applied later via _apply_styles_to_widget

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

        # Buttons created, styles applied later via _apply_styles_to_widget
        self.launch_btn = QPushButton("Launch")
        self.launch_btn.setFixedWidth(80)
        self.launch_btn.setMinimumHeight(32)
        self.button_layout.addWidget(self.launch_btn)

        self.close_btn = QPushButton("Close")
        self.close_btn.setFixedWidth(80)
        self.close_btn.setMinimumHeight(32)
        self.close_btn.setVisible(False)
        self.close_btn.setToolTip("Close App")
        self.button_layout.addWidget(self.close_btn)

        self.remove_btn = QPushButton("✕")
        self.remove_btn.setFixedSize(32, 32)
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
        style_manager = self.window().style_manager if self.window() and hasattr(self.window(), 'style_manager') else None
        tooltip_checkbox = ""
        tooltip_spinbox = ""
        tooltip_buttons = "" # Tooltip for buttons when disabled

        if can_potentially_enable_delay:
            tooltip_checkbox = "Enable to set a specific delay for this app, overriding the profile default."
            tooltip_spinbox = "Delay before launching this app (seconds)."
            tooltip_buttons = "" # Use default button tooltips
        elif is_first_item:
            tooltip_checkbox = "Delay is not applicable for the first app in the sequence."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox
        elif not first_app_path_valid: # Not first item, but first app path is invalid
            tooltip_checkbox = "Delay requires the first app to have a valid path."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox
        else: # Not first item, first app valid, but *this* path is invalid
            tooltip_checkbox = "Delay requires a valid program path in this row."
            tooltip_spinbox = tooltip_checkbox
            tooltip_buttons = tooltip_checkbox

        if style_manager:
            self.custom_delay_checkbox.setStyleSheet(style_manager.get_checkbox_style(enabled=can_potentially_enable_delay))
        else: # Fallback if style manager not found
             checkbox_color = "#FFFFFF" if can_potentially_enable_delay else "#AAAAAA"
             self.custom_delay_checkbox.setStyleSheet(f"background-color: transparent; color: {checkbox_color}; border-radius: 4px;")
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
        if isinstance(app_window, StreamerApp) and hasattr(app_window, 'show_low_delay_warning'):
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
            # Emit data changed signal after path/name update
            self.on_data_changed()


    def launch_program(self):
        """Launch the program (immediately, no delay here)"""
        path = self.path_edit.text()
        app_window = self.window() # Get window ref
        if not app_window or not isinstance(app_window, StreamerApp): return None # Safety check
        style_manager = app_window.style_manager
        process_manager = app_window.process_manager
        event_bus = app_window.event_bus # Get event bus

        if not path:
            event_bus.publish(STATUS_UPDATE, {"message": "Cannot launch: No program path provided", "color": style_manager.warning_color})
            return None
        if not os.path.exists(path):
            event_bus.publish(STATUS_UPDATE, {"message": f"Error: Program path does not exist: {path}", "color": style_manager.error_color})
            return None
        try:
            self.status_label.setText("Launching...")
            self.status_label.setStyleSheet(style_manager.get_status_label_style('launching'))
            QApplication.processEvents()
            program_dir = os.path.dirname(path)
            self.process = subprocess.Popen([path], cwd=program_dir)
            self.process_timer = QTimer(self)
            self.process_timer.timeout.connect(self.check_process_status)
            self.process_timer.start(500)
            self.close_btn.setVisible(True)
            process_manager.track(path, self.process) # Use ProcessManager
            return self.process
        except (OSError, subprocess.SubprocessError, Exception) as e: # Catch broader errors
            error_msg = f"Error launching '{os.path.basename(path)}': {str(e)}"
            self.status_label.setText("Error"); self.status_label.setStyleSheet(style_manager.get_status_label_style('error'))
            event_bus.publish(STATUS_UPDATE, {"message": error_msg, "color": style_manager.error_color})
            # Raise ProcessError to potentially handle it higher up if needed
            # raise ProcessError(error_msg) from e
            return None # Keep returning None for now

    def check_process_status(self):
        """Check the status of the launched process"""
        app_window = self.window()
        if not app_window or not isinstance(app_window, StreamerApp): return # Safety check
        style_manager = app_window.style_manager
        process_manager = app_window.process_manager

        if not hasattr(self, 'process') or self.process is None:
            self.reset_status(); self.close_btn.setVisible(False)
            if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()
            return
        try:
            return_code = self.process.poll()
            if return_code is None:
                self.status_label.setText("Launched"); self.status_label.setStyleSheet(style_manager.get_status_label_style('launched'))
                self.close_btn.setVisible(True)
            else:
                self.reset_status(); self.process = None; self.close_btn.setVisible(False)
                path = self.path_edit.text()
                if path: process_manager.untrack(path) # Use ProcessManager
                if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()
        except Exception as e: # Catch potential errors during poll()
            print(f"Error checking process status for {self.get_name()}: {e}")
            self.reset_status(); self.process = None; self.close_btn.setVisible(False)
            path = self.path_edit.text()
            if path: process_manager.untrack(path) # Use ProcessManager
            if hasattr(self, 'process_timer') and self.process_timer: self.process_timer.stop()

    def close_program(self):
        """Close the running program after confirmation"""
        app_window = self.window()
        if not app_window or not isinstance(app_window, StreamerApp): return # Safety check
        style_manager = app_window.style_manager
        process_manager = app_window.process_manager
        event_bus = app_window.event_bus # Get event bus

        if hasattr(self, 'process') and self.process and self.process.poll() is None:
            path = self.path_edit.text()
            app_name = self.get_name() or "this app"

            # Add confirmation dialog
            result = QMessageBox.question(self, "Confirm Close", f"Are you sure you want to close {app_name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if result != QMessageBox.StandardButton.Yes:
                return # User cancelled

            try:
                print(f"[ProgramWidget] Terminating '{app_name}' (PID: {self.process.pid})...")
                self.process.terminate()
                # Wait briefly for graceful termination
                try:
                    self.process.wait(timeout=0.5) # Wait up to 0.5 seconds
                except subprocess.TimeoutExpired:
                    print(f"  Process {self.process.pid} did not terminate gracefully, killing.")
                    if sys.platform == "win32":
                        try:
                            # Use taskkill on Windows for more robust termination
                            subprocess.run(['taskkill', '/F', '/PID', str(self.process.pid)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except Exception as tk_err:
                            print(f"  taskkill failed ({tk_err}), falling back to process.kill()")
                            self.process.kill() # Fallback kill
                    else:
                        self.process.kill() # Kill on non-Windows

                # Ensure status is updated even if wait/kill fails but process is gone
                if self.process.poll() is not None:
                    self.reset_status(); self.close_btn.setVisible(False)
                    process_manager.untrack(path) # Use ProcessManager
                    app_name = self.get_name() # Get name again in case it changed?
                    event_bus.publish(STATUS_UPDATE, {"message": f"Closed {app_name}", "color": style_manager.warning_color})
                else:
                    # This case should be rare after kill attempts
                    print(f"  Warning: Process {self.process.pid} still running after termination attempts.")
                    event_bus.publish(STATUS_UPDATE, {"message": f"Failed to fully close {app_name}", "color": style_manager.error_color})

            except (OSError, ProcessLookupError, Exception) as e: # Catch errors during termination/kill
                error_msg = f"Error closing program '{app_name}': {str(e)}"
                print(error_msg)
                event_bus.publish(STATUS_UPDATE, {"message": error_msg, "color": style_manager.error_color})
                # Attempt to untrack anyway if the process might be gone
                if path: process_manager.untrack(path)
                self.reset_status(); self.close_btn.setVisible(False)
                # Raise ProcessError to potentially handle it higher up if needed
                # raise ProcessError(error_msg) from e


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
        """Emits the data_changed signal."""
        self.data_changed.emit() # Emit signal for StreamerApp to handle

    def reset_status(self):
        style_manager = self.window().style_manager if self.window() and hasattr(self.window(), 'style_manager') else None
        if style_manager:
            self.status_label.setText("Ready"); self.status_label.setStyleSheet(style_manager.get_status_label_style('ready'))
        else:
             self.status_label.setText("Ready"); self.status_label.setStyleSheet("background-color: transparent; color: white;")
        QApplication.processEvents()

class StreamerApp(QMainWindow):
    """Main application window for EZ Streaming"""

    def __init__(self):
        super().__init__()
        self.programs = [] # Holds {"widget": ProgramWidget, "item": QListWidgetItem}
        self.config_manager = ConfigManager()
        self.current_profile = "Default"
        # self.profiles = {"Default": {"launch_delay": 5, "programs": []}} # Now stores ProfileConfig objects
        self.profiles: dict[str, ProfileConfig] = {} # Initialize as empty dict expecting ProfileConfig objects
        self.changes_made = False
        self.is_initial_loading = True
        self.default_profile_display_name = "Default"
        # self.running_processes = {} # Replaced by ProcessManager
        self.summer_blaster_font = None
        self.title_opacity_effect = None
        self.title_animation = None
        self.show_low_delay_warning = True
        # --- Removed old launch sequence attributes ---

        self.event_bus = UIEventBus() # Instantiate Event Bus
        self.style_manager = StyleManager() # Instantiate StyleManager
        self.process_manager = ProcessManager(self, self.event_bus) # Instantiate ProcessManager, pass event bus
        self.launch_sequence = LaunchSequence(self, self.event_bus) # Instantiate LaunchSequence, pass event bus

        # self.setStyleSheet("QWidget:focus { outline: none; }") # Moved to setup_styling

        self.setup_ui()
        self.connect_signals()
        self.subscribe_to_events() # Subscribe to events
        self.load_config() # Load config which now returns ProfileConfig objects

        self.setWindowTitle("EZ Streaming")
        self.setMinimumSize(1100, 700)
        self.resize(1150, 750)

        self.setup_app_icon_and_font()
        self.update_delete_button_state()
        self.update_rename_button_state()

        self.is_initial_loading = False

    # --- UI Setup Methods ---

    def _setup_header(self, main_layout):
        """Sets up the header section with the title."""
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
            self.title_image_label.setStyleSheet(f"color: {self.style_manager.accent_color}; font-size: 24pt; font-weight: bold;") # Use style manager color
        header_layout.addWidget(self.title_image_label)
        main_layout.addWidget(header_frame)

    def _setup_profile_area(self, main_layout):
        """Sets up the profile selection and management area."""
        profile_frame = QFrame()
        profile_layout = QHBoxLayout(profile_frame)
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.addWidget(QLabel("Current Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumHeight(32); self.profile_combo.setMinimumWidth(220); # Style from main stylesheet
        profile_layout.addWidget(self.profile_combo)
        self.delete_profile_btn = QPushButton("🗑"); self.delete_profile_btn.setFixedSize(36, 36); self.delete_profile_btn.setStyleSheet("font-size: 16px;"); self.delete_profile_btn.setToolTip("Remove Profile")
        profile_layout.addWidget(self.delete_profile_btn)
        self.rename_profile_btn = QPushButton("✏️"); self.rename_profile_btn.setFixedSize(36, 36); self.rename_profile_btn.setStyleSheet("font-size: 16px;"); self.rename_profile_btn.setToolTip("Rename Profile")
        profile_layout.addWidget(self.rename_profile_btn)
        self.duplicate_profile_btn = QPushButton("📋"); self.duplicate_profile_btn.setFixedSize(36, 36); self.duplicate_profile_btn.setStyleSheet("font-size: 16px;"); self.duplicate_profile_btn.setToolTip("Copy Profile")
        profile_layout.addWidget(self.duplicate_profile_btn)
        profile_layout.addWidget(QLabel("New Profile:"), 0, Qt.AlignmentFlag.AlignRight) # Align right
        self.new_profile_entry = QLineEdit(); self.new_profile_entry.setFixedWidth(200); self.new_profile_entry.setMinimumHeight(32); # Style from main stylesheet
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

    def _setup_list_header(self, main_layout):
        """Sets up the header row for the program list."""
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

    def _setup_program_list(self, main_layout):
        """Sets up the main list widget for programs."""
        self.program_list = QListWidget()
        self.program_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.program_list.setDefaultDropAction(Qt.MoveAction)
        self.program_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.program_list.setAlternatingRowColors(True)
        self.program_list.setFocusPolicy(Qt.NoFocus)
        # Styles are now set globally by setup_styling
        main_layout.addWidget(self.program_list)

    def _setup_status_bar(self, main_layout):
        """Sets up the status label."""
        self.status_label = QLabel(""); self.status_label.setMinimumHeight(30)
        main_layout.addWidget(self.status_label)

    def _setup_action_buttons(self, main_layout):
        """Sets up the main action buttons (Add, Close All, Save, Launch All)."""
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

    def _setup_footer(self, main_layout):
        """Sets up the footer credit label."""
        credit_label = QLabel("Created by Dkmariolink - Free Software")
        credit_label.setStyleSheet("color: #AAAAAA; font-size: 8pt;")
        credit_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(credit_label)

    # --- End UI Setup Methods ---

    # Removed track_process and untrack_process, now handled by ProcessManager

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
        """Sets up the main UI by calling helper methods."""
        self.setup_styling()
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        self._setup_header(main_layout)
        self._setup_profile_area(main_layout)
        self._setup_list_header(main_layout)
        self._setup_program_list(main_layout)
        self._setup_status_bar(main_layout)
        self._setup_action_buttons(main_layout)
        self._setup_footer(main_layout)

        self.setCentralWidget(main_widget)

    def setup_styling(self):
        """Applies the main stylesheet using StyleManager."""
        self.setStyleSheet(self.style_manager.get_main_stylesheet())

    def connect_signals(self):
        self.add_btn.clicked.connect(self.add_program_ui_only) # Changed: Only adds UI row
        self.save_btn.clicked.connect(lambda: self.save_config(True))
        self.launch_all_btn.clicked.connect(self.handle_launch_all_click) # Use new handler
        self.close_all_btn.clicked.connect(self.process_manager.close_all) # Use ProcessManager
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

    def subscribe_to_events(self):
        """Subscribe UI update methods to events from the event bus."""
        self.event_bus.subscribe(STATUS_UPDATE, self._handle_status_update)
        self.event_bus.subscribe(PROCESS_LIST_CHANGED, self.update_close_all_button)
        self.event_bus.subscribe(LAUNCH_SEQUENCE_STATE_CHANGED, self._handle_launch_sequence_state)

    # --- Event Handlers ---
    def _handle_status_update(self, data):
        """Handles status updates published on the event bus."""
        if isinstance(data, dict):
            message = data.get("message", "")
            color = data.get("color") # Can be None
            duration = data.get("duration", 5000)
            self.show_status(message, color, duration)
        else:
            print(f"Warning: Received invalid data format for STATUS_UPDATE event: {data}")

    def _handle_launch_sequence_state(self, data):
        """Handles launch sequence state changes."""
        if isinstance(data, dict):
            state = data.get("state")
            if state == "started":
                self.launch_all_btn.setEnabled(False)
            elif state == "finished":
                self.launch_all_btn.setEnabled(True)
                # Optionally use launched_count/total_count from data for more detailed feedback
        else:
             print(f"Warning: Received invalid data format for LAUNCH_SEQUENCE_STATE_CHANGED event: {data}")


    def on_selection_changed(self):
        for i in range(self.program_list.count()):
            item = self.program_list.item(i)
            item.setBackground(QBrush(QColor(self.style_manager.list_item_selected_bg)) if item.isSelected() else QBrush(QColor(self.style_manager.list_item_bg))) # Use style manager colors

    def on_profile_delay_changed(self, value):
        profile = self.profiles.get(self.current_profile)
        # if isinstance(profile, dict): # Changed to check ProfileConfig
        if isinstance(profile, ProfileConfig):
            # profile['launch_delay'] = value # Changed to attribute access
            profile.launch_delay = value
            self.on_data_changed(source="profile_setting") # Use centralized handler
            if 0 < value < 5 and self.show_low_delay_warning:
                self.show_low_delay_warning_message()

    def add_program_ui_only(self, name="", path="", use_custom_delay=False, custom_delay_value=0):
        """Adds a program widget to the UI list only. Does not modify config."""
        program_widget = ProgramWidget(name, path, use_custom_delay, custom_delay_value)
        item = QListWidgetItem(self.program_list)
        self.program_list.addItem(item)
        size_hint = program_widget.sizeHint()
        item.setSizeHint(QSize(size_hint.width(), size_hint.height() + 18))
        self.program_list.setItemWidget(item, program_widget)
        program_widget.removed.connect(self.remove_program) # Connect removal signal
        program_widget.data_changed.connect(lambda: self.on_data_changed(source="program")) # Connect to centralized handler with source
        self.programs.append({"widget": program_widget, "item": item}) # Add to internal widget tracking list

        self._apply_styles_to_widget(program_widget)
        self.program_list.viewport().update()
        QApplication.processEvents()
        self._refresh_delay_ui_states()
        self.on_data_changed(source="program") # Adding a row is a change, specify source

        return program_widget

    def remove_program(self, program_widget):
        """Removes a program widget from the list and marks changes."""
        for i, program_dict in enumerate(self.programs):
            if program_dict["widget"] == program_widget:
                item = program_dict["item"]
                row = self.program_list.row(item)
                self.program_list.takeItem(row)
                self.programs.pop(i)
                # self.mark_unsaved_changes() # Replaced by on_data_changed
                app_name = program_widget.get_name()
                status_msg = f"Program '{app_name}' removed." if app_name else "Blank entry removed."
                # Publish status update via event bus
                self.event_bus.publish(STATUS_UPDATE, {
                    "message": status_msg + " Remember to save your profile.",
                    "color": self.style_manager.warning_color
                })
                self.on_data_changed(source="program") # Removal is a change
                self._refresh_delay_ui_states() # Update delay states after removal
                break

    def show_low_delay_warning_message(self):
        msg_box = QMessageBox(self); msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Low Launch Delay")
        msg_box.setText("Setting a launch delay below 5 seconds may cause system instability or overload. Proceed with caution.")
        checkbox = QCheckBox("Do not show this warning again"); msg_box.setCheckBox(checkbox)
        msg_box.addButton(QMessageBox.StandardButton.Ok); msg_box.exec()
        if checkbox.isChecked():
            self.show_low_delay_warning = False
            self.on_data_changed(source="setting") # Changed a setting

    # --- Launch All Sequence (Now handled by LaunchSequence class) ---
    def handle_launch_all_click(self):
        """Gathers program widgets and starts the launch sequence."""
        if self.launch_sequence.is_running():
            print("Launch sequence is already running.")
            return
        # Pass the list of widget dictionaries currently in the UI
        self.launch_sequence.start(self.programs)

    # Removed start_launch_sequence, _launch_next_app_in_sequence, _update_countdown_status

    # Removed close_all, now handled by ProcessManager

    def update_close_all_button(self, data=None): # Accept optional data from event
        """Updates the enabled state of the 'Close All' button based on running processes."""
        running_count = len(self.process_manager.get_running_processes())
        self.close_all_btn.setEnabled(running_count > 0)
        self.close_all_btn.setText(f"Close All ({running_count})" if running_count > 0 else "Close All")


    def generate_numbered_profile_name(self, base_name):
        if base_name not in self.profiles: return base_name
        counter = 1
        while f"{base_name}{counter}" in self.profiles: counter += 1
        return f"{base_name}{counter}"

    def monitor_process(self, program_widget): pass # Handled by widget timer

    def on_programs_reordered(self, parent, start, end, destination, row):
        """Updates the program order in the current ProfileConfig object."""
        current_profile_obj = self.profiles.get(self.current_profile)
        if not current_profile_obj: return

        # Reorder the internal list of ProgramConfig objects based on the new widget order
        new_program_configs = []
        temp_widget_list = [] # Keep track of widgets in UI order
        for i in range(self.program_list.count()):
            widget = self.program_list.itemWidget(self.program_list.item(i))
            temp_widget_list.append(widget)
            # Find the corresponding ProgramConfig (this is inefficient, consider mapping)
            found = False
            # Search existing configs first
            for pc in current_profile_obj.programs:
                 # Match based on current widget data, as config might not be saved yet
                 if pc.name == widget.get_name() and pc.path == widget.get_path():
                     new_program_configs.append(pc)
                     found = True
                     break
            # If not found (e.g., a newly added unsaved row), create a temporary config
            if not found:
                 new_program_configs.append(ProgramConfig(
                     name=widget.get_name(),
                     path=widget.get_path(),
                     use_custom_delay=widget.use_custom_delay,
                     custom_delay_value=widget.custom_delay_value
                 ))

        # Update the ProfileConfig object's programs list
        current_profile_obj.programs = new_program_configs

        # Update the self.programs list (used for widget/item mapping)
        new_programs_list_map = []
        for widget in temp_widget_list:
             for p_dict in self.programs:
                 if p_dict["widget"] == widget:
                     new_programs_list_map.append(p_dict)
                     break
        self.programs = new_programs_list_map

        self.on_data_changed(source="program") # Reordering is a change
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
        if not profile_name:
            self.event_bus.publish(STATUS_UPDATE, {"message": "Please enter a profile name", "color": self.style_manager.warning_color})
            return

        original_display_name = self.default_profile_display_name
        if profile_name in self.profiles or profile_name == original_display_name:
            numbered_name = self.generate_numbered_profile_name(profile_name)
            result = QMessageBox.question(self, "Profile Already Exists",
                f"Profile '{profile_name}' already exists. Create '{numbered_name}' instead?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.Yes)
            if result == QMessageBox.StandardButton.Yes: profile_name = numbered_name
            else: return

        # Create a new ProfileConfig object
        new_profile = ProfileConfig(name=profile_name)
        # Ensure it has the minimum program slots
        while len(new_profile.programs) < 2:
            new_profile.programs.append(ProgramConfig())
        self.profiles[profile_name] = new_profile

        self.profile_combo.blockSignals(True)
        self.program_list.clear(); self.programs = []
        self.update_profile_combobox()
        self.current_profile = profile_name
        index = self.profile_combo.findText(profile_name)
        if index != -1: self.profile_combo.setCurrentIndex(index)
        self.load_profile(profile_name) # Load the new empty profile
        self.new_profile_entry.clear()
        # self.changes_made = True # Handled by on_data_changed
        self.update_delete_button_state(); self.update_rename_button_state()
        self.profile_combo.blockSignals(False)
        self.on_data_changed(source="profile") # Creating profile is a change
        self.event_bus.publish(STATUS_UPDATE, {"message": f"Created new profile: {profile_name}", "color": self.style_manager.launched_color})

    def duplicate_current_profile(self):
        source_display_name = self.profile_combo.currentText()
        source_internal_name = "Default" if source_display_name == self.default_profile_display_name else source_display_name
        counter = 1; new_profile_name = f"{source_display_name} (Copy)"
        while new_profile_name in self.profiles:
            counter += 1; new_profile_name = f"{source_display_name} (Copy {counter})"

        source_profile_obj = self.profiles.get(source_internal_name)
        if not isinstance(source_profile_obj, ProfileConfig):
             self.event_bus.publish(STATUS_UPDATE, {"message": f"Error: Source profile '{source_internal_name}' not found or invalid.", "color": self.style_manager.error_color})
             return

        # Create a deep copy to avoid modifying the original's program list
        new_profile_obj = ProfileConfig(
            name=new_profile_name,
            launch_delay=source_profile_obj.launch_delay,
            programs=copy.deepcopy(source_profile_obj.programs) # Deep copy the list of ProgramConfig objects
        )

        # Ensure minimum program slots in the copy
        while len(new_profile_obj.programs) < 2:
            new_profile_obj.programs.append(ProgramConfig())

        self.profiles[new_profile_name] = new_profile_obj

        self.profile_combo.blockSignals(True)
        self.program_list.clear(); self.programs = []
        self.update_profile_combobox()
        self.current_profile = new_profile_name
        index = self.profile_combo.findText(new_profile_name)
        if index != -1: self.profile_combo.setCurrentIndex(index)
        self.load_profile(new_profile_name)
        # self.changes_made = True # Handled by on_data_changed
        self.update_delete_button_state(); self.update_rename_button_state()
        self.profile_combo.blockSignals(False)
        self.on_data_changed(source="profile") # Duplicating profile is a change
        self.event_bus.publish(STATUS_UPDATE, {"message": f"Created duplicate profile: {new_profile_name}", "color": self.style_manager.launched_color})

    def rename_current_profile(self):
        current_profile_display = self.profile_combo.currentText()
        current_profile_internal = "Default" if current_profile_display == self.default_profile_display_name else current_profile_display
        is_default = (current_profile_internal == "Default")

        if is_default:
            self.event_bus.publish(STATUS_UPDATE, {"message": "Cannot rename the default profile", "color": self.style_manager.error_color})
            return

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

        # Get the ProfileConfig object
        profile_obj = self.profiles.pop(current_profile_internal) # Remove old entry
        profile_obj.name = new_name # Update the name attribute
        self.profiles[new_name] = profile_obj # Add with new name
        self.current_profile = new_name
        self.event_bus.publish(STATUS_UPDATE, {"message": f"Profile renamed to '{new_name}'", "color": self.style_manager.launched_color})

        self.update_profile_combobox()
        self.profile_combo.setCurrentText(new_name) # Set UI to new name
        # self.changes_made = True # Handled by on_data_changed
        self.save_config(False) # Save immediately after rename
        self.on_data_changed(source="profile") # Renaming profile is a change
        self.update_delete_button_state(); self.update_rename_button_state() # Update buttons for new name

    def delete_current_profile(self):
        current_profile_display = self.profile_combo.currentText()
        current_profile_internal = "Default" if current_profile_display == self.default_profile_display_name else current_profile_display
        is_default = (current_profile_internal == "Default")

        if is_default:
            self.event_bus.publish(STATUS_UPDATE, {"message": "Cannot delete the default profile", "color": self.style_manager.error_color})
            return

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
            self.event_bus.publish(STATUS_UPDATE, {"message": f"Profile '{current_profile_display}' deleted", "color": self.style_manager.warning_color})
            self.on_data_changed(source="profile") # Deleting profile is a change

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
        self.changes_made = False # Reset changes flag after loading new profile
        self.save_btn.setEnabled(False) # Disable save button after loading
        self.update_delete_button_state(); self.update_rename_button_state()
        new_display = self.default_profile_display_name if profile_name == "Default" else profile_name
        self.event_bus.publish(STATUS_UPDATE, {"message": f"Switched to profile: {new_display}", "color": self.style_manager.launched_color})

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
        """Loads the UI elements based on the selected ProfileConfig object."""
        self.program_list.clear(); self.programs = []

        profile_obj = self.profiles.get(profile_name)

        # Ensure profile exists and is a ProfileConfig object
        if not isinstance(profile_obj, ProfileConfig):
             print(f"Warning: Profile '{profile_name}' not found or invalid format. Loading default.")
             profile_obj = self.profiles.get("Default") # Fallback to default
             if not isinstance(profile_obj, ProfileConfig): # If default is also broken
                  print("Error: Default profile is invalid. Creating a new default.")
                  profile_obj = ProfileConfig(name="Default")
                  self.profiles["Default"] = profile_obj
             self.current_profile = "Default" # Switch to default internally
             # Update combobox to reflect the switch to default
             default_display_index = self.profile_combo.findText(self.default_profile_display_name)
             if default_display_index != -1:
                 self.profile_combo.setCurrentIndex(default_display_index)


        # Load profile delay
        self.profile_delay_spinbox.setValue(profile_obj.launch_delay)

        # Load program entries using ProgramConfig objects
        for program_config in profile_obj.programs:
            self._add_with_process_check(
                program_config.name,
                program_config.path,
                program_config.use_custom_delay,
                program_config.custom_delay_value
            )

        self.update_close_all_button()
        self.program_list.viewport().update()
        QApplication.processEvents() # Added layout update
        self._refresh_delay_ui_states() # Update delay states after loading profile
        self.changes_made = False # Reset changes flag after loading
        self.save_btn.setEnabled(False) # Disable save button after loading

    def _apply_styles_to_widget(self, program_widget):
        """Applies consistent styling to a ProgramWidget using StyleManager."""
        if not hasattr(self, 'style_manager'): return # Safety check

        # Apply styles explicitly using StyleManager methods
        button_style = self.style_manager.get_button_style()
        program_widget.browse_btn.setStyleSheet(button_style)
        program_widget.launch_btn.setStyleSheet(button_style)
        program_widget.close_btn.setStyleSheet(button_style)
        program_widget.remove_btn.setStyleSheet(self.style_manager.get_button_style("font-size: 14px;")) # Add specific font size
        line_edit_style = self.style_manager.get_line_edit_style()
        program_widget.name_edit.setStyleSheet(line_edit_style)
        program_widget.path_edit.setStyleSheet(line_edit_style)
        # Use background-color: transparent for labels/checkbox to inherit item background
        program_widget.status_label.setStyleSheet(self.style_manager.get_status_label_style('ready'))
        program_widget.drag_handle.setStyleSheet(self.style_manager.get_drag_handle_style())
        program_widget.custom_delay_checkbox.setStyleSheet(self.style_manager.get_checkbox_style())
        # Spinbox style is handled by main stylesheet

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

        if item: item.setBackground(QBrush(QColor(self.style_manager.list_item_bg))) # Ensure default background using style manager
        if program_widget.style(): program_widget.style().unpolish(program_widget); program_widget.style().polish(program_widget)
        program_widget.update()

    def _add_with_process_check(self, name, path, use_custom_delay, custom_delay_value):
        """Adds a program widget and checks if the process is already running."""
        # Use add_program_ui_only as we are loading from config, not adding a new entry to config yet
        program_widget = self.add_program_ui_only(name, path, use_custom_delay, custom_delay_value)

        # Apply styles using the helper
        self._apply_styles_to_widget(program_widget)
        QApplication.processEvents() # Ensure styles apply visually

        # Check if process is already running using ProcessManager
        if path and self.process_manager.is_running(path):
            process = self.process_manager.get_running_processes()[path]
            if process and process.poll() is None:
                program_widget.process = process
                program_widget.status_label.setText("Launched"); program_widget.status_label.setStyleSheet(self.style_manager.get_status_label_style('launched')) # Use style manager
                program_widget.close_btn.setVisible(True)
                program_widget.process_timer = QTimer(program_widget)
                program_widget.process_timer.timeout.connect(program_widget.check_process_status)
                program_widget.process_timer.start(500)

    # Replaced mark_unsaved_changes with on_data_changed
    def on_data_changed(self, source=None):
        """Centralized handler for data changes."""
        if not self.is_initial_loading:
            self.changes_made = True
            self.save_btn.setEnabled(True) # Enable save button on any change
            self.event_bus.publish(STATUS_UPDATE, {
                "message": "Changes made. Remember to save your profile.",
                "color": self.style_manager.warning_color
            })
            # Specific updates based on source
            if source == "program":
                self._refresh_delay_ui_states()
            elif source == "profile":
                self.update_profile_combobox() # Update if profile list changes (add/rename/delete)
                self.update_delete_button_state()
                self.update_rename_button_state()
            # Add other source checks if needed

    def show_status(self, message, color=None, duration=5000):
        """Displays a status message with a specified color and duration."""
        if color is None: color = self.style_manager.fg_color # Use StyleManager color
        self.status_label.setText(message); self.status_label.setStyleSheet(f"color: {color}; background-color: transparent;") # Ensure transparent bg
        # Stop existing timer if any
        if hasattr(self, '_status_timer') and self._status_timer is not None:
            self._status_timer.stop()
            self._status_timer.deleteLater() # Clean up old timer

        # Start new timer
        self._status_timer = QTimer(self); self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self.clear_status); self._status_timer.start(duration)

    def clear_status(self): self.status_label.setText("")

    def save_config(self, show_confirmation=False):
        """Saves the current state of the UI to the current ProfileConfig object and then saves all profiles."""
        current_profile_obj = self.profiles.get(self.current_profile)
        if not isinstance(current_profile_obj, ProfileConfig):
             print(f"Error: Cannot save, current profile '{self.current_profile}' is invalid.")
             self.event_bus.publish(STATUS_UPDATE, {"message": "Error: Cannot save invalid profile.", "color": self.style_manager.error_color})
             return

        # Update the current ProfileConfig object from the UI widgets
        current_profile_obj.launch_delay = self.profile_delay_spinbox.value()
        current_profile_obj.programs = [] # Clear existing programs in the object
        for program_dict in self.programs: # Iterate through the UI widget list
            widget = program_dict["widget"]
            program_config = ProgramConfig(
                name=widget.get_name(),
                path=widget.get_path(),
                use_custom_delay=widget.use_custom_delay,
                custom_delay_value=widget.custom_delay_value
            )
            current_profile_obj.programs.append(program_config)

        # Ensure minimum program slots
        while len(current_profile_obj.programs) < 2:
            current_profile_obj.programs.append(ProgramConfig())

        # Prepare the data structure for ConfigManager.save_config
        config_to_save = {
            "profiles": self.profiles, # Pass the dictionary of ProfileConfig objects
            "current_profile": self.current_profile,
            "default_profile_display_name": self.default_profile_display_name,
            "show_low_delay_warning": self.show_low_delay_warning
        }

        try:
            success = self.config_manager.save_config(config_to_save) # Pass the whole structure
            self.changes_made = False # Reset flag after attempting save
            self.save_btn.setEnabled(False) # Disable save button after saving

            if success and show_confirmation:
                profile_name = self.default_profile_display_name if self.current_profile == "Default" else self.current_profile
                self.event_bus.publish(STATUS_UPDATE, {"message": f"Profile '{profile_name}' saved successfully.", "color": self.style_manager.launched_color})
            # elif not success: # ConfigError is raised on failure now
            #     self.event_bus.publish(STATUS_UPDATE, {"message": "Failed to save profile.", "color": self.style_manager.error_color})
        except ConfigError as e:
             print(f"Configuration save error: {e}")
             self.event_bus.publish(STATUS_UPDATE, {"message": f"Error saving profile: {e}", "color": self.style_manager.error_color})


    def load_config(self):
        """Loads the configuration using ConfigManager and populates the UI."""
        try:
            config = self.config_manager.load_config() # load_config now returns ProfileConfig objects or raises ConfigError

            if config and isinstance(config.get("profiles"), dict):
                self.profiles = config["profiles"] # Assign the dict of ProfileConfig objects
                self.current_profile = config.get("current_profile", "Default")
                self.default_profile_display_name = config.get("default_profile_display_name", "Default")
                self.show_low_delay_warning = config.get("show_low_delay_warning", True)

                # Ensure current_profile exists, default to "Default" if not
                if self.current_profile not in self.profiles:
                    print(f"Warning: Loaded current_profile '{self.current_profile}' not found. Defaulting.")
                    self.current_profile = "Default"
            else:
                 # If load failed or profiles invalid, ensure a default exists
                 print("Load config failed or profiles invalid. Ensuring default profile.")
                 self.profiles = {} # Reset profiles
                 self.current_profile = "Default"
                 self.default_profile_display_name = "Default"
                 self.show_low_delay_warning = True


            # Ensure Default profile exists *after* loading
            if "Default" not in self.profiles or not isinstance(self.profiles["Default"], ProfileConfig):
                 print("Ensuring Default profile exists.")
                 self.profiles["Default"] = ProfileConfig(name="Default")
                 # Ensure minimum program slots
                 while len(self.profiles["Default"].programs) < 2:
                     self.profiles["Default"].programs.append(ProgramConfig())


            self.is_initial_loading = True
            self.update_profile_combobox()
            self.load_profile(self.current_profile) # Load the initially selected profile
            self.changes_made = False
            self.save_btn.setEnabled(False) # Disable save button initially
            self.update_delete_button_state(); self.update_rename_button_state()
            self.is_initial_loading = False # Set to false after initial load
        except ConfigError as e:
             print(f"Configuration load error: {e}")
             # Show error message to user (ConfigManager already shows one)
             # Use default settings as a fallback
             self.profiles = {}
             self.profiles["Default"] = ProfileConfig(name="Default")
             while len(self.profiles["Default"].programs) < 2:
                 self.profiles["Default"].programs.append(ProgramConfig())
             self.current_profile = "Default"
             self.default_profile_display_name = "Default"
             self.show_low_delay_warning = True
             # Still need to update UI even with defaults
             self.is_initial_loading = True
             self.update_profile_combobox()
             self.load_profile(self.current_profile)
             self.changes_made = False
             self.save_btn.setEnabled(False) # Disable save button initially
             self.update_delete_button_state(); self.update_rename_button_state()
             self.is_initial_loading = False
