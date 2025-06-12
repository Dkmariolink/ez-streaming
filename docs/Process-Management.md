# Process Management

Understand how EZ Streaming tracks, monitors, and manages your applications throughout their lifecycle.

## Overview

EZ Streaming's process management system tracks applications from launch to termination, providing you with real-time status information and control over your streaming setup.

## How Process Tracking Works

### Launch Process
When you launch applications through EZ Streaming:

1. **Process Creation:** EZ Streaming starts the application using Windows APIs
2. **PID Assignment:** The system assigns a unique Process ID (PID) to the application
3. **Registration:** EZ Streaming records the PID, application name, and profile association
4. **Status Updates:** The UI reflects the new process status
5. **Monitoring Begins:** Continuous monitoring for process state changes

### Detection Methods

#### Internal Launch Detection
- **Direct Tracking:** Applications launched via "Launch" or "Launch All" buttons
- **Immediate Registration:** PID captured at launch time
- **Full Control:** EZ Streaming has complete process information

#### External Launch Detection
- **Path Matching:** Detects when applications are launched externally
- **Process Scanning:** Periodically scans running processes for known applications
- **Case-Insensitive Matching:** Uses normalized path comparison for reliability
- **UI Synchronization:** Updates button states and status indicators

### Process States

#### Not Running
- **Status:** Application is not currently active
- **UI State:** "Launch" button enabled, "Close" button disabled
- **Indicator:** No special status indication

#### Launching
- **Status:** Application is in the process of starting
- **UI State:** "Launch" button shows "Launching..." (temporarily)
- **Indicator:** Status bar shows launch progress
- **Duration:** Brief transition state during startup

#### Running (Internal)
- **Status:** Application launched by EZ Streaming and currently active
- **UI State:** "Launch" button disabled and shows "Launched"
- **Indicator:** "Close" button enabled for termination
- **Tracking:** Full process control and monitoring

#### Running (External)
- **Status:** Application detected running but not launched by EZ Streaming
- **UI State:** "Launch" button disabled and shows "Launched"
- **Indicator:** Limited control - may not be closeable via EZ Streaming
- **Detection:** Found through process scanning

#### Terminated
- **Status:** Application has ended (gracefully or crashed)
- **UI State:** Returns to "Not Running" state
- **Cleanup:** Process removed from tracking lists
- **Notification:** Status updates reflect the change

## Process Control Features

### Individual Application Control

#### Launch Control
- **Single Launch:** Click "Launch" button for immediate application start
- **Launch Validation:** Checks path validity before attempting launch
- **Error Handling:** Displays errors if launch fails
- **Status Feedback:** Real-time updates during launch process

#### Close Control
- **Graceful Termination:** Attempts to close applications cleanly
- **Force Termination:** Falls back to force-close if graceful close fails
- **Process Tree:** Closes child processes when possible
- **Confirmation:** Some applications may show save prompts

### Bulk Process Control

#### Launch All
- **Sequential Launch:** Starts all applications in profile order
- **Delay Respect:** Honors configured launch delays
- **Progress Tracking:** Shows current application being launched
- **Error Resilience:** Continues sequence even if one application fails
- **Status Updates:** Real-time feedback in status bar

#### Close All
- **Profile-Specific:** Closes all applications in the current profile
- **Cross-Profile Option:** Can close all tracked applications regardless of profile
- **Graceful First:** Attempts clean shutdown before force-closing
- **Batch Processing:** Handles multiple applications efficiently

### Process Status Monitoring

#### Real-Time Detection
- **Continuous Monitoring:** Regular checks for process state changes
- **External Detection:** Identifies when applications are launched outside EZ Streaming
- **Crash Detection:** Detects when applications terminate unexpectedly
- **UI Synchronization:** Updates interface to reflect current state

#### Process Information
- **Process ID (PID):** Unique identifier for each running application
- **Application Path:** Full path to the executable file
- **Launch Method:** Whether launched internally or detected externally
- **Profile Association:** Which profile the application belongs to
- **Runtime Duration:** How long the application has been running

## Advanced Process Management

### Process Detection Accuracy

#### Path Normalization
- **Case Insensitive:** Handles Windows case-insensitive file system
- **Path Comparison:** Uses normalized paths for accurate matching
- **Symbolic Links:** Resolves links and junctions for proper detection
- **Network Paths:** Handles UNC paths and mapped drives

#### Multiple Instance Handling
- **Instance Detection:** Identifies when multiple instances of the same application are running
- **Profile Isolation:** Each profile tracks its own instances
- **Conflict Resolution:** Handles situations where multiple profiles reference the same application

### Cross-Profile Process Management

#### Profile Switching
- **Process Persistence:** Running applications continue when switching profiles
- **Status Updates:** UI reflects current profile's applications
- **Background Tracking:** EZ Streaming maintains awareness of all launched processes
- **Re-association:** Can detect applications from other profiles

#### Global Process View
- **All Processes:** EZ Streaming tracks processes across all profiles
- **Profile Identification:** Each process remembers its originating profile
- **Selective Control:** Can choose to manage all processes or just current profile

### Performance Monitoring Integration

#### Resource Awareness
- **Process Detection:** Uses process monitoring for accurate application detection
- **Performance Data:** Can access CPU, memory, and GPU usage information
- **System Impact:** Monitors how applications affect overall system performance
- **Optimization Hints:** Provides insights for better launch timing

#### Background Monitoring
- **Continuous Tracking:** Monitors applications even when EZ Streaming is minimized
- **Resource Efficiency:** Minimal overhead for process monitoring
- **Smart Polling:** Adjusts monitoring frequency based on activity level

## Troubleshooting Process Issues

### Common Process Management Problems

#### Applications Not Detected
**Problem:** EZ Streaming doesn't recognize running applications  
**Solutions:**
1. **Verify Path Accuracy:** Ensure the configured path matches the actual executable
2. **Check Path Format:** Use full, absolute paths rather than relative paths
3. **Process Restart:** Restart EZ Streaming to refresh process detection
4. **Manual Refresh:** Switch profiles to trigger process re-scan

#### Process Control Failures
**Problem:** Cannot launch or close applications  
**Solutions:**
1. **Administrator Rights:** Run EZ Streaming as administrator
2. **Path Validation:** Verify application paths are valid and accessible
3. **Antivirus Interference:** Check if security software is blocking process control
4. **Application State:** Some applications may be in a state that prevents control

#### Inconsistent Status Updates
**Problem:** UI doesn't reflect actual application status  
**Solutions:**
1. **Process Refresh:** Switch profiles or restart EZ Streaming
2. **Path Conflicts:** Check for multiple applications with similar paths
3. **System Performance:** High system load can delay status updates
4. **Process Scanning:** Manual profile switch triggers fresh process scan

### Advanced Troubleshooting

#### Process Monitoring Debug
- **Task Manager Comparison:** Compare EZ Streaming's view with Windows Task Manager
- **Process Explorer Usage:** Use advanced tools to verify process states
- **Event Log Review:** Check Windows Event Viewer for process-related errors
- **Path Resolution:** Verify that configured paths resolve correctly

#### Permission Issues
- **User Account Control:** Some applications require elevated privileges
- **File System Permissions:** Ensure read access to application directories
- **Process Security:** Some applications have restrictions on external control
- **Administrative Mode:** Running EZ Streaming as administrator can resolve many issues

## Process Management Best Practices

### Configuration Best Practices

#### Path Management
- **Absolute Paths:** Always use full paths starting with drive letters
- **Path Validation:** Regularly verify that application paths are still valid
- **Update Tracking:** Monitor for application updates that might change paths
- **Standardization:** Use consistent path formats across profiles

#### Profile Organization
- **Logical Grouping:** Group related applications in the same profile
- **Minimal Overlap:** Avoid same applications in multiple profiles when possible
- **Clear Naming:** Use descriptive names for profiles and applications
- **Regular Cleanup:** Remove unused applications and profiles

### Operational Best Practices

#### Launch Management
- **Pre-Launch Checks:** Verify system resources before launching multiple applications
- **Sequential Launches:** Use "Launch All" rather than manual individual launches
- **Error Monitoring:** Watch for launch failures and address them promptly
- **Resource Planning:** Consider system capacity when configuring profiles

#### Shutdown Management
- **Graceful Shutdown:** Use "Close All" for clean application termination
- **Save Prompts:** Allow applications time to save work before forcing closure
- **Resource Cleanup:** Ensure all processes are properly terminated
- **System Stability:** Avoid forcing closure unless necessary

### Maintenance Practices

#### Regular Monitoring
- **Process Health:** Periodically check that all applications are running properly
- **Resource Usage:** Monitor system impact of launched applications
- **Update Tracking:** Keep track of application updates and path changes
- **Performance Assessment:** Evaluate whether all applications are still needed

#### Troubleshooting Preparation
- **Documentation:** Keep notes about unusual process behaviors
- **Backup Configurations:** Maintain backups of working profile configurations
- **Testing Procedures:** Regularly test launch and close functionality
- **System Monitoring:** Watch for signs of process management issues

## Integration with Other Systems

### Windows Integration

#### Windows Task Manager
- **Cross-Reference:** Compare process lists with Task Manager
- **Resource Monitoring:** Use Task Manager for detailed resource information
- **Process Trees:** Understand parent-child process relationships
- **Service Dependencies:** Be aware of Windows services that applications might depend on

#### Windows Services
- **Service Dependencies:** Some applications require specific Windows services
- **Service Management:** Understanding how services affect application launching
- **Startup Types:** How Windows service startup types affect application behavior
- **Troubleshooting:** Service issues can affect process management

### Third-Party Integration

#### Antivirus Software
- **Process Monitoring:** How antivirus affects process detection and control
- **Whitelist Management:** Adding EZ Streaming and applications to antivirus whitelists
- **Real-Time Protection:** Impact on launch times and process management
- **Quarantine Issues:** Recovering applications that have been quarantined

#### System Utilities
- **Process Monitors:** Integration with advanced process monitoring tools
- **Resource Managers:** Compatibility with system resource management software
- **Gaming Software:** How gaming platforms affect process management
- **RGB/Hardware Control:** Managing hardware control applications

## Future Process Management Features

### Planned Enhancements

#### Enhanced Detection
- **Service Monitoring:** Track Windows services associated with applications
- **Dependency Mapping:** Understand and visualize application dependencies
- **Performance Integration:** Deep integration with system performance monitoring
- **Predictive Detection:** Anticipate application states based on patterns

#### Advanced Control
- **Process Priorities:** Control CPU priority for launched applications
- **Resource Limits:** Set memory and CPU limits for applications
- **Affinity Control:** Assign applications to specific CPU cores
- **Startup Sequences:** More sophisticated startup dependency management

#### Monitoring and Analytics
- **Usage Statistics:** Track application usage patterns over time
- **Performance History:** Historical view of application performance impact
- **Optimization Suggestions:** AI-driven recommendations for better process management
- **Health Monitoring:** Proactive detection of application problems

### Long-Term Vision

#### Smart Process Management
- **Machine Learning:** Learn optimal process management strategies
- **Adaptive Behavior:** Automatically adjust based on system performance
- **Predictive Actions:** Anticipate user needs and automate common tasks
- **Integration APIs:** Allow third-party applications to integrate with EZ Streaming

#### Enterprise Features
- **Centralized Management:** Deploy and manage EZ Streaming across multiple systems
- **Policy Enforcement:** Enforce process management policies in organizational settings
- **Audit Trails:** Detailed logging of all process management activities
- **Remote Monitoring:** Monitor EZ Streaming deployments remotely

## Related Topics

- **[Adding Applications](Adding-Applications.md):** Learn how to add applications for process management
- **[Launch Delays and Timing](Launch-Delays-and-Timing.md):** Optimize timing for better process management
- **[Profile Management](Profile-Management.md):** Organize applications for effective process control
- **[System Requirements](System-Requirements.md):** Hardware considerations for process management
- **[Troubleshooting](Troubleshooting.md):** Solutions for process-related issues
