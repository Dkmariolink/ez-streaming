# System Patterns: EZ Streaming

## System Architecture
EZ Streaming employs a modular architecture, primarily built around Python and the PySide6 (Qt) framework. Key components include:

*   **`main.py`**:
    *   The application entry point.
    *   Handles initial setup, including DPI configuration for Qt to ensure proper scaling on high-resolution displays.
    *   Instantiates and shows the main application window (`StreamerApp`).

*   **`app_qt.py`**:
    *   Contains the main application window class (`StreamerApp`), which inherits from `QMainWindow`. This class is responsible for the overall UI structure, layout, and high-level application logic.
    *   Defines the `ProgramWidget` class, representing a single row in the application list (for one program). This widget encapsulates controls like name input, path input, browse button, delay settings, and launch/close buttons for an individual program.
    *   Manages UI setup (creating widgets, layouts, menus, status bar).
    *   Connects UI signals (button clicks, input changes) to appropriate slots (handler methods).
    *   Orchestrates interactions between different managers (ConfigManager, ProcessManager, StyleManager, LaunchSequence).
    *   Handles profile management UI (dropdown, add/rename/duplicate/delete profile actions).
    *   Manages the list of `ProgramWidget` instances.

*   **`config_manager.py`**:
    *   Houses the `ConfigManager` class.
    *   Responsible for all aspects of configuration persistence:
        *   Saving the current application state (profiles, programs, settings) to a JSON file (`ez_streaming_config.json`).
        *   Loading the configuration from the JSON file on application startup.
        *   Determining the appropriate platform-specific directory for storing the configuration file (e.g., AppData on Windows, Application Support on macOS, .config on Linux).
    *   Uses `config_models.py` (`ProfileConfig`, `ProgramConfig`) for structured data representation, serialization, and deserialization.
    *   Handles basic validation and ensures a default profile exists if the config is missing or invalid.

*   **`config_models.py`**:
    *   Defines `dataclass`es:
        *   `ProgramConfig`: Represents a single application entry (name, path, custom delay settings).
        *   `ProfileConfig`: Represents a user profile (name, list of `ProgramConfig` objects, default launch delay).
        *   `GlobalSettings` (implicitly, part of the overall config structure): Stores application-wide settings like `show_low_delay_warning`.
    *   These models provide type safety and replace direct dictionary manipulation for configuration data.
    *   Include `from_dict` and `to_dict` class methods for easy serialization to and from dictionary structures, facilitating JSON conversion.
    *   `ProfileConfig.from_dict` ensures new/empty profiles always have at least two empty `ProgramConfig` slots for a consistent UI.

*   **`style_manager.py`**:
    *   Contains the `StyleManager` class.
    *   Centralizes all application styling (QSS - Qt Style Sheets).
    *   Defines color palettes (dark theme, purple accents).
    *   Provides methods to generate and retrieve consistent QSS for different UI elements (buttons, input fields, labels, tooltips, etc.), ensuring a uniform look and feel.
    *   Applies global application stylesheet.

*   **`process_manager.py`**:
    *   Features the `ProcessManager` class.
    *   Manages and tracks running external application processes launched by EZ Streaming.
    *   `track(pid, program_name, profile_name)`: Adds a process to the tracking list.
    *   `untrack(pid)`: Removes a process from tracking.
    *   `close_all(profile_name=None)`: Attempts to close all tracked processes, or all processes for a specific profile.
    *   Communicates UI updates (e.g., process status changes) via the `UIEventBus`.

*   **`launch_sequence.py`**:
    *   Implements the "Launch All" functionality using a state machine pattern within the `LaunchSequence` class.
    *   Manages the sequential launching of applications within a profile.
    *   Handles the configured delays between application launches using non-blocking `QTimer` objects to keep the UI responsive.
    *   Communicates progress, status updates (e.g., "Launching X...", "Waiting Y seconds..."), and completion/error events via the `UIEventBus`.

*   **`event_bus.py`**:
    *   Provides a simple publish-subscribe event bus implementation (`UIEventBus`).
    *   Used to decouple UI updates from the components that trigger them (e.g., `ProcessManager` and `LaunchSequence` publish events, `StreamerApp` subscribes to update the UI).
    *   Defines event type constants (e.g., `STATUS_UPDATE`, `PROCESS_LIST_CHANGED`, `LAUNCH_SEQUENCE_UPDATE`).

*   **`exceptions.py`**:
    *   Defines custom application-specific exception classes (`AppError`, `ConfigError`, `ProcessError`).
    *   Allows for more structured and specific error handling throughout the application.

*   **`app_locator.py`**:
    *   Contains the `AppLocator` class for finding application executables on the system.
    *   Supports 24 predefined streaming apps including:
        *   Streaming software: OBS, Streamlabs, StreamElements OBS.Live, Twitch Studio, XSplit
        *   Communication: Discord, Twitch Studio
        *   Music: Spotify  
        *   Stream control: Mix It Up, Touch Portal, Streamlabs Chatbot, Loupedeck
        *   Virtual cameras: Snap Camera, VTube Studio
        *   Recording: NVIDIA ShadowPlay, NVIDIA Broadcast
        *   Interactive: Crowd Control, Dixper
        *   Multi-streaming: Restream
        *   And more...
    *   Features:
        *   Smart matching: case-insensitive, partial name matching, aliases
        *   Windows Registry search (read-only) for accurate installation paths
        *   Common directory scanning (Program Files, AppData, D: drive, etc.)
        *   Steam app search in steamapps/common directories
        *   General executable search fallback for any .exe file
        *   Returns similar apps based on search query
    *   Used by `ProgramWidget` to implement the "Locate App by Name" feature.

*   **`resource_monitor.py`**:
    *   Contains the `ResourceMonitor` class for monitoring CPU, GPU, and Memory usage of running processes.
    *   Features:
        *   Process detection by executable path
        *   CPU usage monitoring (normalized across cores)
        *   Memory usage monitoring (percentage of total RAM)
        *   GPU usage monitoring with multiple backends:
            *   NVIDIA GPU support via pynvml
            *   General GPU support via GPUtil
            *   Windows Performance Counter fallback
        *   Color-coding system for resource usage levels
        *   Integrates with psutil for cross-platform process monitoring
    *   Its `get_process_by_path` method is utilized by `ProgramWidget` (via a shared instance in `StreamerApp`) for detecting if a configured application is already running. Other resource monitoring capabilities (CPU, GPU, Memory) exist but are not currently displayed in the UI.

## Key Technical Decisions
*   **Migration from Tkinter to PySide6 (Qt):** Chosen for a more modern UI, richer widget set, better styling capabilities (QSS), and overall more professional feel.
*   **Dataclasses for Configuration (`config_models.py`):** Adopted for type safety, improved readability, and easier maintenance of configuration data structures compared to raw dictionaries.
*   **Centralized Styling (`style_manager.py`):** Ensures a consistent look and feel across the application and simplifies theme management.
*   **Event Bus (`event_bus.py`):** Implemented to decouple background operations (like process management and launch sequences) from direct UI manipulation, improving modularity and testability.
*   **State Machine for Launch Sequence (`launch_sequence.py`):** Provides a robust way to manage the complex logic of sequential launching with delays and status updates.
*   **Non-Blocking Timers (`QTimer`):** Used for launch delays to ensure the UI remains responsive and doesn't freeze during the launch process.
*   **JSON for Configuration:** A human-readable and widely supported format for storing application settings.
*   **Platform-Specific Configuration Directory:** Ensures configuration files are stored in standard user locations.
*   **Custom Exceptions:** For clearer error identification and handling.

## Design Patterns
*   **Model-View-Controller (MVC) / Model-View-Presenter (MVP) (loosely):**
    *   **Model:** `config_models.py` (data structures), `ConfigManager` (data persistence), `ProcessManager` (state of running processes).
    *   **View:** `app_qt.py` (UI elements and layout defined in `StreamerApp` and `ProgramWidget`).
    *   **Controller/Presenter:** Logic within `StreamerApp` methods that respond to UI events and interact with models. `LaunchSequence` also acts as a controller for the launch process.
*   **Observer Pattern (Publish-Subscribe):** Implemented via `UIEventBus`. Components like `ProcessManager` and `LaunchSequence` publish events, and `StreamerApp` (or other UI components) subscribe to these events to update themselves.
*   **State Machine Pattern:** Used in `LaunchSequence` to manage the different stages of launching multiple applications (e.g., idle, launching app, waiting for delay, finished, error).
*   **Singleton (Conceptual for Managers):** While not strictly enforced as singletons in Python, classes like `ConfigManager`, `StyleManager`, `ProcessManager`, and `UIEventBus` are typically instantiated once and used throughout the application lifecycle.
*   **Factory Method (implied in `config_models`):** The `from_dict` class methods in `ProfileConfig` and `ProgramConfig` act like factory methods, creating instances from dictionary representations.

## Component Relationships
*   `main.py` initializes and runs `StreamerApp` (from `app_qt.py`).
*   `StreamerApp` uses:
    *   `ConfigManager` to load/save profiles and settings.
    *   `StyleManager` to apply QSS styles.
    *   `ProcessManager` to track and close launched applications.
    *   `LaunchSequence` to execute the "Launch All" functionality.
    *   `UIEventBus` to subscribe to events from `ProcessManager` and `LaunchSequence` for UI updates.
    *   `ProgramWidget` instances to display and manage individual program rows.
    *   `AppLocator` (via `AppLocatorWorker` thread) for the "Locate App by Name" functionality.
*   `ConfigManager` uses `ProfileConfig` and `ProgramConfig` (from `config_models.py`) to structure and (de)serialize data.
*   `LaunchSequence` and `ProcessManager` publish events to the `UIEventBus`.
*   Many components may raise or handle exceptions defined in `exceptions.py`.

## Critical Implementation Paths
*   **Profile Management:** Creating, loading, saving, duplicating, renaming, and deleting profiles. Ensuring data integrity, especially for the default profile and during save/load operations.
*   **Program Management:** Adding, removing, and reordering programs within a profile, including their paths and delay settings.
*   **Launch Delay Logic:** Correctly implementing profile-default and per-app custom delays, handling UI state for delay controls (disabled for first app/invalid paths), and managing non-blocking timers.
*   **Configuration Persistence:** Robustly saving all relevant data to JSON and reliably loading it back, handling potential errors or missing files.
*   **UI Styling and Consistency:** Applying styles correctly to all elements, including dynamically created `ProgramWidget` instances, and ensuring consistency across interactions (e.g., row selection).
*   **"Launch All" Sequence:** The state machine logic in `LaunchSequence`, including accurate timing, status updates via the event bus, and error handling.
*   **Process Tracking and Closing:** Reliably tracking launched processes and providing functionality to close them individually or en masse.
*   **Event Handling for UI Updates:** Ensuring that events from background tasks correctly trigger UI refreshes without direct coupling.
