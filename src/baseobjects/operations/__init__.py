"""__init__.py
General functions are commonly used.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .bytestobin import bytes_to_bin
from .exceldatetodatetime import excel_date_to_datetime
from .filetimetodatetime import filetime_to_datetime
from .methodnames import get_method_names, get_public_method_names, iter_method_names, iter_public_method_names
from .parseparentheses import parse_parentheses
from .timezoneoffset import timezone_offset
from .unionrecursive import union_recursive
from .updaterecursive import update_recursive
