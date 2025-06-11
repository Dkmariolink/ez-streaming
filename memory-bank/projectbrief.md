# Project Brief: EZ Streaming

## Project Name
EZ Streaming

## Core Purpose
EZ Streaming is a streamlined utility designed for content creators. Its primary function is to allow users to launch multiple streaming-related applications (e.g., OBS, Discord, Spotify, capture software, etc.) with a single click, simplifying their pre-stream setup process.

## Target User
The primary target users are content creators, streamers (video game streamers, artists, musicians, educators, etc.), and anyone who regularly needs to launch a specific set of applications before starting an online broadcast or recording session.

## Key Goals
*   **Simplify Setup:** Drastically reduce the time and effort required to prepare for a stream or recording session.
*   **Save Time:** Allow users to get to content creation faster by automating the application launch sequence.
*   **Provide a Polished and Reliable Tool:** Offer a modern, intuitive, and stable user experience.
*   **Evolve with User-Centric Features:** Continuously improve the application based on user feedback and emerging needs in the streaming community.
*   **Enhance Productivity:** Allow users to manage different sets of applications for various streaming scenarios through profiles.

## Scope

### Current Core Scope:
*   **Application Launching:** Launch multiple user-defined applications.
*   **Profile Management:**
    *   Create, rename, duplicate, and delete profiles.
    *   Each profile stores a list of applications and their settings.
    *   Support for a "default" profile.
*   **Program Management (within profiles):**
    *   Add and remove programs.
    *   Specify application name and path.
    *   Drag-and-drop reordering of applications within a profile.
*   **Process Monitoring:** Basic tracking of launched application statuses.
*   **Launch Delays:**
    *   Configurable default launch delay per profile.
    *   Per-application custom launch delay override.
    *   Warning for low delay values.
    *   Delay controls disabled for the first app in a sequence or if paths are invalid.
    *   Non-blocking timers for UI responsiveness during launch.
*   **Configuration Persistence:** Save and load user configurations (profiles, programs, settings) to a JSON file.
*   **User Interface:** Modern dark theme with purple accents, animated title, consistent styling, and tooltips.
*   **User Experience:** Warning for unsaved changes on close, consistent row selection.

### Future Scope (as per Roadmap):
*   **Phase 2 (User Experience Enhancement):**
    *   Profile Import/Export.
    *   "Copy App from Another Profile" feature.
    *   Profile descriptions, categories/tags, activation scheduling.
    *   "Locate App by Name" button.
    *   Command-line arguments for launched applications.
    *   Auto-save functionality.
    *   Auto-launch option on Windows startup.
    *   Integrated settings menu (theme, accessibility).
    *   Onboarding/Tutorial system.
*   **Phase 3 (Advanced Integration):**
    *   System tray functionality.
    *   Windows startup integration, file association, notifications.
    *   Online update check & patching.
    *   Stream status monitoring (Twitch/YouTube).
    *   Basic chat integration.
*   **Phase 4 (Extended Functionality):**
    *   Performance monitoring for launched apps.
    *   Dependency-based and conditional launching.
    *   Community profile sharing platform.
    *   Potential macOS/Linux versions and mobile companion app.
