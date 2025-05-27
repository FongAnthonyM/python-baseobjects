"""updaterecursive.py
Updates a mapping object and its contained mappings based on another mapping.
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
from collections.abc import Mapping, Iterable

# Third-Party Packages #

# Local Packages #


# Definitions #
# Functions #
def _update_recursive(d: Mapping, updates: Mapping) -> Mapping:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    d.update(
        (key, update_recursive(d.get(key, {}), value) if isinstance(value, Mapping) else value)
        for key, value in updates.items()
    )
    return d


def update_recursive(d: Mapping, updates: Iterable | Mapping) -> Mapping:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    if isinstance(updates, Mapping):
        updates = updates.items()

    d.update(
        (key, _update_recursive(d.get(key, {}), value) if isinstance(value, Mapping) else value)
        for key, value in updates
    )
    return d
