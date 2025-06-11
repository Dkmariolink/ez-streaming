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
Process Manager for EZ Streaming - Handles tracking and closing of launched application processes.
"""
import sys
import subprocess
import time
import os # Added for basename
import psutil  # Add psutil for process monitoring
from PySide6.QtWidgets import QApplication, QMessageBox
from event_bus import UIEventBus, PROCESS_LIST_CHANGED, STATUS_UPDATE # Import event bus and constants

class ProcessManager:
    """Manages running processes launched by the application."""

    def __init__(self, parent_app, event_bus: UIEventBus):
        """
        Initializes the ProcessManager.

        Args:
            parent_app: The main StreamerApp instance.
            event_bus (UIEventBus): The application's event bus.
        """
        self.parent_app = parent_app # Reference to the main StreamerApp (still needed for widgets)
        self.event_bus = event_bus
        self.running_processes = {} # Dictionary to store {path: process_object}

    def track(self, path, process):
        """
        Starts tracking a launched process.

        Args:
            path (str): The executable path of the process.
            process: The subprocess object or psutil.Process object.
        """
        if path and process:
            # Handle both subprocess.Popen and psutil.Process objects
            if hasattr(process, 'pid'):
                pid = process.pid
            else:
                pid = "Unknown"
            
            print(f"[ProcessManager] Tracking: {path} (PID: {pid})")
            self.running_processes[path] = process
            self.event_bus.publish(PROCESS_LIST_CHANGED) # Publish event instead of direct UI call

    def untrack(self, path):
        """
        Stops tracking a process (usually when it terminates or is closed).

        Args:
            path (str): The executable path of the process.
        """
        if path in self.running_processes:
            print(f"[ProcessManager] Untracking: {path}")
            del self.running_processes[path]
            self.event_bus.publish(PROCESS_LIST_CHANGED) # Publish event instead of direct UI call

    def get_running_processes(self):
        """Returns the dictionary of currently tracked running processes."""
        return self.running_processes

    def is_running(self, path):
        """Checks if a process with the given path is currently tracked and running."""
        process = self.running_processes.get(path)
        if process is None:
            return False
            
        # Handle both subprocess.Popen and psutil.Process objects
        if hasattr(process, 'poll'):
            # subprocess.Popen object
            return process.poll() is None
        elif hasattr(process, 'is_running'):
            # psutil.Process object
            try:
                return process.is_running()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return False
        else:
            return False
    
    def find_running_process(self, exe_path):
        """
        Find if a process is running on the system by its executable path.
        Returns the process object if found, None otherwise.
        """
        if not exe_path or not os.path.exists(exe_path):
            return None
            
        exe_name = os.path.basename(exe_path).lower()
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Check by exact exe path first
                    if proc.info['exe'] and os.path.normpath(proc.info['exe'].lower()) == os.path.normpath(exe_path.lower()):
                        return proc
                    # Also check by name for processes that might have been moved
                    elif proc.info['name'] and proc.info['name'].lower() == exe_name:
                        # Verify it's likely the same program
                        return proc
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"[ProcessManager] Error finding process: {e}")
        
        return None
    
    def get_process_stats(self, exe_path):
        """
        Get CPU, memory, and GPU usage for a process.
        Returns dict with 'cpu', 'memory', and 'gpu' percentages, or None if not found.
        """
        proc = self.find_running_process(exe_path)
        if not proc:
            return None
            
        try:
            # Get CPU and memory usage
            cpu_percent = proc.cpu_percent(interval=0.1)  # Short interval for responsiveness
            memory_info = proc.memory_info()
            memory_percent = proc.memory_percent()
            
            # GPU usage would require additional libraries like GPUtil or pynvml
            # For now, we'll set it to 0 or estimate based on process type
            gpu_percent = 0  # Placeholder
            
            return {
                'cpu': round(cpu_percent, 1),
                'memory': round(memory_percent, 1),
                'gpu': round(gpu_percent, 1),
                'pid': proc.pid
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def close_all(self):
        """Attempts to close all tracked running processes."""
        if not self.running_processes:
            self.event_bus.publish(STATUS_UPDATE, {
                "message": "No running programs to close",
                "color": self.parent_app.style_manager.warning_color, # Still need style manager ref via parent
                "duration": 5000
            })
            return

        result = QMessageBox.question(self.parent_app, "Close All Programs",
            f"Are you sure you want to close all {len(self.running_processes)} running programs?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if result != QMessageBox.StandardButton.Yes:
            return

        paths_to_close = list(self.running_processes.keys()) # Copy keys as dict changes during iteration
        closed_count = 0
        failed_to_close = []

        print(f"[ProcessManager] Attempting to close {len(paths_to_close)} processes.")

        for path in paths_to_close:
            process = self.running_processes.get(path)
            if process and process.poll() is None:
                app_name = path # Fallback name
                # Find the corresponding widget to get a better name and reset its UI
                widget_found = False
                for program_data in self.parent_app.programs: # Need parent ref to access UI widgets
                    widget = program_data["widget"]
                    if widget.get_path() == path:
                        app_name = widget.get_name() or os.path.basename(path)
                        print(f"[ProcessManager] Closing '{app_name}' (PID: {process.pid})...")
                        try:
                            print(f"  Terminating PID {process.pid}...")
                            process.terminate()
                            try:
                                process.wait(timeout=0.5)
                            except subprocess.TimeoutExpired:
                                print(f"  Process {process.pid} did not terminate gracefully, killing.")
                                if sys.platform == "win32":
                                    try: subprocess.run(['taskkill', '/F', '/PID', str(process.pid)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                                    except Exception: process.kill()
                                else: process.kill()

                            if process.poll() is not None:
                                closed_count += 1
                                self.untrack(path) # Untrack publishes PROCESS_LIST_CHANGED
                                widget.reset_status() # Update widget UI directly
                                widget.close_btn.setVisible(False)
                            else:
                                print(f"  Warning: Process {process.pid} still running after termination attempts.")
                                failed_to_close.append(app_name)

                        except Exception as e:
                            print(f"  Error terminating process {process.pid}: {e}")
                            failed_to_close.append(app_name)
                            # Attempt to untrack even on error
                            self.untrack(path)
                            widget.reset_status()
                            widget.close_btn.setVisible(False)


                        widget_found = True
                        break # Found the widget for this path

                if not widget_found:
                    # If widget not found, try basic termination
                    print(f"[ProcessManager] Closing '{app_name}' (PID: {process.pid}) directly (no widget found)...")
                    try:
                        process.terminate()
                        process.wait(timeout=0.1)
                    except Exception:
                        process.kill()
                    finally:
                        if process.poll() is not None:
                            closed_count += 1
                            self.untrack(path) # Untrack publishes PROCESS_LIST_CHANGED
                        else:
                            failed_to_close.append(app_name)


                QApplication.processEvents() # Allow UI updates between closures

        # Publish final status update
        status_data = {"duration": 5000}
        if failed_to_close:
             status_data["message"] = f"Closed {closed_count} programs. Failed to close: {', '.join(failed_to_close)}"
             status_data["color"] = self.parent_app.style_manager.warning_color
        else:
             status_data["message"] = f"Closed {closed_count} programs successfully."
             status_data["color"] = self.parent_app.style_manager.launched_color
        self.event_bus.publish(STATUS_UPDATE, status_data)

        # Final PROCESS_LIST_CHANGED event is published by the last untrack call(s)
        # self._update_ui() # No longer needed

    # Removed _update_ui as it's replaced by event publishing
