import eventlet

eventlet.monkey_patch()

from typing import Any, Optional

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from .nfc_manager import SpoolReader

# App settings
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Max upload size of 1MB
socketio = SocketIO(app)

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

spool_reader: SpoolReader = SpoolReader()


@app.route("/", methods=["GET", "POST"])
def root():
    """
    Root page
    """
    return render_template("root.html", filament_presets=filament_presets,
                           filament_types=SpoolReader.get_available_filament_types())


@socketio.on("ping")
def handle_ping():
    """
    Handle a ping from the client
    """
    socketio.emit("nfc_state", {
        "reader_connected": spool_reader.get_connection_state()
    })


@socketio.on("cancel_nfc")
def cancel_nfc():
    """
    Cancel the current nfc action
    """
    spool_reader.cancel_wait_for_tag()
    socketio.emit("canceled")


@socketio.on("read_tag")
def read_tag():
    """
    Read from a tag
    """
    socketio.start_background_task(_read_tag_async, request.sid)


def _read_tag_async(socket_id):
    """
    Read from a tag (async)
    :param socket_id: Id of the socket to respond to
    """
    spool_data: Optional[dict[str, Any]] = spool_reader.read_spool()
    result: dict[str, Any] = {
        "success": spool_data is not None
    }
    if spool_data:
        result["data"] = spool_data
    socketio.emit("read_done", result, to=socket_id)


@socketio.on("write_tag")
def write_tag(tag_data: dict[str, Any]):
    """
    Write to a tag
    :param tag_data: Data to write to the tag
    """
    tag_data["diameter"] = 1.75
    tag_data["length"] = 330
    tag_data["weight"] = 1000
    socketio.start_background_task(_write_tag_async, tag_data, request.sid)


def _write_tag_async(tag_data: dict[str, Any], socket_id):
    """
    Write to a tag (async)
    :param tag_data: Date to write to the tag
    :param socket_id: Id of the socket to respond to
    """
    success: bool = spool_reader.write_spool(spool_specs=tag_data)
    result: dict[str, Any] = {
        "success": success
    }
    socketio.emit("write_done", result, to=socket_id)


@socketio.on("create_dump")
def create_dump():
    """
    Create a dump of a tag
    """
    socketio.start_background_task(_create_dump_async, request.sid)


def _create_dump_async(socket_id):
    """
    Read from a tag (async)
    :param socket_id: Id of the socket to respond to
    """
    uid, dump_data = spool_reader.read_spool_raw()
    result: dict[str, Any] = {
        "success": dump_data is not None
    }
    if dump_data:
        result["filename"] = f"spool_dump_{uid}.txt"
        result["data"] = dump_data
    socketio.emit("dump_done", result, to=socket_id)


def start_web_app(port: int):
    """
    Init point of the web app
    :param port: The server port
    """
    # Start web app
    socketio.run(app, port=port, host="0.0.0.0")
