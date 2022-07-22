""" groupedlist.py

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
from collections import deque
from collections.abc import Iterable, Iterator
from typing import Any, Union, Optional

# Third-Party Packages #

# Local Packages #
from ..bases import BaseList, search_sentinel


# Definitions #
# Classes #
class GroupedList(BaseList):
    """

    Class Attributes:

    Attributes:

    Args:

    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(self, items, parent: Optional["GroupedList"] = None, init: bool = True) -> None:
        # Parent Attributes #
        super().__init__()

        # New Attributes #
        self.parent: GroupedList | None = None

        self.groups: dict[str, "GroupedList"] = {}

        # Object Construction #
        if init:
            self.construct()

    def __iter__(self) -> Iterator[Any]:
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                for sub_item in item:
                    yield sub_item
            else:
                yield item

    def __repr__(self) -> str:
        return repr(self.as_flat_tuple())

    def __cast(self, other: Any) -> Any:
        return other.as_flat_list() if isinstance(other, GroupedList) else other

    def __lt__(self, other: Any) -> bool:
        return self.as_flat_list() < self.__cast(other)

    def __le__(self, other: Any) -> bool:
        return self.as_flat_list() <= self.__cast(other)

    def __eq__(self, other: Any) -> bool:
        return self.as_flat_list() == self.__cast(other)

    def __gt__(self, other: Any) -> bool:
        return self.as_flat_list() > self.__cast(other)

    def __ge__(self, other: Any) -> bool:
        return self.as_flat_list() >= self.__cast(other)

    def __contains__(self, item: Any) -> bool:
        return item in self.as_flat_list()

    def __len__(self) -> int:
        return self.get_length()

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other):
        if isinstance(other, UserList):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    def __radd__(self, other):
        if isinstance(other, UserList):
            return self.__class__(other.data + self.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(other + self.data)
        return self.__class__(list(other) + self.data)

    def __iadd__(self, other):
        if isinstance(other, UserList):
            self.data += other.data
        elif isinstance(other, type(self.data)):
            self.data += other
        else:
            self.data += list(other)
        return self

    def __mul__(self, n):
        return self.__class__(self.data * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst


    # Instance Methods #
    # Constructors/Destructors
    def construct(self, ) -> None:
        pass

    def check_if_child(self, other: "GroupedList") -> bool:
        return self is other.parent

    def check_if_parent(self, other: "GroupedList") -> bool:
        return self.parent is other

    def get_group_lengths(self) -> tuple[int]:
        lengths = deque()
        for item in self.data:
            if isinstance(item, GroupedList) and self.check_if_child(item):
                lengths.append(len(item))
        return tuple(lengths)

    def get_length(self) -> int:
        n_items = len(self.data) - len(self.groups)
        for group in self.groups.values():
            n_items += len(group)
        return n_items

    def create_group(self, name: str, items: Iterable | None = None) -> "GroupedList":
        if name not in self.groups:
            new_group = GroupedList(items, parent=self)
            self.groups[name] = new_group
            return new_group
        else:
            raise KeyError(f"{name} group already exists.")

    def require_group(self, name: str) -> "GroupedList":
        new_group = self.groups.get(name, search_sentinel)
        if new_group is search_sentinel:
            new_group = GroupedList(parent=self)
            self.groups[name] = new_group
        return new_group

    def get_item(self, i, group: str | None = None) -> Any:
        if group is not None:
            return self.groups[group].get_item(i)
        elif i < 0:
            data = self.data.reverse()
            i = - i - 1
            reverse = True
        else:
            data = self.data
            reverse = False

        for item in data:
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = - i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    return item
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = - i - 1 if reverse else i
                    return item.get_item(i)
                else:
                    i - n_items
            else:
                i -= 1

        raise IndexError("index out of range")

    def set_item(self, i, value, group: str | None = None) -> None:
        if group is not None:
            return self.groups[group].set_item(i, value)
        elif i < 0:
            data = self.data.reverse()
            i = - i - 1
            reverse = True
        else:
            data = self.data
            reverse = False

        for j, item in enumerate(data):
            if i <= 0:
                if isinstance(item, GroupedList) and self.check_if_child(item):
                    i = - i - 1 if reverse else i
                    return item.set_item(i, value)
                else:
                    index = - j - 1 if reverse else j
                    return self.data[index]
            elif isinstance(item, GroupedList) and self.check_if_child(item):
                n_items = len(item)
                if i < n_items:
                    i = - i - 1 if reverse else i
                    return item.set_item(i, value)
                else:
                    i - n_items
            else:
                i -= 1

        raise IndexError("index out of range")




    def append(self, item: Any, group: str | None = None):
        if group is None:
            self.data.append(item)
        else:
            group = self.require_group(name=group)
            group.append(item)

    def insert(self, i, item, group: str | None = None):
        if group is None:
            self.data.insert(i, item)
        else:
            group = self.require_group(name=group)
            group.insert(item)

    def pop(self, i=-1):
        return self.data.pop(i)

    def remove(self, item):
        self.data.remove(item)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return self.data.count(item)

    def index(self, item, *args):
        return self.data.index(item, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        self.data.sort(*args, **kwds)

    def extend(self, other):
        if isinstance(other, UserList):
            self.data.extend(other.data)
        else:
            self.data.extend(other)

    def as_flat_tuple(self) -> tuple[Any]:
        return tuple(iter(self))
    
    def as_flat_list(self) -> list[Any]:
        return list(iter(self))
    