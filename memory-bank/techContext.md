# Technical Context: EZ Streaming

## Technologies Used
*   **Programming Language:** Python (Version 3.x, specific version depends on development environment, but generally compatible with modern Python 3 releases).
*   **GUI Framework:** PySide6 (the official Python bindings for Qt 6). This provides the widgets, layout tools, event handling, and styling capabilities for the user interface.
*   **Build/Packaging Tool:** PyInstaller. Used to package the Python application and its dependencies (including PySide6, assets, etc.) into a standalone executable for distribution (e.g., `.exe` on Windows).
*   **Configuration Format:** JSON (JavaScript Object Notation). Used for storing user profiles, application settings, and program lists in a human-readable file (`ez_streaming_config.json`).
*   **Styling:** QSS (Qt Style Sheets). A CSS-like language used to define the visual appearance (colors, fonts, borders, etc.) of Qt widgets. Managed via `style_manager.py`.

## Development Setup
*   **Python Environment:** A standard Python 3 installation is required.
*   **Virtual Environments:** Recommended (e.g., using `venv` or `conda`) to manage project dependencies and isolate them from the global Python installation. The project includes a `fresh_env.txt` which likely lists dependencies for `pip install -r fresh_env.txt`.
*   **Key Dependencies (to be installed via pip):**
    *   `PySide6`: For the Qt GUI framework.
    *   `PyInstaller`: For building executables.
    *   `psutil`: For process and resource monitoring (optional but recommended).
    *   `pynvml`: For NVIDIA GPU monitoring (optional).
    *   `GPUtil`: For general GPU monitoring (optional).
    *   (Other minor dependencies might be implicitly included or listed in a requirements file).
*   **Code Editor/IDE:** Any Python-supporting editor can be used (e.g., VS Code, PyCharm).
*   **Operating System:** Primarily developed and tested on Windows, but Qt and Python are cross-platform, allowing for potential future ports to macOS and Linux (though specific OS integrations might require additional work).

## Technical Constraints
*   **UI Responsiveness:** The application must remain responsive, especially during potentially long-running operations like launching multiple applications with delays. This is addressed by using non-blocking timers (`QTimer`) and potentially offloading heavy tasks if they were to arise.
*   **Cross-Platform Compatibility (Future):** While currently focused on Windows (implied by `.exe` builds and some path considerations), the choice of Python and Qt facilitates future cross-platform support. However, platform-specific features (like "launch with Windows" or system tray integration) will require platform-dependent code.
*   **Dependency Management:** Ensuring that the correct versions of PySide6 and other libraries are used and packaged correctly by PyInstaller.
*   **Error Handling:** Robust error handling is needed for file operations (config loading/saving), process launching, and unexpected UI states. Custom exceptions (`exceptions.py`) aid in this.

## Dependencies
*   **Primary External Dependencies:**
    *   **PySide6:** The core GUI toolkit.
    *   **PyInstaller:** For creating distributable builds.
*   **Standard Python Libraries:**
    *   `json`: For (de)serializing configuration data.
    *   `os`, `sys`, `subprocess`: For file system interactions, system information, and launching external processes.
    *   `dataclasses`: For creating structured configuration models.
    *   `pathlib`: For modern, object-oriented path manipulation.
    *   `enum`: For defining constants like event types.
    *   `logging`: (Potentially used for internal logging, though not explicitly detailed as a core architectural component in handover).

## Tool Usage Patterns
*   **PyInstaller:** Used with a `.spec` file (e.g., `EZStreaming.spec`) to configure the build process. This spec file defines what to include (scripts, data files like assets, hidden imports for libraries PyInstaller might miss).
*   **JSON:** `ConfigManager` uses Python's `json` module (`json.dump`, `json.load`) to write and read the `ez_streaming_config.json` file.
*   **QSS:** `StyleManager` generates and applies QSS strings to style Qt widgets, often by setting the stylesheet property on the main application instance or specific widgets.
*   **Git (Implied):** A version control system like Git is assumed for source code management, given references to repositories and issue tracking.

## Configuration File Details
*   **Filename:** `ez_streaming_config.json`
*   **Location:** Stored in a platform-appropriate user application data directory:
    *   **Windows:** Typically `C:\Users\<Username>\AppData\Roaming\EZStreaming` (or Local, depending on implementation).
    *   **macOS:** Typically `~/Library/Application Support/EZStreaming`.
    *   **Linux:** Typically `~/.config/EZStreaming` or `~/.local/share/EZStreaming`.
    (The exact path is determined by `ConfigManager`, likely using Qt's `QStandardPaths` or similar).
*   **Structure:** A JSON object containing:
    *   A list of profiles, where each profile has a name, a default launch delay, and a list of programs.
    *   Each program has a name, executable path, and custom delay settings.
    *   The name of the currently active/selected profile.
    *   Global settings like `show_low_delay_warning`.
    *   Example (conceptual):
        ```json
        {
          "profiles": [
            {
              "name": "Default",
              "launch_delay": 5,
              "programs": [
                { "name": "OBS", "path": "C:/...", "use_custom_delay": false, "custom_delay_value": 3 },
                { "name": "Discord", "path": "C:/...", "use_custom_delay": true, "custom_delay_value": 2 }
              ]
            }
          ],
          "current_profile_name": "Default",
          "show_low_delay_warning": true
        }
        ```

## Build and Deployment
*   The application is built into an executable using PyInstaller via `build.py` or by directly running PyInstaller with the `EZStreaming.spec` file.
*   The build process needs to include:
    *   All Python source files (`.py`).
    *   The `assets/` folder (containing icons like `icon.ico`, `icon.png`, title images).
    *   Font resources (e.g., `assets/fonts/SummerBlaster.otf`).
    *   All necessary PySide6/Qt libraries and plugins.
    *   Any other data files required at runtime.
*   The output is typically a single executable or a folder containing the executable and its dependencies, placed in a `dist/` or `build/` directory.
