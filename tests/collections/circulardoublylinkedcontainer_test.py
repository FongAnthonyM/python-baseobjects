"""circulardoublylinkedcontainer_test.py
Tests for the CircularDoublyLinkedContainer class in the baseobjects package.

This module provides tests for the CircularDoublyLinkedContainer class, which is a container that uses nodes which are
doubly linked to one another to store data. It tests the functionality of CircularDoublyLinkedContainer including its
properties, methods for adding, removing, and manipulating nodes, and iteration capabilities.
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

# Source Packages #
from src.baseobjects.collections.circulardoublylinkedcontainer import CircularDoublyLinkedContainer, LinkedNode
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestCircularDoublyLinkedContainer(BaseObjectTestSuite):
    """Test the CircularDoublyLinkedContainer class.

    This class tests the functionality of the CircularDoublyLinkedContainer class, which is a container that uses nodes
    which are doubly linked to one another to store data.
    """

    # Attributes #
    TestClass: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_container(self) -> CircularDoublyLinkedContainer:
        """Create an empty CircularDoublyLinkedContainer for testing.

        Returns:
            CircularDoublyLinkedContainer: An empty CircularDoublyLinkedContainer.
        """
        return self.TestClass()

    @pytest.fixture
    def simple_container(self) -> CircularDoublyLinkedContainer:
        """Create a CircularDoublyLinkedContainer with a few items for testing.

        Returns:
            CircularDoublyLinkedContainer: A CircularDoublyLinkedContainer with a few items.
        """
        container = self.TestClass()
        container.append("A")
        container.append("B")
        container.append("C")
        return container

    @pytest.fixture
    def test_object(self) -> CircularDoublyLinkedContainer:
        """Create a test object for testing.

        Returns:
            CircularDoublyLinkedContainer: A CircularDoublyLinkedContainer with a few items.
        """
        container = self.TestClass()
        container.append("A")
        container.append("B")
        container.append("C")
        container.append("D")
        return container

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of CircularDoublyLinkedContainer can be created."""
        # Create an empty instance
        container = self.TestClass()
        assert container is not None
        assert isinstance(container, self.TestClass)
        assert container.first_node is None
        assert len(container.nodes) == 0
        assert container.is_empty is True

    def test_copy(self, test_object: CircularDoublyLinkedContainer) -> None:
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

        # Check that the nodes are the same (shallow copy)
        assert obj_copy.first_node is test_object.first_node
        assert len(obj_copy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        for node1, node2 in zip(obj_copy, test_object, strict=False):
            assert node1 is node2
            assert node1.data == node2.data

    def test_copy_method(self, test_object: CircularDoublyLinkedContainer) -> None:
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

        # Check that the nodes are the same (shallow copy)
        assert obj_copy.first_node is test_object.first_node
        assert len(obj_copy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        for node1, node2 in zip(obj_copy, test_object, strict=False):
            assert node1 is node2
            assert node1.data == node2.data

    def test_deepcopy(self, test_object: CircularDoublyLinkedContainer, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

        # Check that the nodes are different (deep copy)
        assert obj_deepcopy.first_node is not test_object.first_node
        assert len(obj_deepcopy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        # but the nodes should be different objects
        for node1, node2 in zip(obj_deepcopy, test_object, strict=False):
            assert node1 is not node2
            assert node1.data == node2.data

    def test_deepcopy_method(self, test_object: CircularDoublyLinkedContainer, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that the deepcopy method creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)

        # Check that the nodes are different (deep copy)
        assert obj_deepcopy.first_node is not test_object.first_node
        assert len(obj_deepcopy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        # but the nodes should be different objects
        for node1, node2 in zip(obj_deepcopy, test_object, strict=False):
            assert node1 is not node2
            assert node1.data == node2.data

    def test_pickling(self, test_object: CircularDoublyLinkedContainer) -> None:
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

        # Check that the nodes are different objects
        assert unpickled.first_node is not test_object.first_node
        assert len(unpickled.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        # but the nodes should be different objects
        data1 = [node.data for node in unpickled]
        data2 = [node.data for node in test_object]
        assert data1 == data2

    def test_is_empty_property(
        self,
        empty_container: CircularDoublyLinkedContainer,
        simple_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Test the is_empty property.

        This test verifies that the is_empty property correctly indicates whether the container is empty.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Test empty container
        assert empty_container.is_empty is True

        # Test non-empty container
        assert simple_container.is_empty is False

        # Test after clearing
        simple_container.clear()
        assert simple_container.is_empty is True

    def test_last_node_property(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the last_node property.

        This test verifies that the last_node property correctly returns the last node in the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get the last node
        last_node = simple_container.last_node

        # Verify it's the last node
        assert last_node.data == "C"
        assert last_node.next is simple_container.first_node
        assert simple_container.first_node.previous is last_node

    def test_len(
        self,
        empty_container: CircularDoublyLinkedContainer,
        simple_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Test the __len__ method.

        This test verifies that the length of the container is correctly reported.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Test empty container
        assert len(empty_container) == 0

        # Test non-empty container
        assert len(simple_container) == 3

        # Test after adding an item
        simple_container.append("D")
        assert len(simple_container) == 4

        # Test after removing an item
        simple_container.pop()
        assert len(simple_container) == 3

    def test_getitem(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the __getitem__ method.

        This test verifies that items can be retrieved by index.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get items by index
        assert simple_container[0].data == "A"
        assert simple_container[1].data == "B"
        assert simple_container[2].data == "C"

        # Test negative indices
        assert simple_container[-1].data == "C"
        assert simple_container[-2].data == "B"
        assert simple_container[-3].data == "A"

    def test_iter(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the __iter__ method.

        This test verifies that the container can be iterated over.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Iterate and collect data
        data = [node.data for node in simple_container]

        # Verify data
        assert data == ["A", "B", "C"]

    def test_lshift(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the __lshift__ method.

        This test verifies that the container can be shifted left.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Shift left by 1
        simple_container << 1

        # Verify first node has changed
        assert simple_container.first_node.data == "B"

        # Verify data order
        data = [node.data for node in simple_container]
        assert data == ["B", "C", "A"]

    def test_rshift(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the __rshift__ method.

        This test verifies that the container can be shifted right.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Shift right by 1
        simple_container >> 1

        # Verify first node has changed
        assert simple_container.first_node.data == "C"

        # Verify data order
        data = [node.data for node in simple_container]
        assert data == ["C", "A", "B"]

    def test_append_data(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Test the append method with data.

        This test verifies that data can be appended to the container.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
        """
        # Append data
        node1 = empty_container.append("A")

        # Verify node was added
        assert node1.data == "A"
        assert empty_container.first_node is node1
        assert len(empty_container) == 1

        # Append more data
        node2 = empty_container.append("B")

        # Verify node was added
        assert node2.data == "B"
        assert empty_container.first_node is node1
        assert len(empty_container) == 2

        # Verify circular links
        assert node1.next is node2
        assert node2.next is node1
        assert node1.previous is node2
        assert node2.previous is node1

    def test_append_node(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Test the append method with a node.

        This test verifies that a node can be appended to the container.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
        """
        # Create nodes
        node1 = LinkedNode(data="A")
        node2 = LinkedNode(data="B")

        # Append nodes
        empty_container.append(node1)
        empty_container.append(node2)

        # Verify nodes were added
        assert empty_container.first_node is node1
        assert len(empty_container) == 2

        # Verify circular links
        assert node1.next is node2
        assert node2.next is node1
        assert node1.previous is node2
        assert node2.previous is node1

    def test_insert_data(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the insert method with data.

        This test verifies that data can be inserted into the container at a specific position.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Insert at beginning
        node = simple_container.insert("X", 0)

        # Verify node was inserted
        assert node.data == "X"
        assert simple_container.first_node is node
        assert len(simple_container) == 4

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["X", "A", "B", "C"]

        # Insert in middle
        node = simple_container.insert("Y", 2)

        # Verify node was inserted
        assert node.data == "Y"
        assert len(simple_container) == 5

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["X", "A", "Y", "B", "C"]

    def test_insert_node(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the insert method with a node.

        This test verifies that a node can be inserted into the container at a specific position.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Create node
        node = LinkedNode(data="X")

        # Insert at beginning
        simple_container.insert(node, 0)

        # Verify node was inserted
        assert simple_container.first_node is node
        assert len(simple_container) == 4

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["X", "A", "B", "C"]

    def test_remove_node(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the remove_node method.

        This test verifies that a node can be removed from the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get a node to remove
        node = simple_container[1]  # Node with data "B"

        # Remove the node
        simple_container.remove_node(node)

        # Verify node was removed
        assert len(simple_container) == 2
        assert node not in simple_container.nodes

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["A", "C"]

        # Verify links were updated
        assert simple_container.first_node.next.data == "C"
        assert simple_container.first_node.previous.data == "C"

    def test_pop(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the pop method.

        This test verifies that a node can be popped from the container at a specific position.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Pop from middle
        node = simple_container.pop(1)

        # Verify node was popped
        assert node.data == "B"
        assert len(simple_container) == 2

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["A", "C"]

        # Pop from end (default)
        node = simple_container.pop()

        # Verify node was popped
        assert node.data == "C"
        assert len(simple_container) == 1

        # Verify data
        assert simple_container.first_node.data == "A"

    def test_clear(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the clear method.

        This test verifies that the container can be cleared.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Clear container
        simple_container.clear()

        # Verify container is empty
        assert simple_container.is_empty is True
        assert simple_container.first_node is None
        assert len(simple_container) == 0
        assert len(simple_container.nodes) == 0

    def test_move_node_start(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node_start method.

        This test verifies that a node can be moved to the start of the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get a node to move
        node = simple_container[2]  # Node with data "C"

        # Move node to start
        simple_container.move_node_start(node)

        # Verify node is now first
        assert simple_container.first_node is node

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["C", "A", "B"]

    def test_move_node_end(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node_end method.

        This test verifies that a node can be moved to the end of the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get a node to move
        node = simple_container[0]  # Node with data "A"

        # Move node to end
        simple_container.move_node_end(node)

        # Verify node is now last
        assert simple_container.last_node is node

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["B", "C", "A"]

    def test_move_node(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the move_node method.

        This test verifies that a node can be moved to a specific position in the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get a node to move
        node = simple_container[0]  # Node with data "A"

        # Move node to index 1
        simple_container.move_node(node, 1)

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["B", "A", "C"]

    def test_shift_left(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the shift_left method.

        This test verifies that the container can be shifted left.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Shift left by 1
        simple_container.shift_left(1)

        # Verify first node has changed
        assert simple_container.first_node.data == "B"

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["B", "C", "A"]

        # Shift left by 2
        simple_container.shift_left(2)

        # Verify first node has changed
        assert simple_container.first_node.data == "A"

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["A", "B", "C"]

    def test_shift_right(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the shift_right method.

        This test verifies that the container can be shifted right.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Shift right by 1
        simple_container.shift_right(1)

        # Verify first node has changed
        assert simple_container.first_node.data == "C"

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["C", "A", "B"]

        # Shift right by 2
        simple_container.shift_right(2)

        # Verify first node has changed
        assert simple_container.first_node.data == "A"

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == ["A", "B", "C"]

    def test_forward_iter(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the forward_iter method.

        This test verifies that the container can be iterated over in forward order.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Iterate and collect data
        data = [node.data for node in simple_container.forward_iter()]

        # Verify data
        assert data == ["A", "B", "C"]

    def test_reverse_iter(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the reverse_iter method.

        This test verifies that the container can be iterated over in reverse order.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Iterate and collect data
        data = [node.data for node in simple_container.reverse_iter()]

        # Verify data
        assert data == ["C", "B", "A"]

    def test_forward_cycle(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the forward_cycle method.

        This test verifies that the container can be cycled over in forward order.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Create cycle
        cycle = simple_container.forward_cycle()

        # Get first 6 items (2 complete cycles)
        data = []
        for _ in range(6):
            node = next(cycle)
            data.append(node.data)

        # Verify data
        assert data == ["A", "B", "C", "A", "B", "C"]

    def test_reverse_cycle(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Test the reverse_cycle method.

        This test verifies that the container can be cycled over in reverse order.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Create cycle
        cycle = simple_container.reverse_cycle()

        # Get first 6 items (2 complete cycles)
        data = []
        for _ in range(6):
            node = next(cycle)
            data.append(node.data)

        # Verify data
        assert data == ["C", "B", "A", "C", "B", "A"]

    def test_empty_container_operations(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Test operations on an empty container.

        This test verifies that operations on an empty container behave correctly.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
        """
        # Test iteration on empty container
        assert list(empty_container) == []

        # Test forward_iter on empty container
        assert list(empty_container.forward_iter()) == []

        # Test reverse_iter on empty container
        assert list(empty_container.reverse_iter()) == []

        # Test clear on empty container
        empty_container.clear()
        assert empty_container.is_empty is True

        # Test pop on empty container (should raise IndexError)
        with pytest.raises(AttributeError):
            empty_container.pop()


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
