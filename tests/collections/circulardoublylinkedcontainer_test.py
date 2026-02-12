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
from typing import ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.collections.circulardoublylinkedcontainer import CircularDoublyLinkedContainer
from baseobjects.testsuite.collections import CircularDoublyLinkedContainerTestSuite


# Definitions #
# Tests #
class TestCircularDoublyLinkedContainer(CircularDoublyLinkedContainerTestSuite):
    """Tests the CircularDoublyLinkedContainer class.

    This class tests the functionality of the CircularDoublyLinkedContainer class, which is a container that uses nodes
    which are doubly linked to one another to store data.
    """

    # Attributes #
    UnitTestClass: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer

    def test_linked_node_init(self) -> None:
        """Tests LinkedNode initialization."""
        # Source Packages #
        from baseobjects.collections.circulardoublylinkedcontainer import LinkedNode

        # Test init=False
        node = LinkedNode(init=False)
        assert node.data is None
        assert node.previous is None
        assert node.next is None

        # Test explicit previous/next in construct
        node1 = LinkedNode(data=1)
        node2 = LinkedNode(data=2)
        node3 = LinkedNode(data=3, previous=node1, next_=node2)

        assert node3.data == 3
        assert node3.previous is node1
        assert node3.next is node2
        assert node3._previous is not None
        assert node3._previous() is node1
        assert node3._next is not None
        assert node3._next() is node2

    def test_linked_node_pickling_edge_cases(self) -> None:
        """Tests LinkedNode pickling edge cases."""
        # Source Packages #
        from baseobjects.collections.circulardoublylinkedcontainer import LinkedNode

        # Test missing _next/_previous in state dict
        node = LinkedNode(data=1)
        state = node.__getstate__()
        if isinstance(state, dict):
            state_missing = state.copy()
            state_missing.pop("_next", None)
            state_missing.pop("_previous", None)

            new_node = LinkedNode(init=False)
            new_node.__setstate__(state_missing)

            assert new_node.data == 1
            assert new_node.next is None
            assert new_node.previous is None

        # Test __setstate__ with None (hits line 143 else branch)
        node_none = LinkedNode(init=False)
        node_none.__setstate__(None)
        assert node_none.data is None

        # Test __getstate__ with uninitialized node (might return None, hitting line 119 else branch)
        node_empty = LinkedNode(init=False)
        node_empty.__getstate__()

    def test_insert_node_at_index(self) -> None:
        """Tests inserting a LinkedNode object at a specific index."""
        # Source Packages #
        from baseobjects.collections.circulardoublylinkedcontainer import LinkedNode

        container = self.UnitTestClass()
        container.append(1)
        container.append(3)

        new_node = LinkedNode(data=2)

        # Insert node at index 1 (not 0, to hit line 453)
        container.insert(new_node, 1)

        assert container[1] is new_node
        assert container[1].data == 2
        assert len(container) == 3
        assert new_node in container.nodes


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
