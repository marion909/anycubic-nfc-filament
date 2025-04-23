@echo off
setlocal enabledelayedexpansion
echo Installing dependencies for Anycubic NFC Desktop Application...
echo.
echo This script will install all required Python packages.
echo.
echo Step 1: Checking Python installation...
echo.
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

REM Check common installation paths
for %%P in ("%LOCALAPPDATA%\Programs\Python\Python312\python.exe" 
            "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
            "C:\Python312\python.exe" 
            "C:\Python311\python.exe"
            "%PROGRAMFILES%\Python312\python.exe"
            "%PROGRAMFILES%\Python311\python.exe") do (
    if exist %%P (
        echo Found Python at %%P
        set PYTHON_CMD=%%P
        goto PYTHON_FOUND
    )
)

echo.
echo Python is not installed or not in PATH.
echo.
echo Please install Python 3.11 or newer from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
echo If Python is already installed, you can:
echo 1. Add Python to your PATH environment variable
echo 2. Create a file named 'python-path.txt' in this directory with the full path to your Python executable
echo.
echo For Windows Store Python installations, you may need to disable app execution aliases:
echo 1. Open Windows Settings
echo 2. Go to Apps ^> Apps ^& features ^> App execution aliases
echo 3. Turn off the Python aliases
echo.
pause
exit /b 1

:PYTHON_FOUND
echo Using Python command: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo Step 2: Enabling Windows Long Path support (may require administrator privileges)...
echo This is required for Python 3.12 on Windows.
echo.
reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to enable Windows Long Path support. This may cause issues with Python 3.12.
    echo You can try running this script as administrator or manually enable Windows Long Path support.
    echo See: https://pip.pypa.io/warnings/enable-long-paths
    echo.
    echo Continuing anyway...
    echo.
)

echo.
echo Step 3: Installing required packages...
%PYTHON_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to install packages. Please check the error message above.
    echo.
    echo If you're using Python 3.12 and seeing a Long Path error, try:
    echo 1. Run this script as administrator
    echo 2. Or manually enable Windows Long Path support:
    echo    - Open Registry Editor (regedit.exe)
    echo    - Navigate to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
    echo    - Set LongPathsEnabled to 1
    echo    - Restart your computer
    echo.
    pause
    exit /b 1
)

echo.
echo All dependencies have been successfully installed!
echo You can now run the application using run_desktop_app.bat or build the executable using build_desktop_app.bat.
echo.
pause
