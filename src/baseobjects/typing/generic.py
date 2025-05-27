"""generic.py
Generic types.
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

# Third-Party Packages #

# Local Packages #
from typing import TypeVar


# Definitions #
# Types #
KeyType = TypeVar("_KT")  # Key type.
ValueType = TypeVar("_VT")
KT_co = TypeVar("_KT_co", covariant=True)
VT_co = TypeVar("_VT_co", covariant=True)

# Available Types
__all__ = [
    "KeyType",
    "ValueType",
    "KT_co",
    "VT_co",
]
