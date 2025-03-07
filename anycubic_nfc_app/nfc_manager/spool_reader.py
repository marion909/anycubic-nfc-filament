import json
from typing import Any, Optional

from .acr122u import CardData, ACR122U


class SpoolData(CardData):
    """
    Spool data
    """

    def __init__(self, spool_specs: Optional[dict[str, Any]] = None):
        """
        Create a spool data object
        :param spool_specs: Optionally, add spool specs directly
        """
        super().__init__(page_count=0x2d)
        if spool_specs:
            self.set_spool_specs(spool_specs)

    def _write_byte(self, page: int, index: int, data: int) -> None:
        """
        Write a byte
        :param page: Page in the data
        :param index: Index on the page
        :param data: Byte to write
        """
        page_data = bytearray(self.pages[page])
        page_data[index] = data
        self.pages[page] = bytes(page_data)

    def _read_byte(self, page: int, index: int) -> int:
        """
        Write a byte
        :param page: Page in the data
        :param index: Index on the page
        :return: read byte
        """
        return bytearray(self.pages[page])[index]

    def _write_bytes(self, page: int, index: int, data: int) -> None:
        """
        Write two bytes (big endian)
        :param page: Page in the data
        :param index: Index on the page
        :param data: Bytes to write
        """
        low_byte = data % 256
        high_byte = data // 256
        self._write_byte(page, index, low_byte)
        if index == 3:
            self._write_byte(page + 1, 0, high_byte)
        else:
            self._write_byte(page, index + 1, high_byte)

    def _read_bytes(self, page: int, index: int) -> int:
        """
        Read two bytes (big endian)
        :param page: Page in the data
        :param index: Index on the page
        :return: Read bytes
        """
        low_byte: int = self._read_byte(page, index)
        if index == 3:
            high_byte = self._read_byte(page + 1, 0)
        else:
            high_byte = self._read_byte(page, index + 1)
        return high_byte * 256 + low_byte

    def _write_string(self, page: int, data: str) -> None:
        """
        Write a string (max 20 characters)
        :param page: Page in the data
        :param data: String to write
        """
        for i in range(min(len(data), 20)):
            self._write_byte(page + i // 4, i % 4, ord(data[i]))

    def _read_string(self, page) -> str:
        """
        Read a string (max 20 characters)
        :param page: Page in the data
        :return: The read string
        """
        data: str = ""
        i = 0
        byte = self._read_byte(page, i)
        while byte > 0:
            data += chr(byte)
            if len(data) >= 20:
                break
            i += 1
            if i == 4:
                i = 0
                page += 1
            byte = self._read_byte(page, i)
        return data

    def _set_format_version(self, version: int) -> None:
        """
        Set the format version of the tag
        :param version: Version (1 or 2 (adds print speed))
        """
        if version == 1:
            self._write_byte(0x04, 2, 0x64)
            self._write_string(0x0a, "\x00\x00")
        elif version == 2:
            self._write_byte(0x04, 2, 0x65)
            self._write_string(0x0a, "AC")

    def set_spool_specs(self, spool_specs: dict[str, Any]) -> None:
        """
        Set the spool specs data
        :param spool_specs: Spool specs JSON
        """
        # Static
        self._write_byte(0x04, 0, 0x7b)
        self._write_byte(0x27, 3, 0x4d)  # Custom spool marker
        self._set_format_version(2)

        # SKU
        self._write_string(0x05, spool_specs["sku"])

        # Type
        self._write_string(0x0f, spool_specs["type"])

        # Color
        self._write_byte(0x14, 3, spool_specs["color_r"])
        self._write_byte(0x14, 2, spool_specs["color_g"])
        self._write_byte(0x14, 1, spool_specs["color_b"])
        self._write_byte(0x14, 0, spool_specs.get("color_a", 0xff))

        # Additional colors (optional)
        if "color_secondary" in spool_specs:
            self._write_byte(0x15, 3, spool_specs["color_secondary"].get("color_r", 0))
            self._write_byte(0x15, 2, spool_specs["color_secondary"].get("color_g", 0))
            self._write_byte(0x15, 1, spool_specs["color_secondary"].get("color_b", 0))
            self._write_byte(0x15, 0, spool_specs["color_secondary"].get("color_a", 0))
        if "color_tertiary" in spool_specs:
            self._write_byte(0x16, 3, spool_specs["color_tertiary"].get("color_r", 0))
            self._write_byte(0x16, 2, spool_specs["color_tertiary"].get("color_g", 0))
            self._write_byte(0x16, 1, spool_specs["color_tertiary"].get("color_b", 0))
            self._write_byte(0x16, 0, spool_specs["color_tertiary"].get("color_a", 0))

        # Print speed (optional)
        self._write_bytes(0x17, 0, spool_specs.get("speed_min", 0))
        self._write_bytes(0x17, 2, spool_specs.get("speed_max", 0))

        # Nozzle temp
        self._write_bytes(0x18, 0, spool_specs["nozzle_min"])
        self._write_bytes(0x18, 2, spool_specs["nozzle_max"])

        # Additional print speed ranges (optional)
        if "range_b" in spool_specs:
            self._write_bytes(0x19, 0, spool_specs["range_b"].get("speed_min", 0))
            self._write_bytes(0x19, 2, spool_specs["range_b"].get("speed_max", 0))
            self._write_bytes(0x1a, 0, spool_specs["range_b"].get("nozzle_min", 0))
            self._write_bytes(0x1a, 2, spool_specs["range_b"].get("nozzle_max", 0))
        if "range_c" in spool_specs:
            self._write_bytes(0x1b, 0, spool_specs["range_c"].get("speed_min", 0))
            self._write_bytes(0x1b, 2, spool_specs["range_c"].get("speed_max", 0))
            self._write_bytes(0x1c, 0, spool_specs["range_c"].get("nozzle_min", 0))
            self._write_bytes(0x1c, 2, spool_specs["range_c"].get("nozzle_max", 0))

        # Bed temp
        self._write_bytes(0x1d, 0, spool_specs["bed_min"])
        self._write_bytes(0x1d, 2, spool_specs["bed_max"])

        # Diameter
        self._write_bytes(0x1e, 0, round(spool_specs["diameter"] * 100))

        # Length
        self._write_bytes(0x1e, 2, spool_specs["length"])

        # Weight
        self._write_bytes(0x1f, 0, spool_specs["weight"])

    def get_spool_specs(self) -> dict[str, Any]:
        """
        Get the spool specs data
        :return: Spool specs JSON
        """
        # Read specs
        spool_specs: dict[str, Any] = {
            "sku": self._read_string(0x05),
            "type": self._read_string(0x0f),
            "color_r": self._read_byte(0x14, 3),
            "color_g": self._read_byte(0x14, 2),
            "color_b": self._read_byte(0x14, 1),
            "color_a": self._read_byte(0x14, 0),
            "color_secondary": {
                "color_r": self._read_byte(0x15, 3),
                "color_g": self._read_byte(0x15, 2),
                "color_b": self._read_byte(0x15, 1),
                "color_a": self._read_byte(0x15, 0),
            },
            "color_tertiary": {
                "color_r": self._read_byte(0x16, 3),
                "color_g": self._read_byte(0x16, 2),
                "color_b": self._read_byte(0x16, 1),
                "color_a": self._read_byte(0x16, 0),
            },
            "speed_min": self._read_bytes(0x17, 0),
            "speed_max": self._read_bytes(0x17, 2),
            "nozzle_min": self._read_bytes(0x18, 0),
            "nozzle_max": self._read_bytes(0x18, 2),
            "range_b": {
                "speed_min": self._read_bytes(0x19, 0),
                "speed_max": self._read_bytes(0x19, 2),
                "nozzle_min": self._read_bytes(0x1a, 0),
                "nozzle_max": self._read_bytes(0x1a, 2)
            },
            "range_c": {
                "speed_min": self._read_bytes(0x1b, 0),
                "speed_max": self._read_bytes(0x1b, 2),
                "nozzle_min": self._read_bytes(0x1c, 0),
                "nozzle_max": self._read_bytes(0x1c, 2)
            },
            "bed_min": self._read_bytes(0x1d, 0),
            "bed_max": self._read_bytes(0x1d, 2),
            "diameter": self._read_bytes(0x1e, 0) / 100,
            "length": self._read_bytes(0x1e, 2),
            "weight": self._read_bytes(0x1f, 0),
            "is_custom": self._read_bytes(0x27, 3) == 0x4d
        }

        # Return
        return spool_specs

    def dump(self) -> str:
        """
        Dump the data
        :return: The dump as string
        """
        return json.dumps(self.get_spool_specs(), indent=4)


class SpoolReader:
    """
    Reader/writer for Anycubic filament spools
    """

    def __init__(self):
        """
        Initialize card reader
        """
        self.reader: ACR122U = ACR122U()

    def read_spool(self) -> Optional[dict[str, Any]]:
        """
        Wait for a spool, read it and return its data
        :return: JSON data of the spool on success else None
        """
        card_data: Optional[CardData] = self.reader.read_card()
        if not card_data:
            return None
        spool_data: SpoolData = SpoolData()
        spool_data.pages = card_data.pages
        return spool_data.get_spool_specs()

    def read_spool_raw(self) -> Optional[str]:
        """
        Wait for a spool, read it and return its raw data (+ interpretation if possible)
        :return: Raw data of the nfc tag
        """
        card_data: Optional[CardData] = self.reader.read_card()
        if not card_data:
            return None
        raw_data: str = card_data.dump()
        try:
            spool_data: SpoolData = SpoolData()
            spool_data.pages = card_data.pages
            interpretation: str = json.dumps(spool_data.get_spool_specs(), indent=4)
            return f"{raw_data}\n\n{interpretation}"
        except:
            return raw_data

    def write_spool(self, spool_specs: dict[str, Any]) -> bool:
        """
        Wait for a spool and write the data
        :param spool_specs: JSON spool data
        :return: Success state
        """
        spool_data: SpoolData = SpoolData()
        spool_data.set_spool_specs(spool_specs)
        return self.reader.write_card(spool_data)
