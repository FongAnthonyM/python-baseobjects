#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" circulardoublylinkedcontainer.py
An abstract class which creates properties for this class automatically.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Default Libraries #
import copy

# Downloaded Libraries #

# Local Libraries #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class LinkedNode(BaseObject):
    __slots__ = ["previous", "next", "data"]

    # Magic Methods
    # Construction/Destruction
    def __init__(self, data=None, previous=None, next_=None, init=True):
        self.previous = self
        self.next = self

        self.data = None

        if init:
            self.construct(data=data, previous=previous, next_=next_)

    # Instance Methods
    # Constructors
    def construct(self, data=None, previous=None, next_=None):
        self.previous = previous
        self.next = next_

        self.data = data


class CirularDoublyLinkedContainer(BaseObject):
    __slots__ = "first_node"

    # Magic Methods
    # Construction/Destruction
    def __init__(self):
        self.first_node = None

    @property
    def is_empty(self):
        return self.first_node is None

    @property
    def last_node(self):
        return self.first_node.previous

    def __deepcopy__(self, memo=None, _nil=[]):
        """The deepcopy magic method

        Args:
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

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
    def __len__(self):
        return self.get_length()

    def __getitem__(self, item):
        return self.get_item(item)

    # Bitwise Operators
    def __lshift__(self, other):
        self.shift_left(other)

    def __rshift__(self, other):
        self.shift_right(other)

    # Instance Methods
    # Constructors
    # Container Methods
    def get_length(self):
        if self.is_empty:
            return 0
        else:
            length = 1
            node = self.first_node.next
            while node is not self.first_node:
                node = node.next
                length += 1
            return length

    def get_item(self, index):
        node = self.first_node
        i = 0
        if index > 0:
            while i < index:
                node = node.next
                i += 1
        elif index < 0:
            index * -1
            while i < index:
                node = node.previous
                i += 1

        return node

    def append(self, data):
        if isinstance(data, LinkedNode):
            new_node = data
        else:
            new_node = LinkedNode(data)

        if self.first_node is None:
            self.first_node = new_node
        else:
            self.last_node.next = new_node
            self.first_node.previous = new_node

        return new_node

    def insert(self, data, index):
        if isinstance(data, LinkedNode):
            new_node = data
        else:
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

    def clear(self):
        self.first_node = None

    # Node Manipulation
    def move_node_start(self, node):
        self.move_node_end(node)
        self.first_node = node

    def move_node_end(self, node):
        node.next.previous = node.previous
        node.previous.next = node.next
        node.next = self.first_node
        node.previous = self.last_node
        self.last_node.next = node
        self.first_node.previous = node

    def move_node(self, node, index):
        node.next.previous = node.previous
        node.previous.next = node.next
        point = self.get_item(index=index)
        node.next = point
        node.previous = point.previous
        node.previous.next = node
        point.previous = node

    def shift_left(self, value=1):
        if value == 1:
            self.first_node = self.first_node.next
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.next
                i += 1

    def shift_right(self, value=1):
        if value == 1:
            self.first_node = self.first_node.previous
        elif value > 1:
            i = 0
            while i <= value:
                self.first_node = self.first_node.previous
                i += 1
