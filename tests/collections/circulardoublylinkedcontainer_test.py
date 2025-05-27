#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" circulardoublylinkedcontainer_test.py
Tests for the CircularDoublyLinkedContainer class in the baseobjects package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import CircularDoublyLinkedContainer, LinkedNode
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestLinkedNode(ClassTest):
    """Test the LinkedNode class.

    This class tests the functionality of the LinkedNode class, which is a node in a circular doubly linked container.
    """

    # Attributes #
    class_: Type[LinkedNode] = LinkedNode

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of LinkedNode can be created.

        This test verifies that LinkedNode instances can be created with various parameters.
        """
        # Create a basic instance
        node = self.class_()
        assert node is not None
        assert node.data is None
        assert node.previous is None
        assert node.next is None

        # Create an instance with data
        data = "test_data"
        node = self.class_(data=data)
        assert node is not None
        assert node.data == data
        assert node.previous is None
        assert node.next is None

    def test_previous_property(self) -> None:
        """Test the previous property of LinkedNode.

        This test verifies that the previous property correctly gets and sets the previous node.
        """
        node1 = self.class_("node1")
        node2 = self.class_("node2")

        # Set previous
        node1.previous = node2
        assert node1.previous is node2

        # Set previous to None
        node1.previous = None
        assert node1.previous is None

    def test_next_property(self) -> None:
        """Test the next property of LinkedNode.

        This test verifies that the next property correctly gets and sets the next node.
        """
        node1 = self.class_("node1")
        node2 = self.class_("node2")

        # Set next
        node1.next = node2
        assert node1.next is node2

        # Set next to None
        node1.next = None
        assert node1.next is None

    def test_construct(self) -> None:
        """Test the construct method of LinkedNode.

        This test verifies that the construct method correctly initializes the node.
        """
        node1 = self.class_(init=False)
        node2 = self.class_("node2")
        node3 = self.class_("node3")

        # Construct with data and links
        node1.construct(data="node1", previous=node2, next_=node3)
        assert node1.data == "node1"
        assert node1.previous is node2
        assert node1.next is node3


class TestCircularDoublyLinkedContainer(ClassTest):
    """Test the CircularDoublyLinkedContainer class.

    This class tests the functionality of the CircularDoublyLinkedContainer class, which is a container that uses
    nodes which are doubly linked to one another to store data.
    """

    # Attributes #
    class_: Type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_container(self) -> CircularDoublyLinkedContainer:
        """Create an empty container for testing.

        Returns:
            An empty CircularDoublyLinkedContainer.
        """
        return self.class_()

    @pytest.fixture
    def populated_container(self) -> CircularDoublyLinkedContainer:
        """Create a container with three nodes for testing.

        Returns:
            A CircularDoublyLinkedContainer with three nodes.
        """
        container = self.class_()
        container.append("node1")
        container.append("node2")
        container.append("node3")
        return container

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CircularDoublyLinkedContainer can be created.

        This test verifies that CircularDoublyLinkedContainer instances can be created.
        """
        container = self.class_()
        assert container is not None
        assert container.first_node is None
        assert container.nodes == set()
        assert container.is_empty is True

    def test_is_empty_property(
        self,
        empty_container: CircularDoublyLinkedContainer,
        populated_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Test the is_empty property of CircularDoublyLinkedContainer.

        This test verifies that the is_empty property correctly determines if the container is empty.

        Args:
            empty_container: An empty container.
            populated_container: A container with nodes.
        """
        assert empty_container.is_empty is True
        assert populated_container.is_empty is False

    def test_last_node_property(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the last_node property of CircularDoublyLinkedContainer.

        This test verifies that the last_node property correctly returns the last node in the container.

        Args:
            populated_container: A container with nodes.
        """
        assert populated_container.last_node is not None
        assert populated_container.last_node.data == "node3"
        assert populated_container.last_node.next is populated_container.first_node

    def test_deepcopy(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the __deepcopy__ method of CircularDoublyLinkedContainer.

        This test verifies that the __deepcopy__ method creates a new container with copies of the nodes.

        Args:
            populated_container: A container with nodes.
        """
        new_container = copy.deepcopy(populated_container)
        assert new_container is not populated_container
        assert len(new_container.nodes) == len(populated_container.nodes)
        assert new_container.first_node.data == populated_container.first_node.data
        assert new_container.last_node.data == populated_container.last_node.data

    def test_len(
        self,
        empty_container: CircularDoublyLinkedContainer,
        populated_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Test the __len__ method of CircularDoublyLinkedContainer.

        This test verifies that the __len__ method returns the correct number of nodes.

        Args:
            empty_container: An empty container.
            populated_container: A container with nodes.
        """
        assert len(empty_container) == 0
        assert len(populated_container) == 3

    def test_getitem(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the __getitem__ method of CircularDoublyLinkedContainer.

        This test verifies that the __getitem__ method returns the correct node at the given index.

        Args:
            populated_container: A container with nodes.
        """
        assert populated_container[0].data == "node1"
        assert populated_container[1].data == "node2"
        assert populated_container[2].data == "node3"
        assert populated_container[-1].data == "node3"
        assert populated_container[-2].data == "node2"
        assert populated_container[-3].data == "node1"

    def test_iter(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the __iter__ method of CircularDoublyLinkedContainer.

        This test verifies that the __iter__ method returns an iterator that yields the nodes in order.

        Args:
            populated_container: A container with nodes.
        """
        nodes = list(populated_container)
        assert len(nodes) == 3
        assert nodes[0].data == "node1"
        assert nodes[1].data == "node2"
        assert nodes[2].data == "node3"

    def test_lshift(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the __lshift__ method of CircularDoublyLinkedContainer.

        This test verifies that the __lshift__ method shifts the start of nodes to the left.

        Args:
            populated_container: A container with nodes.
        """
        populated_container << 1
        assert populated_container.first_node.data == "node2"
        assert populated_container.last_node.data == "node1"

    def test_rshift(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the __rshift__ method of CircularDoublyLinkedContainer.

        This test verifies that the __rshift__ method shifts the start of nodes to the right.

        Args:
            populated_container: A container with nodes.
        """
        populated_container >> 1
        assert populated_container.first_node.data == "node3"
        assert populated_container.last_node.data == "node2"

    def test_append_data(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Test the append method of CircularDoublyLinkedContainer with data.

        This test verifies that the append method adds a new node with the given data to the end of the container.

        Args:
            empty_container: An empty container.
        """
        # Append to empty container
        node1 = empty_container.append("node1")
        assert node1 is not None
        assert node1.data == "node1"
        assert empty_container.first_node is node1
        assert empty_container.last_node is node1
        assert node1.next is None
        assert node1.previous is None

        # Append to container with one node
        node2 = empty_container.append("node2")
        assert node2 is not None
        assert node2.data == "node2"
        assert empty_container.first_node is node1
        assert empty_container.last_node is node2
        assert node1.next is node2
        assert node2.previous is node1
        assert node2.next is node1
        assert node1.previous is node2

    def test_append_node(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Test the append method of CircularDoublyLinkedContainer with a node.

        This test verifies that the append method adds an existing node to the end of the container.

        Args:
            empty_container: An empty container.
        """
        # Create nodes
        node1 = LinkedNode("node1")
        node2 = LinkedNode("node2")

        # Append to empty container
        empty_container.append(node1)
        assert empty_container.first_node is node1
        assert empty_container.last_node is node1
        assert node1.next is None
        assert node1.previous is None

        # Append to container with one node
        empty_container.append(node2)
        assert empty_container.first_node is node1
        assert empty_container.last_node is node2
        assert node1.next is node2
        assert node2.previous is node1
        assert node2.next is node1
        assert node1.previous is node2

    def test_insert_data(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the insert method of CircularDoublyLinkedContainer with data.

        This test verifies that the insert method adds a new node with the given data at the specified index.

        Args:
            populated_container: A container with nodes.
        """
        # Insert at beginning
        node = populated_container.insert("node0", 0)
        assert node.data == "node0"
        assert populated_container.first_node.data == "node0"
        assert populated_container[0].data == "node0"
        assert populated_container[1].data == "node1"

        # Insert in middle
        node = populated_container.insert("node1.5", 2)
        assert node.data == "node1.5"
        assert populated_container[0].data == "node0"
        assert populated_container[1].data == "node1"
        assert populated_container[2].data == "node1.5"
        assert populated_container[3].data == "node2"

    def test_insert_node(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the insert method of CircularDoublyLinkedContainer with a node.

        This test verifies that the insert method adds an existing node at the specified index.

        Args:
            populated_container: A container with nodes.
        """
        # Create node
        node = LinkedNode("node0")

        # Insert at beginning
        populated_container.insert(node, 0)
        assert populated_container.first_node.data == "node0"
        assert populated_container[0].data == "node0"
        assert populated_container[1].data == "node1"

    def test_remove_node(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the remove_node method of CircularDoublyLinkedContainer.

        This test verifies that the remove_node method removes a node from the container.

        Args:
            populated_container: A container with nodes.
        """
        node = populated_container[1]  # node2
        populated_container.remove_node(node)
        assert len(populated_container.nodes) == 2
        assert populated_container[0].data == "node1"
        assert populated_container[1].data == "node3"

    def test_pop(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the pop method of CircularDoublyLinkedContainer.

        This test verifies that the pop method removes and returns a node at the specified index.

        Args:
            populated_container: A container with nodes.
        """
        # Pop from end
        node = populated_container.pop()
        assert node.data == "node3"
        assert len(populated_container.nodes) == 2
        assert populated_container[0].data == "node1"
        assert populated_container[1].data == "node2"

        # Pop from beginning
        node = populated_container.pop(0)
        assert node.data == "node1"
        assert len(populated_container.nodes) == 1
        assert populated_container[0].data == "node2"

    def test_clear(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the clear method of CircularDoublyLinkedContainer.

        This test verifies that the clear method removes all nodes from the container.

        Args:
            populated_container: A container with nodes.
        """
        populated_container.clear()
        assert populated_container.first_node is None
        assert populated_container.nodes == set()
        assert populated_container.is_empty is True

    def test_move_node_start(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node_start method of CircularDoublyLinkedContainer.

        This test verifies that the move_node_start method moves a node to the start of the container.

        Args:
            populated_container: A container with nodes.
        """
        node = populated_container[2]  # node3
        populated_container.move_node_start(node)
        assert populated_container.first_node is node
        assert populated_container[0].data == "node3"
        assert populated_container[1].data == "node1"
        assert populated_container[2].data == "node2"

    def test_move_node_end(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node_end method of CircularDoublyLinkedContainer.

        This test verifies that the move_node_end method moves a node to the end of the container.

        Args:
            populated_container: A container with nodes.
        """
        node = populated_container[0]  # node1
        populated_container.move_node_end(node)
        assert populated_container.last_node is node
        assert populated_container[0].data == "node2"
        assert populated_container[1].data == "node3"
        assert populated_container[2].data == "node1"

    def test_move_node(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node method of CircularDoublyLinkedContainer.

        This test verifies that the move_node method moves a node to the specified index.

        Args:
            populated_container: A container with nodes.
        """
        node = populated_container[0]  # node1
        populated_container.move_node(node, 1)
        assert populated_container[0].data == "node2"
        assert populated_container[1].data == "node1"
        assert populated_container[2].data == "node3"

    def test_shift_left(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the shift_left method of CircularDoublyLinkedContainer.

        This test verifies that the shift_left method shifts the start of nodes to the left.

        Args:
            populated_container: A container with nodes.
        """
        populated_container.shift_left()
        assert populated_container.first_node.data == "node2"
        assert populated_container[0].data == "node2"
        assert populated_container[1].data == "node3"
        assert populated_container[2].data == "node1"

    def test_shift_right(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the shift_right method of CircularDoublyLinkedContainer.

        This test verifies that the shift_right method shifts the start of nodes to the right.

        Args:
            populated_container: A container with nodes.
        """
        populated_container.shift_right()
        assert populated_container.first_node.data == "node3"
        assert populated_container[0].data == "node3"
        assert populated_container[1].data == "node1"
        assert populated_container[2].data == "node2"

    def test_forward_iter(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the forward_iter method of CircularDoublyLinkedContainer.

        This test verifies that the forward_iter method returns an iterator that yields the nodes in forward order.

        Args:
            populated_container: A container with nodes.
        """
        iterator = populated_container.forward_iter()
        nodes = list(iterator)
        assert len(nodes) == 3
        assert nodes[0].data == "node1"
        assert nodes[1].data == "node2"
        assert nodes[2].data == "node3"

    def test_reverse_iter(self, populated_container: CircularDoublyLinkedContainer) -> None:
        """Test the reverse_iter method of CircularDoublyLinkedContainer.

        This test verifies that the reverse_iter method returns an iterator that yields the nodes in reverse order.

        Args:
            populated_container: A container with nodes.
        """
        iterator = populated_container.reverse_iter()
        nodes = list(iterator)
        assert len(nodes) == 3
        assert nodes[0].data == "node3"
        assert nodes[1].data == "node2"
        assert nodes[2].data == "node1"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
