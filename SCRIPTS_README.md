# Anycubic NFC Desktop Application Scripts

This directory contains several batch scripts to help you set up, build, and run the Anycubic NFC Desktop Application. Below is a description of each script and its purpose.

## Main Setup Script

- **setup_desktop_app.bat**: An all-in-one script that provides a menu to access all the other scripts. This is the recommended starting point for new users.

## Installation and Testing Scripts

- **install_dependencies.bat**: Installs all required Python packages for the application.
- **test_dependencies.bat**: Tests if all required dependencies are installed and if the application files exist.

## Running and Building Scripts

- **run_desktop_app.bat**: Runs the desktop application directly from the source code (for testing or development).
- **build_desktop_app.bat**: Builds the standalone executable file that can be distributed and run without Python installed.

## Maintenance Scripts

- **clean_build.bat**: Cleans up build artifacts (build and dist directories, __pycache__ folders) while preserving the spec files.

## How to Use

1. Start with **setup_desktop_app.bat** for a guided experience
2. Or use the individual scripts as needed:
   - First time setup: Run **install_dependencies.bat** followed by **test_dependencies.bat**
   - Development: Use **run_desktop_app.bat** to test changes without building
   - Distribution: Use **build_desktop_app.bat** to create the standalone executable
   - Cleanup: Use **clean_build.bat** when you want to start fresh

## Requirements

- Python 3.11 or newer (including Python 3.12)
- Windows operating system
- Administrator privileges may be required for installation

## Troubleshooting

If you encounter issues:

1. Make sure Python 3.11 or newer is installed and added to PATH
2. Run **test_dependencies.bat** to check for missing dependencies
3. Try running the scripts as administrator if you encounter permission issues
4. Check the console output for specific error messages

### Windows Long Path Issues with Python 3.12

Python 3.12 on Windows may encounter issues with long file paths during package installation. The updated scripts now attempt to automatically enable Windows Long Path support, but this requires administrator privileges.

If you see errors like:

```
ERROR: Could not install packages due to an OSError: [Errno 2] No such file or directory: '...\long\path\...'
HINT: This error might have occurred since this system does not have Windows Long Path support enabled.
```

To fix this:

1. Run the scripts as administrator
2. If that doesn't work, manually enable Windows Long Path support:
   - Open Registry Editor (regedit.exe)
   - Navigate to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   - Set LongPathsEnabled to 1
   - Restart your computer

### PyInstaller Issues

If you encounter issues with PyInstaller not being found, the updated scripts now check for PyInstaller and install it if necessary. Additionally, the scripts now use `python -m PyInstaller` instead of directly calling `pyinstaller` to avoid PATH issues.
