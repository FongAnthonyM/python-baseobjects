#!/usr/bin/env python
"""baselist_example.py
An example of how to use BaseList class.

This example demonstrates:
1. Creating lists using BaseList
2. Basic list operations with BaseList
3. Inheriting from BaseList to create custom list classes
4. Using BaseObject features with list-like objects
"""

# Imports #
# Standard Libraries #
from collections.abc import Iterable
from typing import Any

# Source Packages #
from baseobjects.bases.collections import BaseList


# Classes #
class SortedList(BaseList):
    """A custom list that maintains its elements in sorted order."""

    def __init__(self, initlist: list[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Initialize a SortedList object.

        Args:
            initlist: Initial list data
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(initlist, *args, **kwargs)
        self.construct()

    def construct(self, *args: Any, **kwargs: Any) -> None:
        """Construct the SortedList object by sorting its elements.

        Args:
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        if self.data:
            self.data.sort()

    def append(self, item: Any) -> None:
        """Add an item to the list and maintain sorted order.

        Args:
            item: The item to add
        """
        self.data.append(item)
        self.data.sort()

    def extend(self, other: Iterable[Any]) -> None:
        """Extend the list with another list and maintain sorted order.

        Args:
            other: The list to extend with
        """
        self.data.extend(other)
        self.data.sort()

    def insert(self, i: int, item: Any) -> None:
        """Insert an item at a specific position and maintain sorted order.

        Note: The position is ignored as the list will be sorted after insertion.

        Args:
            i: The position (ignored)
            item: The item to insert
        """
        self.data.append(item)
        self.data.sort()


class UniqueList(BaseList):
    """A custom list that only contains unique elements."""

    def __init__(self, initlist: list[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Initialize a UniqueList object.

        Args:
            initlist: Initial list data
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(None, *args, **kwargs)
        self.construct(initlist)

    def construct(self, initlist: list[Any] | None = None, *args: Any, **kwargs: Any) -> None:
        """Construct the UniqueList object with unique elements.

        Args:
            initlist: Initial list data
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        if initlist:
            # Add each item only if it's not already in the list
            for item in initlist:
                if item not in self.data:
                    self.data.append(item)

    def append(self, item: Any) -> None:
        """Add an item to the list if it's not already present.

        Args:
            item: The item to add
        """
        if item not in self.data:
            self.data.append(item)

    def extend(self, other: Iterable[Any]) -> None:
        """Extend the list with unique items from another list.

        Args:
            other: The list to extend with
        """
        for item in other:
            if item not in self.data:
                self.data.append(item)

    def insert(self, i: int, item: Any) -> None:
        """Insert an item at a specific position if it's not already present.

        Args:
            i: The position to insert at
            item: The item to insert
        """
        if item not in self.data:
            self.data.insert(i, item)


# Example Sections #
def basic_baselist_example() -> None:
    """Demonstrate basic usage of BaseList."""
    print("\nBasic BaseList Example:")

    # Create a BaseList instance
    base_list = BaseList(["apple", "banana", "cherry"])
    print(f"BaseList: {base_list}")

    # Access items
    print(f"First item: {base_list[0]} == 'apple'")
    print(f"Last item: {base_list[-1]} == 'cherry'")

    # Modify items
    base_list[1] = "blueberry"
    print(f"After modification: {base_list} == ['apple', 'blueberry', 'cherry']")

    # Add items
    base_list.append("date")
    print(f"After append: {base_list} == ['apple', 'blueberry', 'cherry', 'date']")

    # Insert items
    base_list.insert(2, "cantaloupe")
    print(f"After insert: {base_list} == ['apple', 'blueberry', 'cantaloupe', 'cherry', 'date']")

    # Extend the list
    base_list.extend(["elderberry", "fig"])
    print(f"After extend: {base_list} == ['apple', 'blueberry', 'cantaloupe', 'cherry', 'date', 'elderberry', 'fig']")

    # Remove items
    base_list.remove("cherry")
    print(f"After remove: {base_list} == ['apple', 'blueberry', 'cantaloupe', 'date', 'elderberry', 'fig']")

    # Pop items
    popped = base_list.pop()
    print(f"Popped item: {popped} == 'fig'")
    print(f"After pop: {base_list} == ['apple', 'blueberry', 'cantaloupe', 'date', 'elderberry']")

    # List operations
    print(f"Length: {len(base_list)} == 5")
    print(f"'date' in list: {'date' in base_list} == True")
    print(f"'fig' in list: {'fig' in base_list} == False")


def sorted_list_example() -> None:
    """Demonstrate using a custom SortedList class."""
    print("\nSorted List Example:")

    # Create a SortedList with unsorted data
    sorted_list = SortedList([5, 2, 8, 1, 9, 3])
    print(f"Initial sorted list: {sorted_list} == [1, 2, 3, 5, 8, 9]")

    # Add items
    sorted_list.append(4)
    print(f"After append(4): {sorted_list} == [1, 2, 3, 4, 5, 8, 9]")

    # Insert items (position is ignored in SortedList)
    sorted_list.insert(0, 7)  # Position is ignored
    print(f"After insert(0, 7): {sorted_list} == [1, 2, 3, 4, 5, 7, 8, 9]")

    # Extend the list
    sorted_list.extend([6, 0])
    print(f"After extend([6, 0]): {sorted_list} == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]")

    # Remove items
    sorted_list.remove(5)
    print(f"After remove(5): {sorted_list} == [0, 1, 2, 3, 4, 6, 7, 8, 9]")


def unique_list_example() -> None:
    """Demonstrate using a custom UniqueList class."""
    print("\nUnique List Example:")

    # Create a UniqueList with duplicate data
    unique_list = UniqueList(["apple", "banana", "apple", "cherry", "banana"])
    print(f"Initial unique list: {unique_list} == ['apple', 'banana', 'cherry']")

    # Add items
    unique_list.append("date")
    print(f"After append('date'): {unique_list} == ['apple', 'banana', 'cherry', 'date']")

    # Try to add a duplicate
    unique_list.append("apple")
    print(f"After append('apple'): {unique_list} == ['apple', 'banana', 'cherry', 'date']")

    # Insert items
    unique_list.insert(0, "elderberry")
    print(f"After insert(0, 'elderberry'): {unique_list} == ['elderberry', 'apple', 'banana', 'cherry', 'date']")

    # Try to insert a duplicate
    unique_list.insert(2, "banana")
    print(f"After insert(2, 'banana'): {unique_list} == ['elderberry', 'apple', 'banana', 'cherry', 'date']")

    # Extend the list
    unique_list.extend(["fig", "grape", "apple"])
    expected = "['elderberry', 'apple', 'banana', 'cherry', 'date', 'fig', 'grape']"
    print(f"After extend(['fig', 'grape', 'apple']): {unique_list} == {expected}")


def baseobject_features_example() -> None:
    """Demonstrate BaseObject features with BaseList."""
    print("\nBaseObject Features Example:")

    # Create a list with nested structures
    original = BaseList([1, 2, [3, 4], {"key": "value"}])
    print(f"Original list: {original}")

    # Shallow copy
    shallow_copy = original.copy()
    print(f"Shallow copy: {shallow_copy}")
    print(f"Are they the same object? {original is shallow_copy} == False")

    # Modify nested list in shallow copy
    shallow_copy[2].append(5)
    print(f"Original nested list after modifying shallow copy: {original[2]} == [3, 4, 5]")
    print(f"Shallow copy nested list: {shallow_copy[2]} == [3, 4, 5]")

    # Deep copy
    deep_copy = original.deepcopy()
    print(f"\nDeep copy: {deep_copy}")
    print(f"Are they the same object? {original is deep_copy} == False")

    # Modify nested list in deep copy
    deep_copy[2].append(6)
    print(f"Original nested list after modifying deep copy: {original[2]} == [3, 4, 5]")
    print(f"Deep copy nested list: {deep_copy[2]} == [3, 4, 5, 6]")

    # Modify nested dictionary in deep copy
    deep_copy[3]["new_key"] = "new_value"
    print(f"Original nested dict after modifying deep copy: {original[3]} == {{'key': 'value'}}")
    print(f"Deep copy nested dict: {deep_copy[3]} == {{'key': 'value', 'new_key': 'new_value'}}")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_baselist_example()
    sorted_list_example()
    unique_list_example()
    baseobject_features_example()
