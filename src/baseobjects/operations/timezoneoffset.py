"""timezoneoffset.py
A function that gets the offset of a give timezone.

This module contains the a function that gets the offset of a give timezone.
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
from datetime import UTC, datetime, timedelta, tzinfo

# Definitions #
# Constants
INIT_DATE = datetime(1970, 1, 1, tzinfo=UTC)


# Functions #
def timezone_offset(tz: tzinfo) -> timedelta | None:
    """Gets the offset of the given timezone.

    Args:
        tz: The timezone to get the offset from.

    Returns:
        The time delta offset of the given timezone or None if the timezone is not fixed.
    """
    return tz.utcoffset(INIT_DATE)
