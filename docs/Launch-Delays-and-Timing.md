# Launch Delays and Timing

Master the timing system in EZ Streaming to optimize your application launches and prevent system overload.

## Understanding Launch Delays

### Why Delays Matter

Launch delays serve several critical purposes:

#### System Performance
- **Prevents Overload:** Launching multiple applications simultaneously can overwhelm your system
- **Resource Management:** Allows each application to fully initialize before starting the next
- **Stability:** Reduces crashes and freezing during the launch sequence
- **Responsiveness:** Keeps your system responsive during the startup process

#### Application Dependencies
- **Sequential Dependencies:** Some applications work better when others are already running
- **Resource Competition:** Heavy applications need exclusive access to system resources during startup
- **Initialization Time:** Complex applications need time to fully load before others can use them

### Types of Delays in EZ Streaming

#### Profile Default Delay
- **Scope:** Applies to all applications in the profile
- **Location:** Top section of the main interface  
- **Purpose:** Sets the baseline timing for the entire launch sequence
- **Range:** 1-30 seconds

#### Per-Application Custom Delays
- **Scope:** Overrides the default delay for specific applications
- **Control:** Individual checkbox and spinner for each application
- **Purpose:** Fine-tune timing for applications with special requirements
- **Flexibility:** Can be longer or shorter than the profile default

#### First Application Exception
- **Special Rule:** The first application in a profile has no delay
- **Rationale:** No need to wait before starting the first application
- **UI Behavior:** Delay controls are disabled for the first application

## Configuring Profile Default Delays

### Setting the Default Delay
1. Locate the **"Default Launch Delay"** control at the top of the interface
2. Use the spinner or type a value (1-30 seconds)
3. This delay applies between each application launch
4. The setting is saved automatically with the profile

### Recommended Default Delays by System

#### High-Performance Systems (16GB+ RAM, SSD, Modern CPU)
- **Recommended:** 3-5 seconds
- **Rationale:** Fast systems can handle quicker transitions
- **Use Case:** Streamers who want to get online quickly

#### Standard Systems (8-16GB RAM, Mixed Storage)
- **Recommended:** 5-7 seconds  
- **Rationale:** Balanced approach for most users
- **Use Case:** Most streaming setups

#### Budget Systems (4-8GB RAM, HDD, Older CPU)
- **Recommended:** 8-12 seconds
- **Rationale:** Longer delays prevent system strain
- **Use Case:** Older hardware or resource-constrained systems

#### Gaming Systems Under Load
- **Recommended:** 10-15 seconds
- **Rationale:** When running demanding games, other applications need more time
- **Use Case:** Gaming streams with resource-intensive games

## Per-Application Custom Delays

### When to Use Custom Delays

#### Heavy Applications
Applications that should have **longer** custom delays:
- **OBS Studio:** 8-12 seconds (complex initialization)
- **Games:** 10-15 seconds (especially large games)
- **Video Editing Software:** 10-15 seconds (Adobe Premiere, DaVinci Resolve)
- **3D Software:** 12-20 seconds (Blender, Unity, Unreal Engine)
- **Virtual Machines:** 15-30 seconds (depending on VM size)

#### Light Applications  
Applications that can have **shorter** custom delays:
- **Notepad/Text Editors:** 1-2 seconds
- **Calculator:** 1 second
- **Small Utilities:** 1-3 seconds
- **Web Browsers (if already running):** 2-3 seconds

#### Instant Applications
Applications that should have **minimal** delays:
- **Already Running Apps:** 1 second (just for UI feedback)
- **System Utilities:** 1-2 seconds
- **Command Line Tools:** 1 second

### Configuring Custom Delays

#### Setting a Custom Delay
1. Find the application row you want to customize
2. Check the **"Custom delay"** checkbox
3. The spinner becomes enabled
4. Set your desired delay value (1-30 seconds)
5. The custom value overrides the profile default for that application

#### Removing Custom Delays
1. Uncheck the **"Custom delay"** checkbox
2. The application will revert to using the profile default delay
3. The custom value is cleared

### Custom Delay Strategies

#### Progressive Loading Strategy
Start with lighter applications, progress to heavier:
1. **Music Player:** 2 seconds (quick background ambiance)
2. **Chat Application:** 3 seconds (lightweight communication)
3. **Browser:** 5 seconds (for stream dashboard)
4. **OBS Studio:** 10 seconds (heavy streaming software)
5. **Game:** 15 seconds (most resource-intensive)

#### Dependency-Based Strategy
Launch applications in order of dependencies:
1. **Base Applications First:** Discord, Spotify (2-3 seconds each)
2. **Core Tools:** OBS Studio (8-10 seconds)
3. **Content Applications:** Games, creative software (10-15 seconds)
4. **Enhancement Tools:** Stream overlays, bots (3-5 seconds)

## Advanced Timing Configurations

### System-Specific Optimization

#### SSD vs HDD Storage
- **SSD Systems:** Can use 20-30% shorter delays
- **HDD Systems:** Need 50-100% longer delays for disk-intensive applications
- **Mixed Storage:** Adjust delays based on where each application is installed

#### RAM Considerations
- **32GB+ RAM:** Aggressive timing (3-5 second defaults)
- **16GB RAM:** Standard timing (5-7 second defaults)  
- **8GB RAM:** Conservative timing (7-10 second defaults)
- **4GB RAM:** Very conservative timing (10-15 second defaults)

#### CPU Performance Impact
- **High-End CPUs (8+ cores):** Can handle concurrent initialization better
- **Mid-Range CPUs (4-6 cores):** Need moderate delays for stability
- **Budget CPUs (2-4 cores):** Require longer delays to prevent bottlenecks

### Application-Specific Timing Guides

#### Streaming Software
- **OBS Studio:** 8-12 seconds
  - Loads plugins, initializes audio/video devices
  - Heavy GPU initialization
  - Scene and source loading

- **Streamlabs:** 10-15 seconds
  - Additional overlay system
  - Cloud integration initialization
  - Multiple component loading

- **XSplit:** 8-12 seconds
  - Similar to OBS but different optimization
  - Plugin system initialization

#### Games by Category
- **Indie Games:** 5-8 seconds
- **AAA Games:** 15-25 seconds
- **Competitive Games (CS:GO, Valorant):** 10-15 seconds
- **MMORPGs:** 20-30 seconds
- **Simulation Games:** 15-25 seconds

#### Communication Software
- **Discord:** 3-5 seconds
  - Quick startup but needs time for server connections
- **TeamSpeak:** 2-4 seconds
  - Lightweight client
- **Skype:** 5-8 seconds
  - Heavier client with more features

#### Creative Software
- **Photoshop:** 15-20 seconds
- **After Effects:** 20-30 seconds
- **Blender:** 10-15 seconds
- **Unity/Unreal:** 15-25 seconds

## Delay Warning System

### Low Delay Warnings

EZ Streaming includes a warning system for potentially problematic delays:

#### When Warnings Appear
- **Very Low Delays:** Less than 2 seconds for most applications
- **System-Dependent:** Based on detected system capabilities
- **Application-Specific:** Some applications always warn below certain thresholds

#### Warning Dialog Options
- **Proceed Anyway:** Continue with the low delay setting
- **Increase Delay:** Automatically set to recommended minimum
- **Don't Show Again:** Disable warnings for this profile
- **Learn More:** Get information about why delays matter

### Bypassing Warnings

#### When It's Safe to Ignore Warnings
- **High-Performance Systems:** Modern hardware can handle shorter delays
- **Light Applications:** Simple utilities don't need long delays
- **Experienced Users:** You understand the trade-offs
- **Testing Scenarios:** Experimenting with optimization

#### When to Heed Warnings
- **System Instability:** If you experience crashes or freezing
- **First-Time Setup:** When you're new to the application combinations
- **Complex Profiles:** Profiles with many or heavy applications
- **Production Streams:** When reliability is critical

## Timing Optimization Strategies

### Performance Testing

#### Baseline Testing
1. **Start Conservative:** Use longer delays initially
2. **Monitor Performance:** Watch system resources during launches
3. **Gradual Reduction:** Slowly decrease delays while monitoring stability
4. **Find Sweet Spot:** Balance speed with reliability

#### Testing Methodology
1. **Consistent Environment:** Test with the same system load
2. **Multiple Runs:** Launch sequence several times to ensure consistency
3. **Resource Monitoring:** Use Task Manager or other tools to watch system load
4. **Stability Assessment:** Look for crashes, hangs, or performance degradation

### Profile-Specific Optimization

#### Gaming Stream Profile
- **Pre-Game Apps:** Short delays (2-3 seconds) for Discord, music
- **Game Launch:** Long delay (15-20 seconds) before launching the game
- **Post-Game Apps:** Medium delays (5-8 seconds) for overlays, alerts

#### Creative Stream Profile  
- **Reference Materials:** Short delays (2-3 seconds) for browsers, note apps
- **Creative Software:** Long delays (15-25 seconds) for Photoshop, Blender
- **Streaming Tools:** Medium delays (8-10 seconds) for OBS with scenes

#### Podcast Profile
- **Communication First:** Medium delays (3-5 seconds) for Skype, Discord
- **Recording Software:** Long delay (10-15 seconds) for Audacity, Adobe Audition
- **Background Apps:** Short delays (2-3 seconds) for notes, music

## Troubleshooting Timing Issues

### Common Problems and Solutions

#### System Freezes During Launch
**Problem:** System becomes unresponsive during application launches  
**Solutions:**
1. **Increase all delays** by 50-100%
2. **Reduce number of applications** in the profile
3. **Check system resources** - may need hardware upgrade
4. **Launch applications individually** to identify problem apps

#### Applications Crash During Startup
**Problem:** Some applications fail to start properly  
**Solutions:**
1. **Increase custom delays** for problematic applications
2. **Check launch order** - some apps may need others to be ready first
3. **Test manual launches** to verify applications work independently
4. **Review system resources** during launch sequence

#### Inconsistent Launch Behavior
**Problem:** Sometimes launches work, sometimes they don't  
**Solutions:**
1. **Increase delays** to account for system variability
2. **Close unnecessary background apps** before launching
3. **Monitor system load** - high background activity affects timing
4. **Use longer delays** during high system activity periods

#### Applications Launch But Don't Function Properly
**Problem:** Apps start but have issues or missing features  
**Solutions:**
1. **Increase delays** to allow full initialization
2. **Check dependencies** - some applications need others to be fully loaded
3. **Verify launch order** - critical applications should start first
4. **Test with manual launches** to establish baseline behavior

### Advanced Troubleshooting

#### Resource Monitoring During Launch
Use Windows Task Manager or Resource Monitor to watch:
- **CPU Usage:** Spikes indicate heavy initialization
- **Memory Usage:** Rapid allocation shows applications loading
- **Disk Activity:** High disk I/O suggests need for longer delays
- **Network Activity:** Applications connecting to services

#### System Log Analysis
Check Windows Event Viewer for:
- **Application Errors:** Failed launches or crashes
- **System Warnings:** Resource constraints or conflicts
- **Service Issues:** Background services affecting application startup

## Best Practices for Launch Timing

### General Guidelines

#### Conservative Approach
- **Start with longer delays** and optimize down
- **Better to wait a few extra seconds** than deal with crashes
- **Test thoroughly** before using in production streams
- **Document what works** for future reference

#### Performance vs Reliability
- **Production Streams:** Prioritize reliability with longer delays
- **Testing/Practice:** Experiment with shorter delays
- **System Under Load:** Use longer delays when running games or heavy software
- **Dedicated Streaming PC:** Can use more aggressive timing

### Maintenance and Updates

#### Regular Review
- **Monthly Assessment:** Review and optimize timing settings
- **After System Changes:** Update delays when upgrading hardware or software
- **Application Updates:** Some updates change startup behavior
- **Performance Monitoring:** Track whether timing is still optimal

#### Documentation
- **Profile Notes:** Document special timing requirements
- **System Configuration:** Record hardware specs and optimal settings
- **Problem Tracking:** Keep notes about issues and their solutions
- **Version Tracking:** Note which application versions work with which timings

## Future Timing Features

### Planned Enhancements
- **Adaptive Delays:** Automatic delay adjustment based on system performance
- **Smart Dependencies:** Automatic dependency detection and ordering
- **Performance Profiling:** Built-in monitoring and optimization suggestions
- **Conditional Timing:** Different delays based on system state or time of day

### Advanced Features Under Consideration
- **Machine Learning:** Learning optimal delays based on usage patterns
- **System Integration:** Deeper integration with Windows performance monitoring
- **Application Awareness:** Communication with applications to detect readiness
- **Cloud Optimization:** Shared timing configurations for similar systems

## Related Topics

- **[Profile Management](Profile-Management.md):** Organize different timing configurations
- **[Adding Applications](Adding-Applications.md):** Choose applications that work well together
- **[Process Management](Process-Management.md):** Understand how applications are tracked
- **[System Requirements](System-Requirements.md):** Hardware considerations for optimal timing
- **[Troubleshooting](Troubleshooting.md):** Solutions for timing-related issues
