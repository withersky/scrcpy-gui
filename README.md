# Scrcpy GUI - ADB WiFi Manager

A simple PySide6 graphical interface for managing ADB WiFi connections and controlling scrcpy screen mirroring.

![Version](https://img.shields.io/badge/version-1.3-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)

## Features

- **ADB WiFi Connection**: Connect to Android devices over WiFi
- **Wireless Pairing**: Support for Android 11+ wireless pairing
- **Device Management**: View and manage connected devices
- **Scrcpy Control**: Start and control scrcpy screen mirroring with customizable settings
- **Multilingual**: Supports English and Russian interfaces
- **Cross-platform**: Works on Linux (Windows support planned)

## Requirements

- Python 3.6 or higher
- PySide6
- ADB (Android Debug Bridge) - included in repository
- Scrcpy - included in repository

## Installation

### From DEB Package (Ubuntu/Debian)

1. Download the latest `.deb` package from the [Releases](https://github.com/YOUR_USERNAME/scrcpy_gui/releases) page
2. Install the package:
   ```bash
   sudo dpkg -i scrcpy-gui_1.3_all.deb
   sudo apt-get install -f  # Install dependencies if needed
   ```
3. Run `scrcpy-gui` from the terminal or find it in your applications menu

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/scrcpy_gui.git
   cd scrcpy_gui
   ```

2. Install dependencies:
   ```bash
   pip install PySide6
   ```

3. Ensure ADB and Scrcpy are installed on your system:
   - Ubuntu/Debian: `sudo apt install android-tools-adb scrcpy`
   - Arch Linux: `sudo pacman -S android-tools scrcpy`
   - Or download from [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) and [Scrcpy](https://github.com/Genymobile/scrcpy)

4. Run the application:
   ```bash
   python3 scrcpy_gui.py
   ```

## Usage

1. **Connect to a Device**:
   - Enter the device IP and port (e.g., `192.168.1.100:5555`)
   - Click "Connect" button

2. **Wireless Pairing (Android 11+)**:
   - Click "Pair (Android 11+)" button
   - Follow the on-screen instructions
   - Enter the pairing code and ports as shown on your device

3. **Start Scrcpy**:
   - Select a connected device from the dropdown
   - Adjust bitrate and max size settings if needed
   - Click "Start Scrcpy" to begin screen mirroring

## Building DEB Package

To build the DEB package from source:

```bash
chmod +x build-deb.sh
./build-deb.sh
```

The package will be created in the current directory.

## Translations

The application currently supports:
- English
- Russian

To add more languages, edit the `TRANSLATIONS` dictionary in `scrcpy_gui.py`.

## Project Structure

```
scrcpy_gui/
├── scrcpy_gui.py          # Main application file
├── icon.png               # Application icon
├── build-deb.sh           # Script to build DEB package
├── adb, scrcpy, scrcpy-server  # Binary files (included)
├── debian/                # Debian package configuration
│   └── DEBIAN/
│       ├── control        # Package metadata
│       ├── postinst       # Post-installation script
│       ├── postrm         # Post-removal script
│       └── scrcpy-gui.desktop  # Desktop entry
├── .github/
│   └── workflows/
│       └── release.yml    # GitHub Actions for automated releases
├── README.md              # This file
├── DEPLOYMENT.md          # Deployment instructions
├── LICENSE                # GPL-3.0 License
├── .gitignore             # Git ignore rules
└── .gitattributes         # Git attributes for binary files
```

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Scrcpy](https://github.com/Genymobile/scrcpy) - Amazing screen mirroring tool
- [PySide6](https://doc.qt.io/qtforpython-6/) - Qt for Python
- [ADB](https://developer.android.com/studio/command-line/adb) - Android Debug Bridge

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub Issues](https://github.com/YOUR_USERNAME/scrcpy_gui/issues) page.
