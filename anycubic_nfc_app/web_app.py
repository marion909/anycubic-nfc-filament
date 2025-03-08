from typing import Any

from flask import Flask, render_template

# App settings
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Max upload size of 1MB

filament_skus: dict[str, str] = {
    "PLA": "AHPLBK-101",
    "PLA+": "AHPLPBK-102",
    "PLA Matte": "HYGBK-101",
    "PLA Silk": "HSCWH-101",
    "PLA High Speed": "AHHSBK-102",
    "PETG": "HPEBK-103",
    "ASA": "HASBK-101",
    "ABS": "HABBK-102",
    "TPU": "HTPBK-101",
    "PLA Luminous": "HFGBL-101"
}


@app.route("/", methods=["GET", "POST"])
def root():
    """
    Root page
    """
    return render_template("root.html", filament_types=list(filament_skus.keys()))


def start_web_app(port: int, debug=False):
    """
    Init point of the web app
    :param port: The server port
    :param debug: Debugging mode for auto reload
    """
    app.run(port=port, host="0.0.0.0", debug=debug)
