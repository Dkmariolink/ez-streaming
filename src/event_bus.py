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
