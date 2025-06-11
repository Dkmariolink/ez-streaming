# EZ Streaming: Development Roadmap

## Phase 1: Immediate Fixes (Completed)

### High Priority
1. **Default Profile Protection (Completed)**
   - Renaming of default profile disabled.
   - Data corruption bug on profile deletion fixed.
   - *(Note: "(default)" suffix removal reverted based on testing/preference).*

2. **UI Consistency (Completed)**
   - Fixed styling inconsistencies for first-row widgets (buttons, inputs, labels, drag handle) on initial load.
   - Implemented consistent row selection highlighting when clicking input fields.
   - Standardized tooltip appearance across all controls.

3. **UX Enhancements (Completed)**
   - Added warning dialog on window close if profile has unsaved changes.

4. **Final Testing**
   - Thorough testing of all profile operations
   - Verify application behavior with different user scenarios
   - Test with various window sizes and display resolutions
   - Ensure proper behavior on first-time launch

## Phase 2: User Experience Enhancement (1-2 Months)

### Profile Management Improvements
1. **Profile Import/Export**
   - Add ability to export profiles as JSON files
   - Implement profile import functionality
   - Support sharing profiles between installations
   - Add "Copy App from Another Profile" feature

2. **Advanced Profile Features**
   - Add profile descriptions
   - Implement profile categories or tags
   - Add profile activation scheduling

### Program Management Improvements
1. **Enhanced Program Control**
   - Add "Locate App by Name" button below the "Browse" button (with error handling)
   - Implement launch order control
   - Add launch delay options between applications (Completed - profile default, per-app override, low-delay warning, first-app disabled, current-app path check, non-blocking timer)
   - Support command-line arguments for launched applications

2. **Automation Features**
   - Auto-save functionality to prevent data loss
   - Auto-launch option on Windows startup
   - Scheduled profile activation

### UI/UX Enhancements
1. **Integrated Settings Menu**
   - Add non-popup settings panel for theme, accessibility (color blind, high contrast), etc.
2. **Onboarding & Guidance**
   - Implement guided tutorial system for first-time users.
   - Add "New Streamer Starting Guide" section (links to common apps, import help).

## Phase 3: Advanced Integration (3-6 Months)

### System Integration
1. **System Tray Function**
   - Minimize to system tray
   - Quick-access context menu from system tray
   - Background operation mode (detects when streaming app is open, launches all apps of a profile (not already running) specified by the user in the UI in settings if they choose so.)

2. **Windows Integration**
   - Windows startup integration
   - File association for profile files
   - Windows notification integration
   - Online Update Check & Patching System (with Changelogs)

### Streaming Platform Integration
1. **Stream Status Monitoring**
   - Add "Auto-Detect Popular Streaming Apps" button/feature (OBS, Discord, etc.)
   - Twitch/YouTube status checking
   - Viewer count display
   - Stream uptime monitoring

2. **Chat Integration**
   - Basic chat monitoring capabilities
   - Stream event notifications
   - Integration with popular chat bots

## Phase 4: Extended Functionality (6+ Months)

### Resource Management
1. **Performance Monitoring**
   - CPU/RAM usage tracking for running applications
   - System resource monitoring
   - Automatic optimization recommendations
   - "Stream Health/Impact Rating" analysis

2. **Advanced Application Management**
   - Dependency-based launching (start A before B)
   - Conditional launching based on system state
   - Application health monitoring

### Community Features
1. **Profile Sharing Platform**
   - Community profile repository with search/upload functionality.
   - Allow user descriptions for profiles.
   - Implement rating system.
   - Basic moderation/word filtering.
   - Featured profiles for popular streaming types.

2. **Platform Expansion**
   - macOS version development
   - Linux version investigation
   - Mobile companion app exploration

## Maintenance & Ongoing Work

### Documentation
1. **User Documentation**
   - Comprehensive user guide
   - Video tutorials
   - FAQ and troubleshooting guide

2. **Development Documentation**
   - Code documentation improvement
   - Architecture documentation
   - Contribution guidelines

### Community Building
1. **User Engagement**
   - Regular user surveys
   - Feature request tracking
   - Bug bounty program

2. **Code Quality**
   - Continuous integration setup
   - Automated testing implementation
   - Regular code reviews and refactoring

---

*This roadmap is a living document and will be regularly updated based on user feedback, technical challenges, and project priorities. Dates and timeframes are estimates and subject to change.*
