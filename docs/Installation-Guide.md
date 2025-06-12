# Installation Guide

EZ Streaming is designed to be portable and easy to use. No traditional installation is required!

## Download and Setup

### Step 1: Download EZ Streaming
1. Go to the [Download page](download.html) or visit the [GitHub Releases](https://github.com/Dkmariolink/ez-streaming/releases)
2. Download the latest `EZStreaming.exe` file
3. The download is approximately 15 MB

### Step 2: Choose a Location
1. Create a folder where you want to keep EZ Streaming (e.g., `C:\EZStreaming` or `D:\Programs\EZStreaming`)
2. Extract or move the `EZStreaming.exe` file to this folder
3. **Tip:** Choose a location you'll remember, as this is where your configuration will be saved

### Step 3: First Launch
1. Double-click `EZStreaming.exe` to launch the application
2. If Windows SmartScreen appears:
   - Click "More info"
   - Click "Run anyway"
   - This happens because we haven't code-signed the executable yet, but it's completely safe

### Step 4: Initial Setup
On first launch, EZ Streaming will:
- Create a default profile for you
- Show the main interface with two empty program rows
- Create a configuration file in your system's AppData folder

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10 (64-bit) or newer
- **Memory:** 4 GB RAM
- **Storage:** 100 MB free disk space
- **Dependencies:** None required

### Recommended Requirements
- **Operating System:** Windows 11 (64-bit)
- **Memory:** 8 GB RAM or more
- **Storage:** 500 MB free disk space (for larger streaming setups)

## File Locations

### Executable Location
- The `EZStreaming.exe` file can be placed anywhere you prefer
- Common locations:
  - `C:\EZStreaming\`
  - `C:\Program Files\EZStreaming\`
  - `D:\Programs\EZStreaming\`

### Configuration File Location
EZ Streaming stores its configuration in your system's standard application data directory:

**Windows 10/11:**
```
C:\Users\[YourUsername]\AppData\Roaming\EZStreaming\ez_streaming_config.json
```

This file contains:
- All your profiles and their settings
- Application paths and configurations
- Launch delay preferences
- UI preferences

## Portable Usage

EZ Streaming is fully portable! You can:
- Copy the `EZStreaming.exe` file to a USB drive
- Run it on any compatible Windows computer
- Your profiles will be saved locally on each computer

### Making EZ Streaming Truly Portable
If you want to carry your profiles between computers:
1. After setting up your profiles, locate the config file (see above)
2. Copy `ez_streaming_config.json` to the same folder as `EZStreaming.exe`
3. The application will use the local config file if one exists in the same directory

## Windows Startup Integration (Optional)

To have EZ Streaming start automatically with Windows:

### Method 1: Windows Startup Folder
1. Press `Win + R`, type `shell:startup`, and press Enter
2. Create a shortcut to `EZStreaming.exe` in the Startup folder
3. EZ Streaming will now launch when Windows starts

### Method 2: Task Scheduler (Advanced)
1. Open Task Scheduler (`Win + R`, type `taskschd.msc`)
2. Click "Create Basic Task"
3. Name it "EZ Streaming Startup"
4. Set trigger to "When I log on"
5. Set action to start `EZStreaming.exe`

## Uninstalling EZ Streaming

Since EZ Streaming doesn't use a traditional installer:

### To Remove EZ Streaming:
1. Delete the `EZStreaming.exe` file
2. Delete the configuration file at:
   ```
   C:\Users\[YourUsername]\AppData\Roaming\EZStreaming\
   ```
3. Remove any Windows startup shortcuts (if created)

### To Keep Your Profiles:
- Only delete the executable file
- Keep the configuration folder to preserve your settings
- Your profiles can be restored by placing a new executable in any location

## Troubleshooting Installation

### Windows SmartScreen Warning
**Problem:** Windows blocks the executable with a SmartScreen warning.  
**Solution:** Click "More info" → "Run anyway". This is normal for unsigned executables.

### Antivirus False Positive
**Problem:** Antivirus software flags EZ Streaming as suspicious.  
**Solution:** Add EZ Streaming to your antivirus whitelist. This is common with PyInstaller-built applications.

### Permission Errors
**Problem:** "Access denied" or permission errors when running.  
**Solution:** 
- Right-click `EZStreaming.exe` → "Run as administrator"
- Or move the executable to a folder with proper write permissions

### Configuration Not Saving
**Problem:** Settings and profiles don't persist between sessions.  
**Solution:** 
- Ensure the AppData folder is writable
- Try running as administrator once to create the initial config
- Check if antivirus is blocking file writes

## Next Steps

After installation, you might want to:
- Read the [Quick Start Tutorial](Quick-Start-Tutorial.md)
- Learn about [Profile Management](Profile-Management.md)
- Explore [Adding Applications](Adding-Applications.md)

## Advanced Installation Options

### Running from Source Code
For developers or advanced users who want to run from source:
1. Install Python 3.8+ and pip
2. Clone the repository: `git clone https://github.com/Dkmariolink/ez-streaming.git`
3. Install dependencies: `pip install -r fresh_env.txt`
4. Run: `python src/main.py`

See [Building from Source](Building-from-Source.md) for detailed instructions.

### Corporate/Network Environments
If deploying EZ Streaming in a corporate environment:

**Considerations:**
- Application requires write access to user's AppData folder
- May need IT approval for executable files
- Consider deploying via network shares with proper permissions
- Profiles are user-specific and stored locally

**Group Policy:**
- EZ Streaming doesn't require registry modifications
- No system-wide configuration needed
- Each user maintains their own profiles and settings
