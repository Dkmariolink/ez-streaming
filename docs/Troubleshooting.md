# Troubleshooting Guide

This guide covers common issues you might encounter with EZ Streaming and their solutions.

## Installation Issues

### Windows SmartScreen Blocking Installation

**Problem**: Windows shows "Windows protected your PC" message
**Solution**: 
1. Click "More info"
2. Click "Run anyway"
3. This happens because the executable isn't code-signed (common for open-source software)

### Antivirus False Positive

**Problem**: Antivirus software quarantines or blocks EZStreaming.exe
**Solution**:
1. Add EZStreaming.exe to your antivirus whitelist/exceptions
2. Add the entire EZ Streaming folder to the whitelist
3. This is common with PyInstaller-built applications

### Missing DLL Errors

**Problem**: Error messages about missing .dll files
**Solution**:
1. Install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Restart your computer
3. Try launching EZ Streaming again

## Application Launch Issues

### Application Won't Launch

**Problem**: Clicking "Launch" does nothing or shows error
**Diagnosis Steps**:
1. Check if the application path is correct
2. Verify the .exe file exists at that location
3. Try launching the application manually

**Solutions**:
- **Incorrect Path**: Use "Browse" to select the correct .exe file
- **Moved Application**: Re-locate the application using "Locate App by Name"
- **Permissions**: Run EZ Streaming as administrator
- **Corrupted Application**: Reinstall the target application

### Steam Games Won't Launch

**Problem**: Steam games fail to launch or show errors
**Solutions**:
1. **Launch Steam First**: Add Steam to your profile before any Steam games
2. **Use Steam Protocol**: Instead of the game .exe, use steam://rungameid/[APPID]
3. **Check Game Path**: Steam games are usually in `steamapps\common\`
4. **Verify Game Files**: Use Steam to verify game file integrity

### Applications Crash During Launch

**Problem**: Applications start but immediately crash
**Solutions**:
1. **Increase Launch Delays**: Add 2-3 seconds more delay
2. **Launch Order**: Move problematic apps later in the sequence
3. **Administrator Mode**: Run EZ Streaming as administrator
4. **Single Launch Test**: Try launching the app individually first

## Performance Issues

### System Becomes Unresponsive

**Problem**: Computer freezes or becomes very slow during launch
**Solutions**:
1. **Increase Delays**: Use 5-10 second delays between heavy applications
2. **Reduce Simultaneous Launches**: Split heavy apps across multiple profiles
3. **Check System Resources**: Monitor RAM and CPU usage
4. **Close Other Applications**: Free up system resources before launching

### Slow Launch Sequence

**Problem**: Launch sequence takes too long to complete
**Solutions**:
1. **Optimize Delays**: Reduce delays for lightweight applications
2. **Remove Unnecessary Apps**: Only include applications you actually need
3. **Reorder Applications**: Put fastest-launching apps first
4. **Use Individual Launch**: Launch some apps manually for immediate use

### Memory/CPU Usage High

**Problem**: EZ Streaming uses excessive system resources
**Solutions**:
1. **Close Unused Profiles**: Only keep necessary profiles loaded
2. **Disable Monitoring**: Process monitoring uses some resources
3. **Restart Application**: Close and reopen EZ Streaming periodically
4. **Check for Updates**: Newer versions may have performance improvements

## Configuration Issues

### Settings Not Saving

**Problem**: Changes to profiles or settings are lost
**Solutions**:
1. **Check Permissions**: Ensure write access to `%APPDATA%\EZStreaming\`
2. **Run as Administrator**: May be needed for some Windows configurations
3. **Antivirus Interference**: Check if antivirus is blocking file writes
4. **Disk Space**: Ensure sufficient free space on system drive

### Profiles Disappeared

**Problem**: Created profiles are no longer visible
**Solutions**:
1. **Check Config File**: Look for `ez_streaming_config.json` in `%APPDATA%\EZStreaming\`
2. **Restore from Backup**: Check if you have backup config files
3. **Recreate Profiles**: Unfortunately, may need to recreate lost profiles
4. **Export Regularly**: Create backups by copying the config file

### Can't Delete or Rename Default Profile

**Problem**: Default profile options are grayed out
**This is intentional**: The default profile is protected to prevent accidental deletion
**Solution**: Create new profiles for different configurations

## UI/Display Issues

### Interface Appears Corrupted or Wrong Size

**Problem**: UI elements are misaligned or wrong size
**Solutions**:
1. **Restart Application**: Close and reopen EZ Streaming
2. **Check Display Scaling**: Adjust Windows display scaling settings
3. **Update Graphics Drivers**: Ensure graphics drivers are current
4. **Reset Window Size**: Delete config file to reset window settings

### Dark Theme Issues

**Problem**: Text is hard to read or colors look wrong
**Solutions**:
1. **Check Windows Theme**: EZ Streaming respects Windows dark/light mode
2. **Update Windows**: Ensure Windows is up to date
3. **Graphics Driver Update**: Update your graphics drivers
4. **Report Bug**: If persistent, report the issue on GitHub

## Specific Application Issues

### OBS Studio Issues

**Common Problems**:
- OBS crashes when launched through EZ Streaming
- OBS shows "Failed to initialize video" error

**Solutions**:
1. **Close Other Video Software**: Close other apps using webcam/capture cards
2. **Run as Administrator**: Both EZ Streaming and OBS may need admin rights
3. **Increase Launch Delay**: OBS needs time to initialize properly
4. **Check OBS Settings**: Verify OBS settings are correct for your hardware

### Discord Issues

**Common Problems**:
- Discord shows "Update Failed" when launched
- Discord doesn't connect to voice channels

**Solutions**:
1. **Update Discord**: Ensure Discord is up to date
2. **Clear Discord Cache**: Delete Discord cache files
3. **Run as Administrator**: May be needed for Discord updates
4. **Check Network**: Verify internet connection is stable

### Browser Issues

**Common Problems**:
- Browser opens but doesn't load pages
- Multiple browser instances open

**Solutions**:
1. **Check Browser Settings**: Ensure browser is set as default if needed
2. **Clear Browser Data**: Clear cache and cookies
3. **Use Specific Browser Profile**: Launch browser with specific profile arguments
4. **Single Instance**: Use browser settings to prevent multiple instances

## Advanced Troubleshooting

### Enable Debug Logging

For persistent issues:
1. **Contact Support**: Report issues on [GitHub Issues](https://github.com/Dkmariolink/ez-streaming/issues)
2. **Provide Details**: Include Windows version, EZ Streaming version, and specific error messages
3. **Include Config**: Share your profile configuration (remove sensitive info)

### Safe Mode Launch

If EZ Streaming won't start:
1. **Delete Config**: Backup and delete config file to reset settings
2. **Fresh Install**: Extract EZ Streaming to a new folder
3. **Compatibility Mode**: Try running in Windows compatibility mode
4. **Check Dependencies**: Ensure all required system components are installed

### Collect System Information

For bug reports, gather:
- Windows version and build number
- EZ Streaming version
- List of applications you're trying to launch
- Error messages (exact text)
- Steps to reproduce the issue

## Getting Additional Help

### Community Support
- **GitHub Discussions**: [Ask questions and share tips](https://github.com/Dkmariolink/ez-streaming/discussions)
- **GitHub Issues**: [Report bugs and request features](https://github.com/Dkmariolink/ez-streaming/issues)

### Before Requesting Help
1. **Search Existing Issues**: Your problem might already be reported
2. **Try Basic Solutions**: Restart, update, check permissions
3. **Gather Information**: Have system details and error messages ready
4. **Test Minimal Setup**: Try with just one or two applications

### How to Report Bugs
1. **Use GitHub Issues**: Create a detailed issue report
2. **Include Steps**: Exactly how to reproduce the problem
3. **Attach Screenshots**: Visual information helps a lot
4. **Share Config**: Include relevant configuration details
5. **Be Responsive**: Reply to follow-up questions promptly

---

**Still Having Issues?** Don't hesitate to ask for help in our [GitHub Discussions](https://github.com/Dkmariolink/ez-streaming/discussions)!
