"""generic.py
Generic types.

This module provides generic type variables used for type hinting throughout the baseobjects package. It defines
type variables for keys and values, including covariant versions, which are particularly useful for collection
and mapping types. These type variables help improve type safety and code documentation.
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
from typing import TypeVar

# Definitions #
# Types #
KeyType = TypeVar("KeyType", bound=object)  # Key type.
ValueType = TypeVar("ValueType")
KT_co = TypeVar("KT_co", covariant=True)
VT_co = TypeVar("VT_co", covariant=True)

# Available Types
__all__ = [
    "KT_co",
    "KeyType",
    "VT_co",
    "ValueType",
]
