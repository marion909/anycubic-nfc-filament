import sys
import os
import threading
import webbrowser
import time
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon

from anycubic_nfc_app.web_app import app, socketio

# Function to find an available port
def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    port = start_port
    for _ in range(max_attempts):
        try:
            # Try to create a socket with the port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            print(f"Port {port} is already in use, trying next port")
            port += 1
    print(f"Could not find an available port after {max_attempts} attempts")
    return None

# Find an available port
PORT = find_available_port()
if PORT is None:
    print("Error: Could not find an available port. Exiting.")
    sys.exit(1)
print(f"Using port: {PORT}")

def run_flask(port):
    """Run the Flask app in a separate thread"""
    try:
        print(f"Starting Flask server on port {port}...")
        from anycubic_nfc_app.web_app import start_web_app
        start_web_app(port, is_desktop_app=True)
    except Exception as e:
        print(f"Error starting Flask server: {str(e)}")

class AnycubicNFCApp(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Anycubic NFC App")
        self.setMinimumSize(1024, 768)
        
        # Set application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                "anycubic_nfc_app", "static", "images", "favicon", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl(f"http://127.0.0.1:{port}"))
        layout.addWidget(self.web_view)

def check_server_running(port, max_attempts=10, delay=0.5):
    """Check if the server is running by attempting to connect to it"""
    for attempt in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', port))
                return True
        except ConnectionRefusedError:
            time.sleep(delay)
    return False

def main():
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask, args=(PORT,), daemon=True)
    flask_thread.start()
    
    # Give Flask time to start
    time.sleep(2)
    
    # Check if server is running
    server_running = check_server_running(PORT)
    if not server_running:
        print("WARNING: Could not connect to Flask server, but continuing anyway...")
    
    # Create Qt application
    qt_app = QApplication(sys.argv)
    
    # Create and show main window
    window = AnycubicNFCApp(PORT)
    window.show()
    
    # Run the application
    sys.exit(qt_app.exec_())

if __name__ == "__main__":
    main()
