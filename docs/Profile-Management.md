# Profile Management

Profiles are the heart of EZ Streaming's flexibility. Each profile represents a different streaming setup with its own applications, delays, and configurations.

## Understanding Profiles

### What is a Profile?
A profile contains:
- **List of applications** and their paths
- **Launch order** and timing settings
- **Default launch delay** for the profile
- **Custom delays** for individual applications
- **Profile name** and metadata

### Profile Use Cases
- **Gaming Stream Profile:** OBS + Discord + Spotify + Game Launcher
- **Art Stream Profile:** OBS + Digital Art Software + Reference Browser + Lo-fi Music
- **Podcast Profile:** Audacity + Skype + Note-taking App + Background Music
- **Work Profile:** Video Conferencing + Code Editor + Productivity Tools

## The Default Profile

### Special Properties
- **Cannot be deleted:** The Default profile is protected
- **Cannot be renamed:** Name is fixed as "Default"
- **Always exists:** Created automatically on first launch
- **Fallback profile:** Used when other profiles have issues

### Best Practices for Default Profile
- Use it for your most common streaming setup
- Keep it simple and reliable
- Don't experiment with untested applications here

## Creating New Profiles

### Method 1: From Scratch
1. Click the **profile dropdown** (next to the profile name)
2. Click **"New Profile"**
3. Enter a descriptive name (e.g., "Gaming Setup", "Art Stream")
4. Click **"OK"**
5. The new profile starts with two empty application rows

### Method 2: Duplicate Existing Profile
1. Select the profile you want to copy
2. Click the **profile dropdown**
3. Click **"Duplicate Profile"**
4. Enter a new name for the copy
5. Modify the copy as needed

### Naming Best Practices
- **Be descriptive:** "Gaming Stream" vs "Profile1"
- **Include context:** "Monday Podcast", "Weekend Art"
- **Keep it short:** Long names get truncated in the dropdown
- **Use conventions:** Consistent naming helps organization

## Managing Profiles

### Switching Between Profiles
1. Click the **profile dropdown**
2. Select the desired profile
3. The interface updates to show that profile's applications
4. **Note:** Unsaved changes prompt a warning

### Renaming Profiles
1. Click the **profile dropdown**
2. Click **"Rename Profile"**
3. Enter the new name
4. Click **"OK"**
5. **Limitation:** Cannot rename the Default profile

### Deleting Profiles
1. Click the **profile dropdown**
2. Click **"Delete Profile"**
3. Confirm the deletion
4. **Warning:** This action cannot be undone
5. **Protection:** Cannot delete the Default profile

## Profile Configuration

### Default Launch Delay
- **Purpose:** Time to wait between launching each application
- **Location:** Top section of the interface
- **Range:** 1-30 seconds
- **Recommendation:** Start with 5 seconds, adjust based on system performance

### Application Management Within Profiles
Each profile independently manages:
- **Application list:** Different apps for different purposes
- **Launch order:** Optimized for each streaming scenario
- **Custom delays:** Per-app timing overrides
- **Application status:** Which apps are currently running

## Advanced Profile Strategies

### Profile Organization Patterns

#### By Content Type
- **Gaming Profile:** OBS + Discord + Spotify + Steam
- **Music Profile:** OBS + DJ Software + Chat Client + Visualizers  
- **Talk Show Profile:** OBS + Video Chat + Notes + Background Music

#### By Schedule
- **Weekday Stream:** Minimal setup for quick streams
- **Weekend Stream:** Full production setup with all tools
- **Special Events:** Enhanced setup with additional overlays/tools

#### By Audience
- **Twitch Profile:** Twitch-specific tools and chat clients
- **YouTube Profile:** YouTube-focused streaming setup
- **Multi-Platform:** Tools for simultaneous streaming

### Profile Hierarchy Strategy

#### Master Template Profile
Create a "Template" profile with:
- Common applications (OBS, Discord)
- Standard delay settings
- Basic configuration
- **Don't use for streaming** - only for duplication

#### Specialized Profiles
Duplicate the template and customize:
- Add game-specific applications
- Adjust delays for content type
- Include specialized tools

### Performance-Based Profiles

#### Light Profile (4GB RAM systems)
- **Minimal applications:** Only essentials
- **Longer delays:** 8-10 seconds between launches
- **Fewer background apps:** Skip non-essential tools

#### Full Profile (8GB+ RAM systems)
- **Complete toolkit:** All desired applications
- **Standard delays:** 5 seconds default
- **Background utilities:** Music, chat bots, overlays

## Profile Data Management

### Where Profiles Are Stored
Profiles are saved in:
```
C:\Users\[Username]\AppData\Roaming\EZStreaming\ez_streaming_config.json
```

### Configuration Structure
```json
{
  "profiles": [
    {
      "name": "Gaming Setup",
      "launch_delay": 5,
      "programs": [...]
    }
  ],
  "current_profile_name": "Gaming Setup"
}
```

### Backup and Restore

#### Creating Backups
1. **Manual Backup:**
   - Copy the `ez_streaming_config.json` file
   - Store it in a safe location
   - Name it with the date (e.g., `config_backup_2025-06-12.json`)

2. **Automatic Backup:**
   - EZ Streaming creates backups automatically when switching profiles
   - Backup frequency: Before any major configuration change

#### Restoring Profiles
1. Close EZ Streaming
2. Replace the current config file with your backup
3. Restart EZ Streaming
4. Your profiles will be restored

### Sharing Profiles

#### Export Profile (Manual Method)
1. Locate your config file
2. Copy the JSON section for the specific profile
3. Share the JSON data with other users
4. **Note:** Built-in export/import is planned for future versions

#### Profile Compatibility
- **Paths:** Will need adjustment on different systems
- **Applications:** Must be installed on the target system
- **Settings:** Delays and preferences transfer directly

## Troubleshooting Profile Issues

### Profile Won't Load
**Symptoms:** Error message when selecting a profile  
**Solutions:**
1. Check if applications in the profile still exist
2. Verify file paths haven't changed
3. Try duplicating a working profile
4. Restore from backup if necessary

### Applications Missing After Profile Switch
**Symptoms:** Profile loads but shows empty rows  
**Solutions:**
1. Check if config file is corrupted
2. Try restarting EZ Streaming
3. Manually re-add applications
4. Restore from backup

### Profile Dropdown Empty
**Symptoms:** No profiles show in the dropdown  
**Solutions:**
1. Restart EZ Streaming (recreates Default profile)
2. Check config file permissions
3. Clear AppData folder and restart (will reset all profiles)

### Can't Create New Profile
**Symptoms:** "New Profile" option disabled or errors  
**Solutions:**
1. Ensure current profile is saved
2. Try switching to Default profile first
3. Check disk space and permissions
4. Restart the application

## Profile Best Practices

### Organization
- **Limit profile count:** 5-8 profiles maximum for easy management
- **Regular cleanup:** Delete unused profiles periodically
- **Consistent naming:** Use clear, descriptive names

### Configuration
- **Test new profiles:** Run through the launch sequence manually first
- **Document complex setups:** Keep notes about special configurations
- **Regular maintenance:** Update paths when applications get updated

### Performance
- **Monitor system resources:** Adjust delays based on actual performance
- **Profile-specific optimization:** Different delays for different use cases
- **Gradual complexity:** Start simple, add complexity over time

### Backup Strategy
- **Weekly backups:** Export configuration weekly
- **Before major changes:** Always backup before adding many new applications
- **Multiple versions:** Keep several backup versions
- **Test restores:** Periodically verify backups work

## Future Profile Features

Planned enhancements for profile management:

### Near-term (Next Releases)
- **Profile Import/Export:** Built-in sharing functionality
- **Profile descriptions:** Add notes and descriptions to profiles
- **Profile categories:** Organize profiles into groups

### Long-term (Future Versions)
- **Profile scheduling:** Automatic profile switching based on time/day
- **Cloud sync:** Synchronize profiles across multiple computers
- **Profile templates:** Community-shared profile templates
- **Conditional launching:** Launch different apps based on system state

## Related Topics

- **[Adding Applications](Adding-Applications.md):** Learn how to add and configure applications within profiles
- **[Launch Delays and Timing](Launch-Delays-and-Timing.md):** Optimize timing settings for your profiles
- **[Process Management](Process-Management.md):** Understand how EZ Streaming tracks applications across profiles
