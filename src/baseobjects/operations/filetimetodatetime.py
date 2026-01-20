"""filetimetodatetime.py
A function to convert a filetime to a datetime.

This module provides functions for converting Windows FILETIME values to Python datetime objects. It supports multiple
input formats including integers, floats, strings, and byte arrays. The module handles timezone conversions and
maintains the precision of the original FILETIME value.
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
from datetime import UTC, datetime, timedelta
from datetime import tzinfo as TZInfo
from typing import Literal

# Local Packages #
from ..functions import singlekwargdispatch

# Definitions #
# Constants #
FILETIME_INIT_DATE = datetime(1601, 1, 1, tzinfo=UTC)  # The initial date of Filetime.


# Functions #
@singlekwargdispatch
def filetime_to_datetime(
    timestamp: int | float | str | bytes,
    tzinfo: TZInfo | None = UTC,
    byteorder: Literal["little", "big"] = "little",
) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.
        byteorder: The byte order of bytes to use for the conversion, either 'little' or 'big' if the input is bytes.

    Returns:  # noqa: DOC202
        The datetime of the filetime.

    Raises:
        TypeError: If the provided timestamp type is unsupported.
    """
    msg = f"{timestamp.__class__} cannot be converted to a datetime"
    raise TypeError(msg)


@filetime_to_datetime.register(int)
def _filetime_to_datetime_int(timestamp: int, tzinfo: TZInfo | None = None) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=timestamp / 10)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=timestamp / 10)).astimezone(tz=tzinfo)


@filetime_to_datetime.register(float)
@filetime_to_datetime.register(str)
def _filetime_to_datetime_float_str(timestamp: float | str, tzinfo: TZInfo | None = None) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(microseconds=int(timestamp) / 10)
    else:
        return (FILETIME_INIT_DATE + timedelta(microseconds=int(timestamp) / 10)).astimezone(tz=tzinfo)


@filetime_to_datetime.register(bytes)
@filetime_to_datetime.register(bytearray)
def _filetime_to_datetime_bytes(
    timestamp: bytes | bytearray,
    tzinfo: TZInfo | None = None,
    byteorder: Literal["little", "big"] = "little",
) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.
        byteorder: The byte order of bytes to use for the conversion, either 'little' or 'big'.

    Returns:
        The datetime of the filetime.
    """
    delta = timedelta(microseconds=int.from_bytes(timestamp, byteorder=byteorder) / 10)
    if tzinfo is None:
        return FILETIME_INIT_DATE.replace(tzinfo=tzinfo) + delta
    else:
        return (FILETIME_INIT_DATE + delta).astimezone(tz=tzinfo)
