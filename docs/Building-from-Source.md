# Building from Source

Complete guide to building EZ Streaming from source code for development, customization, or contributing to the project.

## Prerequisites

### Required Software

#### Python Environment
- **Python 3.8 or higher** (3.9+ recommended)
- **pip** (Python package installer)
- **venv** (Virtual environment support)

#### Development Tools
- **Git** (Version control)
- **Code Editor** (VS Code, PyCharm, or similar)
- **Windows SDK** (Windows development)

#### Optional Tools
- **PyInstaller** (For building executables)
- **pytest** (For running tests)
- **mypy** (For type checking)
- **black** (For code formatting)

### System Requirements

#### Windows Development
- **Windows 10/11** (64-bit)
- **8GB RAM** minimum, 16GB recommended
- **5GB free disk space** (for development environment)
- **Visual Studio Build Tools** (for some Python packages)

#### Cross-Platform Development
- **Linux:** Ubuntu 20.04+ or equivalent
- **macOS:** macOS 11+ (for future cross-platform support)

## Getting the Source Code

### Cloning the Repository

#### From GitHub
```bash
# Clone the main repository
git clone https://github.com/Dkmariolink/ez-streaming.git
cd ez-streaming

# Or clone your fork for contributing
git clone https://github.com/YOUR_USERNAME/ez-streaming.git
cd ez-streaming
```

#### Development Branch
```bash
# For latest development features
git checkout develop

# Or create a feature branch
git checkout -b feature/your-feature-name
```

### Repository Structure
```
ez-streaming/
├── src/                    # Source code
│   ├── main.py            # Application entry point
│   ├── app_qt.py          # Main application window
│   ├── config_manager.py  # Configuration management
│   ├── process_manager.py # Process management
│   ├── launch_sequence.py # Launch sequence logic
│   ├── style_manager.py   # UI styling
│   ├── event_bus.py       # Event system
│   ├── app_locator.py     # Application finder
│   ├── resource_monitor.py # System monitoring
│   ├── config_models.py   # Data models
│   └── exceptions.py      # Custom exceptions
├── assets/                # Images, icons, fonts
│   ├── fonts/
│   ├── images/
│   └── icons/
├── docs/                  # Documentation
├── tests/                 # Test suite
├── build/                 # Build artifacts
├── dist/                  # Distribution files
├── memory-bank/           # AI assistant memory
├── EZStreaming.spec       # PyInstaller spec file
├── fresh_env.txt          # Python dependencies
├── requirements.txt       # Alternative dependencies file
├── build.py              # Build script
└── README.md             # Project README
```

## Setting Up Development Environment

### Python Virtual Environment

#### Creating Virtual Environment
```bash
# Create virtual environment
python -m venv ez-streaming-env

# Activate virtual environment
# Windows:
ez-streaming-env\Scripts\activate
# Linux/macOS:
source ez-streaming-env/bin/activate
```

#### Installing Dependencies
```bash
# Install from requirements file
pip install -r fresh_env.txt

# Or install manually
pip install PySide6 PyInstaller psutil pynvml GPUtil
```

### Development Dependencies

#### Required for Development
```bash
pip install pytest pytest-qt pytest-mock
pip install mypy types-setuptools
pip install black flake8 isort
pip install coverage pytest-cov
```

#### Optional Development Tools
```bash
pip install pre-commit          # Git hooks
pip install sphinx             # Documentation generation
pip install twine              # Package publishing
pip install wheel              # Wheel building
```

### IDE Configuration

#### Visual Studio Code
Create `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./ez-streaming-env/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm
1. Open project directory
2. Configure Python interpreter to use virtual environment
3. Enable pytest as test runner
4. Configure Black as code formatter

## Running from Source

### Development Mode

#### Basic Run
```bash
# Activate virtual environment
source ez-streaming-env/bin/activate  # or Windows equivalent

# Run the application
python src/main.py
```

#### Debug Mode
```bash
# Run with debug output
python src/main.py --debug

# Run with verbose logging
python src/main.py --verbose
```

#### Development Features
```bash
# Run with development UI (future feature)
python src/main.py --dev

# Run with hot reload (future feature)
python src/main.py --reload
```

### Testing the Build

#### Unit Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config_manager.py

# Run with verbose output
pytest -v
```

#### Integration Tests
```bash
# Run integration tests
pytest tests/integration/

# Run UI tests (requires display)
pytest tests/ui/
```

#### Type Checking
```bash
# Run mypy type checking
mypy src/

# Check specific file
mypy src/config_manager.py
```

#### Code Quality
```bash
# Format code with Black
black src/ tests/

# Check with flake8
flake8 src/ tests/

# Sort imports
isort src/ tests/
```

## Building Executables

### PyInstaller Build

#### Standard Build
```bash
# Build using spec file
pyinstaller EZStreaming.spec

# Or build manually
pyinstaller --onefile --windowed --name EZStreaming src/main.py
```

#### Build with Assets
```bash
# Build including all assets
pyinstaller --onefile --windowed \
    --add-data "assets;assets" \
    --icon "assets/icon.ico" \
    --name EZStreaming \
    src/main.py
```

#### Advanced Build Options
```bash
# Build with debugging info
pyinstaller --onefile --windowed --debug all EZStreaming.spec

# Build with console (for debugging)
pyinstaller --onefile --console EZStreaming.spec

# Build with optimization
pyinstaller --onefile --windowed --optimize 2 EZStreaming.spec
```

### Using Build Script

#### Automated Build
```bash
# Run the build script
python build.py

# Build with specific options
python build.py --debug
python build.py --release
python build.py --clean
```

#### Build Script Options
```python
# build.py command line options
--clean         # Clean build directories first
--debug         # Build with debug information
--release       # Build optimized release version
--no-upx        # Skip UPX compression
--verbose       # Verbose build output
```

### Build Configuration

#### EZStreaming.spec File
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('assets/fonts', 'assets/fonts'),
        ('assets/images', 'assets/images'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui', 
        'PySide6.QtWidgets',
        'psutil',
        'pynvml',
        'GPUtil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EZStreaming',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico'
)
```

## Build Optimization

### Size Optimization

#### Reducing Binary Size
```bash
# Use UPX compression
pyinstaller --upx-dir=/path/to/upx EZStreaming.spec

# Exclude unnecessary modules
pyinstaller --exclude-module tkinter --exclude-module matplotlib EZStreaming.spec

# Strip debug symbols
pyinstaller --strip EZStreaming.spec
```

#### Asset Optimization
- **Compress images:** Use optimized PNG/JPEG formats
- **Minimize fonts:** Include only required font weights
- **Remove unused assets:** Clean up unused files

### Performance Optimization

#### Startup Performance
```python
# In main.py, optimize imports
import sys
import os
from PySide6.QtWidgets import QApplication

# Lazy imports for faster startup
def load_heavy_modules():
    global psutil, pynvml
    import psutil
    import pynvml
```

#### Runtime Performance
- **Compiled Python:** Use `python -O` for optimized bytecode
- **Memory optimization:** Profile memory usage and optimize
- **I/O optimization:** Minimize file system operations

## Platform-Specific Builds

### Windows Build

#### Windows-Specific Requirements
```bash
# Install Windows-specific packages
pip install pywin32
pip install wmi

# For Windows registry access
pip install winreg-alt
```

#### Windows Build Command
```bash
# Build for Windows
pyinstaller --onefile --windowed \
    --add-data "assets;assets" \
    --icon "assets/icon.ico" \
    --version-file version.txt \
    --name EZStreaming \
    src/main.py
```

### Future Cross-Platform Builds

#### macOS Build (Planned)
```bash
# macOS-specific build
pyinstaller --onefile --windowed \
    --add-data "assets:assets" \
    --icon "assets/icon.icns" \
    --osx-bundle-identifier com.dkmariolink.ezstreaming \
    --name EZStreaming \
    src/main.py
```

#### Linux Build (Planned)
```bash
# Linux-specific build
pyinstaller --onefile \
    --add-data "assets:assets" \
    --name ezstreaming \
    src/main.py
```

## Development Workflow

### Git Workflow

#### Branch Strategy
```bash
# Main branches
main        # Stable release branch
develop     # Development integration branch

# Feature branches
feature/profile-import-export
feature/auto-save
bugfix/launch-delay-ui

# Release branches
release/v1.3.0
```

#### Commit Guidelines
```bash
# Commit message format
<type>(<scope>): <subject>

# Examples
feat(ui): add profile import/export functionality
fix(launch): resolve timing issue with heavy applications
docs(readme): update installation instructions
refactor(config): improve error handling in ConfigManager
```

### Testing Workflow

#### Pre-commit Testing
```bash
# Run all checks before committing
black src/ tests/          # Format code
flake8 src/ tests/         # Lint code
mypy src/                  # Type check
pytest                     # Run tests
```

#### Continuous Integration
```yaml
# .github/workflows/ci.yml (example)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r fresh_env.txt
      - run: pytest
      - run: mypy src/
```

### Release Workflow

#### Version Management
```python
# src/version.py
__version__ = "1.2.0"
__build__ = "20250612"
```

#### Release Process
1. **Update version numbers** in all relevant files
2. **Run full test suite** to ensure stability
3. **Build release executable** with optimizations
4. **Test release build** thoroughly
5. **Create release notes** documenting changes
6. **Tag release** in version control
7. **Upload to GitHub releases** with assets

## Troubleshooting Build Issues

### Common Build Problems

#### PyInstaller Issues
**Problem:** Module not found during runtime  
**Solution:**
```bash
# Add to hiddenimports in spec file
hiddenimports=['missing_module_name']

# Or use hook files
echo "hiddenimports = ['missing_module']" > hook-missing_module.py
```

**Problem:** Assets not included in build  
**Solution:**
```bash
# Update datas in spec file
datas=[('assets', 'assets'), ('config', 'config')]
```

#### PySide6 Issues
**Problem:** Qt platform plugin not found  
**Solution:**
```bash
# Include Qt plugins
datas=[('venv/Lib/site-packages/PySide6/plugins', 'PySide6/plugins')]
```

#### Permission Issues
**Problem:** Build fails with permission errors  
**Solution:**
```bash
# Run as administrator (Windows)
# Or fix permissions (Linux/macOS)
chmod +x build.py
```

### Debug Build Issues

#### Debug Build
```bash
# Build with debug info
pyinstaller --debug all EZStreaming.spec

# Run with debug output
./dist/EZStreaming.exe --debug
```

#### Logging Build Issues
```python
# Add to main.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing to the Build System

### Build System Improvements

#### Adding New Build Options
1. **Modify build.py** to add new command-line options
2. **Update EZStreaming.spec** for new build configurations
3. **Test across different environments**
4. **Document new options** in this guide

#### Cross-Platform Support
1. **Add platform detection** to build system
2. **Create platform-specific spec files**
3. **Handle platform-specific dependencies**
4. **Test on target platforms**

### Documentation Updates

#### When to Update This Guide
- **New dependencies** are added to the project
- **Build process changes** or new options are added
- **Platform support** is added or modified
- **Troubleshooting solutions** are discovered

#### Documentation Standards
- **Clear step-by-step instructions**
- **Code examples** for all commands
- **Troubleshooting sections** for common issues
- **Cross-references** to related documentation

## Advanced Build Topics

### Custom PyInstaller Hooks

#### Creating Custom Hooks
```python
# hook-mymodule.py
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('mymodule')
hiddenimports = ['mymodule.submodule']
```

### Build Automation

#### Automated Build Pipeline
```python
# build_pipeline.py
import subprocess
import os
import shutil

def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def run_tests():
    """Run test suite"""
    result = subprocess.run(['pytest'], capture_output=True)
    return result.returncode == 0

def build_executable():
    """Build the executable"""
    result = subprocess.run(['pyinstaller', 'EZStreaming.spec'])
    return result.returncode == 0
```

### Performance Profiling

#### Build Performance
```bash
# Profile PyInstaller build
time pyinstaller EZStreaming.spec

# Profile application startup
python -m cProfile -o profile.stats src/main.py
```

#### Runtime Performance
```python
# Add profiling to application
import cProfile
import pstats

def profile_startup():
    pr = cProfile.Profile()
    pr.enable()
    # Application code here
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Related Topics

- **[Development Setup](Development-Setup.md):** Development environment configuration
- **[Architecture Overview](Architecture-Overview.md):** Understanding the codebase structure
- **[Contributing](../CONTRIBUTING.md):** How to contribute to the project
- **[System Requirements](System-Requirements.md):** Hardware and software requirements
