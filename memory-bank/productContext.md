# Product Context: EZ Streaming

## Why This Project Exists
EZ Streaming was born out of a common frustration experienced by content creators: the repetitive and time-consuming task of manually launching multiple applications before starting a stream or recording session. This pre-flight checklist can include streaming software (like OBS), communication apps (Discord), music players (Spotify), game launchers, browser windows, and various other utilities. Each second spent on setup is a second not spent on creating content or engaging with an audience. EZ Streaming aims to give that time back to creators.

## Problems It Solves
*   **Reduces Pre-Stream Tedium:** Automates the launching of a suite of applications, turning a multi-step, multi-click process into a single-click action.
*   **Saves Time:** Allows creators to start their sessions more quickly and efficiently.
*   **Minimizes Forgotten Applications:** Ensures all necessary tools are running, preventing mid-stream interruptions to launch a missed program.
*   **Improves Consistency:** Helps maintain a consistent setup across different streaming sessions or for different types of content by using profiles.
*   **Lowers Cognitive Load:** Frees creators from having to remember and manually manage their application startup sequence, allowing them to focus on their content.
*   **Addresses Dated Solutions:** Moves beyond simple batch files or clunky interfaces by providing a modern, user-friendly Qt-based application.

## How It Should Work (User Perspective)
From a user's point of view, EZ Streaming should feel like a seamless and intuitive assistant:

1.  **Initial Setup:**
    *   The user installs EZ Streaming.
    *   On first launch, they are greeted with a clean, modern dark interface.
    *   They can create a "profile" (e.g., "Gaming Stream," "Art Session," "Podcast Recording").
    *   Within a profile, they add applications by providing a name (e.g., "OBS," "Discord") and browsing to the application's executable file.
2.  **Configuration:**
    *   Users can add multiple applications to each profile.
    *   They can reorder applications via drag-and-drop to define the launch sequence.
    *   They can set a default launch delay for all apps in a profile (e.g., wait 5 seconds between launching each app).
    *   They can override the default delay for specific applications if needed, setting a custom delay.
    *   The application provides visual cues, such as disabling delay options for the first app or warning about very low (potentially problematic) delays.
    *   All changes can be saved. The application warns if there are unsaved changes upon attempting to close.
3.  **Daily Use:**
    *   The user selects the desired profile from a dropdown list.
    *   They click a "Launch All" button.
    *   EZ Streaming launches each application in the specified order, respecting the configured delays. The UI remains responsive.
    *   The status of launched applications can be monitored.
    *   Users can also launch or close individual applications from the list.
4.  **Management:**
    *   Users can easily create new profiles, duplicate existing ones (as a template), rename them, or delete them.
    *   The "default" profile is clearly marked and protected from accidental renaming.

## User Experience Goals
*   **Professional & Modern:** The application should look and feel like a high-quality, contemporary tool, aligning with the aesthetic of modern streaming setups (dark theme, purple accents).
*   **Clean & Intuitive:** The UI should be uncluttered, with clear labels and controls. Users should be able to understand how to use the core features with minimal guidance.
*   **Reliable & Stable:** The application must perform its functions consistently without crashes or data loss. Configuration saving and loading should be robust.
*   **Visually Consistent:** All UI elements (buttons, inputs, tooltips, highlighting) should follow a consistent design language.
*   **Responsive:** The UI should not freeze or become unresponsive, especially during operations like launching multiple applications.
*   **Helpful & Forgiving:** Features like unsaved changes warnings, clear tooltips, and sensible defaults contribute to a positive user experience.
*   **Efficient:** The application should streamline workflows, not add complexity.
*   **Enjoyable to Use:** Beyond mere functionality, the goal is for users to find the application pleasant and satisfying to interact with.
