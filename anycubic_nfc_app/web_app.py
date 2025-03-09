from typing import Any

from flask import Flask, render_template

from .nfc_manager import SpoolReader

# App settings
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Max upload size of 1MB

filament_presets: dict[str, dict[str, Any]] = {
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


@app.route("/", methods=["GET", "POST"])
def root():
    """
    Root page
    """
    return render_template("root.html", filament_presets=filament_presets,
                           filament_types=SpoolReader.get_available_filament_types())


def start_web_app(port: int, debug=False):
    """
    Init point of the web app
    :param port: The server port
    :param debug: Debugging mode for auto reload
    """
    app.run(port=port, host="0.0.0.0", debug=debug)
