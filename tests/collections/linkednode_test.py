"""linkednode_test.py
Tests for the LinkedNode class in the baseobjects package.

This module provides tests for the LinkedNode class, which is a node in a circular doubly linked container.
It tests the functionality of LinkedNode including its properties, construction, and methods.
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
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections.circulardoublylinkedcontainer import LinkedNode
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestLinkedNode(BaseObjectTestSuite):
    """Test the LinkedNode class.

    This class tests the functionality of the LinkedNode class, which is a node in a circular doubly linked container.
    """

    # Attributes #
    TestClass: Type[LinkedNode] = LinkedNode

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_node(self) -> LinkedNode:
        """Create an empty LinkedNode for testing.

        Returns:
            LinkedNode: An empty LinkedNode.
        """
        return self.TestClass()

    @pytest.fixture
    def data_node(self) -> LinkedNode:
        """Create a LinkedNode with data for testing.

        Returns:
            LinkedNode: A LinkedNode with data.
        """
        return self.TestClass(data="test_data")

    @pytest.fixture
    def linked_nodes(self) -> tuple[LinkedNode, LinkedNode, LinkedNode]:
        """Create a set of linked nodes for testing.

        Returns:
            tuple[LinkedNode, LinkedNode, LinkedNode]: A tuple of three linked nodes.
        """
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass(data="node2")
        node3 = self.TestClass(data="node3")

        # Link the nodes in a circular fashion
        node1.next = node2
        node2.next = node3
        node3.next = node1

        node1.previous = node3
        node2.previous = node1
        node3.previous = node2

        return node1, node2, node3

    @pytest.fixture
    def test_object(self) -> LinkedNode:
        """Create a test object for testing.

        Returns:
            LinkedNode: A LinkedNode with data and links.
        """
        node = self.TestClass(data="test_data")
        return node

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of LinkedNode can be created with various parameters."""
        # Create an empty instance
        node = self.TestClass()
        assert node is not None
        assert isinstance(node, self.TestClass)
        assert node.data is None
        assert node.previous is None
        assert node.next is None

        # Create an instance with data
        node = self.TestClass(data="test_data")
        assert node is not None
        assert isinstance(node, self.TestClass)
        assert node.data == "test_data"
        assert node.previous is None
        assert node.next is None

        # Create an instance with data and links
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass(data="node2", previous=node1)
        node1.next = node2

        assert node1.next is node2
        assert node2.previous is node1

    def test_copy(self, test_object: LinkedNode) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.data == test_object.data
        assert obj_copy.previous is None
        assert obj_copy.next is None

    def test_copy_method(self, test_object: LinkedNode) -> None:
        """Test the copy method behavior of the object.

        This test verifies that the copy method creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.TestClass)
        assert obj_copy.data == test_object.data
        assert obj_copy.previous is None
        assert obj_copy.next is None

    def test_deepcopy(self, test_object: LinkedNode, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set up a mutable data object
        test_object.data = ["mutable", "data"]

        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.data == test_object.data
        assert id(obj_deepcopy.data) != id(test_object.data)  # Different list objects
        assert obj_deepcopy.previous is None
        assert obj_deepcopy.next is None

    def test_deepcopy_method(self, test_object: LinkedNode, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that the deepcopy method creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set up a mutable data object
        test_object.data = ["mutable", "data"]

        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy.data == test_object.data
        assert id(obj_deepcopy.data) != id(test_object.data)  # Different list objects
        assert obj_deepcopy.previous is None
        assert obj_deepcopy.next is None

    def test_pickling(self, test_object: LinkedNode) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)
        assert unpickled.data == test_object.data
        assert unpickled.previous is None
        assert unpickled.next is None

    def test_previous_property(self, linked_nodes: tuple[LinkedNode, LinkedNode, LinkedNode]) -> None:
        """Test the previous property.

        This test verifies that the previous property correctly returns the previous node.

        Args:
            linked_nodes: A fixture providing a tuple of linked nodes.
        """
        node1, node2, node3 = linked_nodes

        # Test previous references
        assert node1.previous is node3
        assert node2.previous is node1
        assert node3.previous is node2

    def test_next_property(self, linked_nodes: tuple[LinkedNode, LinkedNode, LinkedNode]) -> None:
        """Test the next property.

        This test verifies that the next property correctly returns the next node.

        Args:
            linked_nodes: A fixture providing a tuple of linked nodes.
        """
        node1, node2, node3 = linked_nodes

        # Test next references
        assert node1.next is node2
        assert node2.next is node3
        assert node3.next is node1

    def test_previous_setter(self) -> None:
        """Test the previous setter property."""
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass(data="node2")

        # Set previous
        node1.previous = node2

        # Verify
        assert node1.previous is node2

        # Set to None
        node1.previous = None

        # Verify
        assert node1.previous is None

    def test_next_setter(self) -> None:
        """Test the next setter property."""
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass(data="node2")

        # Set next
        node1.next = node2

        # Verify
        assert node1.next is node2

        # Set to None
        node1.next = None

        # Verify
        assert node1.next is None

    def test_construct_method(self) -> None:
        """Test the construct method."""
        # Create nodes
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass()
        node3 = self.TestClass()

        # Construct node2 with data and links
        node2.construct(data="node2", previous=node1, next_=node3)

        # Verify
        assert node2.data == "node2"
        assert node2.previous is node1
        assert node2.next is node3

    def test_circular_reference(self) -> None:
        """Test circular references between nodes."""
        # Create nodes
        node1 = self.TestClass(data="node1")
        node2 = self.TestClass(data="node2")

        # Create circular reference
        node1.next = node2
        node2.previous = node1
        node2.next = node1
        node1.previous = node2

        # Verify circular reference
        assert node1.next is node2
        assert node2.next is node1
        assert node1.previous is node2
        assert node2.previous is node1

        # Verify we can traverse the circle
        current = node1
        for _ in range(4):  # Traverse the circle twice
            current = current.next
        assert current is node1


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
