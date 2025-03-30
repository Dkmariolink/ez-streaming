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
Simple Event Bus for UI Updates in EZ Streaming
"""

# --- Event Constants ---
STATUS_UPDATE = "status_update" # data = {"message": str, "color": str|None, "duration": int}
PROCESS_LIST_CHANGED = "process_list_changed" # data = None (or potentially list of running pids/paths)
LAUNCH_SEQUENCE_STATE_CHANGED = "launch_sequence_state_changed" # data = {"state": str, "launched_count": int, "total_count": int} # state = 'started'|'finished'

class UIEventBus:
    """A simple publish-subscribe event bus for decoupling UI updates."""

    def __init__(self):
        """Initializes the event bus."""
        self._listeners = {}
        print("[UIEventBus] Initialized.")

    def subscribe(self, event_type: str, callback):
        """
        Subscribe a callback function to an event type.

        Args:
            event_type (str): The name of the event to subscribe to.
            callback (callable): The function to call when the event is published.
                                 It should accept a single argument (the event data).
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        if callback not in self._listeners[event_type]:
            self._listeners[event_type].append(callback)
            # print(f"[UIEventBus] '{callback.__name__}' subscribed to '{event_type}'.") # Optional debug log

    def unsubscribe(self, event_type: str, callback):
        """
        Unsubscribe a callback function from an event type.

        Args:
            event_type (str): The name of the event to unsubscribe from.
            callback (callable): The callback function to remove.
        """
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            # print(f"[UIEventBus] '{callback.__name__}' unsubscribed from '{event_type}'.") # Optional debug log
            if not self._listeners[event_type]: # Remove event type if no listeners left
                del self._listeners[event_type]

    def publish(self, event_type: str, data=None):
        """
        Publish an event to all subscribed listeners.

        Args:
            event_type (str): The name of the event to publish.
            data (any, optional): Data to pass to the callback functions. Defaults to None.
        """
        # print(f"[UIEventBus] Publishing '{event_type}' with data: {data}") # Optional debug log
        if event_type in self._listeners:
            # Iterate over a copy in case a callback unsubscribes during iteration
            for callback in self._listeners[event_type][:]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"[UIEventBus] Error in callback for event '{event_type}': {e}")
                    # Decide how to handle callback errors (e.g., log, remove listener?)
