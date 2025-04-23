@echo off
setlocal enabledelayedexpansion
echo Starting Anycubic NFC Desktop Application...
echo.

echo Checking Python installation...
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
echo Starting application...
%PYTHON_CMD% desktop_app.py
