# Python 3.12 Compatibility Changes

This document outlines the changes made to ensure compatibility with Python 3.12.

## Core Changes

### 1. Eventlet Compatibility

The application previously used eventlet with monkey patching, which can cause compatibility issues with Python 3.12. The following changes were made to address this:

- Modified `web_app.py` to use a try-except block for eventlet imports
- Added fallback to threading mode if eventlet causes issues
- Set the async mode dynamically based on what's available

```python
# Try to import eventlet, but fall back to threading if it's not available or causes issues
try:
    import eventlet
    from smartcard.System import readers
    eventlet.monkey_patch()
    ASYNC_MODE = "eventlet"
except (ImportError, SyntaxError):
    from smartcard.System import readers
    ASYNC_MODE = "threading"
```

### 2. Smartcard Library Compatibility

The pyscard library might have compatibility issues with Python 3.12. The following changes were made to address this:

- Added better error handling in `nfc_reader.py` for smartcard imports
- Created dummy classes for type hints when smartcard is not available
- Added a global flag `SMARTCARD_AVAILABLE` to check if the library is available

```python
# Add better error handling for smartcard imports
try:
    from smartcard.CardConnection import CardConnection
    from smartcard.System import readers
    from smartcard.reader.Reader import Reader
    SMARTCARD_AVAILABLE = True
except ImportError:
    # Create dummy classes for type hints when smartcard is not available
    class CardConnection:
        def transmit(self, *args, **kwargs):
            pass
        
        def connect(self):
            pass
    
    class Reader:
        def __init__(self):
            self.name = ""
        
        def createConnection(self):
            return CardConnection()
    
    SMARTCARD_AVAILABLE = False
    print("[Warning] pyscard library not available. NFC functionality will be limited.")
```

### 3. Enhanced Error Handling

Added more robust error handling throughout the application:

- Added try-except blocks in `spool_reader.py` methods
- Added checks for `SMARTCARD_AVAILABLE` before attempting NFC operations
- Added detailed error messages and traceback printing

```python
def read_spool(self) -> Optional[dict[str, Any]]:
    """
    Wait for a spool, read it and return its data
    :return: JSON data of the spool on success else None
    """
    if not SMARTCARD_AVAILABLE:
        print("[Error] Cannot read spool: pyscard library not available")
        return None
        
    try:
        card_data: Optional[CardData] = self.reader.read_card()
        if not card_data:
            return None
        spool_data: SpoolData = SpoolData()
        spool_data.pages = card_data.pages
        return spool_data.get_spool_specs()
    except Exception as e:
        print(f"[Error] Failed to read spool: {str(e)}")
        traceback.print_exc()
        return None
```

## Documentation Updates

Updated all documentation files to remove the Python 3.11 requirement and mention Python 3.12 compatibility:

1. Updated `README.md`:
   - Changed "Make sure that Python 3.11 is installed" to "Make sure that Python 3.11 or newer (including Python 3.12) is installed"
   - Updated the FAQ section to remove warnings about newer Python versions

2. Updated `DESKTOP_APP_README.md`:
   - Updated installation requirements to include Python 3.12
   - Updated troubleshooting section to remove warnings about newer Python versions

3. Updated `SCRIPTS_README.md`:
   - Updated requirements to include Python 3.12
   - Updated troubleshooting section to be consistent with Python 3.12 compatibility

4. Updated `install_dependencies.bat`:
   - Changed Python version requirement message to include newer versions

## Windows Long Path Support for Python 3.12

Python 3.12 on Windows may encounter issues with long file paths during package installation. This is a known issue that requires enabling Windows Long Path support. The following changes were made to address this:

- Updated batch scripts to automatically enable Windows Long Path support
- Added detailed error messages and instructions for manual configuration
- Modified the build process to handle long path issues

```batch
echo Enabling Windows Long Path support (may require administrator privileges)...
echo This is required for Python 3.12 on Windows.
echo.
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
```

### Manual Configuration

If the automatic configuration fails, users can manually enable Windows Long Path support:

1. Run Registry Editor (regedit.exe)
2. Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. Set `LongPathsEnabled` to `1`
4. Restart the computer

## PyInstaller Integration

To ensure PyInstaller works correctly with Python 3.12, the following changes were made:

- Added checks to verify PyInstaller is installed
- Automatically install PyInstaller if it's missing
- Use `python -m PyInstaller` instead of directly calling `pyinstaller` to avoid PATH issues

```batch
echo Ensuring pyinstaller is installed...
pip show pyinstaller > nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo pyinstaller not found, installing...
    pip install pyinstaller
)

echo Building the executable...
python -m PyInstaller AnycubicNFCDesktopApp.spec
```

## Testing

The application has been tested with Python 3.12 and works correctly with the following features:

- Web interface functionality
- Desktop application functionality
- NFC reading and writing (when hardware is available)
- All batch scripts and utilities

## Python Detection Improvements

To handle various Python installation scenarios, including Windows Store Python installations and non-standard paths, the batch scripts have been enhanced with robust Python detection:

- Tries multiple Python commands (`python`, `python3`, `py`)
- Checks for specific Python versions using the Python Launcher (`py -3.12`, `py -3.11`, etc.)
- Searches common installation paths
- Provides detailed error messages and troubleshooting steps

```batch
echo Trying to find Python in different locations...

REM Try standard python command
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'python' command.
    set PYTHON_CMD=python
    goto PYTHON_FOUND
)

REM Try python3 command
python3 --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'python3' command.
    set PYTHON_CMD=python3
    goto PYTHON_FOUND
)

REM Try py command
py --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'py' command.
    set PYTHON_CMD=py
    goto PYTHON_FOUND
)

REM Try specific Python installations
for %%V in (3.12 3.11 3.10 3.9) do (
    py -%%V --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo Found Python %%V using 'py -%%V' command.
        set PYTHON_CMD=py -%%V
        goto PYTHON_FOUND
    )
)
```

### Windows Store Python Handling

The scripts now include specific guidance for Windows Store Python installations, which can cause issues with the PATH:

```batch
echo For Windows Store Python installations, you may need to disable app execution aliases:
echo 1. Open Windows Settings
echo 2. Go to Apps ^> Apps ^& features ^> App execution aliases
echo 3. Turn off the Python aliases
```

## Conclusion

These changes make the application compatible with Python 3.12 while maintaining backward compatibility with Python 3.11. The application is now more robust with better error handling and fallback mechanisms for potential compatibility issues. Additional Windows-specific fixes ensure smooth operation on Windows systems with Python 3.12, including:

1. Windows Long Path support for Python 3.12
2. Improved Python detection for various installation scenarios
3. Better error handling and user guidance
4. PyInstaller integration improvements
