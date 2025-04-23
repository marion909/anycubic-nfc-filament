@echo on
setlocal enabledelayedexpansion
echo Building Anycubic NFC Desktop Application (Verbose Mode)...
echo.

echo Step 1: Checking Python installation...
echo.
echo Trying to find Python in different locations...

REM Try standard python command
python --version
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'python' command.
    set PYTHON_CMD=python
    goto PYTHON_FOUND
)

REM Try python3 command
python3 --version
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'python3' command.
    set PYTHON_CMD=python3
    goto PYTHON_FOUND
)

REM Try py command
py --version
if %ERRORLEVEL% EQU 0 (
    echo Found Python using 'py' command.
    set PYTHON_CMD=py
    goto PYTHON_FOUND
)

REM Try specific Python installations
for %%V in (3.12 3.11 3.10 3.9) do (
    py -%%V --version
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
echo Step 2: Checking Windows Long Path support...
echo.
reg query "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled"
echo Registry query result: %ERRORLEVEL%

echo.
echo Step 3: Installing required packages...
echo.
echo Installing required packages one by one for better error tracking...

echo Installing Flask...
%PYTHON_CMD% -m pip install Flask
echo Result: %ERRORLEVEL%

echo Installing pyscard...
%PYTHON_CMD% -m pip install pyscard
echo Result: %ERRORLEVEL%

echo Installing Flask-SocketIO...
%PYTHON_CMD% -m pip install Flask-SocketIO
echo Result: %ERRORLEVEL%

echo Installing eventlet...
%PYTHON_CMD% -m pip install eventlet
echo Result: %ERRORLEVEL%

echo Installing argparse...
%PYTHON_CMD% -m pip install argparse
echo Result: %ERRORLEVEL%

echo Installing PyQt5...
%PYTHON_CMD% -m pip install PyQt5
echo Result: %ERRORLEVEL%

echo Installing PyQtWebEngine...
%PYTHON_CMD% -m pip install PyQtWebEngine
echo Result: %ERRORLEVEL%

echo.
echo Step 4: Ensuring pyinstaller is installed...
%PYTHON_CMD% -m pip show pyinstaller
if %ERRORLEVEL% NEQ 0 (
    echo pyinstaller not found, installing...
    %PYTHON_CMD% -m pip install pyinstaller
    echo Result: %ERRORLEVEL%
) else (
    echo pyinstaller is already installed.
)

echo.
echo Step 5: Building the executable...
echo.
echo Running PyInstaller with verbose output...
echo This may take a while, please be patient...
%PYTHON_CMD% -m PyInstaller --clean AnycubicNFCDesktopApp.spec -v --log-level=DEBUG
echo PyInstaller result: %ERRORLEVEL%
echo Checking if dist directory was created...
if exist dist (
    echo Dist directory exists, listing contents:
    dir dist
) else (
    echo ERROR: Dist directory was not created!
    echo PyInstaller failed to create the dist directory.
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to build the executable. Please check the error message above.
    echo.
    pause
    exit /b 1
)

echo.
echo Build complete! The executable can be found in the 'dist' folder.
echo.
pause
