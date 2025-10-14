"""circulardoublylinkedcontainer.py
A circular doubly linked container for efficient ordered data storage.

This module provides the CircularDoublyLinkedContainer class and supporting LinkedNode class for implementing a
circular doubly linked list data structure. This container is particularly efficient for storing ordered data that
frequently changes size, as it allows for constant-time insertions and deletions at any position once a reference
to that position is obtained. The circular nature of the container enables efficient traversal in both directions.
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
import copy
import weakref
from collections.abc import Iterable
from typing import Any, Optional

# Local Packages #
from ..bases import BaseObject, BaseReducible
from ..functions import singlekwargdispatch


# Definitions #
# Classes #
class LinkedNode(BaseReducible):
    """A node in a circular doubly linked container.

    Attributes:
        _previous: A weak reference to the previous node.
        _next: A weak reference to the next node.
        data: The data contained within this node.

    Args:
        data: The data to contain within this node.
        previous: The previous node.
        next_: The next node.
    """

    # Attributes #
    _previous: weakref.ReferenceType | None = None
    _next: weakref.ReferenceType | None = None

    data: Any | None = None

    # Properties #
    @property
    def previous(self) -> Any:
        """The previous node."""
        try:
            return self._previous()
        except TypeError:
            return None

    @previous.setter
    def previous(self, value: Any) -> None:
        self._previous = None if value is None else weakref.ref(value)

    @property
    def next(self) -> Any:
        """The next node."""
        try:
            return self._next()
        except TypeError:
            return None

    @next.setter
    def next(self, value: Any) -> None:
        self._next = None if value is None else weakref.ref(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        data: Any | None = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a linked node.

        Args:
            data: Optional data to store in the node.
            previous: Optional previous node.
            next_: Optional next node.
            *args: Positional arguments forwarded to the parent.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments for construction.
        """
        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(data=data, previous=previous, next_=next_)

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the object's state for pickling.

        This method prepares the object for pickling by converting the weak references to other nodes into strong
        references. This is necessary because weak references cannot be pickled directly. The method first gets the
        state from the parent class, then adds the nodes as a strong reference.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: Neither __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        # Convert weak reference to strong reference for pickling
        state["_next"] = self.next
        state["_previous"] = self.previous
        return state

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        This method restores the object from a pickled state by first extracting the nodes from the state. Then sets the
        state using the parent class's __setstate__ method. Finally, it converts the strong reference to the other nodes
        back into weak references.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object.
        """
        next_ = state.pop("_next", None)
        previous = state.pop("_previous", None)
        super().__setstate__(state)
        if next_ is not None:
            self._next = weakref.ref(next_)
        if previous is not None:
            self._previous = weakref.ref(previous)

    # Instance Methods #
    # Constructors
    def construct(
        self,
        data: Any | None = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object.

        Args:
            data: The data to contain within this node.
            previous: The previous node.
            next_: The next node.
        """
        if previous is not None:
            self._previous = weakref.ref(previous)

        if next_ is not None:
            self._next = weakref.ref(next_)

        self.data = data

        super().construct(*args, **kwargs)


class CircularDoublyLinkedContainer(BaseObject):
    """A container that uses nodes which are doubly linked to one another to store data.

    Attributes:
        first_node: The first linked node in this container.
        nodes: The set of nodes in this container.
    """

    # Attributes #
    first_node: LinkedNode | None = None
    nodes: set[LinkedNode]

    # Properties #
    @property
    def is_empty(self) -> bool:
        """Determines if this container is empty."""
        return self.first_node is None

    @property
    def last_node(self) -> LinkedNode:
        """The last node in this container."""
        return self.first_node if (last_node := self.first_node.previous) is None else last_node

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize an empty circular doubly linked container."""
        # Parent Initialization #
        super().__init__(*args, **kwargs)

        # Attributes #
        self.nodes: set[LinkedNode] = set()

    def __deepcopy__(self, memo: dict | None = None, _nil=None) -> "CircularDoublyLinkedContainer":
        """Creates a deep copy of this object.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        if _nil is None:
            _nil = []
        new_obj = type(self)()
        if not self.is_empty:
            original_node = self.first_node
            new_obj.append(data=copy.deepcopy(original_node.data))
            while original_node.next is not self.first_node:
                original_node = original_node.next
                new_obj.append(data=copy.deepcopy(original_node.data))

        return new_obj

    # Container Methods
    def __len__(self) -> int:
        """Gets this object's length (number of nodes).

        Returns:
            The number of nodes in this object.
        """
        return self.get_length()

    def __getitem__(self, item: int) -> LinkedNode:
        """The method that allows index retrievals a node.

        Args:
            item: The index of the item to get.

        Returns:
            The node based on the index.
        """
        return self.get_item(item)

    def __iter__(self) -> Iterable:
        """Returns an iterable representation of this object.

        Returns:
            The iterable representation of this of object.
        """
        return self.forward_iter()

    # Bitwise Operators
    def __lshift__(self, other: int) -> None:
        """Shifts the start of nodes to the left by an amount.

        Args:
            other: The number of nodes to shift to the left.
        """
        self.shift_left(other)

    def __rshift__(self, other: int) -> None:
        """Shifts the start of nodes to the right by an amount.

        Args:
            other: The number of nodes to right to the left.
        """
        self.shift_right(other)

    # Instance Methods #
    # Container Methods
    def get_length(self) -> int:
        """Gets the number of nodes in this container.

        Returns:
            The number of nodes in this object.
        """
        return len(self.nodes)

    def get_item(self, index: int) -> LinkedNode:
        """Gets a node based on its index from the start node.

        Args:
            index: The index of the item to get.

        Returns:
            The node based on the index.
        """
        node = self.first_node

        # Forward Indexing
        if index > 0:
            for _i in range(index):
                node = node.next
        # Reverse Indexing
        elif index < 0:
            index *= -1
            for _i in range(index):
                node = node.previous

        return node

    @singlekwargdispatch(kwarg="data")
    def append(self, data: Any) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)
        self.nodes.add(new_node)

        if self.first_node is None:
            self.first_node = new_node
        else:
            weak_node = weakref.ref(new_node)
            new_node.next = self.first_node
            new_node.previous = self.last_node
            self.last_node._next = weak_node
            self.first_node._previous = weak_node

        return new_node

    @append.register
    def _(self, data: LinkedNode) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        self.nodes.add(data)

        if self.first_node is None:
            self.first_node = data
        else:
            weak_node = weakref.ref(data)
            data.next = self.first_node
            data.previous = self.last_node
            self.last_node._next = weak_node
            self.first_node._previous = weak_node

        return data

    @singlekwargdispatch(kwarg="data")
    def insert(self, data: Any, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns:
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)
        self.nodes.add(new_node)

        if self.first_node is None:
            self.first_node = new_node
        else:
            if index == 0:
                point = self.first_node
                self.first_node = new_node
            else:
                point = self.get_item(index=index)
            weak_node = weakref.ref(new_node)
            new_node.next = point
            previous = point._previous
            new_node._previous = weakref.ref(point) if previous is None else previous
            new_node.previous._next = weak_node
            point._previous = weak_node

        return new_node

    @insert.register
    def _(self, data: LinkedNode, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns:
            The LinkedNode added to the container.
        """
        self.nodes.add(data)

        if self.first_node is None:
            self.first_node = data
        else:
            if index == 0:
                point = self.first_node
                self.first_node = data
            else:
                point = self.get_item(index=index)
            weak_node = weakref.ref(data)
            data.next = point
            previous = point._previous
            data._previous = weakref.ref(point) if previous is None else previous
            data.previous._next = weak_node
            point._previous = weak_node
        return data

    def remove_node(self, node: LinkedNode) -> None:
        """Removes a node from the container.

        Args:
            node: The node to move.
        """
        if node is self.first_node:
            self.first_node = node.next
        if self.first_node is not None:
            node.next.previous = node.previous
            node.previous.next = node.next
        self.nodes.remove(node)

    def pop(self, index: int = -1) -> LinkedNode:
        """Removes a node at the index within the container and return it.

        Args:
            index: The index of the node to pop.

        Returns:
            The LinkedNode removed from the container.
        """
        node = self.get_item(index=index)
        self.remove_node(node)
        return node

    def clear(self) -> None:
        """Clears this container by removing the first node."""
        self.nodes.clear()
        self.first_node = None

    # Node Manipulation
    def move_node_start(self, node: LinkedNode) -> None:
        """Move a node to the start of the container.

        Args:
            node: The node to move.
        """
        if node is not self.first_node:
            self.move_node_end(node)
            self.first_node = node

    def move_node_end(self, node: LinkedNode) -> None:
        """Move a node to the end of container.

        Args:
            node: The node to move.
        """
        if node is not self.last_node:
            if node is self.first_node:
                self.first_node = node.next
            node.next.previous = node.previous
            node.previous.next = node.next
            node.next = self.first_node
            node.previous = self.last_node
            self.last_node.next = node
            self.first_node.previous = node

    def move_node(self, node: LinkedNode, index: int) -> None:
        """Move a node to an index within the container.

        Args:
            node: The node to move.
            index: The place to move the node to.
        """
        if node is self.first_node and index != 0:
            self.first_node = node.next
        if (point := self.get_item(index=index)) is not node:
            node.next.previous = node.previous
            node.previous.next = node.next
            node.next = point
            node.previous = point.previous
            node.previous.next = node
            point.previous = node

    def shift_left(self, value: int = 1) -> None:
        """Shift the start of nodes to the left by an amount.

        Args:
            value: The number of nodes to shift to the left.
        """
        if value == 1:
            self.first_node = self.first_node.next
        elif value > 1:
            i = 0
            while i < value:
                self.first_node = self.first_node.next
                i += 1

    def shift_right(self, value: int = 1) -> None:
        """Shift the start of nodes to the right by an amount.

        Args:
            value: The number of nodes to right to the left.
        """
        if value == 1:
            self.first_node = self.first_node.previous
        elif value > 1:
            i = 0
            while i < value:
                self.first_node = self.first_node.previous
                i += 1

    # Iteration
    def forward_iter(self) -> Iterable:
        """Creates an iterable which iterates through the nodes from first to last.

        Yields:
            LinkedNode: Each node from first to last.
        """
        if self.first_node is not None:
            node = self.first_node
            yield node
            if (node := node.next) is not None:
                while node is not self.first_node:
                    yield node
                    node = node.next

    def reverse_iter(self) -> Iterable:
        """Creates an iterable which iterates through the nodes from last to first.

        Yields:
            LinkedNode: Each node from last to first.
        """
        if self.first_node is not None:
            node = self.last_node
            yield node
            if (node := node.previous) is not None:
                while node is not self.last_node:
                    yield node
                    node = node.previous

    def forward_cycle(self) -> Iterable:
        """Creates an iterable which cycles through the nodes from first to last.

        Yields:
            LinkedNode: Each node in sequence, cycling from first to last indefinitely.
        """
        if self.first_node is not None:
            node = self.first_node
            while True:
                yield node
                node = node.next

    def reverse_cycle(self) -> Iterable:
        """Creates an iterable which cycles through the nodes from last to first.

        Yields:
            LinkedNode: Each node in sequence, cycling from last to first indefinitely.
        """
        node = self.last_node
        while True:
            yield node
            node = node.previous
