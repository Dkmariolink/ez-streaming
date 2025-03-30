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
Launch Sequence State Machine for EZ Streaming
"""
import time
import os
from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtWidgets import QApplication # For processEvents
from event_bus import UIEventBus, STATUS_UPDATE, LAUNCH_SEQUENCE_STATE_CHANGED # Import event bus and constants

# Define states
STATE_IDLE = "idle"
STATE_DELAYING = "delaying"
STATE_LAUNCHING = "launching"
STATE_COMPLETE = "complete"
STATE_ERROR = "error" # Not currently used, but could be

class LaunchSequence(QObject):
    """Manages the state and execution of the program launch sequence."""

    # Signals can still be useful for direct Qt connections if needed,
    # but primary communication will be via event bus.
    # sequence_started = Signal()
    # sequence_step = Signal(str, int)
    # sequence_finished = Signal(int, int)
    # sequence_error = Signal(str)

    def __init__(self, app_ref, event_bus: UIEventBus):
        super().__init__()
        self.app = app_ref # Reference to the main StreamerApp instance (needed for profile/widget access)
        self.event_bus = event_bus
        self.queue = [] # List of ProgramWidget dictionaries {"widget":..., "item":...}
        self.current_index = 0
        self.state = STATE_IDLE
        self.delay_timer = QTimer(self)
        self.delay_timer.setSingleShot(True)
        self.delay_timer.timeout.connect(self._handle_delay_finished)
        self.countdown_timer = QTimer(self) # For status updates during delay
        self.countdown_timer.timeout.connect(self._update_countdown_status)
        self.countdown_end_time = 0

    def is_running(self):
        """Check if the sequence is currently active."""
        return self.state != STATE_IDLE and self.state != STATE_COMPLETE # and self.state != STATE_ERROR

    def start(self, program_widget_dicts):
        """Starts the launch sequence."""
        if self.is_running():
            print("Launch sequence already running.")
            return

        self.queue = [p for p in program_widget_dicts if p["widget"].get_path() and os.path.exists(p["widget"].get_path())]
        if not self.queue:
            self.event_bus.publish(STATUS_UPDATE, {
                "message": "No programs configured with valid paths to launch",
                "color": self.app.style_manager.warning_color,
                "duration": 5000
            })
            self.state = STATE_IDLE
            return

        print(f"[LaunchSequence] Starting sequence with {len(self.queue)} programs.")
        self.current_index = 0
        self.state = STATE_LAUNCHING # Initial state is to launch the first one
        self.event_bus.publish(LAUNCH_SEQUENCE_STATE_CHANGED, {"state": "started"})
        # self.app.launch_all_btn.setEnabled(False) # UI update handled by subscriber
        self._process_next()

    def _process_next(self):
        """Processes the next item in the launch queue."""
        if self.current_index >= len(self.queue):
            self._finish_sequence()
            return

        program_data = self.queue[self.current_index]
        widget = program_data["widget"]

        # Determine delay for the *next* launch (if applicable)
        # Delay is applied *before* launching the current app (except for the first)
        delay_ms = 0
        if self.current_index > 0:
            prev_widget_data = self.queue[self.current_index - 1] # Get previous widget for delay calc
            prev_widget = prev_widget_data["widget"]
            current_profile_obj = self.app.profiles.get(self.app.current_profile)
            profile_delay = current_profile_obj.launch_delay if current_profile_obj else 5
            effective_delay = prev_widget.custom_delay_value if prev_widget.use_custom_delay else profile_delay
            delay_ms = effective_delay * 1000

            # Check for low delay warning (using previous widget's delay setting)
            if 0 < effective_delay < 5 and self.app.show_low_delay_warning:
                # Let the main app handle showing the warning dialog if needed
                # This could also be an event, e.g., event_bus.publish("low_delay_warning_check")
                self.app.show_low_delay_warning_message()


        if delay_ms > 0:
            print(f"[LaunchSequence] Delaying {delay_ms}ms before launching '{widget.get_name()}'")
            self.state = STATE_DELAYING
            self.countdown_end_time = time.time() + (delay_ms / 1000.0)
            self.countdown_timer.start(100) # Update status approx 10 times/sec
            self._update_countdown_status() # Show initial time
            self.delay_timer.start(delay_ms) # Start the actual delay timer
        else:
            # No delay, launch immediately
            self._launch_current()

    def _handle_delay_finished(self):
        """Called when the QTimer for the delay finishes."""
        print("[LaunchSequence] Delay finished.")
        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
        self._launch_current()

    def _update_countdown_status(self):
        """Updates the status label during a delay via event bus."""
        remaining_time = self.countdown_end_time - time.time()
        if remaining_time > 0 and self.current_index < len(self.queue):
            next_app_name = self.queue[self.current_index]["widget"].get_name() or "next app"
            status_msg = f"Launching {next_app_name} in {int(remaining_time + 0.99)}s..."
            self.event_bus.publish(STATUS_UPDATE, {
                "message": status_msg,
                "color": self.app.style_manager.warning_color,
                "duration": 200 # Short duration for countdown updates
            })
        else:
            # Ensure timer stops if it fires slightly late
            if self.countdown_timer.isActive():
                self.countdown_timer.stop()

    def _launch_current(self):
        """Launches the program at the current index."""
        if self.current_index >= len(self.queue):
            self._finish_sequence() # Should not happen here, but safety check
            return

        program_data = self.queue[self.current_index]
        widget = program_data["widget"]
        app_name = widget.get_name() or "application"
        print(f"[LaunchSequence] Launching '{app_name}' (Index: {self.current_index})")
        self.state = STATE_LAUNCHING
        self.event_bus.publish(STATUS_UPDATE, {
            "message": f"Launching {app_name}...",
            "color": self.app.style_manager.launching_color,
            "duration": 3000 # Longer duration for launch message
        })
        QApplication.processEvents() # Update UI

        process = widget.launch_program() # This uses ProcessManager.track which publishes PROCESS_LIST_CHANGED

        # Move to the next item immediately after attempting launch
        self.current_index += 1
        # Schedule the next processing step very shortly after
        QTimer.singleShot(50, self._process_next) # 50ms delay before processing next

    def _finish_sequence(self):
        """Called when the launch sequence is complete."""
        print("[LaunchSequence] Sequence finished.")
        self.state = STATE_COMPLETE
        launched_count = len([p for p in self.queue if p["widget"].process and p["widget"].process.poll() is None])
        total_count = len(self.queue)

        status_data = {"duration": 5000}
        if launched_count > 0:
             final_msg = f"Successfully launched {launched_count}/{total_count} programs"
             color = self.app.style_manager.launched_color
             if launched_count < total_count:
                 final_msg += " (some may have failed)"
                 color = self.app.style_manager.warning_color
             status_data["message"] = final_msg
             status_data["color"] = color
        else:
             status_data["message"] = "No programs were launched (check paths/errors)"
             status_data["color"] = self.app.style_manager.warning_color

        self.event_bus.publish(STATUS_UPDATE, status_data)
        self.event_bus.publish(LAUNCH_SEQUENCE_STATE_CHANGED, {
            "state": "finished",
            "launched_count": launched_count,
            "total_count": total_count
        })

        # Reset internal state
        self.queue = []
        self.current_index = 0
        # self.app.launch_all_btn.setEnabled(True) # UI update handled by subscriber
        # self.sequence_finished.emit(launched_count, total_count) # Replaced by event bus
