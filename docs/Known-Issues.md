# Known Issues

Current known issues in EZ Streaming, their workarounds, and planned fixes.

## Current Known Issues

### High Priority Issues

#### Issue #1: Windows SmartScreen False Positive
**Status:** Known Issue  
**Affects:** All Windows users  
**Severity:** Medium (User Experience)

**Description:**
Windows SmartScreen shows a security warning when running EZ Streaming for the first time, stating "Windows protected your PC" with an "Unrecognized app" message.

**Root Cause:**
EZ Streaming executable is not code-signed, which triggers Windows SmartScreen protection for unsigned applications.

**Workaround:**
1. Click "More info" in the SmartScreen dialog
2. Click "Run anyway" to proceed
3. Windows will remember this choice for future runs

**Planned Fix:**
- Code signing certificate acquisition planned for v1.3.0
- Will eliminate the security warning completely

**Impact:** Low (one-time inconvenience)

#### Issue #2: Antivirus False Positives
**Status:** Known Issue  
**Affects:** Users with certain antivirus software  
**Severity:** Medium (User Experience)

**Description:**
Some antivirus programs (notably Avast, AVG, Windows Defender occasionally) flag EZ Streaming as potentially unwanted software (PUP) or malware.

**Root Cause:**
PyInstaller-built executables often trigger heuristic detection in antivirus software due to their packing method.

**Affected Antivirus:**
- Avast (most common)
- AVG  
- Bitdefender (occasional)
- Windows Defender (rare)

**Workaround:**
1. Add EZ Streaming to antivirus whitelist/exclusions
2. Download only from official GitHub releases
3. Verify file integrity using checksums (when available)

**Planned Fix:**
- Code signing will reduce false positives significantly
- Working with antivirus vendors to whitelist the application
- Exploring alternative packaging methods

**Impact:** Medium (prevents some users from running the application)

### Medium Priority Issues

#### Issue #3: Process Detection Delays
**Status:** Under Investigation  
**Affects:** Systems with many running processes  
**Severity:** Low (Performance)

**Description:**
On systems with 100+ running processes, EZ Streaming may take 2-3 seconds to detect when applications are launched externally or to update button states.

**Root Cause:**
Process scanning algorithm needs optimization for systems with high process counts.

**Workaround:**
- Close unnecessary background applications
- Use "Launch All" instead of individual launches for better experience
- Process detection is eventually consistent (will update within 5 seconds)

**Planned Fix:**
- Optimize process scanning algorithm in v1.3.0
- Implement incremental process detection
- Add process monitoring caching

**Impact:** Low (slight delay in UI updates)

#### Issue #4: Path Updates After Application Updates
**Status:** Known Limitation  
**Affects:** Users whose applications update frequently  
**Severity:** Low (Maintenance)

**Description:**
When applications like Discord, Spotify, or browsers update, their executable paths may change, causing EZ Streaming to show invalid path errors.

**Root Cause:**
Some applications change their executable location during updates, and EZ Streaming stores absolute paths.

**Common Affected Applications:**
- Discord (updates frequently)
- Spotify (occasional path changes)
- Chrome/Edge (with automatic updates)
- Steam games (after updates)

**Workaround:**
1. Use "Browse" to relocate the updated executable
2. Use "Locate App by Name" to re-discover the application
3. Consider using more stable paths when available

**Planned Fix:**
- Implement path validation and auto-correction in v1.3.0
- Add update detection and path recovery
- Provide notifications for path changes

**Impact:** Low (requires occasional maintenance)

#### Issue #5: Launch Delay UI Inconsistencies
**Status:** UI Polish Needed  
**Affects:** Users configuring custom delays  
**Severity:** Low (User Experience)

**Description:**
The launch delay UI sometimes shows inconsistent states:
- Delay controls may briefly flicker during profile switches
- First application delay controls should be disabled but occasionally remain enabled
- Custom delay checkbox state may not reflect actual configuration immediately

**Root Cause:**
UI state synchronization timing issues during profile loading and switching.

**Workaround:**
- Settings are correctly saved despite UI display issues
- Switching profiles or restarting EZ Streaming resolves display problems
- Actual functionality is not affected

**Planned Fix:**
- Improve UI state synchronization in v1.2.1
- Add proper loading states during profile switches
- Implement more robust UI state management

**Impact:** Very Low (cosmetic issue only)

### Low Priority Issues

#### Issue #6: High DPI Scaling Minor Issues
**Status:** Minor Polish Needed  
**Affects:** Users with display scaling >150%  
**Severity:** Very Low (Visual)

**Description:**
On high-DPI displays with scaling above 150%, some UI elements may appear slightly misaligned:
- Column headers may have minor spacing issues
- Tooltips may appear slightly offset
- Button text may be positioned sub-optimally

**Root Cause:**
Qt's high-DPI handling, while generally good, has minor inconsistencies with complex layouts.

**Workaround:**
- Functionality is not affected
- Most scaling levels (100-150%) work perfectly
- Issues are purely cosmetic

**Planned Fix:**
- Fine-tune high-DPI layouts in future UI updates
- Test on more high-DPI configurations
- Implement manual DPI override option

**Impact:** Very Low (minor visual imperfections)

#### Issue #7: Drag-and-Drop Visual Feedback
**Status:** Enhancement Needed  
**Affects:** Users reordering applications  
**Severity:** Very Low (User Experience)

**Description:**
When dragging applications to reorder them, the visual feedback could be improved:
- Drop zones not clearly indicated
- Drag preview could be more polished
- Drop animation is basic

**Root Cause:**
Basic drag-and-drop implementation prioritizes functionality over visual polish.

**Workaround:**
- Drag-and-drop functionality works correctly
- Visual feedback is adequate for most users
- Focus on drag handle (≡) for better control

**Planned Fix:**
- Enhance drag-and-drop visual feedback in future UI updates
- Add better drop zone indicators
- Improve drag preview appearance

**Impact:** Very Low (minor user experience improvement)

## Resolved Issues (Recent Fixes)

### Recently Fixed in v1.2.0

#### ✅ Profile Deletion Data Corruption
**Status:** Fixed in v1.2.0  
**Issue:** Deleting profiles could occasionally corrupt configuration data
**Solution:** Implemented proper profile deletion with data validation
**Impact:** Configuration stability significantly improved

#### ✅ Process Detection Case Sensitivity
**Status:** Fixed in v1.2.0  
**Issue:** Process detection failed on case-mismatched paths
**Solution:** Implemented case-insensitive path matching using `os.path.normcase`
**Impact:** Much more reliable process detection

#### ✅ Launch Button State Inconsistencies
**Status:** Fixed in v1.2.0  
**Issue:** Launch buttons didn't always reflect actual application status
**Solution:** Improved process detection and UI state synchronization
**Impact:** More accurate and reliable UI status indicators

#### ✅ Column Header Alignment
**Status:** Fixed in v1.2.0  
**Issue:** Column headers didn't align properly with row content
**Solution:** Redesigned header layout with proper spacers and alignment
**Impact:** Much cleaner and more professional appearance

### Recently Fixed in v1.1.0

#### ✅ Default Profile Renaming Protection
**Status:** Fixed in v1.1.0  
**Issue:** Users could rename or delete the Default profile, causing crashes
**Solution:** Added protection logic for the Default profile
**Impact:** Eliminated crashes related to missing Default profile

#### ✅ Memory Leak in Launch Sequence
**Status:** Fixed in v1.1.0  
**Issue:** QTimer objects weren't properly cleaned up after launch sequences
**Solution:** Implemented proper timer cleanup and memory management
**Impact:** Reduced memory usage during extended use

## Platform-Specific Issues

### Windows-Specific Issues

#### Windows 11 Context Menu Integration
**Status:** Future Enhancement  
**Affects:** Windows 11 users  
**Severity:** Very Low (Feature Request)

**Description:**
EZ Streaming doesn't integrate with Windows 11's new context menu system for "Add to EZ Streaming" functionality.

**Current Status:** Not implemented
**Planned:** Possible future feature based on user demand

#### Windows Startup Integration
**Status:** Not Yet Implemented  
**Affects:** Users wanting auto-startup  
**Severity:** Low (Feature Request)

**Description:**
No built-in option to start EZ Streaming automatically with Windows.

**Workaround:**
- Manually add to Windows Startup folder
- Use Task Scheduler for advanced startup options

**Planned Fix:** Built-in Windows startup integration in v1.3.0

### Cross-Platform Limitations

#### macOS Support
**Status:** Not Available  
**Affects:** macOS users  
**Severity:** Medium (Platform Limitation)

**Description:**
EZ Streaming currently only supports Windows. macOS support is requested by users.

**Current Status:** In planning phase
**Planned:** macOS port in roadmap for 2025-2026

#### Linux Support
**Status:** Not Available  
**Affects:** Linux users  
**Severity:** Low (Platform Limitation)

**Description:**
Linux support requested by some users, particularly those using Linux for streaming.

**Current Status:** Under consideration
**Planned:** Possible future development based on demand

## Workarounds and Best Practices

### General Workarounds

#### For Antivirus Issues
1. **Download from official sources only** - GitHub releases page
2. **Add to whitelist immediately** after download
3. **Verify checksums** when available
4. **Report false positives** to antivirus vendors

#### For Performance Issues
1. **Close background applications** before launching profiles
2. **Use SSD storage** for better performance
3. **Increase launch delays** on slower systems
4. **Monitor system resources** during launches

#### For Path Issues
1. **Use "Locate App by Name"** instead of manual browsing when possible
2. **Keep applications updated** but be aware paths may change
3. **Create backup profiles** before major application updates
4. **Document custom paths** for important applications

### Best Practices to Avoid Issues

#### Profile Management
- **Backup configuration files** regularly
- **Test new profiles** thoroughly before relying on them
- **Keep profile names descriptive** and organized
- **Don't overload profiles** with too many applications

#### Application Configuration
- **Verify paths** after adding new applications
- **Test individual launches** before using "Launch All"
- **Use appropriate delays** for your system specifications
- **Monitor for application updates** that might change paths

#### System Maintenance
- **Keep Windows updated** for best compatibility
- **Maintain adequate free disk space**
- **Monitor system resources** during streaming sessions
- **Restart EZ Streaming occasionally** to refresh process detection

## Reporting New Issues

### Before Reporting
1. **Check this list** to see if the issue is already known
2. **Search GitHub Issues** for existing reports
3. **Try workarounds** mentioned in this document
4. **Update to the latest version** of EZ Streaming

### Information to Include
When reporting a new issue, please include:

#### System Information
- Windows version (10/11, build number)
- System specifications (CPU, RAM, storage type)
- EZ Streaming version
- Antivirus software (if relevant)

#### Issue Details
- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Error messages** (exact text)

#### Configuration Information
- Number of profiles and applications
- Types of applications being launched
- Custom settings or unusual configurations

### Where to Report
- **GitHub Issues:** https://github.com/Dkmariolink/ez-streaming/issues
- **Email:** For sensitive issues not suitable for public discussion
- **GitHub Discussions:** For questions or uncertain issues

## Issue Resolution Timeline

### Priority Levels

#### Critical (Security, Data Loss)
- **Response Time:** Within 24 hours
- **Fix Timeline:** Emergency release within 1 week
- **Examples:** Data corruption, security vulnerabilities

#### High (Major Functionality)
- **Response Time:** Within 48 hours  
- **Fix Timeline:** Next minor release (2-4 weeks)
- **Examples:** Application won't start, major features broken

#### Medium (User Experience)
- **Response Time:** Within 1 week
- **Fix Timeline:** Next minor or major release (1-3 months)
- **Examples:** UI issues, performance problems

#### Low (Polish, Enhancement)
- **Response Time:** When development time permits
- **Fix Timeline:** Future releases based on priority
- **Examples:** Visual improvements, convenience features

### Development Cycle
- **Patch Releases (1.2.x):** Critical and high-priority fixes
- **Minor Releases (1.x.0):** Medium-priority fixes and small features
- **Major Releases (2.0.0):** Low-priority fixes and significant new features

## Contributing to Issue Resolution

### How Users Can Help

#### Testing
- **Test pre-release versions** when available
- **Verify bug fixes** in new releases
- **Report regression issues** if fixes cause new problems

#### Documentation
- **Contribute to workarounds** when you find solutions
- **Improve issue descriptions** with additional details
- **Help other users** in GitHub Discussions

#### Development
- **Submit pull requests** for fixes you've implemented
- **Contribute to testing infrastructure**
- **Help with code review** if you're experienced

### Community Support
The EZ Streaming community is encouraged to:
- **Help each other** with workarounds and solutions
- **Share experiences** with different system configurations
- **Contribute to documentation** improvements
- **Report when issues are resolved** in their environment

---

**Last Updated:** June 12, 2025  
**Version:** Covers EZ Streaming v1.2.0 and earlier

For the most current information, check the [GitHub Issues](https://github.com/Dkmariolink/ez-streaming/issues) page.
