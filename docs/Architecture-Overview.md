# Architecture Overview

Understand the technical architecture and design principles behind EZ Streaming's robust and extensible platform.

## System Architecture Overview

EZ Streaming follows a modular, event-driven architecture built on Python and PySide6 (Qt), designed for maintainability, extensibility, and performance.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     EZ Streaming                             │
├─────────────────────────────────────────────────────────────┤
│  User Interface Layer (PySide6/Qt)                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  │   Main Window   │  │ Program Widgets │  │  Style Manager  │
│  │  (StreamerApp)  │  │ (ProgramWidget) │  │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  │ Profile Manager │  │ Launch Sequence │  │ Process Manager │
│  │               │  │  (State Machine) │  │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘
├─────────────────────────────────────────────────────────────┤
│  Service Layer                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  │ Config Manager  │  │  App Locator    │  │Resource Monitor │
│  │               │  │                 │  │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  │   Event Bus     │  │ Data Models     │  │   Exceptions    │
│  │  (Pub/Sub)      │  │ (Config Types)  │  │                 │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### User Interface Layer

#### main.py - Application Entry Point
```python
# Application bootstrap and initialization
- High-DPI display support configuration
- Application instance creation and management
- Main window instantiation and display
- System-level error handling
```

**Key Responsibilities:**
- Configure Qt for optimal display scaling
- Handle application lifecycle events
- Provide crash recovery and error reporting
- Set up application-wide configurations

#### app_qt.py - Main Application Window
```python
class StreamerApp(QMainWindow):
    # Central UI coordinator and event handler
```

**Core Functions:**
- **UI Layout Management:** Creates and manages the main interface layout
- **Event Coordination:** Connects UI events to business logic
- **Widget Management:** Creates and manages ProgramWidget instances
- **Profile UI:** Handles profile dropdown and management UI
- **Status Communication:** Updates status bar and user feedback

**Design Patterns:**
- **Model-View-Controller:** Separates UI from business logic
- **Observer Pattern:** Subscribes to events from business layer
- **Factory Pattern:** Creates ProgramWidget instances dynamically

#### ProgramWidget - Individual Application Row
```python
class ProgramWidget(QWidget):
    # Encapsulates UI for a single application
```

**Responsibilities:**
- **Application Configuration:** Name, path, and delay settings
- **Action Controls:** Launch, close, and browse buttons
- **Status Display:** Visual feedback for application state
- **Drag-and-Drop:** Reordering interface for applications

### Business Logic Layer

#### Launch Sequence - State Machine
```python
class LaunchSequence:
    # Manages sequential application launching
```

**State Machine Design:**
```
IDLE → LAUNCHING_APP → WAITING_DELAY → LAUNCHING_NEXT → COMPLETED
  ↓                                                        ↑
ERROR ←─────────────────────────────────────────────────────┘
```

**Key Features:**
- **Non-blocking Delays:** Uses QTimer for responsive UI during delays
- **Error Resilience:** Continues sequence even if individual apps fail
- **Progress Tracking:** Real-time status updates via event bus
- **Cancellation Support:** Can interrupt the launch sequence

#### Process Manager - Application Lifecycle
```python
class ProcessManager:
    # Tracks and manages launched applications
```

**Core Capabilities:**
- **Process Tracking:** Maintains registry of launched applications
- **Status Monitoring:** Detects application state changes
- **Lifecycle Management:** Handles launch, monitor, and termination
- **Cross-Profile Tracking:** Manages processes across profile switches

**Data Structures:**
```python
tracked_processes = {
    pid: {
        'name': str,
        'profile': str,
        'launch_time': datetime,
        'status': ProcessStatus
    }
}
```

### Service Layer

#### Config Manager - Data Persistence
```python
class ConfigManager:
    # Handles all configuration persistence
```

**Architecture Features:**
- **Platform-Aware Storage:** Uses OS-appropriate data directories
- **Atomic Writes:** Prevents corruption during save operations
- **Backup Management:** Maintains configuration backups
- **Schema Validation:** Ensures configuration data integrity

**Storage Strategy:**
```
Windows: %APPDATA%\EZStreaming\ez_streaming_config.json
macOS: ~/Library/Application Support/EZStreaming/config.json
Linux: ~/.config/EZStreaming/ez_streaming_config.json
```

#### App Locator - Smart Application Discovery
```python
class AppLocator:
    # Intelligent application finding system
```

**Search Strategy:**
1. **Registry Search:** Windows Registry for installed applications
2. **Directory Scanning:** Common installation directories
3. **Steam Integration:** Steam library directory scanning
4. **Fuzzy Matching:** Intelligent name matching algorithms
5. **Path Validation:** Verification of executable accessibility

**Supported Search Locations:**
- Program Files directories
- User AppData directories
- Steam installation directories
- Epic Games directories
- Custom installation paths

#### Resource Monitor - System Integration
```python
class ResourceMonitor:
    # System resource and process monitoring
```

**Monitoring Capabilities:**
- **Process Detection:** Accurate process identification
- **Resource Usage:** CPU, Memory, and GPU monitoring
- **Performance Metrics:** Application performance tracking
- **System Health:** Overall system resource assessment

### Infrastructure Layer

#### Event Bus - Decoupled Communication
```python
class UIEventBus:
    # Publish-subscribe event system
```

**Event Types:**
```python
STATUS_UPDATE = "status_update"
PROCESS_LIST_CHANGED = "process_list_changed"
LAUNCH_SEQUENCE_UPDATE = "launch_sequence_update"
CONFIG_CHANGED = "config_changed"
```

**Benefits:**
- **Loose Coupling:** Components communicate without direct dependencies
- **Extensibility:** Easy to add new event types and handlers
- **Testing:** Simplified unit testing through event mocking
- **Debugging:** Centralized event logging and monitoring

#### Data Models - Type Safety
```python
@dataclass
class ProfileConfig:
    name: str
    launch_delay: int
    programs: List[ProgramConfig]

@dataclass
class ProgramConfig:
    name: str
    path: str
    use_custom_delay: bool
    custom_delay_value: int
```

**Design Benefits:**
- **Type Safety:** Compile-time type checking with mypy
- **Serialization:** Automatic JSON conversion methods
- **Validation:** Built-in data validation and constraints
- **Documentation:** Self-documenting data structures

## Design Patterns and Principles

### Architectural Patterns

#### Model-View-Controller (MVC)
- **Model:** ConfigManager, data models (ProfileConfig, ProgramConfig)
- **View:** Qt widgets (StreamerApp, ProgramWidget)  
- **Controller:** Business logic classes (ProcessManager, LaunchSequence)

#### Observer Pattern
- **Publishers:** ProcessManager, LaunchSequence, ConfigManager
- **Subscribers:** StreamerApp, ProgramWidget instances
- **Medium:** UIEventBus for decoupled communication

#### State Machine Pattern
- **Implementation:** LaunchSequence for managing application launch flow
- **Benefits:** Clear state transitions, error handling, progress tracking
- **Extensibility:** Easy to add new states and transitions

#### Factory Pattern
- **Usage:** Dynamic creation of ProgramWidget instances
- **Benefits:** Consistent widget creation and initialization
- **Flexibility:** Easy to modify widget creation logic

### SOLID Principles Implementation

#### Single Responsibility Principle
- **ConfigManager:** Only handles configuration persistence
- **ProcessManager:** Only manages application processes
- **StyleManager:** Only handles UI styling
- **LaunchSequence:** Only manages launch sequences

#### Open/Closed Principle
- **Event System:** New event types can be added without modifying existing code
- **Plugin Architecture:** Ready for future plugin systems
- **Component Interfaces:** Well-defined interfaces for component interaction

#### Liskov Substitution Principle
- **Data Models:** ProfileConfig and ProgramConfig are interchangeable in collections
- **Widget Hierarchy:** All widgets follow Qt's substitution principles

#### Interface Segregation Principle
- **Event Bus:** Components only subscribe to events they need
- **Manager Interfaces:** Specific interfaces for different management functions

#### Dependency Inversion Principle
- **Event-Driven:** High-level modules depend on abstractions (events) not concrete implementations
- **Configuration:** Business logic depends on configuration abstractions, not storage details

## Data Flow Architecture

### Configuration Flow
```
User Input → UI Events → Business Logic → ConfigManager → File System
     ↑                                                           ↓
     └─────────────── UI Updates ← Event Bus ← Config Events ←──┘
```

### Launch Flow
```
User Action → LaunchSequence → ProcessManager → System APIs
     ↑                                              ↓
     └── Status Updates ← Event Bus ← Status Events ←┘
```

### Process Monitoring Flow
```
System Processes → ResourceMonitor → ProcessManager → Event Bus → UI Updates
```

## Error Handling Architecture

### Exception Hierarchy
```python
class AppError(Exception):
    """Base exception for all application errors"""

class ConfigError(AppError):
    """Configuration-related errors"""

class ProcessError(AppError):
    """Process management errors"""

class LaunchError(AppError):
    """Application launch errors"""
```

### Error Handling Strategy
1. **Graceful Degradation:** Application continues functioning despite individual component failures
2. **User Feedback:** Clear error messages and recovery suggestions
3. **Logging:** Comprehensive error logging for debugging
4. **Recovery:** Automatic recovery mechanisms where possible

### Resilience Patterns
- **Circuit Breaker:** Prevents cascading failures in launch sequences
- **Retry Logic:** Automatic retry for transient failures
- **Fallback Mechanisms:** Alternative approaches when primary methods fail
- **Isolation:** Component failures don't affect other components

## Performance Architecture

### Optimization Strategies

#### UI Responsiveness
- **Asynchronous Operations:** Non-blocking I/O and process operations
- **Background Threading:** Heavy operations moved to background threads
- **Progressive Loading:** UI loads incrementally for better perceived performance
- **Event Batching:** Multiple related events batched for efficiency

#### Memory Management
- **Object Pooling:** Reuse of expensive objects like QTimer instances
- **Lazy Loading:** Components loaded only when needed
- **Garbage Collection:** Proper cleanup of Qt objects and Python references
- **Resource Monitoring:** Built-in memory usage tracking

#### Process Efficiency
- **Smart Polling:** Adaptive polling intervals based on system activity
- **Caching:** Aggressive caching of application discovery results
- **Batch Operations:** Group related system operations for efficiency
- **Resource Sharing:** Shared resources across components

### Scalability Considerations

#### Profile Scaling
- **Efficient Storage:** JSON structure optimized for large numbers of profiles
- **Index Management:** Fast lookup structures for profile management
- **Memory Usage:** Profiles loaded on-demand rather than all at once

#### Application Scaling
- **Dynamic Lists:** UI scales to hundreds of applications per profile
- **Efficient Rendering:** Only visible widgets are actively rendered
- **Process Tracking:** Efficient data structures for large numbers of tracked processes

## Security Architecture

### Security Principles

#### Process Security
- **Least Privilege:** Runs with minimal required permissions
- **Process Isolation:** Launched applications run in their own security contexts
- **Path Validation:** Extensive validation of application paths before execution
- **Safe Defaults:** Secure default configurations

#### Data Security
- **Local Storage:** All configuration data stays on local machine
- **No Network:** No network communication for core functionality
- **File Permissions:** Appropriate file system permissions for configuration storage
- **Input Validation:** All user input validated and sanitized

#### Code Security
- **Type Safety:** Strong typing throughout the codebase
- **Input Sanitization:** All external input properly sanitized
- **Exception Handling:** Comprehensive exception handling prevents crashes
- **Resource Limits:** Bounded resource usage prevents resource exhaustion

## Testing Architecture

### Testing Strategy

#### Unit Testing
- **Component Isolation:** Each component testable in isolation
- **Mock Objects:** Extensive use of mocks for external dependencies
- **Event Testing:** Event bus interactions thoroughly tested
- **Data Model Testing:** All data models have comprehensive test coverage

#### Integration Testing
- **Component Integration:** Tests for interaction between components
- **Event Flow Testing:** End-to-end event flow testing
- **Configuration Testing:** Full configuration save/load cycle testing
- **Process Integration:** Testing of actual process launch and management

#### UI Testing
- **Widget Testing:** Individual widget functionality testing
- **User Workflow Testing:** Complete user workflow simulation
- **Error Scenario Testing:** UI behavior under error conditions
- **Accessibility Testing:** Keyboard navigation and screen reader compatibility

## Deployment Architecture

### Build System
- **PyInstaller:** Executable packaging for distribution
- **Dependency Management:** Automatic inclusion of all required dependencies
- **Asset Bundling:** Fonts, icons, and other assets embedded in executable
- **Platform Targeting:** Windows-specific optimizations and features

### Distribution Strategy
- **Portable Executable:** No installation required
- **Single File:** Self-contained executable with all dependencies
- **Update Mechanism:** Future-ready for automatic update system
- **Configuration Portability:** Support for portable configuration files

## Future Architecture Evolution

### Planned Enhancements

#### Plugin Architecture
- **Plugin Interface:** Well-defined API for third-party plugins
- **Dynamic Loading:** Runtime plugin discovery and loading
- **Sandboxing:** Safe execution environment for plugins
- **Plugin Management:** UI for plugin installation and management

#### Microservice Architecture
- **Service Decomposition:** Break large components into smaller services
- **API Layer:** RESTful API for external integrations
- **Service Discovery:** Automatic discovery of available services
- **Load Balancing:** Distribution of work across service instances

#### Cloud Integration
- **Configuration Sync:** Cloud synchronization of profiles and settings
- **Telemetry:** Optional anonymous usage telemetry
- **Community Features:** Shared profiles and application databases
- **Remote Management:** Enterprise management capabilities

### Technology Evolution

#### Cross-Platform Support
- **macOS Port:** Native macOS application using same architecture
- **Linux Support:** Linux distribution with appropriate system integrations
- **Mobile Companion:** Mobile app for remote control and monitoring

#### Modern Technologies
- **Async/Await:** Migration to modern Python async programming
- **Type Annotations:** Full type annotation coverage for better tooling
- **Modern Qt:** Upgrade to latest Qt versions for improved performance
- **Container Support:** Docker containers for development and testing

## Related Topics

- **[Building from Source](Building-from-Source.md):** Detailed build instructions and development setup
- **[System Requirements](System-Requirements.md):** Hardware and software requirements
- **[Development Setup](Development-Setup.md):** Setting up development environment
- **[Contributing](../CONTRIBUTING.md):** How to contribute to the architecture
