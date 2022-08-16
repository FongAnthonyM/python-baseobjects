""" updaterecursive.py
Updates a mapping object and its contained mappings based on another mapping.
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
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Fuctions #
def update_recursive(d: Mapping, updates: Mapping) -> Mapping:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update revursively.
        updates: The mapping updates.

    Returns:
        The orginal mapping that has been updated.
    """
    for key, value in updates.items():
        if isinstance(value, Mapping):
            d[key] = update_recursive(d.get(key, {}), value)
        else:
            d[key] = value
    return d
