# Progress: EZ Streaming

## What Works (Current State)
As of the latest handover and initial memory bank setup:

*   **Core Application Launching:** Successfully launches multiple applications as defined in user profiles.
*   **Modern User Interface (PySide6):**
    *   Dark theme with purple accents, inspired by Twitch.
    *   Animated title.
    *   Consistent styling across UI elements (buttons, inputs, labels, tooltips).
    *   Improved column header alignment in the program list, including a dedicated "Status" header.
    *   Fixed styling issues (e.g., unwanted background on launch button container).
    *   DPI awareness for proper scaling.
*   **Profile Management:**
    *   Create, rename (non-default), duplicate, and delete profiles.
    *   Clear indication and protection of the "Default" profile.
    *   Profiles correctly persist their associated programs and settings.
    *   New/empty profiles consistently start with two empty program rows.
*   **Program Management (within Profiles):**
    *   Add and remove programs.
    *   Specify program name and executable path.
    *   Drag-and-drop reordering of programs.
    *   Individual program launch and close buttons, with the launch button correctly disabling and updating text when an app is running.
    *   Auto-population of app name when browsing for an executable.
    *   "Browse" button logically placed before the "Path" input field.
    *   **"Locate App by Name" button** (COMPLETED):
        *   Searches for both predefined streaming apps and any .exe file
        *   Smart matching with case-insensitive and partial name support
        *   Registry search for accurate paths (Windows)
        *   General executable search in common directories
        *   **Steam app search** - finds apps in steamapps/common folders
        *   **D: drive support** - added D: drive paths for Epic Games and other apps
        *   Comprehensive feedback with message boxes for not-found apps
        *   Shows "Similar apps" based on search (not all 24 available apps)
        *   **24 streaming apps supported** including OBS, Discord, Spotify, Mix It Up, StreamElements, Twitch Studio, XSplit, NVIDIA ShadowPlay, VTube Studio, and more
        *   Asynchronous search keeps UI responsive
        *   Helpful tips asking if app is installed, suggesting manual browse
*   **Launch Delay Functionality:**
    *   Profile-level default launch delay.
    *   Per-application custom launch delay override with checkbox and spinbox.
    *   Visual warning for low delay values (configurable to not show again).
    *   Delay controls are correctly disabled for the first application in a list or if the application's path (or the first app's path) is invalid.
    *   Uses non-blocking `QTimer` for delays, keeping the UI responsive during "Launch All".
    *   Visual styling improvements (rounded arrows, consistent spacing).
*   **Process Monitoring & Management:**
    *   Improved tracking of launched application statuses (via `ProcessManager`), including better detection of externally launched applications (using `os.path.normcase` for path matching). UI correctly reflects status for these.
    *   "Close All" functionality for programs within a profile or all tracked programs.
    *   Status updates communicated via `UIEventBus` (e.g., for "Launching X...").
    *   (Note: UI for real-time CPU/GPU/Memory metrics was removed due to performance impact; backend `ResourceMonitor` class is retained for process detection.)
*   **Configuration Persistence:**
    *   Profiles, programs, and settings are saved to `ez_streaming_config.json` in the user's application data directory.
    *   Configuration is reliably loaded on startup.
    *   Handles missing or basic invalid configuration files by creating a default setup.
*   **User Experience (UX) Enhancements:**
    *   Warning dialog on window close if the current profile has unsaved changes.
    *   Consistent row selection behavior when clicking within input fields.
    *   Transparent status background for program rows.
*   **Robustness & Stability:**
    *   Addressed several critical bugs (profile duplication, default profile data corruption, UI inconsistencies on load).
    *   Custom exceptions for more structured error handling.
    *   Modular architecture (managers for config, style, process; event bus).

## What's Left to Build (Immediate & Short-Term from Roadmap Phase 2)
1.  **Profile Import/Export (Next Immediate Task):**
    *   Export profiles to JSON files.
    *   Import profiles from JSON files.
    *   "Copy App from Another Profile" feature.
2.  **Auto-Save Functionality:**
    *   Periodically save changes or save on significant actions to prevent data loss.
3.  **Startup with Windows Option:**
    *   Add a setting to allow EZ Streaming to launch automatically when Windows starts.
4.  **Advanced Profile Features (Longer Short-Term):**
    *   Profile descriptions.
    *   Profile categories or tags.
    *   Profile activation scheduling.
5.  **Enhanced Program Control (Longer Short-Term):**
    *   Support for command-line arguments for launched applications.
6.  **UI/UX Enhancements (Longer Short-Term):**
    *   Integrated non-popup settings panel (theme, accessibility).
    *   Onboarding/Tutorial system.
    *   "New Streamer Starting Guide."

## Current Status
*   **Phase 1 (Immediate Fixes):** Completed. The application has a stable core, a polished UI, and key bug fixes have been implemented.
*   **Phase 2 (User Experience Enhancement):** In Progress. The "Locate App by Name" feature has been completed as the first item from this phase.
*   **Overall:** The application is functional, reliable for its current feature set, and has a solid foundation for future development.

## Known Issues (as of Memory Bank Initialization)
*   No critical known issues are pending from the recent bug-fixing phase detailed in the handover document.
*   This section will be updated if new issues are discovered during development or testing of new features.

## Evolution of Project Decisions (Summary)
*   **Initial Concept:** A simple utility to solve a personal pain point (manual app launching).
*   **Early Versions:** Started with batch scripts, then evolved to a basic Tkinter GUI.
*   **Modernization:** Migrated to PySide6 (Qt) for a more professional look, better features, and improved maintainability. This was a significant technical decision.
*   **Iterative Refinement:** Continuous improvements to UI/UX based on usability testing and developer insights (e.g., launch delay feature, styling consistency, bug fixes related to profile management).
*   **Architectural Maturity:** Introduction of managers (config, style, process), data models (`config_models`), an event bus, and custom exceptions to create a more robust and modular codebase.
*   **User-Centric Roadmap:** Future development is guided by a phased roadmap focusing on enhancing user experience, adding automation, and integrating more deeply with the streaming ecosystem.
*   **UI & Process Handling (May 2025):** Addressed UI alignment issues (headers) and refined process detection logic (e.g. `os.path.normcase`, `check_if_already_running`) for better accuracy and user experience.
*   **Performance Prioritization (May 2025):** Temporarily removed the UI for real-time performance monitoring due to its impact on application responsiveness, prioritizing stability and core functionality. Backend monitoring capabilities in `ResourceMonitor` are retained for process detection.
