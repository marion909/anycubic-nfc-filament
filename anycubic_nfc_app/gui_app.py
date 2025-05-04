import sys
import os
import json
from typing import Any, Optional, Dict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, 
                            QHBoxLayout, QLabel, QComboBox, QLineEdit, QTabWidget, 
                            QFormLayout, QSpinBox, QDoubleSpinBox, QColorDialog, QMessageBox,
                            QStatusBar, QFileDialog, QGroupBox, QSizePolicy, QFrame,
                            QStyle, QScrollArea, QToolTip)
from PyQt5.QtGui import QColor, QPixmap, QIcon, QFont, QPalette, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize

from .nfc_manager import SpoolReader, SpoolData, NFCReader


class NFCThread(QThread):
    """Thread for NFC operations to prevent GUI freezing"""
    read_complete = pyqtSignal(object)
    write_complete = pyqtSignal(bool)
    dump_complete = pyqtSignal(tuple)
    
    def __init__(self, spool_reader, mode='read', data=None):
        super().__init__()
        self.spool_reader = spool_reader
        self.mode = mode
        self.data = data
    
    def run(self):
        if self.mode == 'read':
            data = self.spool_reader.read_spool()
            self.read_complete.emit(data)
        elif self.mode == 'write':
            success = self.spool_reader.write_spool(self.data)
            self.write_complete.emit(success)
        elif self.mode == 'dump':
            uid, dump_data = self.spool_reader.read_spool_raw()
            self.dump_complete.emit((uid, dump_data))


class ColorButton(QPushButton):
    """Custom button for color selection"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 255, 255)
        self.clicked.connect(self.show_color_dialog)
        self.update_color()
        self.setMinimumHeight(40)
        self.setToolTip("Klicken Sie hier, um eine Filamentfarbe auszuwählen")
        
    def show_color_dialog(self):
        color = QColorDialog.getColor(self.color, self.parent(), "Filamentfarbe auswählen")
        if color.isValid():
            self.color = color
            self.update_color()
            
    def update_color(self):
        self.setStyleSheet(f"""
            QPushButton {{ 
                background-color: {self.color.name()}; 
                min-height: 40px;
                border: 2px solid #888;
                border-radius: 5px;
            }}
            QPushButton:hover {{ 
                border: 2px solid #555;
            }}
        """)
        
    def get_hex_color(self):
        return self.color.name()
        
    def set_hex_color(self, hex_color):
        if hex_color and hex_color.startswith('#'):
            self.color = QColor(hex_color)
            self.update_color()


class StyledButton(QPushButton):
    """Custom styled button with consistent look and feel"""
    def __init__(self, text, icon_name=None, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        
        if icon_name:
            self.setIcon(self.style().standardIcon(getattr(QStyle, icon_name)))
            self.setIconSize(QSize(20, 20))
            
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)


class CancelButton(QPushButton):
    """Styled cancel button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.setIconSize(QSize(20, 20))
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #922b21;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)


class SaveButton(QPushButton):
    """Styled save button"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(40)
        self.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.setIconSize(QSize(20, 20))
        
        self.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)


class RangeWidget(QGroupBox):
    """Widget for temperature/speed range settings"""
    def __init__(self, title, has_speed=False, parent=None):
        super().__init__(title, parent)
        self.has_speed = has_speed
        self.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        layout.setContentsMargins(15, 20, 15, 10)
        layout.setSpacing(10)
        
        if has_speed:
            self.speed_min = QSpinBox()
            self.speed_min.setRange(0, 1000)
            self.speed_min.setSingleStep(10)
            self.speed_min.setMinimumHeight(30)
            self.speed_min.setToolTip("Minimale Druckgeschwindigkeit in mm/s")
            
            self.speed_max = QSpinBox()
            self.speed_max.setRange(0, 1000)
            self.speed_max.setSingleStep(10)
            self.speed_max.setMinimumHeight(30)
            self.speed_max.setToolTip("Maximale Druckgeschwindigkeit in mm/s")
            
            speed_layout = QHBoxLayout()
            speed_layout.addWidget(self.speed_min)
            speed_layout.addWidget(QLabel("-"))
            speed_layout.addWidget(self.speed_max)
            
            layout.addRow(QLabel("Geschwindigkeit (mm/s):"), speed_layout)
        
        self.nozzle_min = QSpinBox()
        self.nozzle_min.setRange(0, 350)
        self.nozzle_min.setMinimumHeight(30)
        self.nozzle_min.setToolTip("Minimale Düsentemperatur in °C")
        
        self.nozzle_max = QSpinBox()
        self.nozzle_max.setRange(0, 350)
        self.nozzle_max.setMinimumHeight(30)
        self.nozzle_max.setToolTip("Maximale Düsentemperatur in °C")
        
        nozzle_layout = QHBoxLayout()
        nozzle_layout.addWidget(self.nozzle_min)
        nozzle_layout.addWidget(QLabel("-"))
        nozzle_layout.addWidget(self.nozzle_max)
        
        layout.addRow(QLabel("Düsentemperatur (°C):"), nozzle_layout)
        
        self.setLayout(layout)
        
    def get_data(self):
        data = {
            "nozzle_min": self.nozzle_min.value(),
            "nozzle_max": self.nozzle_max.value()
        }
        if self.has_speed:
            data["speed_min"] = self.speed_min.value()
            data["speed_max"] = self.speed_max.value()
        return data
        
    def set_data(self, data):
        if not data:
            return
            
        self.nozzle_min.setValue(data.get("nozzle_min", 0))
        self.nozzle_max.setValue(data.get("nozzle_max", 0))
        
        if self.has_speed:
            self.speed_min.setValue(data.get("speed_min", 0))
            self.speed_max.setValue(data.get("speed_max", 0))


class StyledScrollLabel(QScrollArea):
    """Scrollable label with styling for display data"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Sunken)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.content = QLabel("Keine Daten")
        self.content.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.content.setWordWrap(True)
        self.content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.content.setCursor(Qt.IBeamCursor)
        self.content.setStyleSheet("""
            background-color: #f8f9fa;
            padding: 10px;
            font-family: Consolas, monospace;
        """)
        
        self.setWidget(self.content)
        
    def setText(self, text):
        self.content.setText(text)
        
    def text(self):
        return self.content.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # NFC reader setup
        self.spool_reader = SpoolReader()
        self.current_nfc_thread = None
        
        # Load filament presets
        self.load_filament_presets()
        
        # Setup UI
        self.init_ui()
        
    def load_filament_presets(self):
        self.filament_presets = {
            "PLA": {
                "type": "PLA",
                "range_a": {
                    "nozzle_min": 190,
                    "nozzle_max": 230
                },
                "bed_min": 50,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PLA+": {
                "type": "PLA+",
                "range_a": {
                    "nozzle_min": 190,
                    "nozzle_max": 230
                },
                "bed_min": 50,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PLA High Speed": {
                "type": "PLA High Speed",
                "range_a": {
                    "speed_min": 50,
                    "speed_max": 150,
                    "nozzle_min": 190,
                    "nozzle_max": 210
                },
                "range_b": {
                    "speed_min": 150,
                    "speed_max": 300,
                    "nozzle_min": 210,
                    "nozzle_max": 230
                },
                "range_c": {
                    "speed_min": 300,
                    "speed_max": 600,
                    "nozzle_min": 230,
                    "nozzle_max": 260
                },
                "bed_min": 50,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PLA Matte": {
                "type": "PLA Matte",
                "range_a": {
                    "nozzle_min": 210,
                    "nozzle_max": 230
                },
                "bed_min": 50,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PLA Silk": {
                "type": "PLA Silk",
                "range_a": {
                    "nozzle_min": 215,
                    "nozzle_max": 230
                },
                "bed_min": 50,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PETG": {
                "type": "PETG",
                "range_a": {
                    "nozzle_min": 220,
                    "nozzle_max": 260
                },
                "bed_min": 70,
                "bed_max": 90,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "ASA": {
                "type": "ASA",
                "range_a": {
                    "nozzle_min": 240,
                    "nozzle_max": 280
                },
                "bed_min": 90,
                "bed_max": 110,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "ABS": {
                "type": "ABS",
                "range_a": {
                    "nozzle_min": 240,
                    "nozzle_max": 280
                },
                "bed_min": 80,
                "bed_max": 100,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "TPU": {
                "type": "TPU",
                "range_a": {
                    "nozzle_min": 210,
                    "nozzle_max": 250
                },
                "bed_min": 30,
                "bed_max": 60,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
            "PLA Luminous": {
                "type": "PLA Luminous",
                "range_a": {
                    "nozzle_min": 190,
                    "nozzle_max": 230
                },
                "bed_min": 35,
                "bed_max": 45,
                "diameter": 1.75,
                "length": 330,
                "weight": 1000
            },
        }
        
    def apply_global_styles(self):
        """Apply global stylesheet to the application"""
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
                background-color: white;
                border-radius: 5px;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                min-width: 120px;
                min-height: 35px;
                padding: 5px 15px;
                margin-right: 2px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                margin-bottom: -1px;
            }
            QTabBar::tab:!selected {
                margin-top: 2px;
            }
            QTabBar::tab:hover {
                background-color: #d6dbdf;
            }
            QLabel {
                color: #2c3e50;
            }
            QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox {
                min-height: 30px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 2px 10px;
                background-color: white;
            }
            QComboBox:hover, QLineEdit:hover, QSpinBox:hover, QDoubleSpinBox:hover {
                border: 1px solid #3498db;
            }
            QComboBox::down-arrow {
                image: url("down-arrow.png");
                width: 16px;
                height: 16px;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button {
                border-left: 1px solid #bdc3c7;
                border-bottom: 1px solid #bdc3c7;
                border-top-right-radius: 3px;
                background-color: #f5f5f5;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button {
                border-left: 1px solid #bdc3c7;
                border-top-right-radius: 3px;
                background-color: #f5f5f5;
            }
            QStatusBar {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
            }
            QToolTip {
                background-color: #2c3e50;
                color: white;
                border: none;
                padding: 5px;
                opacity: 200;
            }
        """)
        
    def init_ui(self):
        self.setWindowTitle('Anycubic NFC Filament Tool')
        self.setMinimumSize(800, 600)
        
        # Apply global styles
        self.apply_global_styles()
        
        # Try to set a better font
        QFontDatabase.addApplicationFont(":/fonts/OpenSans-Regular.ttf")
        self.setFont(QFont("Open Sans", 10))
        
        # Set app icon
        icon_path = os.path.join(os.path.dirname(__file__), "static", "images", "nfc.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
        # Header with title and NFC status
        header_layout = QHBoxLayout()
        header_title = QLabel("Anycubic ACE Pro NFC Filament Tool")
        header_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        self.nfc_status_label = QLabel("")
        self.update_nfc_status_display()
        
        header_layout.addWidget(header_title)
        header_layout.addStretch(1)
        header_layout.addWidget(self.nfc_status_label)
        main_layout.addLayout(header_layout)
        
        # Add a divider line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #bdc3c7;")
        main_layout.addWidget(divider)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(False)
        self.write_tab = QWidget()
        self.read_tab = QWidget()
        self.dump_tab = QWidget()
        
        self.tabs.addTab(self.write_tab, "NFC Tag schreiben")
        self.tabs.addTab(self.read_tab, "NFC Tag lesen")
        self.tabs.addTab(self.dump_tab, "Raw Dump erstellen")
        
        # Setup tabs
        self.setup_write_tab()
        self.setup_read_tab()
        self.setup_dump_tab()
        
        main_layout.addWidget(self.tabs)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.status_bar.setSizeGripEnabled(False)
        self.setStatusBar(self.status_bar)
        
        # Check NFC reader connection
        if self.spool_reader.get_connection_state():
            self.status_bar.showMessage("NFC Reader verbunden")
        else:
            self.status_bar.showMessage("Kein NFC Reader gefunden", 0)
        
        # Set central widget
        self.setCentralWidget(main_widget)
        
    def update_nfc_status_display(self):
        """Updates the NFC status display with icon"""
        is_connected = self.spool_reader.get_connection_state()
        
        if is_connected:
            self.nfc_status_label.setText("NFC Reader verbunden")
            self.nfc_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            self.nfc_status_label.setText("Kein NFC Reader verbunden")
            self.nfc_status_label.setStyleSheet("color: #c0392b; font-weight: bold;")
        
    def setup_write_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Add introduction text
        intro = QLabel("Hier können Sie einen NFC-Tag mit Filament-Daten für Ihren Anycubic ACE Pro 3D-Drucker beschreiben.")
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 11px; color: #7f8c8d; margin-bottom: 10px; max-height: 50px;")
        layout.addWidget(intro)
        
        # Top section - Filament type selection in a group box
        type_group = QGroupBox("Filament-Typ")
        type_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        type_layout = QHBoxLayout()
        
        self.filament_type = QComboBox()
        self.filament_type.setToolTip("Wählen Sie den Filament-Typ aus")
        for filament in SpoolData.get_available_filament_types():
            self.filament_type.addItem(filament)
        self.filament_type.setMinimumHeight(35)
        self.filament_type.setMinimumWidth(200)
        self.filament_type.currentTextChanged.connect(self.filament_type_changed)
        
        type_layout.addWidget(QLabel("Filament Typ:"))
        type_layout.addWidget(self.filament_type, 1)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # Middle section - Form with filament properties
        properties_group = QGroupBox("Filament-Eigenschaften")
        properties_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setContentsMargins(15, 20, 15, 10)
        form_layout.setSpacing(10)
        
        # Manufacturer
        self.manufacturer = QLineEdit("AC")
        self.manufacturer.setMinimumHeight(35)
        self.manufacturer.setPlaceholderText("Herstellername eingeben")
        self.manufacturer.setToolTip("Name des Filament-Herstellers (z.B. 'AC' für Anycubic)")
        form_layout.addRow(QLabel("Hersteller:"), self.manufacturer)
        
        # Color selector
        color_label = QLabel("Farbe:")
        self.color_button = ColorButton()
        form_layout.addRow(color_label, self.color_button)
        
        # Bed temperature
        bed_label = QLabel("Bett Temperatur (°C):")
        
        bed_layout = QHBoxLayout()
        self.bed_min = QSpinBox()
        self.bed_min.setMinimumHeight(35)
        self.bed_min.setRange(0, 150)
        self.bed_min.setToolTip("Minimale Bett-Temperatur in °C")
        
        self.bed_max = QSpinBox()
        self.bed_max.setMinimumHeight(35)
        self.bed_max.setRange(0, 150)
        self.bed_max.setToolTip("Maximale Bett-Temperatur in °C")
        
        bed_layout.addWidget(self.bed_min)
        bed_layout.addWidget(QLabel("-"))
        bed_layout.addWidget(self.bed_max)
        
        form_layout.addRow(bed_label, bed_layout)
        
        # Filament properties
        self.diameter = QDoubleSpinBox()
        self.diameter.setMinimumHeight(35)
        self.diameter.setRange(1.0, 3.0)
        self.diameter.setSingleStep(0.05)
        self.diameter.setValue(1.75)
        self.diameter.setToolTip("Standard: 1.75mm für die meisten Anycubic Drucker")
        
        self.length = QSpinBox()
        self.length.setMinimumHeight(35)
        self.length.setRange(0, 1000)
        self.length.setValue(330)
        self.length.setToolTip("Länge des Filaments auf der Spule")
        
        self.weight = QSpinBox()
        self.weight.setMinimumHeight(35)
        self.weight.setRange(0, 10000)
        self.weight.setValue(1000)
        self.weight.setToolTip("Gewicht des Filaments auf der Spule (typischerweise 1000g)")
        
        form_layout.addRow(QLabel("Durchmesser (mm):"), self.diameter)
        form_layout.addRow(QLabel("Länge (m):"), self.length)
        form_layout.addRow(QLabel("Gewicht (g):"), self.weight)
        
        properties_group.setLayout(form_layout)
        layout.addWidget(properties_group)
        
        # Range tabs in a group
        temp_group = QGroupBox("Temperatur- und Geschwindigkeitsbereiche")
        temp_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        temp_layout = QVBoxLayout()
        self.range_tabs = QTabWidget()
        self.range_tabs.setDocumentMode(True)
        self.range_tabs.setStyleSheet("""
            QTabBar::tab {
                min-width: 80px;
            }
        """)
        
        # Range A (required)
        self.range_a = RangeWidget("Hauptbereich (A)", has_speed=True)
        self.range_tabs.addTab(self.range_a, "Bereich A")
        
        # Range B (optional)
        self.range_b = RangeWidget("Zusätzlicher Bereich (B)", has_speed=True)
        self.range_tabs.addTab(self.range_b, "Bereich B")
        
        # Range C (optional)
        self.range_c = RangeWidget("Zusätzlicher Bereich (C)", has_speed=True)
        self.range_tabs.addTab(self.range_c, "Bereich C")
        
        temp_layout.addWidget(self.range_tabs)
        temp_group.setLayout(temp_layout)
        layout.addWidget(temp_group)
        
        # Bottom section - Write button
        button_layout = QHBoxLayout()
        self.write_button = StyledButton("NFC Tag schreiben", "SP_DialogApplyButton")
        self.write_button.setMinimumWidth(200)
        self.write_button.clicked.connect(self.start_write_tag)
        self.write_button.setToolTip("Startet den Schreibvorgang. Halten Sie den NFC Tag bereit.")
        
        self.cancel_write_button = CancelButton("Abbrechen")
        self.cancel_write_button.clicked.connect(self.cancel_nfc_operation)
        self.cancel_write_button.setEnabled(False)
        self.cancel_write_button.setToolTip("Bricht den laufenden Schreibvorgang ab")
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.write_button)
        button_layout.addWidget(self.cancel_write_button)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        layout.addStretch(1)
        
        # Apply layout
        self.write_tab.setLayout(layout)
        
        # Set initial values from first filament type
        self.filament_type_changed(self.filament_type.currentText())
        
    def setup_read_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Add introduction text
        intro = QLabel("Lesen Sie die Daten eines beschriebenen NFC-Tags aus.")
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 11px; color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(intro)
        
        # Middle section - Data display
        data_group = QGroupBox("Tag-Daten")
        data_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        data_layout = QVBoxLayout()
        self.read_data = StyledScrollLabel()
        data_layout.addWidget(self.read_data)
        data_group.setLayout(data_layout)
        
        layout.addWidget(data_group, 1)
        
        # Bottom section - Read button
        button_layout = QHBoxLayout()
        self.read_button = StyledButton("NFC Tag lesen", "SP_DialogResetButton")
        self.read_button.setMinimumWidth(200)
        self.read_button.clicked.connect(self.start_read_tag)
        self.read_button.setToolTip("Startet den Lesevorgang. Halten Sie den NFC Tag bereit.")
        
        self.cancel_read_button = CancelButton("Abbrechen")
        self.cancel_read_button.clicked.connect(self.cancel_nfc_operation)
        self.cancel_read_button.setEnabled(False)
        self.cancel_read_button.setToolTip("Bricht den laufenden Lesevorgang ab")
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.read_button)
        button_layout.addWidget(self.cancel_read_button)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        
        # Apply layout
        self.read_tab.setLayout(layout)
        
    def setup_dump_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Add introduction text
        intro = QLabel("Erstellen Sie einen Raw-Dump des NFC-Tags für Diagnosezwecke oder zur Analyse.")
        intro.setWordWrap(True)
        intro.setStyleSheet("font-size: 11px; color: #7f8c8d; margin-bottom: 10px;")
        layout.addWidget(intro)
        
        # Middle section - Data display
        data_group = QGroupBox("Dump-Daten")
        data_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        data_layout = QVBoxLayout()
        self.dump_data = StyledScrollLabel()
        data_layout.addWidget(self.dump_data)
        data_group.setLayout(data_layout)
        
        layout.addWidget(data_group, 1)
        
        # Bottom section - Buttons
        button_layout = QHBoxLayout()
        self.dump_button = StyledButton("Dump erstellen", "SP_DialogResetButton")
        self.dump_button.setMinimumWidth(150)
        self.dump_button.clicked.connect(self.start_create_dump)
        self.dump_button.setToolTip("Erstellt einen Dump des NFC Tags. Halten Sie den Tag bereit.")
        
        self.save_dump_button = SaveButton("Dump speichern")
        self.save_dump_button.setMinimumWidth(150)
        self.save_dump_button.clicked.connect(self.save_dump)
        self.save_dump_button.setEnabled(False)
        self.save_dump_button.setToolTip("Speichert den Dump als Textdatei")
        
        self.cancel_dump_button = CancelButton("Abbrechen")
        self.cancel_dump_button.clicked.connect(self.cancel_nfc_operation)
        self.cancel_dump_button.setEnabled(False)
        self.cancel_dump_button.setToolTip("Bricht den laufenden Dump-Vorgang ab")
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.dump_button)
        button_layout.addWidget(self.save_dump_button)
        button_layout.addWidget(self.cancel_dump_button)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        
        # Apply layout
        self.dump_tab.setLayout(layout)
        
    def filament_type_changed(self, filament_type):
        """Update the form with preset values when filament type changes"""
        if filament_type in self.filament_presets:
            preset = self.filament_presets[filament_type]
            
            # Update bed temperatures
            self.bed_min.setValue(preset.get("bed_min", 0))
            self.bed_max.setValue(preset.get("bed_max", 0))
            
            # Update filament properties
            self.diameter.setValue(preset.get("diameter", 1.75))
            self.length.setValue(preset.get("length", 330))
            self.weight.setValue(preset.get("weight", 1000))
            
            # Update ranges
            if "range_a" in preset:
                self.range_a.set_data(preset["range_a"])
            if "range_b" in preset:
                self.range_b.set_data(preset["range_b"])
            else:
                self.range_b.set_data({"nozzle_min": 0, "nozzle_max": 0, "speed_min": 0, "speed_max": 0})
            if "range_c" in preset:
                self.range_c.set_data(preset["range_c"])
            else:
                self.range_c.set_data({"nozzle_min": 0, "nozzle_max": 0, "speed_min": 0, "speed_max": 0})
    
    def get_form_data(self):
        """Collect all form data into a dictionary for writing to NFC tag"""
        data = {
            "type": self.filament_type.currentText(),
            "manufacturer": self.manufacturer.text(),
            "color": self.color_button.get_hex_color(),
            "bed_min": self.bed_min.value(),
            "bed_max": self.bed_max.value(),
            "diameter": self.diameter.value(),
            "length": self.length.value(),
            "weight": self.weight.value(),
            "range_a": self.range_a.get_data()
        }
        
        # Add optional ranges if they have values
        range_b_data = self.range_b.get_data()
        if range_b_data["nozzle_min"] > 0 or range_b_data["nozzle_max"] > 0:
            data["range_b"] = range_b_data
            
        range_c_data = self.range_c.get_data()
        if range_c_data["nozzle_min"] > 0 or range_c_data["nozzle_max"] > 0:
            data["range_c"] = range_c_data
            
        return data
    
    def start_write_tag(self):
        """Start the NFC tag writing process"""
        if not self.spool_reader.get_connection_state():
            QMessageBox.warning(self, "Fehler", "Kein NFC Reader gefunden. Bitte schließen Sie einen kompatiblen NFC Reader an und starten Sie die Anwendung neu.")
            return
            
        self.status_bar.showMessage("Warte auf NFC Tag zum Beschreiben... Halten Sie ein Tag an den Reader.", 0)
        self.write_button.setEnabled(False)
        self.cancel_write_button.setEnabled(True)
        
        data = self.get_form_data()
        self.current_nfc_thread = NFCThread(self.spool_reader, 'write', data)
        self.current_nfc_thread.write_complete.connect(self.on_write_complete)
        self.current_nfc_thread.start()
    
    def start_read_tag(self):
        """Start the NFC tag reading process"""
        if not self.spool_reader.get_connection_state():
            QMessageBox.warning(self, "Fehler", "Kein NFC Reader gefunden. Bitte schließen Sie einen kompatiblen NFC Reader an und starten Sie die Anwendung neu.")
            return
            
        self.status_bar.showMessage("Warte auf NFC Tag zum Lesen... Halten Sie ein Tag an den Reader.", 0)
        self.read_button.setEnabled(False)
        self.cancel_read_button.setEnabled(True)
        
        self.current_nfc_thread = NFCThread(self.spool_reader, 'read')
        self.current_nfc_thread.read_complete.connect(self.on_read_complete)
        self.current_nfc_thread.start()
    
    def start_create_dump(self):
        """Start the NFC tag dump process"""
        if not self.spool_reader.get_connection_state():
            QMessageBox.warning(self, "Fehler", "Kein NFC Reader gefunden. Bitte schließen Sie einen kompatiblen NFC Reader an und starten Sie die Anwendung neu.")
            return
            
        self.status_bar.showMessage("Warte auf NFC Tag zum Erstellen eines Dumps... Halten Sie ein Tag an den Reader.", 0)
        self.dump_button.setEnabled(False)
        self.save_dump_button.setEnabled(False)
        self.cancel_dump_button.setEnabled(True)
        
        self.current_nfc_thread = NFCThread(self.spool_reader, 'dump')
        self.current_nfc_thread.dump_complete.connect(self.on_dump_complete)
        self.current_nfc_thread.start()
    
    def cancel_nfc_operation(self):
        """Cancel any ongoing NFC operation"""
        if self.current_nfc_thread and self.current_nfc_thread.isRunning():
            self.spool_reader.cancel_wait_for_tag()
            self.status_bar.showMessage("NFC Operation abgebrochen", 5000)
        
        self.write_button.setEnabled(True)
        self.read_button.setEnabled(True)
        self.dump_button.setEnabled(True)
        self.cancel_write_button.setEnabled(False)
        self.cancel_read_button.setEnabled(False)
        self.cancel_dump_button.setEnabled(False)
    
    def on_write_complete(self, success):
        """Handle write completion"""
        self.write_button.setEnabled(True)
        self.cancel_write_button.setEnabled(False)
        
        if success:
            self.status_bar.showMessage("NFC Tag erfolgreich beschrieben", 5000)
            QMessageBox.information(self, "Erfolg", 
                                   "NFC Tag wurde erfolgreich beschrieben.\n\n"
                                   "Sie können dieses Tag nun mit Ihrem Anycubic ACE Pro 3D-Drucker verwenden.")
        else:
            self.status_bar.showMessage("Fehler beim Beschreiben des NFC Tags", 5000)
            QMessageBox.warning(self, "Fehler", 
                               "Fehler beim Beschreiben des NFC Tags.\n\n"
                               "Bitte versuchen Sie es erneut und stellen Sie sicher, dass der NFC Tag kompatibel ist "
                               "und richtig am Reader platziert wurde.")
    
    def on_read_complete(self, data):
        """Handle read completion"""
        self.read_button.setEnabled(True)
        self.cancel_read_button.setEnabled(False)
        
        if data:
            self.status_bar.showMessage("NFC Tag erfolgreich gelesen", 5000)
            # Format the JSON nicely with a custom format function
            formatted_json = self.format_json_output(data)
            self.read_data.setText(formatted_json)
        else:
            self.status_bar.showMessage("Fehler beim Lesen des NFC Tags", 5000)
            self.read_data.setText("Keine Daten")
            QMessageBox.warning(self, "Fehler", 
                               "Fehler beim Lesen des NFC Tags.\n\n"
                               "Bitte versuchen Sie es erneut und stellen Sie sicher, dass der NFC Tag richtig am Reader platziert wurde.")
    
    def format_json_output(self, data):
        """Format JSON data in a more readable way"""
        try:
            # Convert the Python dictionary to a formatted string
            formatted = "Filament-Daten\n"
            formatted += "═════════════\n\n"
            
            # Basic info
            formatted += f"Typ:         {data.get('type', 'Unbekannt')}\n"
            formatted += f"Hersteller:  {data.get('manufacturer', 'Unbekannt')}\n"
            formatted += f"Farbe:       {data.get('color', '#FFFFFF')}\n"
            formatted += f"Durchmesser: {data.get('diameter', 1.75)} mm\n"
            formatted += f"Länge:       {data.get('length', 0)} m\n"
            formatted += f"Gewicht:     {data.get('weight', 0)} g\n\n"
            
            # Bed temperature
            formatted += f"Bett-Temperatur: {data.get('bed_min', 0)} - {data.get('bed_max', 0)} °C\n\n"
            
            # Ranges
            if 'range_a' in data:
                formatted += "Bereich A:\n"
                if 'speed_min' in data['range_a'] and 'speed_max' in data['range_a']:
                    formatted += f"  Geschwindigkeit: {data['range_a'].get('speed_min', 0)} - {data['range_a'].get('speed_max', 0)} mm/s\n"
                formatted += f"  Düsentemp.:    {data['range_a'].get('nozzle_min', 0)} - {data['range_a'].get('nozzle_max', 0)} °C\n\n"
            
            if 'range_b' in data:
                formatted += "Bereich B:\n"
                if 'speed_min' in data['range_b'] and 'speed_max' in data['range_b']:
                    formatted += f"  Geschwindigkeit: {data['range_b'].get('speed_min', 0)} - {data['range_b'].get('speed_max', 0)} mm/s\n"
                formatted += f"  Düsentemp.:    {data['range_b'].get('nozzle_min', 0)} - {data['range_b'].get('nozzle_max', 0)} °C\n\n"
            
            if 'range_c' in data:
                formatted += "Bereich C:\n"
                if 'speed_min' in data['range_c'] and 'speed_max' in data['range_c']:
                    formatted += f"  Geschwindigkeit: {data['range_c'].get('speed_min', 0)} - {data['range_c'].get('speed_max', 0)} mm/s\n"
                formatted += f"  Düsentemp.:    {data['range_c'].get('nozzle_min', 0)} - {data['range_c'].get('nozzle_max', 0)} °C\n\n"
            
            # Additional technical info
            formatted += f"UID: {data.get('uid', 'Unbekannt')}\n"
            
            # Raw data for advanced users
            if 'raw' in data:
                formatted += "\nRohdaten für fortgeschrittene Benutzer:\n"
                for key, value in data['raw'].items():
                    formatted += f"  {key}: {value}\n"
            
            return formatted
        except Exception:
            # Fallback to regular json if formatting fails
            return json.dumps(data, indent=4)
    
    def on_dump_complete(self, dump_data):
        """Handle dump completion"""
        uid, data = dump_data
        self.dump_button.setEnabled(True)
        self.cancel_dump_button.setEnabled(False)
        
        if data:
            self.status_bar.showMessage("Dump erfolgreich erstellt", 5000)
            self.dump_data.setText(data)
            self.save_dump_button.setEnabled(True)
            self.current_dump_uid = uid
        else:
            self.status_bar.showMessage("Fehler beim Erstellen des Dumps", 5000)
            self.dump_data.setText("Keine Daten")
            self.save_dump_button.setEnabled(False)
            QMessageBox.warning(self, "Fehler", 
                               "Fehler beim Erstellen des Dumps.\n\n"
                               "Bitte versuchen Sie es erneut und stellen Sie sicher, dass der NFC Tag richtig am Reader platziert wurde.")
    
    def save_dump(self):
        """Save dump data to file"""
        if not hasattr(self, 'current_dump_uid') or not self.dump_data.text() or self.dump_data.text() == "Keine Daten":
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Dump speichern",
            f"spool_dump_{self.current_dump_uid}.txt",
            "Textdateien (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.dump_data.text())
                self.status_bar.showMessage(f"Dump wurde gespeichert als {filename}", 5000)
                QMessageBox.information(self, "Speichern erfolgreich", f"Der Dump wurde erfolgreich gespeichert als:\n{filename}")
            except Exception as e:
                QMessageBox.warning(self, "Fehler", f"Fehler beim Speichern der Datei: {str(e)}")


def start_gui_app():
    """
    Start the GUI application
    """
    # Parse arguments for NFC reader selection
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--print_readers', action='store_true',
                      help='Add this flag to print connected readers on startup')
    parser.add_argument('--preferred_reader', type=str, default=None,
                      help='Default reader to select (the reader name must contain that)')
    args = parser.parse_args()

    # Print connected readers if requested
    if args.print_readers:
        from smartcard.System import readers
        connected_readers = [r.name.lower() for r in readers()]
        print(f"Connected readers: {connected_readers}\n")

    # Set preferred reader if specified
    if args.preferred_reader:
        print(f"Set '{args.preferred_reader}' as preferred reader (the reader name must contain that)\n")
        NFCReader.preferred_reader = args.preferred_reader

    # Set high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Start the application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())