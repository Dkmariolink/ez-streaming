# EZ Streaming

**A free Windows utility for streamers to launch multiple applications with a single click.**

![image](https://github.com/user-attachments/assets/ea177cdd-3415-4afc-8140-52156587b65d)



## Features

- Simple, streamlined interface
- Launch multiple applications with one click
- Create different profiles for different streaming setups
- Easy program selection with file browser
- Configurable launch delay between applications (profile default and per-app override)
- Remembers your configuration between sessions
- Dark theme optimized for streamers

## Installation

### Windows

1. Download the latest release from the [Releases page](https://github.com/dkmariolink/ez-streaming/releases)
2. Extract the ZIP file to any location
3. Run `EZStreaming.exe`

### From Source

1. Ensure you have Python 3.8 or newer installed
2. Clone this repository
   ```
   git clone https://github.com/yourusername/ez-streaming.git
   cd ez-streaming
   ```
3. Run the application
   ```
   python src/main.py
   ```

## Usage

1. Add your streaming applications using the "Add Program" button
2. Navigate to each executable using the "Browse" button
3. Optionally, set a default launch delay (in seconds) for the profile using the spinbox at the top right.
4. Optionally, enable "Custom Delay" for specific apps and set their individual pre-launch delays (0-60 seconds). The first app in the list cannot have a delay.
5. Click "Launch All" to start all programs sequentially with the configured delays.
6. Create different profiles for different streaming setups.

## Building from Source

### Windows

```
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico --name EZStreaming src/main.py
```

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

EZ Streaming is licensed under the **GNU General Public License v3.0 (GPLv3)**.

This means the software is free to use, modify, and distribute, but under the condition that any derivative works you distribute must also be licensed under the GPLv3. This ensures the software and its derivatives remain free and open source.

The full license text is available in the `LICENSE` file.

## Credits

Created by [Dkmariolink](https://x.com/TheDkmariolink) - Free Software

## Questions / Comments?

 Message me on Discord (Dkmariolink) or Twitter (@TheDkmariolink), or if you're old school, shoot me an email @ TheDkmariolink@gmail.com
