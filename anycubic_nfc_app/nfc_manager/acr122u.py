import time
from typing import List, Optional

from smartcard.CardConnection import CardConnection
from smartcard.System import readers
from smartcard.reader.Reader import Reader


class CardData:
    """
    Card data
    """

    def __init__(self, page_count: int = 0x2d):
        """
        Create card data object
        :param page_count: Number of pages
        """
        self.pages: list[bytes] = page_count * [b"\x00\x00\x00\x00"]

    def dump(self) -> str:
        """
        Dump the data
        :return: The dump as string
        """
        pages: list[str] = []
        for page, page_data in enumerate(self.pages):
            hex_data: list[str] = [f"{x:02x}" for x in page_data]
            ascii_data: str = ''.join([chr(x) for x in page_data])
            pages.append(f"[Page {page:02x}] {':'.join(hex_data)} - {ascii_data}")
        return "\n".join(pages)


class ACR122U:
    """
    ACR122U reader/writer
    """

    def __init__(self):
        """
        Create an instance
        """
        self.reader: Reader = self._get_reader()

    @classmethod
    def _get_reader(cls) -> Reader:
        """
        Get a connection to the reader device
        :return: Reader connection
        """
        available_readers: list[Reader] = readers()
        if not available_readers:
            raise Exception("No NFC reader found")
        return available_readers[0]

    @classmethod
    def _read_page(cls, connection: CardConnection, page: int) -> Optional[bytes]:
        """
        Read from page on card
        :param connection: Connection to the card
        :param page: Page number
        :return: The read data (4 bytes)
        """
        read_page_command: list[int] = [0xFF, 0xB0, 0x00, page, 0x04]
        response, sw1, sw2 = connection.transmit(read_page_command)
        if sw1 == 0x90 and sw2 == 0x00:
            return response
        else:
            return None

    @classmethod
    def _write_page(cls, connection: CardConnection, page: int, data: bytes) -> bool:
        """
        Write to page on card
        :param connection: Connection to the card
        :param page: Page number
        :param data: Data to write
        :return: Success state
        """
        write_page_command: List[int] = [0xFF, 0xD6, 0x00, page, 0x04] + list(data)
        response, sw1, sw2 = connection.transmit(write_page_command)
        if sw1 == 0x90 and sw2 == 0x00:
            return True
        else:
            return False

    def _wait_for_card(self) -> CardConnection:
        """
        Wait for a card to be found
        :return: The connection to the card
        """
        connection: CardConnection = self.reader.createConnection()
        while True:
            try:
                connection.connect()
                return connection
            except Exception:
                time.sleep(0.5)

    def read_card(self, page_count: int = 0x2d) -> Optional[CardData]:
        """
        Read data from card
        :param page_count: Number of pages on the card
        :return: The data of the card on success else None
        """
        connection: CardConnection = self._wait_for_card()
        data: CardData = CardData(page_count)
        for page in range(0, page_count):
            d: bytes = self._read_page(connection, page)
            if d is None:
                print(f"[Error] Failed to read page {page}. Reading cancelled.")
                return None
            else:
                data.pages[page] = d
        return data

    def write_card(self, card_data: CardData, page_count: int = 0x2d) -> bool:
        """
        Write data to card
        :param card_data: Data to write
        :param page_count: Number of pages on the card
        :return: Success state
        """
        connection: CardConnection = self._wait_for_card()
        for page, page_data in enumerate(card_data.pages):
            # Don't write to management data pages
            if 0x03 < page < page_count - 5:
                if not self._write_page(connection, page, page_data):
                    return False
        return True
