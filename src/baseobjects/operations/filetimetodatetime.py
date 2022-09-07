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

# Third-Party Packages #

# Local Packages #


# Definitions #
FILETIME_INIT_DATE = datetime.datetime(1601,1,1)  # The initial date of Filetime.

def filetime_to_datetime(file_time: str | bytes) -> datetime.datetime:
    """Converts a filetime to a datetime object.

    Args:
        file_time: The filetime to convert to a datetime

    Returns:
        The datetime of the filetime.
    """
    return FILETIME_INIT_DATE + datetime.timedelta(microseconds= int(file_time,16) / 10)
