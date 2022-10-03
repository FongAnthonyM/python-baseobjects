""" filetimetodatetime.py
A function to convert a filetime to a datetime.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import datetime
from functools import singledispatch

# Third-Party Packages #

# Local Packages #


# Definitions #
FILETIME_INIT_DATE = datetime.datetime(1601, 1, 1)  # The initial date of Filetime.


@singledispatch
def filetime_to_datetime(timestamp: int | float | str | bytes) -> datetime.datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.

    Returns:
        The datetime of the filetime.
    """
    raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


@filetime_to_datetime.register
def _filetime_to_datetime(timestamp: int) -> datetime.datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.

    Returns:
        The datetime of the filetime.
    """
    return FILETIME_INIT_DATE + datetime.timedelta(microseconds=timestamp)


@filetime_to_datetime.register(float)
@filetime_to_datetime.register(str)
def _filetime_to_datetime(timestamp: float | str) -> datetime.datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.

    Returns:
        The datetime of the filetime.
    """
    return FILETIME_INIT_DATE + datetime.timedelta(microseconds=int(timestamp) / 10)


@filetime_to_datetime.register(bytes)
def _filetime_to_datetime(timestamp: bytes) -> datetime.datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.

    Returns:
        The datetime of the filetime.
    """
    return FILETIME_INIT_DATE + datetime.timedelta(microseconds=int.from_bytes(timestamp, "little") / 10)
