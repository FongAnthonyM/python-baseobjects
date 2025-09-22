"""groupedlist.py
A list which contains any item, but nested GroupLists' contents are treated as if they are elements of this list.

This module provides the GroupedList class, which extends BaseList to implement a hierarchical list structure where
nested GroupedList instances are treated as if their contents are direct elements of the parent list. This allows for
organizing items into logical groups while still being able to iterate through all items as if they were in a flat
list. The class supports named groups, parent-child relationships, and various operations for manipulating the
hierarchical structure.
"""

# Future Imports #
from __future__ import annotations

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from collections import deque
from collections.abc import Iterable, Iterator
from typing import Any

# Third-Party Packages #
import bidict

# Local Packages #
from ..bases import BaseList, SEARCHSENTINEL


# Definitions #
# Classes #
class GroupedList(BaseList):
    """A list which contains any item, but nested GroupLists' contents are treated as if they are elements of this list.

    Attributes:
        parents: The parent and the ancestor GroupLists which this GroupList was created from.
        groups: The named GroupLists within this GroupList.

    Args:
        items: The items to add to this GroupList.
        parent: The parent GroupList of this GroupList.
        parents: The parent and ancestors of this GroupList
        init: Determines if this object will construct.
    """

    # Attributes #
    # Attributes #
    parents: set[GroupedList]
    groups: bidict.bidict

    # Magic Methods #
    # Construction/Destruction #
    def __init__(
        self,
        items: Iterable[Any] | None = None,
        parent: GroupedList | None = None,
        parents: Iterable[GroupedList] | None = None,
        init: bool = True,
    ) -> None:
        # Attributes #
        self.parents = set()
        self.groups = bidict.bidict()

        # Parent Initialization #
        super().__init__()

        # Object Construction #
        if init:
            self.construct(items=items, parent=parent, parents=parents)

    def __copy__(self) -> GroupedList:
        """Creates a shallow copy of this GroupedList.

        Returns:
            A new GroupedList instance with the same data, parents, and groups.
        """
        new = self.__class__(items=self.data, parents=self.parents)
        self.add_parent_to_children(new)
        new.groups.update(self.groups)
        return new

    # Container Methods #
    def __len__(self) -> int:
        """Returns the total number of items in this GroupedList, including items in child groups.

        Returns:
            The total number of items in this GroupedList.
        """
        return self.get_length()

    def __getitem__(self, i: int | str | slice) -> Any | list[Any]:
        """Gets an item or group from this GroupedList.

        Args:
            i: If an integer, the index of the item to get.
               If a string, the name of the group to get.
               If a slice, the slice of items to get.

        Returns:
            The item, group, or slice of items.

        Raises:
            TypeError: If the index type is not supported.
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        match i:
            case slice():
                return self.get_slice(i)
            case str():
                return self.groups[i]
            case int():
                return self.get_item(i)
            case _:
                raise TypeError(f"Invalid index type: {type(i)}")

    def __setitem__(self, i: int | str | slice, item: Any) -> None:
        """Sets an item in this GroupedList.

        Args:
            i: If an integer, the index where the item should be set.
               If a string, the name of the group to set.
               If a slice, the slice of items to set.
            item: The value to set.

        Raises:
            TypeError: If the index type is not supported.
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        match i:
            case slice():
                self.set_slice(i, item)
            case str():
                self.add_group(item, i)
            case int():
                self.set_item(i, item)
            case _:
                raise TypeError(f"Invalid index type: {type(i)}")

    def __delitem__(self, i: int | str | slice) -> None:
        """Deletes an item from this GroupedList.

        Args:
            i: If an integer, the index of the item to delete.
               If a string, the name of the group to delete.
               If a slice, the slice of items to delete.

        Raises:
            TypeError: If the index type is not supported.
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        match i:
            case slice():
                self.delete_slice(i)
            case str():
                self.remove_group(i)
            case int():
                self.delete_item(i)
            case _:
                raise TypeError(f"Invalid index type: {type(i)}")

    def __iter__(self) -> Iterator[Any]:
        """Returns an iterator over all items in this GroupedList, including items in child groups.

        Yields:
            Each item in this GroupedList, including items in child groups.
        """
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                for sub_item in item:
                    yield sub_item
            else:
                yield item

    def __contains__(self, item: Any) -> bool:
        """Checks if an item is in this GroupedList, including in child groups.

        Args:
            item: The item to check for.

        Returns:
            True if the item is in this GroupedList or any of its child groups, False otherwise.
        """
        return item in self.as_flat_list()

    # Representation
    def __repr__(self) -> str:
        """Returns a string representation of this GroupedList.

        Returns:
            A string representation of the flat tuple of items in this GroupedList.
        """
        return repr(self.as_flat_tuple())

    def __hash__(self) -> int:
        """Overrides hash to make the class hashable.

        Returns:
            The system ID of the class.
        """
        return id(self)

    # Type Conversion
    def __cast(self, other: Any) -> Any:
        """Casts another object to a comparable type.

        Args:
            other: The object to cast.

        Returns:
            If other is a GroupedList, returns its flat list representation.
            Otherwise, returns the object unchanged.
        """
        return other.as_flat_list() if isinstance(other, GroupedList) else other

    # Comparison
    def __lt__(self, other: Any) -> bool:
        """Checks if this GroupedList is less than another object.

        Args:
            other: The object to compare with.

        Returns:
            True if this GroupedList is less than the other object, False otherwise.
        """
        return self.as_flat_list() < self.__cast(other)

    def __le__(self, other: Any) -> bool:
        """Checks if this GroupedList is less than or equal to another object.

        Args:
            other: The object to compare with.

        Returns:
            True if this GroupedList is less than or equal to the other object, False otherwise.
        """
        return self.as_flat_list() <= self.__cast(other)

    def __eq__(self, other: Any) -> bool:
        """Checks if this GroupedList is equal to another object.

        Args:
            other: The object to compare with.

        Returns:
            True if this GroupedList is equal to the other object, False otherwise.
        """
        return self.as_flat_list() == self.__cast(other)

    def __gt__(self, other: Any) -> bool:
        """Checks if this GroupedList is greater than another object.

        Args:
            other: The object to compare with.

        Returns:
            True if this GroupedList is greater than the other object, False otherwise.
        """
        return self.as_flat_list() > self.__cast(other)

    def __ge__(self, other: Any) -> bool:
        """Checks if this GroupedList is greater than or equal to another object.

        Args:
            other: The object to compare with.

        Returns:
            True if this GroupedList is greater than or equal to the other object, False otherwise.
        """
        return self.as_flat_list() >= self.__cast(other)

    # Arithmetic
    def __add__(self, other: Any) -> GroupedList:
        """Adds this GroupedList to another object.

        Args:
            other: The object to add to this GroupedList.

        Returns:
            A new GroupedList containing the items from this GroupedList and the other object.
        """
        return self.add(other)

    def __radd__(self, other: Any) -> GroupedList:
        """Adds another object to this GroupedList (right-side addition).

        Args:
            other: The object to add this GroupedList to.

        Returns:
            A new GroupedList containing the items from the other object and this GroupedList.
        """
        return self.radd(other)

    def __iadd__(self, other: Any) -> GroupedList:
        """Adds another object to this GroupedList in-place.

        Args:
            other: The object to add to this GroupedList.

        Returns:
            This GroupedList with the items from the other object added.
        """
        return self.iadd(other)

    def __mul__(self, n: int) -> GroupedList:
        """Multiplies this GroupedList by a number.

        Args:
            n: The number to multiply by.

        Returns:
            A new GroupedList containing the items from this GroupedList repeated n times.
        """
        new = self.__class__(items=self.data * n, parents=self.parents)
        self.add_parent_to_children(new)
        new.groups.update(self.groups)
        return new

    __rmul__ = __mul__

    def __imul__(self, n: int) -> GroupedList:
        """Multiplies this GroupedList by a number in-place.

        Args:
            n: The number to multiply by.

        Returns:
            This GroupedList with its items repeated n times.
        """
        self.data *= n
        return self

    # Instance Methods #
    # Constructors/Destructors #
    def construct(
        self,
        items: Iterable[Any] | None = None,
        parent: GroupedList | None = None,
        parents: Iterable[GroupedList] | None = None,
    ) -> None:
        """Constructs this object.

        Args:
            items: The items to add to this GroupList.
            parent: The parent GroupList of this GroupList.
            parents: The parent and ancestors of this GroupList
        """
        if parent is not None:
            self.parents.add(parent)

        if parents is not None:
            self.parents.update(parents)

        if items is not None:
            self.data.clear()
            self.data.extend(items)

    def check_if_child(self, other: GroupedList) -> bool:
        """Checks if this GroupedList is a child of another GroupedList.

        Args:
            other: The GroupedList to check if this is a child of.

        Returns:
            True if this GroupedList is a child of the other GroupedList, False otherwise.
        """
        return self in other.parents

    def check_if_parent(self, other: GroupedList) -> bool:
        """Checks if this GroupedList is a parent of another GroupedList.

        Args:
            other: The GroupedList to check if this is a parent of.

        Returns:
            True if this GroupedList is a parent of the other GroupedList, False otherwise.
        """
        return other in self.parents

    def add_parent_to_children(self, other: GroupedList) -> None:
        """Adds another GroupedList as a parent to all child GroupedLists of this GroupedList.

        Args:
            other: The GroupedList to add as a parent to all child GroupedLists.
        """
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.parents.add(other)

    def remove_parent_from_children(self, other: GroupedList) -> None:
        """Removes another GroupedList as a parent from all child GroupedLists of this GroupedList.

        Args:
            other: The GroupedList to remove as a parent from all child GroupedLists.
        """
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.parents.remove(other)

    def get_group_lengths(self, recurse: bool = False) -> tuple[int, tuple]:
        """Gets the lengths of this GroupedList and its child groups.

        Args:
            recurse: If True, recursively get the lengths of child groups.
                    If False, only get the direct length of child groups.

        Returns:
            A tuple containing:
                - The number of non-group items in this GroupedList
                - A tuple of lengths of child groups
        """
        lengths = deque()
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                if recurse:
                    lengths.append(item.get_group_lengths(recurse))
                else:
                    lengths.append(len(item))

        if len(lengths) == 0:
            return len(self.data) - len(self.groups)
        else:
            return len(self.data) - len(self.groups), tuple(lengths)

    def get_length(self) -> int:
        """Gets the total number of items in this GroupedList, including items in child groups.

        Returns:
            The total number of items in this GroupedList.
        """
        n_items = len(self.data) - len(self.groups)
        for group in self.groups.values():
            n_items += len(group)
        return n_items

    def create_group(
        self,
        name: str,
        items: Iterable | None = None,
        parents: Iterable[GroupedList] | None = None,
    ) -> GroupedList:
        """Creates a new group with the given name and adds it to this GroupedList.

        Args:
            name: The name of the group to create.
            items: The items to add to the new group.
            parents: The parents of the new group.

        Returns:
            The newly created group.

        Raises:
            KeyError: If a group with the given name already exists.
        """
        if name not in self.groups:
            new_group = self.__class__(items=items, parent=self, parents=parents)
            self.groups[name] = new_group
            self.data.append(new_group)
            return new_group
        else:
            raise KeyError(f"{name} group already exists.")

    def require_group(
        self,
        name: str | Iterable[str],
        items: Iterable | None = None,
        parents: Iterable[GroupedList] | None = None,
    ) -> GroupedList:
        """Gets an existing group with the given name or creates it if it doesn't exist.

        Args:
            name: The name of the group to get or create. Can be a single string or an iterable of strings for nested
                groups.
            items: The items to add to the new group.
            parents: The parents of the new group.

        Returns:
            The existing or newly created group.
        """
        if isinstance(name, str):
            names = [name]
        else:
            names = list(name)

        # Require name at this level
        first = names.pop()
        new_group = self.groups.get(first, SEARCHSENTINEL)
        if new_group is SEARCHSENTINEL:
            new_group = self.__class__(items=items, parent=self, parents=parents)
            self.groups[first] = new_group
            self.data.append(new_group)

        # Recurse if needed
        if names:
            new_group = new_group.require_group(names)

        return new_group

    def remove_group(self, group: str | GroupedList) -> None:
        """Removes a group from this GroupedList.

        Args:
            group: The group to remove, either as a string name or a GroupedList object.

        Raises:
            KeyError: If the group name does not exist.
            ValueError: If the group object is not in this GroupedList.
        """
        if isinstance(group, str):
            name = group
            group = self.groups[name]
        else:
            name = self.groups.inverse[group]

        self.data.remove(group)
        group.parents.remove(self)
        del self.groups[name]

    def get_group(self, name: str | Iterable[str]) -> GroupedList:
        """Gets an existing group with the given name.

        Args:
            name: The name of the group to get. Can be a single string or
                 an iterable of strings for nested groups.

        Returns:
            The group with the given name.

        Raises:
            KeyError: If the group name does not exist.
        """
        if isinstance(name, str):
            names = [name]
        else:
            names = list(name)

        # Get name at this level
        first = names.pop()
        new_group = self.groups[first]

        # Recurse if needed
        if names:
            new_group = new_group.get_group(names)

        return new_group

    def add_group(self, group: GroupedList, name: str) -> None:
        """Adds an existing group to this GroupedList with the given name.

        Args:
            group: The group to add.
            name: The name to give to the group.
        """
        if group is self:
            raise ValueError("Cannot add this GroupedList to itself.")
        elif self.check_if_parent(group):
            raise ValueError("Cannot add a GroupedList that is already a parent of this GroupedList.")
        elif name in self.groups:
            raise KeyError(f"{name} group already exists.")

        self.data.append(group)
        self.groups[name] = group

    def get_item(self, i, group: str | None = None) -> Any:
        """Gets an item from this GroupedList or a specific group.

        Args:
            i: The index of the item to get.
            group: The name of the group to get the item from, or None to get from this GroupedList.

        Returns:
            The item at the specified index.

        Raises:
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].get_item(i)
        elif i < 0:
            data = reversed(self.data)
            i = -i - 1
            reverse = True
        else:
            data = self.data
            reverse = False

        for item in data:
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    return item
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def get_slice(self, slice_: slice, group: str | None = None):
        """Gets a slice of items from this GroupedList or a specific group.

        Args:
            slice_: The slice of items to get.
            group: The name of the group to get the slice from, or None to get from this GroupedList.

        Returns:
            A list containing the items in the specified slice.

        Raises:
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].get_slice(slice_)
        else:
            return self.as_flat_list()[slice_]

    def set_item(self, i, value, group: str | None = None) -> None:
        """Sets an item in this GroupedList or a specific group.

        Args:
            i: The index of the item to set.
            value: The value to set the item to.
            group: The name of the group to set the item in, or None to set in this GroupedList.

        Raises:
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].set_item(i, value)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    item.set_item(i, value)
                else:
                    self.data[j] = value

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    item.set_item(i, value)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def set_slice(self, slice_: slice, value: Iterable[Any], group: str | None = None) -> None:
        """Sets a slice of items in this GroupedList or a specific group.

        Args:
            slice_: The slice of items to set.
            value: The values to set the items to.
            group: The name of the group to set the items in, or None to set in this GroupedList.

        Raises:
            ValueError: If the length of values doesn't match the slice length.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].set_slice(slice_, value)

        flat_list = self.as_flat_list()
        indices = range(*slice_.indices(len(flat_list)))
        values = list(value)

        if len(indices) != len(values):
            raise ValueError(
                "attempt to assign sequence of size {} to slice of size {}".format(len(values), len(indices))
            )

        for i, val in zip(indices, values):
            self.set_item(i, val)

    def delete_item(self, i, group: str | None = None) -> None:
        """Deletes an item from this GroupedList or a specific group.

        Args:
            i: The index of the item to delete.
            group: The name of the group to delete the item from, or None to delete from this GroupedList.

        Raises:
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].delete_item(i)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    item.delete_item(i)
                else:
                    del self.data[j]

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    item.delete_item(i)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def delete_slice(self, slice_: slice, group: str | None = None) -> None:
        """Deletes a slice of items from this GroupedList or a specific group.

        Args:
            slice_: The slice of items to delete.
            group: The name of the group to delete the items from, or None to delete from this GroupedList.

        Raises:
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].delete_slice(slice_)

        flat_list = self.as_flat_list()
        indices = range(*slice_.indices(len(flat_list)))

        # Delete items in reverse order to avoid index shifting
        for i in sorted(indices, reverse=True):
            self.delete_item(i)

    def append(self, item: Any, group: str | None = None) -> None:
        """Appends an item to this GroupedList or a specific group.

        Args:
            item: The item to append.
            group: The name of the group to append the item to, or None to append to this GroupedList.
                  If the group doesn't exist, it will be created.
        """
        if group is None:
            self.data.append(item)
        else:
            group = self.require_group(name=group)
            group.append(item)

    def insert(self, i, item, group: str | None = None):
        """Inserts an item at a specific position in this GroupedList or a specific group.

        Args:
            i: The index where the item should be inserted.
            item: The item to insert.
            group: The name of the group to insert the item into, or None to insert into this GroupedList.

        Raises:
            KeyError: If the group name does not exist.
        """
        if group is None:
            return self.data.insert(i, item)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, contained_item in enumerate(self.data):
            if i <= 0:
                if isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                    i = -i - 1 if reverse else i
                    contained_item.set_item(i, item)
                else:
                    index = -j - 1 if reverse else j
                    self.data.insert(index, item)

                if reverse:
                    self.data.reverse()

                return
            elif isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                n_items = len(contained_item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    contained_item.insert(i, item)
                    if reverse:
                        self.data.reverse()
                    return
                else:
                    i -= n_items
            else:
                i -= 1

        self.data.append(item)
        if reverse:
            self.data.reverse()

    def pop(self, i=-1, group: str | None = None):
        """Removes and returns an item at a specific position in this GroupedList or a specific group.

        Args:
            i: The index of the item to remove. Default is -1, which removes the last item.
            group: The name of the group to remove the item from, or None to remove from this GroupedList.

        Returns:
            The item that was removed.

        Raises:
            IndexError: If the index is out of range.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].delete_item(i)
        elif i < 0:
            self.data.reverse()
            i = -i - 1
            reverse = True
        else:
            reverse = False

        for j, item in enumerate(self.data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = -i - 1 if reverse else i
                    result = item.pop(i)
                else:
                    index = -j - 1 if reverse else j
                    result = self.data[index]
                    del self.data[index]

                if reverse:
                    self.data.reverse()

                return result
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = -i - 1 if reverse else i
                    if reverse:
                        self.data.reverse()
                    return item.pop(i)
                else:
                    i -= n_items
            else:
                i -= 1
        return self.data.pop(i)

    def remove(self, item: Any, group: str | None = None) -> None:
        """Removes the first occurrence of an item from this GroupedList or a specific group.

        Args:
            item: The item to remove.
            group: The name of the group to remove the item from, or None to remove from this GroupedList.

        Raises:
            ValueError: If the item is not found.
            KeyError: If the group name does not exist.
        """
        if group is not None:
            return self.groups[group].remove(item)
        else:
            for contained_item in self.data:
                if contained_item is item:
                    self.data.remove(item)
                    return
                elif isinstance(contained_item, GroupedList) and self.check_if_child(contained_item):
                    if item in contained_item:
                        contained_item.remove(item)
                        return
        raise ValueError("item is not present in this object")

    def clear(self, group: str | None = None) -> None:
        """Removes all items from this GroupedList or a specific group.

        Args:
            group: The name of the group to clear, or None to clear this GroupedList.

        Raises:
            KeyError: If the group name does not exist.
        """
        if group is None:
            self.data.clear()
            self.groups.clear()
        else:
            self.groups[group].clear()

    def count(self, item) -> int:
        """Counts the number of occurrences of an item in this GroupedList.

        Args:
            item: The item to count.

        Returns:
            The number of times the item appears in this GroupedList.
        """
        return self.as_flat_list().count(item)

    def index(self, item, *args) -> int:
        """Returns the index of the first occurrence of an item in this GroupedList.

        Args:
            item: The item to find.
            *args: Additional arguments to pass to the underlying list's index method.

        Returns:
            The index of the first occurrence of the item.

        Raises:
            ValueError: If the item is not found.
        """
        return self.as_flat_list().index(item, *args)

    def reverse(self) -> None:
        """Reverses the order of items in this GroupedList and all child groups."""
        self.data.reverse()
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                item.reverse()

    def sort(self, /, *args, **kwds) -> None:
        """Sorts the items in this GroupedList.

        Args:
            *args: Positional arguments to pass to the underlying list's sort method.
            **kwds: Keyword arguments to pass to the underlying list's sort method.
        """
        self.data.sort(*args, **kwds)

    def extend(self, other: Iterable[Any], group: str | None = None) -> None:
        """Extends this GroupedList or a specific group with items from another iterable.

        Args:
            other: The iterable to extend with.
            group: The name of the group to extend, or None to extend this GroupedList.

        Raises:
            KeyError: If the group name does not exist.
        """
        if isinstance(other, GroupedList):
            other.add_parent_to_children(self)
            self.data.extend(other.data)
            self.groups.update(other.groups | self.groups)
        elif group is not None:
            self.groups[group].extend(other)
        else:
            self.data.extend(other)

    def add(self, other: Any) -> GroupedList:
        """Creates a new GroupedList by adding this GroupedList and another object.

        Args:
            other: The object to add to this GroupedList.

        Returns:
            A new GroupedList containing the items from this GroupedList and the other object.
        """
        if not isinstance(other, Iterable):
            other = list(other)
        new = self.copy()
        new.extend(other)
        return new

    def radd(self, other: Any) -> GroupedList:
        """Creates a new GroupedList by adding another object and this GroupedList (right-side addition).

        Args:
            other: The object to add this GroupedList to.

        Returns:
            A new GroupedList containing the items from the other object and this GroupedList.
        """
        if isinstance(other, GroupedList):
            new = other.copy()
        else:
            if not isinstance(other, Iterable):
                other = list(other)
            new = self.__class__(items=other)

        new.extend(self)
        return new

    def iadd(self, other) -> GroupedList:
        """Adds another object to this GroupedList in-place.

        Args:
            other: The object to add to this GroupedList.

        Returns:
            This GroupedList with the items from the other object added.
        """
        if not isinstance(other, Iterable):
            other = list(other)
        self.extend(other)
        return self

    def as_flat_tuple(self) -> tuple[Any]:
        """Return the contents of this GroupList as a flat tuple.

        Returns:
            A tuple with the contents of this GroupList.
        """
        return tuple(iter(self))

    def as_flat_list(self) -> list[Any]:
        """Return the contents of this GroupList as a flat list.

        Returns:
            A list with the contents of this GroupList.
        """
        return list(iter(self))
