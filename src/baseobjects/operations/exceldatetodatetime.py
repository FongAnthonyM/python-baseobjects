"""exceldatetodatetime.py
A function to convert an excel date to a datetime.
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
from datetime import datetime, timedelta, timezone
from datetime import tzinfo as TZInfo

# Local Packages #
from ..functions import singlekwargdispatch

# Definitions #
# Constants #
EXCEL_INIT_DATE = datetime(1899, 12, 30)  # The initial date of Filetime.


# Functions #
@singlekwargdispatch
def excel_date_to_datetime(timestamp: int | float | str | bytes, tzinfo: TZInfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    raise TypeError(f"{timestamp.__class__} cannot be converted to a datetime")


@excel_date_to_datetime.register(float)
@excel_date_to_datetime.register(int)
def _excel_date_to_datetime(timestamp: float | int, tzinfo: TZInfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=timestamp)


@excel_date_to_datetime.register(str)
@excel_date_to_datetime.register(bytes)
def _excel_date_to_datetime(timestamp: str | bytes, tzinfo: TZInfo | None = timezone.utc) -> datetime:
    """Converts a filetime to a datetime object.

    Args:
        timestamp: The filetime to convert to a datetime.
        tzinfo: The timezone of the datetime.

    Returns:
        The datetime of the filetime.
    """
    return EXCEL_INIT_DATE.replace(tzinfo=tzinfo) + timedelta(days=float(timestamp))
