"""unionrecursive.py
Unions a mapping object and its contained mappings within another mapping.

This module contains the unions a mapping object and its contained mappings within another mapping.
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
from collections.abc import MutableMapping
from copy import deepcopy
from typing import Any

# Local Packages #
from .updaterecursive import update_recursive


# Definitions #
# Functions #
def union_recursive(d: MutableMapping[Any, Any], other: MutableMapping[Any, Any]) -> MutableMapping[Any, Any]:
    """Unions a mapping object and its contained mappings within another mapping.

    Args:
        d: The mapping type to union recursively.
        other: The other mapping to union with.

    Returns:
        A new mapping as the union of the two mappings recursively.
    """
    return update_recursive(deepcopy(d), other)
