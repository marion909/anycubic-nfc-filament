from flask import Flask, render_template

# App settings
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Max upload size of 1MB


filament_types: list[str] = [
    "PLA", "PETG", "TPU",
    "ABS", "ASA", "PET",
    "PA", "PC", "PLA-CF",
    "PA-CF", "PA-GF", "ABS-GF"
]

@app.route("/", methods=["GET", "POST"])
def root():
    """
    Root page
    """
    return render_template("root.html")


def start_web_app(port: int, debug=False):
    """
    Init point of the web app
    :param port: The server port
    :param debug: Debugging mode for auto reload
    """
    app.run(port=port, host="0.0.0.0", debug=debug)
