# EZ Streaming Privacy Policy

**Last Updated:** June 10, 2025  
**Effective Date:** June 10, 2025

## Overview

EZ Streaming is committed to protecting your privacy. This desktop application is designed with privacy-first principles, storing all data locally on your device with no external data transmission or cloud services.

## Data Collection

### What Data We Collect

EZ Streaming collects the following information to provide application launching and profile management:

- **Application Configuration:**
  - Executable file paths for your streaming applications
  - Application names (user-defined or auto-detected)
  - Launch delay settings and preferences
  - Profile names and organization

- **Application State Information:**
  - Process status of launched applications
  - Launch sequence timing and order
  - Application success/failure status

- **User Preferences:**
  - UI settings and preferences
  - Profile selection and defaults
  - Warning dialog preferences
  - Theme and display options

### What Data We Do NOT Collect

EZ Streaming does not collect:
- Personal identifying information (name, email, address)
- Streaming content or media files
- Account information or credentials for streaming platforms
- Chat logs, messages, or communications
- Streaming analytics or viewer data
- Financial or payment information
- Location data or IP addresses
- Usage analytics or telemetry data
- Application content or opened files
- Network traffic or streaming data
## Data Storage and Usage

### Local Storage Only
- All data is stored locally on your Windows device
- Configuration saved to `ez_streaming_config.json` in your user application data folder
- No cloud storage, synchronization, or remote backup
- No data transmitted to external servers or third parties
- Data remains entirely under your local control

### Purpose of Data Use
Data is used exclusively for:
- Launching your configured streaming applications
- Managing different profile setups for various content types
- Remembering your preferences between application sessions
- Providing process monitoring and status updates
- Enabling intelligent application discovery and management

## Data Control and Retention

### Your Control
- **View Data:** Access all configuration through the application interface
- **Modify Data:** Change any settings, profiles, or application configurations
- **Delete Data:** Clear profiles, remove applications, or delete all data
- **Export Data:** Configuration is stored in human-readable JSON format
- **Backup/Restore:** Manual backup by copying configuration files

### Automatic Cleanup
- EZ Streaming does not automatically delete user data
- Configuration persists between application sessions
- Users can manually clear unused profiles or applications
- No automatic data expiration or cleanup processes

## Data Sharing and Third Parties

### No Data Sharing
EZ Streaming does not:
- Transmit data to external servers or cloud services
- Share data with third-party services or analytics platforms
- Upload configuration or usage data anywhere
- Communicate with streaming platforms' APIs
- Send telemetry or crash reports externally
- Use data for advertising or marketing purposes

### No Analytics or Tracking
- No usage analytics collected
- No crash reporting or error telemetry
- No user behavior tracking or monitoring
- No integration with analytics services
- No external service dependencies for core functionality
## Security

### Local Security
- Data is protected by Windows user account permissions
- Configuration files stored in standard user application data directories
- Application follows Windows security best practices
- No network communications or external connections
- No authentication or account systems

### Application Permissions
EZ Streaming only requires:
- **File System Access:** To read and execute your chosen applications
- **Process Management:** To launch, monitor, and manage application processes
- **Registry Read Access:** For intelligent application discovery (read-only)
- **User Data Folder Access:** To save and load configuration files

## Open Source Transparency

EZ Streaming is open source software:
- **Repository:** https://github.com/Dkmariolink/ez-streaming
- **License:** GNU General Public License v3.0 (GPLv3)
- **Code Review:** All code is publicly available for security audit
- **Community:** Contributions welcome following our guidelines
- **No Hidden Features:** All functionality is transparent and reviewable

## Technical Implementation

### Configuration File Details
- **Location:** `%APPDATA%\EZStreaming\ez_streaming_config.json` (Windows)
- **Format:** Human-readable JSON
- **Contents:** Profile names, application paths, delay settings, user preferences
- **Access:** Only by EZ Streaming application and user with file permissions

### Process Monitoring
- **Scope:** Limited to applications launched by EZ Streaming
- **Data:** Process IDs, running status, basic resource usage detection
- **Purpose:** Application management and user interface updates
- **Retention:** Cleared when application exits or processes terminate

### Application Discovery
- **Registry Access:** Read-only access to Windows Registry for finding installed applications
- **File System Scanning:** Limited to common installation directories
- **Data Collection:** Application names and installation paths only
- **Usage:** Helping users locate streaming applications more easily

## Changes to Privacy Policy

### Updates
- Privacy policy changes will be posted in this document
- Users will be notified of significant changes through application updates
- Continued use after changes constitutes acceptance
- Version history maintained in this document

### Version History
- v1.0.0 (June 10, 2025): Initial privacy policy for public release
## Legal Compliance

### Applicable Laws
This privacy policy complies with:
- General Data Protection Regulation (GDPR) principles for EU users
- California Consumer Privacy Act (CCPA) requirements
- Other applicable data protection laws

### User Rights
Users have the right to:
- Access their data (through application interface)
- Modify their data (through application settings)
- Delete their data (through application interface or file system)
- Understand how their data is used (through this policy)
- Port their data (configuration files are in open JSON format)

## Contact Information

### Questions and Support
For privacy-related questions or concerns:
- **Issues:** https://github.com/Dkmariolink/ez-streaming/issues
- **Repository:** https://github.com/Dkmariolink/ez-streaming
- **Developer:** TheDkmariolink@gmail.com
- **Twitter:** @TheDkmariolink

### Data Protection
For this application, the developer serves as the primary contact for all privacy and data protection matters. As an open source project with no data collection, formal data protection officer designation is not required.

## Special Considerations for Content Creators

### Streaming Platform Independence
- EZ Streaming does not integrate with streaming platform APIs
- No data shared with Twitch, YouTube, Facebook Gaming, or other platforms
- No tracking of streaming activity or content
- Platform integrations (if added in future) will be opt-in and clearly documented

### Application Execution Privacy
- EZ Streaming launches applications but does not monitor their behavior
- Each launched application operates under its own privacy policy
- EZ Streaming cannot and does not control data practices of launched applications
- Users should review privacy policies of their streaming applications separately

### Profile and Setup Privacy
- Profile names and application choices remain private and local
- No sharing or synchronization of streaming setups
- Community features (if added) will be explicitly opt-in
- Setup sharing capabilities will be manual export/import only
## Technical Architecture for Privacy

### Design Principles
- **Local-First:** All functionality works without internet connection
- **No Telemetry:** No usage tracking or analytics collection
- **Minimal Permissions:** Request only necessary system access
- **Transparent Operation:** All actions visible and controllable by user
- **Data Ownership:** User retains full control over all configuration data

### Future Privacy Considerations
If new features are added that involve data collection or external services:
- Explicit user consent will be required
- Privacy policy will be updated with clear disclosure
- Features will be optional and clearly marked
- Users will maintain ability to opt-out or disable features

---

**Summary:** EZ Streaming is a privacy-first desktop application that stores all data locally on your Windows device. We collect only the configuration information necessary to launch your streaming applications and manage your profiles. We never share this data with anyone, and you maintain complete control over your information with options to view, modify, or delete it at any time.

For the most current version of this privacy policy and complete technical details, visit our GitHub repository: https://github.com/Dkmariolink/ez-streaming