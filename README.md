# EZ Streaming

A free utility for streamers to launch multiple applications with a single click.

## Features

- Simple, streamlined interface
- Launch multiple applications with one click
- Create different profiles for different streaming setups
- Easy program selection with file browser
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
3. Click "Launch All" to start all programs
4. Create different profiles for different streaming setups

## Building from Source

### Windows

```
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets/icon.ico --name EZStreaming src/main.py
```

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## Credits

Created by [Dkmariolink](https://x.com/TheDkmariolink) - Free Software
