#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" circulardoublylinkedcontainer.py
A circular doubly linked container which is a fast and efficient way to store ordered data, especially if constantly
changes size.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
import copy
from functools import singledispatchmethod
from typing import Any, Optional

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class LinkedNode(BaseObject):
    """A node in a circular doubly linked container.

    Attributes:
        previous: The previous node.
        next: The next node.
        data: The data contained within this node.

    Args:
        data: The data to contain within this node.
        previous: The previous node.
        next_: The next node.
    """

    __slots__ = ["previous", "next", "data"]

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        data: Optional[Any] = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
        init: bool = True,
    ) -> None:
        # Attributes #
        self.previous: "LinkedNode" = self
        self.next: "LinkedNode" = self

        self.data: Optional[Any] = None

        # Object Construction #
        if init:
            self.construct(data=data, previous=previous, next_=next_)

    # Instance Methods #
    # Constructors
    def construct(
        self,
        data: Optional[Any] = None,
        previous: Optional["LinkedNode"] = None,
        next_: Optional["LinkedNode"] = None,
    ) -> None:
        """Constructs this object.

        Args:
            data: The data to contain within this node.
            previous: The previous node.
            next_: The next node.
        """
        self.previous = previous
        self.next = next_

        self.data = data


class CircularDoublyLinkedContainer(BaseObject):
    """A container that uses nodes which are doubly linked to one another to store data.

    Attributes:
        first_node: The first linked node in this container.
    """

    __slots__ = "first_node"

    # Magic Methods #
    # Construction/Destruction
    def __init__(self) -> None:
        # Attributes #
        self.first_node: Optional[LinkedNode] = None

    @property
    def is_empty(self) -> bool:
        """Determines if this container is empty."""
        return self.first_node is None

    @property
    def last_node(self) -> LinkedNode:
        """The last node in this container."""
        return self.first_node.previous

    def __deepcopy__(
        self, memo: Optional[dict] = None, _nil=[]
    ) -> "CircularDoublyLinkedContainer":
        """Creates a deep copy of this object.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        new_obj = type(self)()
        if not self.is_empty:
            original_node = self.first_node
            new_obj.append(data=copy.deepcopy(original_node.data))
            while original_node.next is not self.first_node:
                new_obj.append(data=copy.deepcopy(original_node.data))
                original_node = original_node.next

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
        if self.is_empty:
            return 0
        else:
            length = 1
            node = self.first_node.next
            while node is not self.first_node:
                node = node.next
                length += 1
            return length

    def get_item(self, index: int) -> LinkedNode:
        """Gets a node based on its index from the start node.

        Args:
            index: The index of the item to get.

        Returns:
            The node based on the index.
        """
        node = self.first_node
        i = 0

        # Forward Indexing
        if index > 0:
            while i < index:
                node = node.next
                i += 1
        # Reverse Indexing
        elif index < 0:
            index *= -1
            while i < index:
                node = node.previous
                i += 1

        return node

    @singledispatchmethod
    def append(self, data) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)

        if self.first_node is None:
            self.first_node = new_node
        else:
            self.last_node.next = new_node
            self.first_node.previous = new_node

        return new_node

    @append.register
    def _(self, data: LinkedNode) -> LinkedNode:
        """Add a new node and data to the end of the container.

        Args:
            data: The data to add to the new last node.

        Returns:
            The LinkedNode added to the container.
        """
        new_node = data

        if self.first_node is None:
            self.first_node = new_node
        else:
            self.last_node.next = new_node
            self.first_node.previous = new_node

        return new_node

    @singledispatchmethod
    def insert(self, data, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns
            The LinkedNode added to the container.
        """
        new_node = LinkedNode(data)

        if self.first_node is None:
            self.first_node = new_node
        else:
            point = self.get_item(index=index)
            new_node.next = point
            new_node.previous = point.previous
            new_node.previous.next = new_node
            point.previous = new_node

        return new_node

    @insert.register
    def _(self, data: LinkedNode, index: int) -> LinkedNode:
        """Add a new node and data at index within the container.

        Args:
            data: The data to add to the new node.
            index: The place to insert the new node at.

        Returns
            The LinkedNode added to the container.
        """
        new_node = data

        if self.first_node is None:
            self.first_node = new_node
        else:
            point = self.get_item(index=index)
            new_node.next = point
            new_node.previous = point.previous
            new_node.previous.next = new_node
            point.previous = new_node

        return new_node

    def clear(self) -> None:
        """Clears this container by removing the first node."""
        del self.first_node
        self.first_node = None

    # Node Manipulation
    def move_node_start(self, node: LinkedNode) -> None:
        """Move a node to the start of the container.

        Args:
            node: The node to move.
        """
        self.move_node_end(node)
        self.first_node = node

    def move_node_end(self, node: LinkedNode) -> None:
        """Move a node to the end of container.

        Args:
            node: The node to move.
        """
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
        node.next.previous = node.previous
        node.previous.next = node.next
        point = self.get_item(index=index)
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
            while i <= value:
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
            while i <= value:
                self.first_node = self.first_node.previous
                i += 1
