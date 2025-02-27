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
        "sku": "MOLODOS-PLA",
        "type": "PLA",
        "color_r": 255,
        "color_g": 0,
        "color_b": 0,
        "color_a": 255,
        "color_secondary": {
            "color_r": 0,
            "color_g": 0,
            "color_b": 0,
            "color_a": 0
        },
        "color_tertiary": {
            "color_r": 0,
            "color_g": 0,
            "color_b": 0,
            "color_a": 0
        },
        "speed_min": 0,
        "speed_max": 0,
        "nozzle_min": 200,
        "nozzle_max": 210,
        "range_b": {
            "speed_min": 0,
            "speed_max": 0,
            "nozzle_min": 0,
            "nozzle_max": 0
        },
        "range_c": {
            "speed_min": 0,
            "speed_max": 0,
            "nozzle_min": 0,
            "nozzle_max": 0
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
    # read_spool()
    # read_spool_raw()
    start_web_app(8080, debug=True)
