# Contributing to EZ Streaming

Thank you for your interest in contributing to EZ Streaming! This Windows utility helps content creators streamline their streaming setup, and we welcome contributions from developers, designers, content creators, and users alike.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Architecture Guidelines](#architecture-guidelines)
- [Community and Support](#community-and-support)

## Code of Conduct

EZ Streaming is committed to providing a welcoming and inclusive environment for all contributors. We expect:

- **Respectful communication** in all interactions
- **Constructive feedback** that helps improve the project
- **Inclusive language** that welcomes contributors of all backgrounds
- **Focus on user needs** - always consider how changes benefit content creators
- **Professional conduct** in line with the content creation community values

## Getting Started

### Quick Overview
EZ Streaming is a Windows desktop application that:
- Launches multiple streaming applications with configurable delays
- Manages different profiles for various content types
- Provides intelligent application discovery for 24+ streaming tools
- Uses a modern Qt-based interface optimized for content creators
- Follows a modular architecture for maintainability
### Repository Structure
```
ez-streaming/
├── src/                     # Python source code
│   ├── main.py             # Application entry point
│   ├── app_qt.py           # Main UI and application logic
│   ├── config_manager.py   # Configuration persistence
│   ├── style_manager.py    # UI styling and themes
│   ├── process_manager.py  # Process tracking and management
│   ├── launch_sequence.py  # Sequential app launching
│   ├── app_locator.py      # Application discovery system
│   ├── event_bus.py        # Event communication
│   ├── config_models.py    # Data models and structures
│   ├── resource_monitor.py # System resource monitoring
│   └── exceptions.py       # Custom exception classes
├── assets/                 # Icons, images, and resources
├── docs/                   # GitHub Pages documentation
├── memory-bank/            # Development documentation
├── build.py               # Build and packaging scripts
├── fresh_env.txt          # Python dependencies
└── README.md              # Project documentation
```

### Branches
- **`master`**: Stable releases ready for distribution
- **`development`**: Active development and new features
- **Feature branches**: Individual features (e.g., `feature/profile-import`)

## Types of Contributions

### 🐛 Bug Reports
Help us improve EZ Streaming by reporting issues:
- Use GitHub Issues with the "bug" label
- Include Windows version and system specifications
- Provide steps to reproduce the issue
- Include screenshots or error messages if relevant
- Test with multiple streaming applications if applicable
- Check existing issues before creating new ones
### 💡 Feature Requests
Suggest new functionality for content creators:
- Use GitHub Issues with the "enhancement" label
- Describe the streaming workflow problem your feature would solve
- Explain why it would benefit content creators
- Consider how it fits with the existing architecture
- Provide examples of how other creators might use it

### 📝 Documentation
Improve project documentation:
- Fix typos or unclear explanations in README or guides
- Add examples for common streaming setups
- Create tutorials for specific use cases
- Improve code comments and docstrings
- Translate documentation to other languages

### 🎨 Design Contributions
Enhance user experience for streamers:
- UI/UX improvements for the main interface
- Icon design and visual assets
- Color scheme and accessibility improvements
- User flow optimization for common tasks
- Dark theme refinements (our primary theme)

### 💻 Code Contributions
Implement features and fixes:
- Bug fixes and performance improvements
- New streaming application integrations
- Profile management enhancements
- Windows system integration features
- Accessibility improvements

## Development Setup

### Prerequisites
- **Python 3.8+** with pip package manager
- **Windows 10/11** (primary development platform)
- **Git** for version control
- **Code Editor** (VS Code, PyCharm, or similar)
- **Familiarity** with Python, Qt/PySide6, and Windows development
### Local Development
1. **Fork and Clone**
   ```bash
   git clone https://github.com/[your-username]/ez-streaming.git
   cd ez-streaming
   ```

2. **Switch to Development Branch**
   ```bash
   git checkout development
   ```

3. **Set Up Python Environment**
   ```bash
   # Create virtual environment (recommended)
   python -m venv venv
   venv\Scripts\activate  # Windows
   
   # Install dependencies
   pip install -r fresh_env.txt
   ```

4. **Run Application**
   ```bash
   python src/main.py
   ```

5. **Test Changes**
   - Make your modifications
   - Test with various streaming applications
   - Verify UI responsiveness and styling

### Key Dependencies
- **PySide6**: Qt6 Python bindings for GUI
- **PyInstaller**: For building executable releases
- **psutil**: System and process monitoring
- **pynvml**: NVIDIA GPU monitoring (optional)
- **GPUtil**: General GPU monitoring (optional)

## Contribution Guidelines

### Code Style
- **Python**: Follow PEP 8, use type hints where helpful
- **Qt/PySide6**: Maintain consistent styling via StyleManager
- **Architecture**: Leverage existing manager classes and event bus
- **Comments**: Explain complex logic, especially UI interactions
- **Error Handling**: Use custom exceptions from exceptions.py

### Commit Messages
Follow conventional commit format:
```
type(scope): description

Examples:
feat(app-locator): add support for Streamlabs Desktop
fix(ui): resolve profile dropdown selection bug
docs(readme): update installation instructions
style(interface): improve dark theme contrast
refactor(config): optimize profile loading performance
```
### Testing Guidelines
- **Manual Testing**: Test with clean Windows user profile
- **Streaming App Testing**: Verify with popular applications (OBS, Discord, etc.)
- **Profile Testing**: Test profile creation, deletion, and switching
- **Performance Testing**: Check memory usage and responsiveness
- **Error Handling**: Test edge cases and invalid configurations

### Architecture Requirements
All contributions must respect the existing architecture:
- **Manager Pattern**: Use appropriate managers for different concerns
- **Event Bus**: Use UIEventBus for decoupled communication
- **Data Models**: Use dataclasses from config_models.py
- **Styling**: Apply styles through StyleManager
- **Configuration**: Handle persistence through ConfigManager

## Pull Request Process

### Before Submitting
1. **Create Feature Branch**
   ```bash
   git checkout development
   git pull origin development
   git checkout -b feature/your-feature-name
   ```

2. **Implement Changes**
   - Follow coding guidelines and architecture patterns
   - Test thoroughly with multiple streaming setups
   - Update documentation if needed
   - Add or modify tests if applicable

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat(scope): your descriptive message"
   git push origin feature/your-feature-name
   ```

### Pull Request Template
When creating a PR, include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring
## Testing
- [ ] Tested with clean Windows profile
- [ ] Verified with multiple streaming applications
- [ ] Checked profile management functionality
- [ ] Tested launch sequences with delays
- [ ] Verified UI responsiveness

## Streaming Applications Tested
- [ ] OBS Studio
- [ ] Discord
- [ ] Spotify
- [ ] [Other specific apps relevant to your changes]

## Screenshots (if applicable)
Add screenshots showing UI changes or new features.

## Performance Impact
- [ ] No negative performance impact
- [ ] Improves performance
- [ ] Performance impact acceptable for feature value

## Breaking Changes
List any breaking changes and migration steps.
```

### Review Process
1. **Automated Checks**: Code style and basic functionality validation
2. **Maintainer Review**: Architecture alignment and code quality
3. **User Testing**: Functionality verification with real streaming setups
4. **Merge**: To development branch first, then master for releases

## Architecture Guidelines

### Manager Pattern
EZ Streaming uses a manager-based architecture:
- **ConfigManager**: Handles all configuration persistence
- **StyleManager**: Manages UI themes and styling
- **ProcessManager**: Tracks and controls launched applications
- **ResourceMonitor**: Monitors system resources and process detection

### Event Communication
Use the UIEventBus for decoupled communication:
```python
from event_bus import UIEventBus, EventType

# Publishing events
UIEventBus.publish(EventType.STATUS_UPDATE, "Launching OBS...")

# Subscribing to events
UIEventBus.subscribe(EventType.PROCESS_LIST_CHANGED, self.update_ui)
```
### Data Models
Use structured data models from config_models.py:
```python
from config_models import ProfileConfig, ProgramConfig

# Create structured configuration
program = ProgramConfig(
    name="OBS Studio",
    path="C:/Program Files/obs-studio/bin/64bit/obs64.exe",
    use_custom_delay=True,
    custom_delay_value=3
)
```

### UI Consistency
Maintain consistent styling through StyleManager:
```python
self.setStyleSheet(self.style_manager.get_button_style("primary"))
```

## Community and Support

### Getting Help
- **GitHub Discussions**: General questions and community interaction
- **GitHub Issues**: Bug reports and feature requests
- **Developer Documentation**: memory-bank/ folder contains detailed docs

### Communication Channels
- **Primary**: GitHub Issues and Discussions
- **Updates**: Watch repository for release notifications
- **Community**: Discord server for real-time discussions (link in README)

### Recognition
Contributors will be:
- Credited in release notes for their contributions
- Listed in the project's contributors section
- Invited to participate in roadmap discussions
- Recognized in the application's about dialog

## Development Roadmap

### Current Focus (Phase 2)
- Profile Import/Export functionality
- Auto-save capabilities
- Windows startup integration
- Enhanced application discovery
- Performance optimizations

### Future Considerations (Phase 3+)
- Cross-platform support (macOS/Linux)
- Stream platform integrations (Twitch/YouTube APIs)
- Advanced automation features
- Community profile sharing
- Mobile companion applications

## Testing with Streaming Applications

### Recommended Test Suite
When testing changes, verify with these popular applications:

**Essential:**
- OBS Studio
- Discord
- Spotify
**Common Streaming Tools:**
- Streamlabs (if available)
- XSplit (if available)
- Mix It Up
- Touch Portal

**System Tools:**
- NVIDIA ShadowPlay
- Windows Game Bar
- VoiceMeeter (if available)

### Testing Scenarios
- **Cold Start**: Test launching from completely closed state
- **Mixed State**: Some apps already running, others closed
- **Error Conditions**: Invalid paths, missing applications
- **Resource Usage**: Monitor system impact during mass launches
- **Profile Switching**: Test switching between different profiles

## Questions?

If you have questions about contributing:
1. Check existing GitHub Issues and Discussions
2. Review the memory-bank/ documentation for technical details
3. Create a new Discussion for general questions
4. Create an Issue for specific bugs or feature requests

**Thank you for helping make EZ Streaming better for content creators worldwide!** Every contribution, no matter how small, helps streamers save time and focus on what they do best - creating amazing content.

---

*EZ Streaming is open source software licensed under GPLv3. By contributing, you agree that your contributions will be licensed under the same license, ensuring the project remains free and open source forever.*