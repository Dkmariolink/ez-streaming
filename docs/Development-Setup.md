# Development Setup

This guide will help you set up a development environment for contributing to EZ Streaming.

## Prerequisites

### Required Software
- **Python 3.8+** (Python 3.10+ recommended)
- **Git** for version control
- **Code editor** (VS Code, PyCharm, or your preferred editor)

### System Requirements
- **Windows 10/11** (primary development platform)
- **8GB RAM** minimum (16GB recommended for PyInstaller builds)
- **2GB free disk space** for dependencies and builds

## Environment Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dkmariolink/ez-streaming.git
cd ez-streaming
```

### 2. Create Virtual Environment

Using `venv` (recommended):
```bash
python -m venv venv
venv\Scripts\activate
```

Using `conda`:
```bash
conda create -n ezstreaming python=3.10
conda activate ezstreaming
```

### 3. Install Dependencies

Install from requirements file:
```bash
pip install -r fresh_env.txt
```

Or install manually:
```bash
pip install PySide6 psutil pynvml GPUtil pyinstaller
```

### Key Dependencies Explained

- **PySide6**: Qt6 Python bindings for the GUI framework
- **psutil**: Cross-platform process and system monitoring
- **pynvml**: NVIDIA GPU monitoring (optional)
- **GPUtil**: General GPU monitoring (optional)  
- **PyInstaller**: For building standalone executables

## Project Structure

```
ez-streaming/
├── src/                    # Main source code
│   ├── main.py            # Application entry point
│   ├── streamer_app.py    # Main application window
│   ├── config_manager.py  # Configuration handling
│   ├── style_manager.py   # UI styling and themes
│   ├── process_manager.py # Process launching and monitoring
│   └── ui/                # UI components
├── assets/                # Images, fonts, and resources
├── docs/                  # GitHub Pages documentation
├── memory-bank/           # Project documentation
├── build.py              # Build script
├── EZStreaming.spec      # PyInstaller configuration
└── fresh_env.txt         # Dependencies list
```

## Development Workflow

### Running from Source

To run EZ Streaming in development mode:

```bash
# Make sure virtual environment is activated
cd src
python main.py
```

### Code Style Guidelines

EZ Streaming follows Python best practices:

- **PEP 8** style guide
- **4 spaces** for indentation  
- **Type hints** where appropriate
- **Docstrings** for classes and functions
- **Clear variable names** and comments

### Architecture Overview

EZ Streaming uses a modular architecture:

- **ConfigManager**: Handles loading/saving profiles and settings
- **StyleManager**: Manages UI themes and styling
- **ProcessManager**: Launches and monitors applications  
- **UIEventBus**: Communication between UI components
- **ResourceMonitor**: System resource monitoring

### Key Classes

- `StreamerApp`: Main application window
- `ProgramWidget`: Individual application row in the UI
- `ProfileManager`: Profile creation and management
- `LaunchSequence`: Application launch coordination

## Building and Packaging

### Development Build

For testing builds during development:

```bash
python build.py
```

This will create a `dist/` folder with the executable and dependencies.

### PyInstaller Configuration

The build process is configured via `EZStreaming.spec`:

- Includes all Python files and assets
- Bundles PySide6 and dependencies
- Creates single-directory distribution
- Includes fonts and images

### Build Troubleshooting

**Missing modules error:**
```bash
# Add hidden imports to EZStreaming.spec
hiddenimports=['module_name']
```

**Asset not found:**
```bash
# Verify assets are listed in EZStreaming.spec datas section
datas=[('assets', 'assets')]
```

## Testing

### Manual Testing Checklist

Before submitting changes:

1. **Core Functionality**
   - [ ] Profile creation/deletion works
   - [ ] Application adding/removing works  
   - [ ] Launch delays function properly
   - [ ] "Launch All" works without errors

2. **UI/UX Testing**
   - [ ] All buttons respond correctly
   - [ ] Drag-and-drop reordering works
   - [ ] Tooltips display properly
   - [ ] Window resizing works correctly

3. **Configuration**
   - [ ] Settings save/load correctly
   - [ ] Profile switching works
   - [ ] Configuration file handles errors gracefully

### Automated Testing

Currently EZ Streaming uses manual testing. Automated test contributions are welcome!

## Contributing Code

### Before You Start

1. **Check existing issues** for similar work
2. **Open an issue** to discuss major changes
3. **Follow the coding style** established in the project

### Submission Process

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** with clear commit messages
4. **Test thoroughly** using the checklist above
5. **Submit a pull request** with description of changes

### Pull Request Guidelines

- **Clear title** describing the change
- **Detailed description** of what was modified and why
- **Reference issues** if applicable (`Fixes #123`)
- **Include screenshots** for UI changes
- **Ensure builds work** on clean systems

## Development Tools

### Recommended VS Code Extensions

- **Python** - Python language support
- **Pylance** - Python language server
- **Qt for Python** - PySide6 snippets and tools
- **GitLens** - Git integration enhancements

### Debugging Tips

**GUI Debugging:**
- Use `print()` statements for quick debugging
- Qt Creator's debugger for complex UI issues
- Resource monitoring tools for performance issues

**Process Debugging:**
- Windows Task Manager for launched processes
- Process Explorer for deeper process analysis
- Event Viewer for system-level errors

## Common Development Tasks

### Adding New Applications

To add built-in support for new streaming applications:

1. Update the application list in `locate_app_dialog.py`
2. Add search paths for the application
3. Include common installation directories
4. Test detection across different systems

### UI Modifications

When modifying the interface:

1. Follow existing styling patterns in `style_manager.py`
2. Test with different window sizes
3. Ensure tooltips are helpful and accurate
4. Maintain consistent spacing and alignment

### Adding Features

For new features:

1. Design the feature architecture first
2. Update configuration schema if needed
3. Add UI components following existing patterns
4. Update documentation and help text
5. Test edge cases thoroughly

## Getting Help

### Development Support

- **GitHub Issues**: Report bugs and request features
- **GitHub Discussions**: Ask questions and share ideas
- **Email**: [TheDkmariolink@gmail.com](mailto:TheDkmariolink@gmail.com)

### Documentation

- **Memory Bank**: Detailed project documentation in `/memory-bank/`
- **Code Comments**: Inline documentation in source files
- **Wiki**: This wiki for user and developer guides

---

**Ready to contribute?** Check out our [Contributing Guide](../CONTRIBUTING.md) for more details on the contribution process!