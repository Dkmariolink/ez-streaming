# First Setup Guide

This guide will walk you through creating your first streaming profile in EZ Streaming.

## Initial Launch

When you first open EZ Streaming, you'll see:
- A default profile already created
- Two empty application rows ready for configuration
- The main interface with profile management controls

## Creating Your First Profile

### Step 1: Add Your Streaming Applications

You have three ways to add applications:

#### Method 1: Locate App by Name (Recommended)
1. Click the **"Locate App by Name"** button
2. Type the name of your application (e.g., "OBS", "Discord", "Spotify")
3. EZ Streaming will automatically find and add the application

**Supported Applications Include:**
- **Streaming**: OBS Studio, Streamlabs, XSplit, Twitch Studio
- **Communication**: Discord, TeamSpeak, Skype
- **Content**: Spotify, VLC Media Player, Audacity
- **Enhancement**: Mix It Up, Touch Portal, StreamElements
- **Virtual Production**: VTube Studio, NVIDIA Broadcast
- **Recording**: NVIDIA ShadowPlay, Action!, Bandicam

#### Method 2: Browse for Applications
1. Click the **"Browse"** button
2. Navigate to your application's executable file (.exe)
3. Select the file to add it to your profile

#### Method 3: Drag and Drop
1. Open File Explorer
2. Navigate to your application's folder
3. Drag the .exe file directly into EZ Streaming

### Step 2: Configure Launch Order

The order of applications in your list determines their launch sequence:

1. **Drag and drop** rows to reorder them
2. **First application** launches immediately
3. **Subsequent applications** launch with delays

**Recommended Order:**
1. Core streaming software (OBS, Streamlabs)
2. Communication tools (Discord, TeamSpeak)
3. Content applications (Spotify, browser)
4. Enhancement tools (chatbots, overlays)

### Step 3: Set Launch Delays

Launch delays prevent system overload and ensure applications start properly:

#### Profile Default Delay
1. Set a default delay for all applications in your profile
2. **Recommended**: 3-5 seconds for most setups
3. **Heavy applications**: 5-10 seconds for resource-intensive apps

#### Per-Application Custom Delays
1. Check the delay checkbox for specific applications
2. Override the default with a custom delay
3. **Use cases**:
   - Longer delays for heavy applications like OBS
   - Shorter delays for lightweight utilities
   - Zero delay for instant-launch applications

**Delay Guidelines:**
- **0-2 seconds**: Light applications (Discord, Spotify)
- **3-5 seconds**: Standard applications (browsers, utilities)
- **5-10 seconds**: Heavy applications (OBS, games, video editors)

### Step 4: Test Your Setup

Before relying on your profile:

1. **Individual Testing**
   - Use individual "Launch" buttons to test each application
   - Verify all paths are correct and applications start properly

2. **Full Profile Testing**
   - Click **"Launch All"** to test the complete sequence
   - Observe the launch timing and adjust delays if needed

3. **System Monitoring**
   - Watch system resources during launch
   - Adjust delays if you notice performance issues

## Advanced First Setup

### Creating Multiple Profiles

Different streaming scenarios need different setups:

1. **Gaming Profile**
   - Game capture software
   - Voice chat applications
   - Performance monitoring tools

2. **Art Stream Profile**
   - Drawing/design software
   - Reference browsers
   - Music applications

3. **Podcast Profile**
   - Recording software
   - Call applications
   - Note-taking tools

### Profile Management
1. **Create New Profile**: Click the dropdown and select "New Profile"
2. **Duplicate Profile**: Use existing profiles as templates
3. **Rename Profile**: Right-click or use profile options
4. **Delete Profile**: Remove profiles you no longer need

### Application Management Tips

#### Finding Hidden Applications
Some applications install in non-standard locations:
- **Steam Games**: Usually in `C:\Program Files (x86)\Steam\steamapps\common\`
- **Epic Games**: Usually in `C:\Program Files\Epic Games\`
- **Microsoft Store Apps**: Check `C:\Program Files\WindowsApps\`

#### Handling Shortcuts vs Executables
- **Always use .exe files**, not shortcuts (.lnk)
- **Shortcuts may break** if moved or updated
- **Use "Browse" to find the actual executable**

## Troubleshooting First Setup

### Application Won't Launch
1. **Verify Path**: Ensure the path to the .exe file is correct
2. **Check Permissions**: Run EZ Streaming as administrator if needed
3. **Test Manually**: Try launching the application manually first

### Launch Delays Too Short
Signs your delays are too short:
- Applications crash or fail to start
- System becomes unresponsive during launch
- Applications launch but don't work properly

**Solution**: Increase delays by 2-3 seconds

### Launch Delays Too Long
Signs your delays are too long:
- Launch sequence takes unnecessarily long
- You lose momentum waiting for apps to start

**Solution**: Decrease delays gradually while testing

### Profile Not Saving
1. **Check Permissions**: Ensure EZ Streaming can write to its config folder
2. **Manual Save**: Changes should auto-save, but try restarting the application
3. **Config Location**: Check `%APPDATA%\EZStreaming\` for config files

## Next Steps

Once your first profile is working:

1. **Explore Advanced Features**:
   - Process monitoring and control
   - Profile import/export (coming soon)
   - Startup integration

2. **Optimize Your Workflow**:
   - Fine-tune launch delays
   - Create specialized profiles
   - Share your setup with the community

3. **Join the Community**:
   - Share your profiles in [GitHub Discussions](https://github.com/Dkmariolink/ez-streaming/discussions)
   - Get help and tips from other users
   - Suggest new features

---

**Ready for more?** Check out our [Best Practices Guide](Best-Practices) for advanced tips and optimization techniques!
