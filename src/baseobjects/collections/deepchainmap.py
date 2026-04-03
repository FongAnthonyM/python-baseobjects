"""deepchainmap.py
A ChainMap that updates and deletes items from the first mapping that contains the key.

This module provides the DeepChainMap class, which extends the standard library's ChainMap to provide more intuitive
update and delete behavior. Unlike the standard ChainMap, which always updates or adds items to the first mapping,
DeepChainMap updates items in the first mapping that contains the key, and only adds new items to the first mapping.
This behavior is particularly useful for nested configuration scenarios where existing values must be modified in
their original location.
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
from collections import ChainMap
from typing import Any

# Local Packages #
from ..bases import BaseObject
from ..typing import KeyType, ValueType


# Definitions #
# Classes #
class DeepChainMap(BaseObject, ChainMap[Any, Any]):
    """A ChainMap that updates and deletes items from the first mapping that contains the key.

    DeepChainMap is a subclass of ChainMap that provides a more intuitive update and delete behavior.
    When setting an existing key, it updates the value in the first mapping that contains the key.
    When deleting a key, it removes it from the first mapping that contains it.
    When setting a new key, it adds it to the first mapping.

    Attributes:
        maps: A list of mappings that make up the chain.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes this object with the given arguments.

        Args:
            *args: Variable length argument list. The first arguments are treated as mappings. If no mappings are
                provided, an empty mapping is used.
            **kwargs: Arbitrary keyword arguments passed to BaseObject.
        """
        # Parent Initialization #
        super().__init__(*args, **kwargs)
        ChainMap.__init__(self, *args)

    # Container Methods
    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        """Sets an item in this object.

        If the key exists in any mapping, updates the value in the first mapping that contains the key. If the key
        doesn't exist in any mapping, adds it to the first mapping.

        Args:
            key: The key to set.
            value: The value to set for the key.
        """
        for mapping in self.maps:
            if key in mapping:
                mapping[key] = value
                return
        self.maps[0][key] = value

    def __delitem__(self, key: KeyType) -> None:
        """Deletes an item from this object.

        Removes the key from the first mapping that contains it.

        Args:
            key: The key to delete.

        Raises:
            KeyError: If the key is not found in any mapping.
        """
        for mapping in self.maps:
            if key in mapping:
                del mapping[key]
                return
        raise KeyError(key)
