"""bytestobin.py
A function to convert bytes to a tuple of binary values.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from typing import Any


# Definitions #
# Constants #
big_array = (128, 64, 32, 16, 8, 4, 2, 1)
little_array = (8, 4, 2, 1, 128, 64, 32, 16)


# Functions #
def bytes_to_bin(bytes_: bytes, byteorder: str = "big", out_type: type = int) -> tuple[Any]:
    """Converts bytes to a tuple of binary values.

    Args:
        bytes_: The bytes to convert to binary.
        byteorder: The byte order of bytes to use for the conversion, either 'little' or 'big'.
        out_type: The type to represent the binary values as, such as int, bool, or str.

    Returns:
        The tuple of binary values from the bytes.

    Raises:
        ValueError: If byteorder is not 'little' or 'big'.
    """
    if byteorder == "big":
        return tuple(out_type(bool(byte & place)) for byte in bytes_ for place in big_array)
    if byteorder == "little":
        return tuple(out_type(bool(byte & place)) for byte in bytes_ for place in little_array)
    else:
        msg = "byteorder must be either 'little' or 'big'"
        raise ValueError(msg)
