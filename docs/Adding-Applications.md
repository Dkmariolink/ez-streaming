# Adding Applications

Learn how to add and configure applications in EZ Streaming for your perfect streaming setup.

## Overview

EZ Streaming can launch any Windows executable, from popular streaming software to custom tools. The application includes smart detection for 24+ popular streaming applications and universal support for any Windows program.

## Methods for Adding Applications

### Method 1: "Locate App by Name" (Recommended)

The smart search feature can automatically find and configure popular applications:

#### How to Use Smart Search
1. Click the **"Locate App by Name"** button in any program row
2. Type the application name (e.g., "OBS", "Discord", "Spotify")
3. Click **"Search"**
4. Select from the results
5. The name and path are automatically filled in

#### What Makes Smart Search Powerful
- **Fuzzy Matching:** Finds apps even with partial or approximate names
- **Multiple Locations:** Searches common installation directories
- **Registry Integration:** Uses Windows Registry for accurate paths
- **Steam Support:** Automatically detects Steam games
- **Case Insensitive:** Works regardless of capitalization

#### Smart Search Locations
The search system checks:
- `C:\Program Files\` and `C:\Program Files (x86)\`
- `C:\Users\[Username]\AppData\Local\`
- `C:\Users\[Username]\AppData\Roaming\`
- `D:\` drive (for Epic Games and other installations)
- Steam directories (`steamapps\common\`)
- Windows Registry entries

### Method 2: Browse Manually

For applications not in the smart detection list or in custom locations:

#### Manual Browse Steps
1. Click the **"Browse"** button in any program row
2. Navigate to the application's installation folder
3. Select the main executable file (usually `.exe`)
4. The application name is auto-populated from the file name
5. Customize the name if desired

#### Finding Application Executables

**Common Application Locations:**
- **OBS Studio:** `C:\Program Files\obs-studio\bin\64bit\obs64.exe`
- **Discord:** `C:\Users\[Username]\AppData\Local\Discord\Update.exe --processStart Discord.exe`
- **Spotify:** `C:\Users\[Username]\AppData\Roaming\Spotify\Spotify.exe`
- **Steam Games:** `C:\Program Files (x86)\Steam\steamapps\common\[GameName]\`

**Tips for Finding Executables:**
- Right-click desktop shortcuts → "Open file location"
- Check application's "About" or "Properties" dialog
- Look in Task Manager → Details tab → Right-click → "Open file location"

## Supported Applications

### Applications with Smart Detection

EZ Streaming has built-in smart detection for these popular applications:

#### Streaming Software
- **OBS Studio** - Most popular streaming software
- **Streamlabs** - All-in-one streaming solution
- **StreamElements OBS.Live** - Browser-based streaming
- **Twitch Studio** - Twitch's official streaming software
- **XSplit** - Professional streaming and recording

#### Communication & Chat
- **Discord** - Voice, video, and text communication
- **TeamSpeak** - Voice communication for gaming
- **Skype** - Video calling and messaging

#### Music & Audio
- **Spotify** - Music streaming service
- **VLC Media Player** - Versatile media player
- **Audacity** - Audio editing and recording

#### Stream Enhancement Tools
- **Mix It Up** - Advanced bot and interaction system
- **Touch Portal** - Stream deck alternative
- **Streamlabs Chatbot** - Chat moderation and interactions
- **Loupedeck** - Physical control surface

#### Virtual Production
- **VTube Studio** - VTuber avatar software
- **Snap Camera** - Virtual camera effects
- **NVIDIA Broadcast** - AI-powered streaming enhancement

#### Recording & Capture
- **NVIDIA ShadowPlay** - GPU-accelerated recording
- **Bandicam** - Screen recording software
- **Fraps** - Gaming recording and benchmarking

#### Interactive & Engagement
- **Crowd Control** - Audience interaction for games
- **Dixper** - Interactive streaming platform
- **StreamLabs** - Stream alerts and donations

#### Multi-streaming & Distribution
- **Restream** - Multi-platform streaming
- **Lightstream** - Cloud-based streaming

### Universal Application Support

**Important:** While EZ Streaming has smart detection for 24+ applications, it can launch **any Windows executable**. This includes:

- **Games:** Steam games, Epic Games, GOG games, standalone games
- **Productivity Tools:** Notepad++, Visual Studio Code, Photoshop
- **Browsers:** Chrome, Firefox, Edge (with specific URLs)
- **Custom Software:** Your own applications or specialized tools
- **Utilities:** System monitors, RGB control software, macro tools

## Configuring Applications

### Application Name
- **Purpose:** Display name in the EZ Streaming interface
- **Auto-Detection:** Automatically filled when browsing or using smart search
- **Customization:** Edit to your preference (e.g., "OBS Studio" → "Streaming Software")
- **Best Practices:** Keep names short but descriptive

### Application Path
- **Requirements:** Must point to a valid executable file
- **Format:** Full path to the `.exe` file
- **Validation:** EZ Streaming checks if the path exists
- **Updates:** May need updating when applications are updated or moved

### Launch Status Indicators
- **Valid Path:** Green checkmark or normal appearance
- **Invalid Path:** Red warning or disabled controls
- **Already Running:** "Launched" button state, disabled launch control
- **Process Detection:** Automatic detection of externally launched apps

## Advanced Application Configuration

### Steam Games

EZ Streaming can automatically detect Steam games:

#### Steam Game Detection
- **Search Method:** Use "Locate App by Name" and search for the game name
- **Location:** Found in `Steam\steamapps\common\[GameName]\`
- **Executable:** Usually the main game executable, not Steam.exe
- **Direct Launch:** Launches the game directly, bypassing Steam overlay issues

#### Steam Integration Tips
- **Steam Running:** Ensure Steam is running for games that require it
- **Launch Options:** Some games may need specific launch parameters
- **Anti-Cheat:** Be aware of anti-cheat systems that might conflict

### Browser Applications

You can launch browsers with specific URLs:

#### Browser Configuration Examples
- **Twitch Dashboard:** `"C:\Program Files\Google\Chrome\Application\chrome.exe" --new-window "https://dashboard.twitch.tv"`
- **YouTube Studio:** `"C:\Program Files\Google\Chrome\Application\chrome.exe" --app="https://studio.youtube.com"`
- **Stream Deck Web:** `"C:\Program Files\Microsoft\Edge\Application\msedge.exe" --app="https://streamdeck.elgato.com"`

### Applications with Special Requirements

#### Applications Requiring Administrator Rights
- **Solution:** Run EZ Streaming as administrator
- **Alternative:** Create a scheduled task to run the application with elevated privileges
- **Note:** This affects all applications launched by EZ Streaming

#### Applications with Command Line Arguments
**Current Limitation:** EZ Streaming doesn't yet support command-line arguments
**Workaround:** Create a batch file that launches the application with arguments, then add the batch file to EZ Streaming

**Example Batch File:**
```batch
@echo off
"C:\Program Files\OBS Studio\bin\64bit\obs64.exe" --minimize-to-tray --startvirtualcam
```

## Application Management

### Reordering Applications

Applications launch in the order they appear in the list:

#### How to Reorder
1. Click and drag the **drag handle** (≡) on the left side of any row
2. Drop the application in the desired position
3. The new order is saved automatically

#### Strategic Ordering
- **Heavy Applications First:** OBS, games, resource-intensive software
- **Dependencies:** Applications that depend on others should come after
- **Quick Starters Last:** Lightweight apps like Spotify, Discord

### Removing Applications

#### Individual Removal
1. Click the **"Remove"** button (X) on the application row
2. The application is immediately removed from the profile
3. **Note:** This doesn't uninstall the application, just removes it from the profile

#### Bulk Management
- **New Profiles:** Start with empty rows for clean organization
- **Profile Duplication:** Copy profiles and remove unwanted applications
- **Fresh Start:** Create new profiles when current ones become cluttered

### Application Status Management

#### Launch Status
- **Launch Button:** Starts the individual application immediately
- **Status Updates:** Shows "Launching..." during startup
- **Running Detection:** Button changes to "Launched" when app is detected
- **External Detection:** Detects apps launched outside of EZ Streaming

#### Close Management
- **Individual Close:** Use the "Close" button to terminate specific applications
- **Close All:** Terminates all applications tracked by the current profile
- **Process Tracking:** EZ Streaming tracks launched processes for proper management

## Troubleshooting Application Issues

### Application Won't Launch

#### Path Issues
**Problem:** Invalid or outdated application path  
**Solutions:**
1. Use "Browse" to locate the current executable
2. Check if the application was updated or moved
3. Verify file permissions
4. Try running EZ Streaming as administrator

#### Permission Issues
**Problem:** "Access denied" or similar errors  
**Solutions:**
1. Run EZ Streaming as administrator
2. Check if the application requires special permissions
3. Verify antivirus isn't blocking the launch
4. Try launching the application manually first

### Smart Search Can't Find Application

#### Troubleshooting Steps
1. **Verify Installation:** Ensure the application is actually installed
2. **Check Common Locations:** Look in Program Files, AppData, etc.
3. **Try Alternative Names:** Search for different variations of the name
4. **Use Manual Browse:** Fall back to manual file selection
5. **Check for Portable Apps:** Some applications don't install to standard locations

#### Improving Search Results
- **Use exact names:** "OBS Studio" vs "OBS"
- **Try abbreviations:** "VS Code" for Visual Studio Code  
- **Check aliases:** Some applications have multiple common names

### Application Launches but Doesn't Work Properly

#### Common Issues and Solutions

**Crashes Immediately:**
- Check if the application needs additional files or dependencies
- Try launching manually first to see error messages
- Verify the correct executable is selected (not an installer or updater)

**Wrong Window or Instance:**
- Some applications may open multiple windows or processes
- Try different executables in the application folder
- Check application settings for startup behavior

**Hangs During Launch:**
- Increase launch delays to give more time for startup
- Check if the application is waiting for user input
- Verify system resources are sufficient

## Best Practices for Application Management

### Organization Strategies

#### Group by Function
- **Core Streaming:** OBS, streaming software first
- **Communication:** Discord, chat applications
- **Content:** Games, creative software
- **Utilities:** Music, monitoring tools last

#### Profile-Specific Applications
- **Gaming Profile:** Game launcher, recording software, voice chat
- **Creative Profile:** Art software, reference browsers, ambient music
- **Podcast Profile:** Recording software, communication tools, notes

### Performance Optimization

#### Application Selection
- **Essential Only:** Only add applications you actually use
- **Resource Awareness:** Consider system impact of each application
- **Alternatives:** Choose lighter alternatives when possible
- **Background Apps:** Minimize applications that run in the background

#### Launch Strategy
- **Staggered Startup:** Use appropriate delays between applications
- **Priority Order:** Launch most important applications first
- **System Monitoring:** Watch resource usage during launches

### Maintenance

#### Regular Reviews
- **Monthly Cleanup:** Remove unused applications from profiles
- **Path Verification:** Check that application paths are still valid
- **Update Tracking:** Update paths when applications are updated
- **Performance Assessment:** Evaluate if all applications are still needed

#### Documentation
- **Profile Notes:** Keep notes about special configurations
- **Version Tracking:** Note which versions of applications work well together
- **Troubleshooting Log:** Document solutions to recurring issues

## Future Application Features

### Planned Enhancements
- **Command Line Arguments:** Support for launching applications with specific parameters
- **Application Categories:** Group applications by type for better organization
- **Dependency Management:** Automatic handling of application dependencies
- **Update Detection:** Notification when application paths become invalid

### Community Features
- **Application Database:** Shared database of application configurations
- **Profile Sharing:** Share complete application setups with other users
- **Best Practices:** Community-contributed optimal configurations

## Related Topics

- **[Launch Delays and Timing](Launch-Delays-and-Timing.md):** Optimize timing for your applications
- **[Profile Management](Profile-Management.md):** Organize applications into different profiles
- **[Process Management](Process-Management.md):** Understand how EZ Streaming tracks running applications
- **[Troubleshooting](Troubleshooting.md):** Solutions for common application issues
