# System Requirements

Comprehensive guide to hardware and software requirements for running EZ Streaming effectively.

## Minimum System Requirements

### Operating System
- **Windows 10** (64-bit) or newer
- **Version 1903** (May 2019 Update) or later
- **Windows 11** fully supported

### Hardware Requirements

#### Processor (CPU)
- **Minimum:** Intel Core i3-4000 series or AMD FX-6000 series
- **Architecture:** 64-bit (x64) required
- **Cores:** 2+ cores recommended
- **Clock Speed:** 2.0 GHz base frequency minimum

#### Memory (RAM)
- **Minimum:** 4 GB RAM
- **Available:** At least 1 GB free RAM for EZ Streaming
- **System Load:** Additional RAM needed for launched applications

#### Storage
- **Free Space:** 100 MB for EZ Streaming executable
- **Configuration:** 10 MB for configuration and user data
- **Temporary:** 50 MB for temporary files during operation
- **Type:** HDD acceptable, SSD recommended for better performance

#### Graphics
- **Minimum:** DirectX 11 compatible graphics card
- **VRAM:** 512 MB minimum
- **Resolution:** 1024x768 minimum display resolution
- **DPI:** Supports high-DPI displays (100%-300% scaling)

### Software Dependencies
- **No additional software** required - completely portable
- **Visual C++ Redistributable** (included in Windows 10/11)
- **.NET Framework** not required

## Recommended System Requirements

### Operating System
- **Windows 11** (latest version)
- **Windows 10** version 21H2 or newer
- **Regular updates** installed for best compatibility

### Hardware Recommendations

#### Processor (CPU)
- **Recommended:** Intel Core i5-8000 series or AMD Ryzen 5 2000 series
- **Cores:** 4+ cores for smooth multitasking
- **Clock Speed:** 3.0 GHz base frequency
- **Features:** Hardware virtualization support (for compatibility)

#### Memory (RAM)
- **Recommended:** 8 GB RAM or more
- **Available:** 2+ GB free RAM
- **Usage:** Additional RAM scales with number of applications launched
- **Performance:** 16 GB+ for heavy streaming setups

#### Storage
- **Recommended:** SSD (Solid State Drive)
- **Free Space:** 500 MB+ for optimal performance
- **Speed:** Faster storage improves application launch times
- **Location:** Install on fastest available drive

#### Graphics
- **Recommended:** Dedicated graphics card
- **VRAM:** 2 GB+ for streaming applications
- **DirectX:** DirectX 12 support
- **Multi-Monitor:** Native support for multiple displays

## Performance Scaling by System Specs

### Budget Systems (4GB RAM, Dual-Core CPU)

#### Optimal Configuration
- **Profile Size:** 3-5 applications maximum
- **Launch Delays:** 8-12 seconds between applications
- **Application Types:** Lightweight applications preferred
- **Background Apps:** Minimize running background applications

#### Expected Performance
- **Launch Time:** 30-60 seconds for full profile
- **System Impact:** Noticeable system slowdown during launches
- **Stability:** Good with appropriate delays
- **Multitasking:** Limited during launch sequences

#### Recommended Applications
- **Streaming:** OBS Studio (basic scenes)
- **Communication:** Discord (voice only)
- **Music:** Spotify (lightweight mode)
- **Avoid:** Heavy games, multiple browsers, resource-intensive software

### Standard Systems (8GB RAM, Quad-Core CPU)

#### Optimal Configuration
- **Profile Size:** 5-8 applications
- **Launch Delays:** 5-7 seconds between applications
- **Application Types:** Mix of light and moderate applications
- **Background Apps:** Moderate background activity acceptable

#### Expected Performance
- **Launch Time:** 45-90 seconds for full profile
- **System Impact:** Minimal system slowdown
- **Stability:** Excellent with default settings
- **Multitasking:** Good performance during launches

#### Recommended Applications
- **Streaming:** OBS Studio with multiple scenes
- **Communication:** Discord with video
- **Games:** Most indie and competitive games
- **Creative:** Basic photo editing software
- **Browsers:** Multiple browser tabs

### High-Performance Systems (16GB+ RAM, 6+ Core CPU)

#### Optimal Configuration
- **Profile Size:** 8-15 applications
- **Launch Delays:** 3-5 seconds between applications
- **Application Types:** Any applications including heavy software
- **Background Apps:** Multiple background applications supported

#### Expected Performance
- **Launch Time:** 30-75 seconds for full profile
- **System Impact:** No noticeable slowdown
- **Stability:** Excellent even with aggressive timing
- **Multitasking:** Full system responsiveness maintained

#### Recommended Applications
- **Streaming:** Multiple streaming applications
- **Games:** AAA games with high settings
- **Creative:** Professional creative software (Photoshop, Premiere)
- **Development:** IDEs, compilers, virtual machines
- **Utilities:** System monitoring, RGB control, macro software

## Storage Requirements and Performance

### Storage Type Impact

#### Hard Disk Drive (HDD)
- **Launch Times:** 50-100% longer application startup
- **Recommended Delays:** 8-15 seconds between applications
- **System Impact:** Higher disk I/O causes system pauses
- **Configuration:** Store EZ Streaming on fastest available drive

#### Solid State Drive (SSD)
- **Launch Times:** Optimal application startup performance
- **Recommended Delays:** 3-8 seconds between applications
- **System Impact:** Minimal disk I/O bottlenecks
- **Configuration:** Ideal storage type for EZ Streaming

#### NVMe SSD
- **Launch Times:** Fastest possible application startup
- **Recommended Delays:** 2-5 seconds between applications
- **System Impact:** No disk I/O limitations
- **Configuration:** Best performance option

### Storage Space Requirements

#### EZ Streaming Executable
- **Executable Size:** ~15-20 MB
- **Required Space:** 100 MB (for updates and temporary files)
- **Installation:** No installation - just executable

#### Configuration Data
- **Basic Configuration:** 1-5 KB per profile
- **Large Configurations:** 50-100 KB for complex setups
- **Growth:** Scales with number of profiles and applications
- **Backup Space:** 10 MB recommended for configuration backups

#### Launched Applications
- **Variable Requirements:** Depends on applications in profiles
- **Large Games:** AAA games may require 50-100+ GB
- **Streaming Software:** OBS, Streamlabs typically 500 MB - 2 GB
- **Communication:** Discord, Skype typically 100-500 MB

## Network Requirements

### EZ Streaming Core Functionality
- **Network Access:** Not required for core functionality
- **Offline Operation:** Fully functional without internet connection
- **Local Configuration:** All data stored locally

### Application-Specific Network Requirements
- **Streaming Applications:** Require internet for streaming
- **Communication Apps:** Need network for voice/video/chat
- **Music Services:** Spotify, YouTube Music require internet
- **Game Launchers:** Steam, Epic Games need internet for updates

### Network Performance Impact
- **EZ Streaming:** No network usage
- **Launched Applications:** Network usage depends on applications
- **Bandwidth:** No additional bandwidth requirements from EZ Streaming

## System Compatibility

### Windows Version Compatibility

#### Windows 11 (Recommended)
- **Compatibility:** Full compatibility
- **Performance:** Optimal performance
- **Features:** All features supported
- **Updates:** Regular compatibility testing

#### Windows 10
- **Version 21H2:** Full compatibility, recommended
- **Version 21H1:** Full compatibility
- **Version 20H2:** Full compatibility
- **Version 2004:** Compatible with minor limitations
- **Version 1909:** Compatible, update recommended
- **Version 1903:** Minimum supported version

#### Older Windows Versions
- **Windows 8.1:** Not officially supported
- **Windows 7:** Not supported (lacks required frameworks)
- **Windows Server:** Not tested, may work

### Hardware Architecture
- **x64 (64-bit):** Fully supported and required
- **ARM64:** Not currently supported
- **x86 (32-bit):** Not supported

## Performance Factors

### CPU Performance Impact

#### Single-Core Performance
- **Application Launch:** Critical for individual application startup
- **UI Responsiveness:** Affects EZ Streaming interface smoothness
- **Recommendation:** Higher single-core performance preferred

#### Multi-Core Performance
- **Multitasking:** Important for running multiple applications simultaneously
- **Background Processing:** Enables better system responsiveness
- **Scaling:** More cores = better performance with large profiles

#### CPU Features
- **Virtualization:** Helpful for compatibility with some applications
- **Instruction Sets:** Modern instruction sets improve performance
- **Cache:** Larger CPU cache improves application switching performance

### Memory Performance Impact

#### Memory Amount
- **4 GB:** Suitable for basic profiles (3-5 light applications)
- **8 GB:** Good for standard profiles (5-8 mixed applications)
- **16 GB:** Excellent for large profiles (8-15 applications)
- **32 GB+:** Optimal for professional setups with heavy applications

#### Memory Speed
- **DDR3:** Adequate for basic functionality
- **DDR4:** Recommended for better performance
- **DDR5:** Optimal performance, future-ready

#### Memory Configuration
- **Single Channel:** Basic performance
- **Dual Channel:** Recommended configuration
- **Quad Channel:** Professional/workstation benefit

### Graphics Performance Impact

#### EZ Streaming UI
- **Requirements:** Minimal graphics requirements
- **Scaling:** Supports high-DPI displays
- **Performance:** Hardware acceleration for smooth UI

#### Launched Applications
- **Games:** Graphics performance critical for gaming applications
- **Streaming:** GPU encoding improves streaming performance
- **Creative:** Graphics cards accelerate creative applications

## System Optimization

### Windows Optimization

#### Performance Settings
```
Windows Settings → System → About → Advanced system settings
→ Performance Settings → Adjust for best performance
```

#### Power Settings
```
Control Panel → Power Options → High Performance
OR
Windows Settings → System → Power & sleep → Additional power settings
```

#### Background Apps
```
Windows Settings → Privacy → Background apps
→ Disable unnecessary background applications
```

### Hardware Optimization

#### RAM Optimization
- **Close Unnecessary Programs:** Free up RAM before launching profiles
- **Disable Startup Programs:** Reduce memory usage at boot
- **Memory Diagnostic:** Use Windows Memory Diagnostic for issues

#### Storage Optimization
- **Disk Cleanup:** Regular cleanup of temporary files
- **Defragmentation:** Defragment HDDs (not needed for SSDs)
- **Free Space:** Maintain 10-15% free space for optimal performance

#### CPU Optimization
- **Background Processes:** Minimize unnecessary background processes
- **Power Settings:** Use high-performance power profile
- **Thermal Management:** Ensure adequate cooling for sustained performance

## Troubleshooting Performance Issues

### Common Performance Problems

#### Slow Application Launches
**Symptoms:** Applications take much longer than expected to start  
**Causes:**
- Insufficient RAM
- Slow storage (HDD vs SSD)
- Too many background processes
- Antivirus scanning during launch

**Solutions:**
- Increase launch delays
- Upgrade to SSD storage
- Close unnecessary background applications
- Add EZ Streaming and applications to antivirus whitelist

#### System Freezing During Launch
**Symptoms:** System becomes unresponsive during application launches  
**Causes:**
- Insufficient system resources
- Too aggressive launch timing
- Hardware limitations

**Solutions:**
- Increase launch delays significantly
- Reduce number of applications in profile
- Close background applications
- Consider hardware upgrade

#### High Memory Usage
**Symptoms:** System runs out of memory with launched applications  
**Causes:**
- Insufficient RAM for application requirements
- Memory leaks in applications
- Too many applications launched simultaneously

**Solutions:**
- Upgrade system RAM
- Monitor application memory usage
- Create smaller, specialized profiles
- Close applications when not needed

### Performance Monitoring

#### Windows Performance Tools
- **Task Manager:** Basic resource monitoring
- **Resource Monitor:** Detailed resource analysis
- **Performance Monitor:** Advanced system metrics
- **Event Viewer:** System error and warning logs

#### Third-Party Tools
- **CPU-Z:** Hardware information and monitoring
- **HWiNFO64:** Comprehensive system monitoring
- **CrystalDiskInfo:** Storage health monitoring
- **MemTest86:** Memory testing and validation

## Future System Requirements

### Planned Features Impact

#### Cross-Platform Support
- **macOS:** Will require macOS 11+ (Big Sur)
- **Linux:** Ubuntu 20.04+ or equivalent distributions
- **Hardware:** Similar requirements across platforms

#### Advanced Features
- **Cloud Sync:** Minimal additional requirements
- **Performance Monitoring:** May require additional system permissions
- **Plugin System:** Requirements depend on plugins used

#### Resource Monitoring UI
- **Additional RAM:** 50-100 MB for monitoring interface
- **CPU Impact:** 1-2% CPU usage for real-time monitoring
- **Graphics:** Hardware acceleration for smooth charts/graphs

### Hardware Trends
- **Minimum Requirements:** May increase with new Windows versions
- **Recommended Specs:** Will scale with typical hardware improvements
- **New Technologies:** Support for emerging hardware technologies

## Specific Use Case Requirements

### Gaming Streamers
- **CPU:** 6+ cores for game + streaming + EZ Streaming
- **RAM:** 16+ GB for modern games and streaming software
- **Graphics:** Dedicated GPU with hardware encoding
- **Storage:** SSD for game installations and faster loading

### Creative Streamers
- **CPU:** High single-core and multi-core performance
- **RAM:** 16-32 GB for creative applications
- **Graphics:** Professional or high-end consumer GPU
- **Storage:** Fast SSD with high capacity

### Podcast/Talk Show Streamers
- **CPU:** 4+ cores sufficient for audio/video processing
- **RAM:** 8-16 GB adequate for communication and recording software
- **Graphics:** Basic graphics sufficient
- **Storage:** SSD recommended for recording storage

### Professional/Corporate Use
- **CPU:** Business-class processors with reliability features
- **RAM:** 16+ GB for professional applications
- **Graphics:** Professional graphics cards for certified drivers
- **Storage:** Enterprise SSD with reliability features

## Related Topics

- **[Installation Guide](Installation-Guide.md):** Step-by-step installation instructions
- **[Launch Delays and Timing](Launch-Delays-and-Timing.md):** Optimizing timing based on system performance
- **[Troubleshooting](Troubleshooting.md):** Solutions for performance-related issues
- **[Building from Source](Building-from-Source.md):** Development environment requirements
