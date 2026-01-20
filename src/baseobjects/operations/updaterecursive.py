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
from collections.abc import Iterable, Mapping, MutableMapping
from typing import Any


# Definitions #
# Functions #
def _update_recursive(d: MutableMapping[Any, Any], updates: Iterable[tuple[Any, Any]]) -> MutableMapping[Any, Any]:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    for key, value in updates:
        #  Get the existing value, defaulting to empty dict if not present
        if isinstance(value, Mapping) and isinstance((existing := d.get(key, None)), MutableMapping):
            d[key] = _update_recursive(existing, value.items())
        else:
            # For non-Mapping values, simply update
            d[key] = value
    return d


def update_recursive(
    d: MutableMapping[Any, Any],
    updates: Iterable[tuple[Any, Any]] | Mapping[Any, Any],
) -> MutableMapping[Any, Any]:
    """Updates a mapping object and its contained mappings based on another mapping.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    return _update_recursive(d, updates.items() if isinstance(updates, Mapping) else updates)
