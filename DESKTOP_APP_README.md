# Anycubic NFC Desktop Application

This is a standalone desktop application version of the Anycubic NFC Filament tool. It provides the same functionality as the web application but in a self-contained window without requiring a web browser.

## Features

- All the same features as the web application
- Standalone window interface
- No need to open a web browser
- Same NFC tag reading and writing capabilities

## Installation

### Option 1: Download Pre-built Executable (Recommended)

1. Download the latest desktop application `.exe` file from the [releases page](https://github.com/Molodos/anycubic-nfc-filament/releases/latest)
2. No installation required - just double-click the executable to run it

### Option 2: Build from Source

1. Make sure you have Python 3.11 or newer (including Python 3.12) installed
2. Clone or download this repository
3. Run the `build_desktop_app.bat` file by double-clicking it
4. The script will install the required packages and build the executable
5. The executable can be found in the `dist` folder

## Usage

1. Start the application by double-clicking the executable file
2. The application will open in its own window
3. Make sure that a supported NFC reader (like the ACR122U) is connected to your computer
4. Use the interface to read from or write to NFC tags
5. For detailed usage instructions, refer to the main [README.md](README.md) file

## Troubleshooting

If you encounter issues with the desktop application:

1. Run the `test_dependencies.bat` file to check if all required dependencies are installed
2. Make sure your NFC reader is properly connected and recognized by your computer
3. Try running the application as administrator if you encounter permission issues
4. Check the console output for specific error messages that might help identify the issue

### Windows Long Path Issues with Python 3.12

Python 3.12 on Windows may encounter issues with long file paths during package installation. If you see errors like:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: '...\long\path\...'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

To fix this:

1. Run the `install_dependencies.bat` script as administrator, which will attempt to enable Windows Long Path support automatically
2. If that doesn't work, you can manually enable Windows Long Path support:
   - Open Registry Editor (regedit.exe)
   - Navigate to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   - Set LongPathsEnabled to 1
   - Restart your computer

## Development

If you want to run the application directly from the source code (for development or testing):

1. Install all required dependencies with `pip install -r requirements.txt`
2. Run the application with `python desktop_app.py` or use the `run_desktop_app.bat` file

## License

This application is released under the same license as the main Anycubic NFC Filament tool.
