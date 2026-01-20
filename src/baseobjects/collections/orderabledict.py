"""orderabledict.py
A dictionary with an adjustable order and additional supporting methods.

This module provides the OrderableDict class, which extends BaseDict to implement a dictionary that maintains an
explicit ordering of its keys. Unlike OrderedDict from the standard library, OrderableDict allows for direct
manipulation of the key order through various methods. It supports accessing items by their position in the order,
moving items within the order, and other operations that combine dictionary functionality with list-like ordering
capabilities.
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
from collections.abc import Hashable, Iterator
from typing import Any

# Local Packages #
from ..bases import DEFAULTSENTINEL, BaseDict


# Definitions #
# Classes #
class OrderableDict(BaseDict):
    """A dictionary with an adjustable order and additional supporting methods.

    Attributes:
        order: The order of this dictionary.

    Args:
        dict_: An object to build this dictionary from
        *args: Arguments for creating a dictionary.
        **kwargs: Keyword arguments for creating a dictionary.
    """

    # Attributes #
    order: list[Hashable]

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict_: Any = None, /, *args: Any, **kwargs: Any) -> None:
        """Initializes this object with the given arguments.

        Args:
            dict_: Optional mapping or iterable to initialize from.
            *args: Additional positional arguments passed to BaseDict.
            **kwargs: Additional keyword arguments passed to BaseDict.
        """
        # Attributes #
        self.order = []

        # Parent Initialization #
        super().__init__(dict_, *args, **kwargs)

    # Container Methods
    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Sets an item in this object."""
        if key not in self.data:
            self.order.append(key)
        self.data[key] = value

    def __delitem__(self, key: Hashable) -> None:
        """Deletes an item from this object."""
        del self.data[key]
        self.order.remove(key)

    def __iter__(self) -> Iterator[Hashable]:
        """Returns an iterator for the keys."""
        return iter(self.order)

    # Instance Methods #
    def get_index(self, index: int, default: Any = DEFAULTSENTINEL) -> Any:
        """Gets a value base on its key's index in the order.

        Args:
            index: The index of the key to get.
            default: The value to return if the index is outside the range.

        Returns:
            The requested value.

        Raises:
            IndexError: If the index is outside the range and no default is provided.
        """
        try:
            return self.data.get(self.order[index])
        except IndexError as e:
            if default is not DEFAULTSENTINEL:
                return default
            else:
                raise e

    def set_index(self, index: int, value: Any) -> None:
        """Sets a key's value based on its index in the order.

        Args:
            index: The index of the key to set.
            value: The value to set at the key
        """
        self.data[self.order[index]] = value

    def setdefault(self, key: Hashable, default: Any = None) -> Any:
        """Gets a value with a key but adds the key and a default value to this dictionary if it was not present.

        Args:
            key: The key to get or add if it was not in the dictionary.
            default: The value to add to the dictionary if not present.

        Returns:
            Any: The value associated with the key (existing or the provided default).
        """
        if key not in self.data:
            self.order.append(key)
        return self.data.setdefault(key, default)

    def insert(self, index: int, key: Hashable, value: Any) -> None:
        """Adds a key and value and inserts it into order or raises an error if the key already exists.

        Args:
            index: The index to insert into the order.
            key: The key of value to insert.
            value: The value to set at the key.

        Raises:
            KeyError: If the key already exists in the dictionary.
        """
        if key in self.data:
            msg = "Key already exists."
            raise KeyError(msg)

        self.order.insert(index, key)
        self.data[key] = value

    def insert_move(self, index: int, key: Hashable, value: Any) -> None:
        """Adds a key and value and inserts it into order or moves the key if it already exists.

        Args:
            index: The index to insert into the order.
            key: The key of value to insert.
            value: The value to set at the key.
        """
        if key in self.data:
            old = self.order.index(key)
            if index < old:
                self.order.remove(key)
                self.order.insert(index, key)
            elif index > old + 1:
                self.order.remove(key)
                self.order.insert(index - 1, key)
        else:
            self.order.insert(index, key)

        self.data[key] = value

    def append(self, key: Hashable, value: Any) -> None:
        """Adds a key and value to this dictionary and appends it to the order if it was not present.

        Args:
            key: The key to add to the dictionary.
            value: The value to add to the dictionary
        """
        self[key] = value

    def update(self, m: Any = None, /, **kwargs: Any) -> None:
        """Updates the keys and values of this dictionary, any new keys are appended to the order.

        Args:
            m: An object with the keys and values to add.
            **kwargs: The new values to add with the names as the keys.
        """
        for key, value in ({} if m is None else dict(m) | kwargs).items():
            self[key] = value

    def pop(self, key: Hashable, default: Any = DEFAULTSENTINEL) -> Any:
        """Pops a value from the key in this orderable dictionary.

        Args:
            key: The key of the value to pop.
            default: The value to return if the key is not found.

        Returns:
            The requested value.

        Raises:
            KeyError: The key was not found.
        """
        if key in self.data:
            self.order.remove(key)
            return self.data.pop(key)

        if default is not DEFAULTSENTINEL:
            return default

        raise KeyError(key)

    def pop_index(self, index: int = -1) -> Any:
        """Pops the value at the index in this orderable dictionary.

        Args:
            index: The index of the value to pop.

        Returns:
            The value requested.
        """
        return self.data.pop(self.order.pop(index))

    def popitem(self) -> tuple[Hashable, Any]:
        """Pops the last key and its value.

        Returns:
            The key and value.
        """
        key = self.order.pop()
        return key, self.data.pop(key)

    def remove(self, key: Hashable) -> None:
        """Removes a key from this dictionary."""
        del self[key]

    def clear(self) -> None:
        """Clears the contents of this object."""
        self.data.clear()
        self.order.clear()

    def reverse(self) -> None:
        """Reverses the order of this dictionary."""
        self.order.reverse()
