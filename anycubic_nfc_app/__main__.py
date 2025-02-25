import json
from typing import Any

from .nfc_manager import SpoolReader


def write_spool() -> None:
    """
    Spool write example
    """
    reader: SpoolReader = SpoolReader()
    spool_specs: dict[str, Any] = {
        "sku": "AHPLPBW-102",
        "type": "PLA+",
        "color_r": 255,
        "color_g": 0,
        "color_b": 0,
        "speed_min": 50,
        "speed_max": 100,
        "nozzle_min": 205,
        "nozzle_max": 215,
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


if __name__ == "__main__":
    """
    App init point
    """
    read_spool()
