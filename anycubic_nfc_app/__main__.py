import json
from typing import Any

from .web_app import start_web_app
from .nfc_manager import SpoolReader


def write_spool() -> None:
    """
    Spool write example
    """
    reader: SpoolReader = SpoolReader()
    spool_specs: dict[str, Any] = {
        "type": "PLA High Speed",
        "color": "#000000",
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
            "nozzle_max": 240
        },
        "bed_min": 50,
        "bed_max": 60,
        "diameter": 1.75,
        "length": 330,
        "weight": 1000
    }
    if reader.write_spool(spool_specs):
        print("Write success")
    else:
        print("Write failure")


def read_spool() -> None:
    """
    Spool read example
    """
    reader: SpoolReader = SpoolReader()
    spool_specs: dict[str, Any] = reader.read_spool()
    print(json.dumps(spool_specs, indent=4))


def read_spool_raw() -> None:
    """
    Spool raw read example
    """
    reader: SpoolReader = SpoolReader()
    spool_data_raw: str = reader.read_spool_raw()
    print(spool_data_raw)


if __name__ == "__main__":
    """
    App init point
    """
    # write_spool()
    # read_spool_raw()
    start_web_app(8081, debug=True)
