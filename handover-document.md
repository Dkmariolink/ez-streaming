# EZ Streaming: Comprehensive Handover Document

## Project Overview
EZ Streaming is a streamlined utility for content creators that allows launching multiple streaming applications with a single click. Built with Python and PySide6 (Qt), the application features a modern dark interface with purple accents inspired by Twitch's color scheme.

## Current Status
The application has successfully been migrated from the original Tkinter implementation to a modern Qt interface using PySide6. The core functionality is working properly with a number of UI and UX improvements:

- Modern dark theme with animated title
- Profile management (create, rename, duplicate, delete)
- Program management (add, remove, launch, close)
- Drag and drop reordering of applications
- Process monitoring with status tracking
- Multi-profile support with proper persistence
- Application closing functionality (both individual and "Close All")
- Row selection consistency when clicking within input fields
- Consistent tooltip styling across all controls
- Warning dialog on close if profile has unsaved changes
- **Launch Delay:** Configurable delay between launching apps (profile default and per-app override via checkbox/spinbox). Includes low-delay warning and disables delay controls for the first app, if the first app's path is invalid, or if the current row's path is invalid. Uses non-blocking `QTimer` for delays during "Launch All".
- **UI/QoL (March 2025):** Rounded delay arrows, consistent arrow spacing/styling, transparent status background, auto-name population on browse, Browse button moved before Path input.

## Technical Implementation

### Architecture
- **main.py**: Entry point with DPI configuration for Qt.
- **app_qt.py**: Main application window (`StreamerApp`) and individual program row widget (`ProgramWidget`). Handles UI setup, signal connections, and high-level application flow.
- **config_manager.py**: Handles saving and loading the configuration file (`ez_streaming_config.json`) in the appropriate user directory. Uses `config_models` for data structure.
- **config_models.py**: Defines `dataclass`es (`ProfileConfig`, `ProgramConfig`) for structured representation of configuration data, replacing direct dictionary manipulation. Includes `from_dict` and `to_dict` methods for serialization.
- **style_manager.py**: Centralizes application styling (colors, QSS generation) via the `StyleManager` class. Provides methods to get consistent stylesheets for different UI elements.
- **process_manager.py**: Manages tracking of running external application processes via the `ProcessManager` class. Handles adding (`track`), removing (`untrack`), and closing (`close_all`) tracked processes. Communicates UI updates via the event bus.
- **launch_sequence.py**: Implements the "Launch All" logic as a state machine (`LaunchSequence` class). Manages delays between launches and communicates progress/status via the event bus.
- **event_bus.py**: A simple publish-subscribe event bus (`UIEventBus`) used to decouple UI updates from the components that trigger them (e.g., `ProcessManager`, `LaunchSequence`). Defines event constants like `STATUS_UPDATE`, `PROCESS_LIST_CHANGED`.
- **exceptions.py**: Defines custom application-specific exceptions (`AppError`, `ConfigError`, `ProcessError`) for more structured error handling.

### Configuration
- Uses JSON format stored in user's AppData/Application Support/.config directory (platform-dependent).
- Managed by `ConfigManager`, which serializes/deserializes data using `ProfileConfig` and `ProgramConfig` models.
- Tracks profiles (name, launch_delay, list of programs), individual programs (name, path, use_custom_delay, custom_delay_value), the current profile name, and global settings (`show_low_delay_warning`).
- `ProfileConfig.from_dict` ensures new profiles always have at least 2 empty `ProgramConfig` slots.
- `ConfigManager.load_config` handles basic validation and ensures a default profile exists if the config is missing or invalid.

### Current Issues & Solutions

#### Resolved Issues:
1. **Profile duplication bug**: Fixed inconsistent behavior when creating or renaming profiles
2. **Row consistency**: Ensured all profiles have exactly 2 rows when empty
3. **UI styling consistency**: Addressed styling issues with consistent item formatting, including fixing first-row widget styling inconsistencies on initial load (buttons, inputs, labels) via explicit style application.
4. **Process tracking**: Implemented robust process monitoring across profile changes.
5. **Profile indicators**: Added "(default)" tag to clearly identify the default profile (Note: Renaming is disabled, but tag removal was reverted based on user preference/testing).
6. **Default Profile Data Corruption**: Fixed bug where deleting a profile could corrupt the default profile's data due to incorrect save order. Ensured default profile loads before saving after deletion.
7. **Row Selection Consistency**: Implemented event filter to ensure clicking within input fields correctly selects and highlights the corresponding row.
8. **Tooltip Styling**: Applied consistent tooltip styling globally via application stylesheet.
9. **Unsaved Changes Warning**: Added a confirmation dialog on window close if the current profile has unsaved changes.

#### Pending Changes:
*(No immediate pending changes related to recent fixes)*

## Testing & Deployment

### Testing Procedure
1. Test all profile operations:
   - Creating new profiles
   - Duplicating profiles
   - Renaming profiles (regular profiles only)
   - Deleting profiles (non-default only)
   - Switching between profiles

2. Test program operations:
   - Adding programs
   - Removing programs
   - Launching programs
   - Closing programs
   - Reordering programs via drag and drop
   - Setting profile default delay
   - Enabling/disabling and setting custom per-app delays
   - Verifying delay controls are disabled for the first app
   - Verifying low-delay warning appears correctly (and can be disabled)

3. Test persistence:
   - Verify configuration saves correctly (including delay settings)
   - Verify configuration loads correctly on restart
   - Test with various numbers of profiles and programs

### Deployment
1. Build with PyInstaller using the updated spec file
2. Ensure the following are included in the build:
   - Assets folder with icons
   - Font resources
   - All necessary Qt dependencies

## Next Steps

1. **Immediate Tasks**:
   - **Next Feature:** Implement "Locate App by Name" button below the "Browse" button (see Roadmap Phase 2).

2. **Short-term Enhancements**:
   - Add capability to import/export profiles
   - Implement auto-save functionality
   - Add startup option to launch with Windows

3. **Future Features**:
   - Scheduling capability
   - Stream integration
   - System tray functionality

## Resources
- Source code repository: [GitHub Repository]
- Documentation: [Project Wiki]
- Issue tracking: [GitHub Issues]

---

*This document was created to facilitate continued development of the EZ Streaming application.*
