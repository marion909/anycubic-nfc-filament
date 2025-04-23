@echo off
echo Anycubic NFC Desktop Application Setup
echo =====================================
echo.
echo This script will guide you through the setup process for the Anycubic NFC Desktop Application.
echo.

:MENU
echo Please select an option:
echo 1. Install dependencies
echo 2. Test dependencies
echo 3. Run the application (from source)
echo 4. Build the executable
echo 5. Clean build artifacts
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto INSTALL
if "%choice%"=="2" goto TEST
if "%choice%"=="3" goto RUN
if "%choice%"=="4" goto BUILD
if "%choice%"=="5" goto CLEAN
if "%choice%"=="6" goto END

echo Invalid choice. Please try again.
echo.
goto MENU

:INSTALL
echo.
echo Installing dependencies...
call install_dependencies.bat
echo.
goto MENU

:TEST
echo.
echo Testing dependencies...
call test_dependencies.bat
echo.
goto MENU

:RUN
echo.
echo Running the application...
call run_desktop_app.bat
echo.
goto MENU

:BUILD
echo.
echo Building the executable...
call build_desktop_app.bat
echo.
goto MENU

:CLEAN
echo.
echo Cleaning build artifacts...
call clean_build.bat
echo.
goto MENU

:END
echo.
echo Thank you for using the Anycubic NFC Desktop Application Setup.
echo.
pause
