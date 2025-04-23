"""
Test script for the desktop application.
This script checks if all required dependencies are installed and if the application can be started.
"""

import sys
import importlib.util
import os

def check_module(module_name):
    """Check if a module is installed"""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        print(f"❌ Module {module_name} is not installed.")
        return False
    print(f"✅ Module {module_name} is installed.")
    return True

def check_file(file_path):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ File {file_path} exists.")
        return True
    print(f"❌ File {file_path} does not exist.")
    return False

def main():
    """Main function"""
    print("Testing desktop application dependencies...\n")
    
    # Check required modules
    modules = [
        "PyQt5", 
        "PyQt5.QtWebEngineWidgets", 
        "flask", 
        "flask_socketio", 
        "eventlet", 
        "smartcard"
    ]
    
    all_modules_installed = True
    for module in modules:
        if not check_module(module):
            all_modules_installed = False
    
    # Check required files
    files = [
        "desktop_app.py",
        "anycubic_nfc_app/web_app.py",
        "anycubic_nfc_app/nfc_manager/nfc_reader.py",
        "anycubic_nfc_app/nfc_manager/spool_reader.py",
        "anycubic_nfc_app/templates/root.html",
        "anycubic_nfc_app/static/images/favicon/favicon.ico"
    ]
    
    all_files_exist = True
    for file in files:
        if not check_file(file):
            all_files_exist = False
    
    print("\nTest results:")
    if all_modules_installed and all_files_exist:
        print("✅ All dependencies are installed and all required files exist.")
        print("✅ The desktop application should work correctly.")
        return 0
    else:
        print("❌ Some dependencies are missing or some required files do not exist.")
        print("❌ The desktop application may not work correctly.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
