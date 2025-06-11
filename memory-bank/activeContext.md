# Active Context: EZ Streaming

## Current Work Focus
*   **Recently Completed Tasks (May 30, 2025):**
    *   **UI Adjustments:**
        *   Corrected alignment of "Actions" and "Status" column headers in the program list.
        *   Removed unwanted background from the launch button container.
    *   **Performance Monitoring UI Removal:** The per-app CPU/GPU/Memory display UI (`ResourceWidget`) was removed due to significant application performance degradation. The backend `ResourceMonitor` class is retained for process detection.
    *   **Process Detection & UI Feedback:**
        *   Improved detection of already running applications (including those launched externally) using `os.path.normcase` for path comparisons in `ResourceMonitor`.
        *   Ensured the "Launch" button in `ProgramWidget` is disabled and its text changes to "Launched" when an application is running.
        *   Refined `ProgramWidget.check_if_already_running()` for better UI consistency.
*   **Next Primary Tasks (Phase 2 Short-term from Roadmap):**
    *   Profile Import/Export functionality.
    *   Auto-save functionality.
    *   Option to launch EZ Streaming with Windows startup.

## Recent Changes

*   **UI and Process Monitoring Refinements (May 30, 2025):**
    *   Adjusted column header alignment in `StreamerApp` (`_setup_list_header`) for "Path", "Actions", and added a "Status" header, using spacers and revised fixed widths for better visual correspondence with row content.
    *   Removed the dark background from the `action_container` in `ProgramWidget` by setting its stylesheet to transparent.
    *   Removed the `ResourceWidget` and associated UI elements for displaying real-time CPU/GPU/Memory from `ProgramWidget` and `StreamerApp` due to performance issues.
    *   Modified `ProgramWidget.set_running_state_ui` to correctly disable the Launch button and update its text when an application is running.
    *   Enhanced `ResourceMonitor.get_process_by_path` to use `os.path.normcase` for more reliable case-insensitive path matching.
    *   Updated `ProgramWidget.check_if_already_running` to better utilize `ResourceMonitor` (via a shared instance in `StreamerApp`) and `ProcessManager` for detecting externally launched applications and consistently updating the UI.
    *   Initial performance optimizations in `ResourceMonitor` (e.g., `cpu_percent(interval=None)`, removing direct `nvidia-smi` subprocess call from `get_process_resources`) were attempted before the UI removal decision.

*   **Previous - Enhanced "Locate App by Name" feature (Archive - Pre May 2025):**
    *   (Details of this older feature remain for historical context but are superseded by the above recent changes as primary focus)
    *   Added Steam app search, fixed VTube Studio discovery, improved error feedback, showed similar apps, better fuzzy matching, D: drive support, simplified status bar, added 12 new streaming apps, improved popup messaging.

*   **Previous - Initial Resource Monitoring Feature (Archive - Pre May 2025, UI now removed):**
    *   (Details of this older feature, whose UI was removed, remain for historical context)
    *   Initially replaced Launch button with CPU/GPU/Memory display, color-coded percentages, 2-second updates, GPU monitoring backends.

*   **General UI/QoL & Bug Fixes (Archive - March 2025):**
    *   (Historical context) Rounded delay arrows, consistent styling, transparent status background, auto-populate name, "Browse" button moved.
    *   Launch Delay Feature: Fully implemented.
*   **Profile Management:** Default profile renaming disabled, data corruption bug on profile deletion fixed.
*   **UI Consistency:** Fixed first-row widget styling, consistent row selection highlighting, standardized tooltip appearance.
*   **UX Enhancements:** Added warning dialog on window close for unsaved changes.
*   **Bug Fixes:** Addressed profile duplication issues, ensured new profiles have 2 empty rows, robust process tracking across profile changes.

## Active Decisions & Considerations
*   **Performance Monitoring:** The UI for real-time performance metrics (CPU/GPU/Memory) was removed due to its significant negative impact on overall application responsiveness. The backend `ResourceMonitor` class capabilities are retained for process detection. A future revisit of optimized performance monitoring UI could be considered if the performance issues can be fully resolved.
*   **Next Feature Focus:** Profile Import/Export functionality remains the next major feature from the roadmap.
*   **Platform Expansion:** While the app is Windows-focused, future cross-platform support should be considered in design decisions.
*   **Auto-save Strategy:** Need to decide between time-based auto-save or action-triggered saves.
*   **Windows Startup Integration:** Will require registry modifications on Windows - need careful implementation.

## Important Patterns & Preferences (Reiterated from System/Product Context)
*   **Modern Dark UI:** Continue adhering to the Twitch-inspired dark theme with purple accents.
*   **Focus on UX:** Prioritize intuitive interaction, clear feedback, and robust error handling.
*   **Decoupled Architecture:** Leverage the `UIEventBus` if the "Locate App" feature involves background tasks or needs to communicate status updates broadly (though likely not for initial implementation).
*   **Modularity:** Keep the path-finding logic separate from the UI code as much as possible, perhaps in a new utility module or within `ProcessManager` if it makes sense.

## Learnings & Project Insights (Ongoing)
*   The detailed handover document has been invaluable for understanding the current state.
*   The clear separation of concerns (e.g., `ConfigManager`, `StyleManager`) makes adding new features more straightforward.
*   User-facing features like "Launch Delay" have required careful consideration of edge cases and UI states. The "Locate App" feature will likely present similar challenges.
*   **"Locate App" implementation insights:**
    *   Steam apps require special handling - they're in steamapps/common subdirectories
    *   Fuzzy matching is essential for user-friendly app discovery
    *   Clear, helpful error messages improve user experience significantly
    *   Showing similar apps (not all apps) is more helpful to users
    *   Registry searches (read-only) are valuable for finding accurate installation paths
    *   Simplicity wins - removed clickable status label for cleaner UX
    *   24 streaming apps now supported, covering most common use cases
    *   Asking "Is the application installed?" helps users understand why search might fail
*   **Process Detection & UI Learnings (May 2025):**
    *   Accurate horizontal alignment of complex list headers with row content often requires careful use of spacers, fixed widths, and stretch factors in Qt layouts.
    *   Using `os.path.normcase` for path comparisons is crucial for reliable process detection on case-insensitive file systems like Windows.
    *   Ensuring consistent UI state (e.g., Launch button enabled/disabled state) for both internally and externally launched/closed applications requires robust checking and updates (e.g., via `check_if_already_running` and `check_process_status`).
*   **Resource Monitoring Insights (Updated May 2025):**
    *   While providing real-time resource data (CPU/GPU/Memory) can be informative, its implementation must be highly optimized to avoid degrading overall application performance. The initial implementation of the UI for this feature was too resource-intensive.
    *   The backend `ResourceMonitor` class still provides valuable process detection capabilities (`get_process_by_path`) even if its detailed metrics are not currently displayed.
    *   (Previous insights on color-coding, GPU backends, update intervals remain relevant if the feature is revisited).
