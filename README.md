# EZ Streaming 🎮

**A powerful Windows utility for content creators to launch multiple streaming applications with a single click.**

![EZ Streaming Interface](https://github.com/user-attachments/assets/ea177cdd-3415-4afc-8140-521565867b65d)

## ✨ Features

- **One-Click Launch** - Start all your streaming applications sequentially with a single click
- **Multiple Profiles** - Create different setups for gaming, art streams, podcasts, or any content type
- **Smart Launch Delays** - Configurable delays between app launches to prevent system overload
- **Intelligent App Finder** - Built-in search logic for 24+ popular streaming applications
- **Real-Time Process Management** - Monitor and control launched applications with live status updates
- **Modern Dark Interface** - Sleek dark theme optimized for content creators
- **Persistent Configuration** - Your setups are automatically saved and restored
- **Flexible Ordering** - Drag-and-drop to arrange your launch sequence
- **Windows Optimized** - Native Windows integration with startup options

## 🎭 Perfect For

- **Streamers** - Twitch, YouTube, Facebook Gaming creators
- **Content Creators** - Podcasters, educators, artists
- **Gamers** - Competitive players with complex setups
- **Professionals** - Anyone who needs to launch multiple applications regularly

## 🚀 Quick Start

### 🪟 Windows Installation

1. **Download the latest release** from the [Releases page](https://github.com/Dkmariolink/ez-streaming/releases)
2. **Extract the ZIP file** to your preferred location
3. **Run `EZStreaming.exe`**
4. **Create your first profile** and add your streaming apps
5. **Click "Launch All"** and start creating!

### 🔧 Application Support

**EZ Streaming works with any Windows executable (.exe) file.** 

The "Locate App by Name" feature includes built-in search logic for these popular streaming applications:

**Streaming Software:**
- OBS Studio, Streamlabs, XSplit, Twitch Studio
- StreamElements OBS.Live, Restream

**Communication:**
- Discord, TeamSpeak, Skype

**Content & Music:**
- Spotify, VLC Media Player, Audacity

**Stream Enhancement:**
- Mix It Up, Touch Portal, Streamlabs Chatbot
- Loupedeck, Stream Deck

**Virtual Production:**
- VTube Studio, Snap Camera, NVIDIA Broadcast
- Virtual Audio Cable

**Recording & Capture:**
- NVIDIA ShadowPlay, Action!, Bandicam

**Interactive Features:**
- Crowd Control, Dixper

**Pro Tip:** These are applications with built-in search logic for the "Locate App by Name" feature. You can add any Windows executable using the "Browse" button or by dragging files directly into the interface!

## 📚 Usage Guide

### 🎯 Creating Your First Profile

1. **Launch EZ Streaming** and you'll see the default profile
2. **Add your applications** using one of these methods:
   - Click "Locate App by Name" for automatic detection of supported apps
   - Use "Browse" to manually select any executable files
   - Drag applications directly into the interface
3. **Set launch delays** if needed (recommended 2-5 seconds between apps)
4. **Arrange the order** by dragging rows up or down
5. **Save your profile** - changes are automatically persisted

### 🔧 Advanced Features

#### ⏱️ Launch Delays
- **Profile Default Delay**: Set a standard delay for all apps in the profile
- **Per-App Custom Delay**: Override the default for specific applications
- **Smart Validation**: The first app in your sequence launches immediately

#### 📁 Multiple Profiles
- **Create profiles** for different content types (Gaming, Art, Podcast)
- **Duplicate profiles** as templates for similar setups
- **Quick switching** between profiles via dropdown
- **Protected Default**: The default profile cannot be accidentally renamed

#### 📊 Process Management
- **Monitor status** of launched applications in real-time
- **Individual control** - launch or close specific apps
- **Bulk operations** - close all apps in a profile
- **External detection** - shows if apps are already running

#### 🔍 Smart App Discovery
- **24+ supported apps** with intelligent search
- **Steam integration** - finds games in steamapps/common directories
- **Registry search** - locates apps using Windows registry (read-only)
- **Multi-drive support** - searches C: and D: drives
- **Fuzzy matching** - finds apps even with partial names

## 💻 Development

### 📋 Prerequisites
- **Python 3.8+** with pip
- **Windows 10/11** (primary platform)
- **Git** for version control

### 🛠️ Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Dkmariolink/ez-streaming.git
   cd ez-streaming
   ```

2. **Switch to development branch:**
   ```bash
   git checkout development
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run from source:**
   ```bash
   python src/main.py
   ```

### 📁 Project Structure
```
ez-streaming/
├── src/                                    # Source code
│   ├── main.py                            # Application entry point
│   ├── app_qt.py                          # Main UI and application logic
│   ├── config_manager.py                  # Configuration persistence
│   ├── style_manager.py                   # UI styling and themes
│   ├── process_manager.py                 # Process tracking
│   ├── launch_sequence.py                 # Launch orchestration
│   ├── app_locator.py                     # Application discovery
│   └── ...                                # Additional modules
├── assets/                                # Icons and resources
├── docs/                                  # GitHub Pages documentation
└── build.py                               # Build configuration
```

### 🏗️ Building from Source

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build.py
```

The built executable will be in the `dist/` directory.

## 🤝 Contributing

We welcome contributions from developers, designers, and users! Here's how you can help:

### 🎯 Types of Contributions

- **Bug Reports** - Help us fix issues and improve stability
- **Feature Requests** - Suggest new functionality for streamers
- **Documentation** - Improve guides and help content
- **Code** - Implement features, fix bugs, optimize performance
- **Design** - UI/UX improvements and visual enhancements

### 🔄 Development Process

1. **Fork** the repository
2. **Create a feature branch** from `development`
   ```bash
   git checkout development
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** following coding guidelines
4. **Test thoroughly** with multiple streaming setups
5. **Submit a pull request** with detailed description

### 📝 Coding Guidelines
- **Python**: Follow PEP 8, use type hints where helpful
- **Qt/PySide6**: Maintain consistent styling and responsive UI
- **Architecture**: Leverage the existing manager pattern
- **Testing**: Verify with various application combinations

See our full [Contributing Guide](CONTRIBUTING.md) for detailed information.

## 🔒 Privacy & Security

EZ Streaming is built with privacy in mind. For complete details about data handling and security measures, please see our [Privacy Policy](PRIVACY.md).

**Quick Overview:**
- No data collection or transmission
- All data stays on your device
- No telemetry or usage tracking
- Open source transparency
- Minimal system permissions

## 🗺️ Roadmap

### 📈 Phase 2: User Experience Enhancement (In Progress)
- **Profile Import/Export** - Share setups with other creators
- **Auto-save functionality** - Never lose your configurations
- **Windows startup integration** - Launch with your system
- **Command-line arguments** - Advanced application control
- **Enhanced app discovery** - Even smarter application finding

### 🔮 Phase 3: Advanced Integration (Planned)
- **System tray functionality** - Minimize to tray
- **Stream status monitoring** - Integration with Twitch/YouTube APIs
- **Notification system** - Alerts for launch events
- **Performance monitoring** - Track resource usage
- **Auto-update system** - Seamless updates

### 🌟 Phase 4: Extended Functionality (Future)
- **macOS/Linux support** - Cross-platform availability
- **Mobile companion app** - Remote control capabilities
- **Community features** - Profile sharing platform
- **Advanced automation** - Conditional and dependency-based launching

## 💻 System Requirements

### 📋 Minimum Requirements
- **OS**: Windows 10 (64-bit)
- **RAM**: 4 GB
- **Storage**: 100 MB free space
- **Network**: None required (works offline)

### ✨ Recommended
- **OS**: Windows 11 (64-bit)
- **RAM**: 8 GB or more
- **Storage**: 500 MB free space
- **Display**: 1920x1080 or higher

## 📄 License

EZ Streaming is licensed under the **GNU General Public License v3.0 (GPLv3)**.

This ensures the software remains free and open source forever. You can:
- Use the software for any purpose
- Study and modify the source code
- Distribute copies to help others
- Distribute your modifications

All derivative works must also be licensed under GPLv3. See [LICENSE](LICENSE) for full details.

## 🙏 Acknowledgments

- **PySide6/Qt** - For the excellent GUI framework
- **PyInstaller** - For seamless executable packaging
- **Python community** - For the amazing ecosystem
- **Content creators** - For inspiration and feedback
- **Open source contributors** - Making this project better

## 💖 Support the Project

If EZ Streaming helps your content creation workflow:

- Star this repository to show your support
- Report bugs and suggest improvements
- Share with other creators who might benefit
- Buy me a coffee at [Buy Me a Coffee](https://www.buymeacoffee.com/dkmariolink)
- Contribute code to help the project grow

## 📞 Contact & Support

### 🆘 Get Help
- **Issues**: [GitHub Issues](https://github.com/Dkmariolink/ez-streaming/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Dkmariolink/ez-streaming/discussions)
- **Documentation**: [Project Wiki](https://github.com/Dkmariolink/ez-streaming/wiki)

### 🤝 Connect with the Developer
- **GitHub**: [@Dkmariolink](https://github.com/Dkmariolink)
- **Twitter**: [@TheDkmariolink](https://x.com/TheDkmariolink)
- **Discord**: Dkmariolink
- **Email**: TheDkmariolink@gmail.com

---

**Ready to streamline your streaming setup?** [Download EZ Streaming](https://github.com/Dkmariolink/ez-streaming/releases) and transform your content creation workflow today!

*Made with care by [Dkmariolink](https://github.com/Dkmariolink) - Empowering content creators worldwide*
