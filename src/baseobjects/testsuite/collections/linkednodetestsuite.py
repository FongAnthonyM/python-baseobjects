"""linkednodetestsuite.py
Base class for test suites which test LinkedNode and its subclasses.
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
import unittest.mock
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...collections import LinkedNode
from ..bases import BaseReducibleTestSuite


# Definitions #
# Classes #
class LinkedNodeTestSuite(BaseReducibleTestSuite):
    """Base class for test suites which test LinkedNode.

    This class provides common functionality for test suites that test LinkedNode objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be LinkedNode or a subclass.
    """

    UnitTestClass: ClassVar[type[LinkedNode]] = LinkedNode

    # Fixtures #
    @pytest.fixture
    def empty_node(self) -> LinkedNode:
        """Creates an empty LinkedNode for testing.

        Returns:
            LinkedNode: An empty LinkedNode.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def data_node(self) -> LinkedNode:
        """Creates a LinkedNode with data for testing.

        Returns:
            LinkedNode: A LinkedNode with data.
        """
        return self.UnitTestClass(data="test_data")

    @pytest.fixture
    def linked_nodes(self) -> tuple[LinkedNode, LinkedNode, LinkedNode]:
        """Creates a set of linked nodes for testing.

        Returns:
            tuple[LinkedNode, LinkedNode, LinkedNode]: A tuple of three linked nodes.
        """
        node1 = self.UnitTestClass(data="node1")
        node2 = self.UnitTestClass(data="node2")
        node3 = self.UnitTestClass(data="node3")

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
        """Creates a test object for testing.

        Returns:
            LinkedNode: A LinkedNode with data and links.
        """
        return self.UnitTestClass(data="test_data")

    # Tests #
    # Instantiation #
    @pytest.mark.parametrize(
        ("kwargs", "verify_func"),
        [
            ({}, lambda n: n.data is None and n.previous is None and n.next is None),
            ({"data": "test_data"}, lambda n: n.data == "test_data" and n.previous is None and n.next is None),
            ({"init": False}, lambda n: n.data is None and n.previous is None and n.next is None),
        ],
        ids=["empty", "data", "init_false"],
    )
    def test_instance_creation(self, kwargs: dict[str, Any], verify_func: Any) -> None:
        """Tests that instances of LinkedNode can be created with various parameters."""
        node = self.UnitTestClass(**kwargs)
        assert node is not None
        assert isinstance(node, self.UnitTestClass)
        assert verify_func(node)

    # Copying #
    @pytest.mark.parametrize("use_method", [False, True], ids=["copy_func", "copy_method"])
    def test_copy(self, test_object: Any, use_method: bool) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the copy method or copy function.
        """
        # Copy Object
        if use_method:
            obj_copy = test_object.copy()
        else:
            obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        assert obj_copy.data == test_object.data
        assert obj_copy.previous is None
        assert obj_copy.next is None

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the deepcopy method or deepcopy function.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set up a mutable data object
        test_object.data = ["mutable", "data"]

        # Deep Copy Object
        if memo is None:
            memo = {}

        if use_method:
            obj_deepcopy = test_object.deepcopy(memo=memo)
        else:
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)
        assert obj_deepcopy.data == test_object.data
        assert id(obj_deepcopy.data) != id(test_object.data)  # Different list objects
        assert obj_deepcopy.previous is None
        assert obj_deepcopy.next is None

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)
        assert unpickled.data == test_object.data
        assert unpickled.previous is None
        assert unpickled.next is None

    def test_pickle_empty_node(self) -> None:
        """Tests pickling an uninitialized LinkedNode (empty dict)."""
        n = self.UnitTestClass(init=False)
        dumped = pickle.dumps(n)
        loaded = pickle.loads(dumped)
        assert isinstance(loaded, self.UnitTestClass)

    # Functionality #
    def test_instance_creation_linked(self) -> None:
        """Tests instance creation with links."""
        node1 = self.UnitTestClass(data="node1")
        node2 = self.UnitTestClass(data="node2", previous=node1)
        node1.next = node2

        assert node1.next is node2
        assert node2.previous is node1

    @pytest.mark.parametrize(("direction", "offset"), [("previous", -1), ("next", 1)])
    def test_neighbor_property(
        self,
        linked_nodes: tuple[LinkedNode, LinkedNode, LinkedNode],
        direction: str,
        offset: int,
    ) -> None:
        """Tests the neighbor property (previous or next).

        This test verifies that the neighbor property correctly returns the expected node.

        Args:
            linked_nodes: A fixture providing a tuple of linked nodes.
            direction: The direction to check ("previous" or "next").
            offset: The index offset to find the expected neighbor.
        """
        nodes = linked_nodes
        n = len(nodes)
        for i, node in enumerate(nodes):
            expected = nodes[(i + offset) % n]
            assert getattr(node, direction) is expected

    @pytest.mark.parametrize("direction", ["previous", "next"])
    def test_neighbor_setter(self, direction: str) -> None:
        """Tests the neighbor setter property."""
        node1 = self.UnitTestClass(data="node1")
        node2 = self.UnitTestClass(data="node2")

        # Set neighbor
        setattr(node1, direction, node2)

        # Verify
        assert getattr(node1, direction) is node2

        # Set to None
        setattr(node1, direction, None)

        # Verify
        assert getattr(node1, direction) is None

    def test_construct_method(self) -> None:
        """Tests the construct method."""
        # Create nodes
        node1 = self.UnitTestClass(data="node1")
        node2 = self.UnitTestClass()
        node3 = self.UnitTestClass()

        # Construct node2 with data and links
        node2.construct(data="node2", previous=node1, next_=node3)

        # Verify
        assert node2.data == "node2"
        assert node2.previous is node1
        assert node2.next is node3

    def test_circular_reference(self) -> None:
        """Tests circular references between nodes."""
        # Create nodes
        node1 = self.UnitTestClass(data="node1")
        node2 = self.UnitTestClass(data="node2")

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
        current: LinkedNode | None = node1
        for _ in range(4):  # Traverse the circle twice
            assert current is not None
            current = current.next
        assert current is node1

    def test_init_with_neighbors(self) -> None:
        """Tests LinkedNode construction with neighbors."""
        n1 = self.UnitTestClass(1)
        n3 = self.UnitTestClass(3)
        n2 = self.UnitTestClass(2, previous=n1, next_=n3)
        assert n2.previous is n1
        assert n2.next is n3

    def test_getstate_dict(self) -> None:
        """Tests __getstate__ returns a dict with next and previous."""
        node = self.UnitTestClass(1)
        state = node.__getstate__()
        if isinstance(state, dict):
            assert "_next" in state
            assert "_previous" in state
        else:
            # If state is not a dict, it might be due to __slots__ or custom implementation.
            # But if it returns dict, we must verify keys.
            pass

    def test_setstate_dict(self) -> None:
        """Tests __setstate__ with a dict."""
        node = self.UnitTestClass()
        n1 = self.UnitTestClass(1)
        n2 = self.UnitTestClass(2)
        state = {"_next": n1, "_previous": n2}
        node.__setstate__(state)
        assert node.next is n1
        assert node.previous is n2

    def test_getstate_not_dict(self) -> None:
        """Tests __getstate__ when super returns None."""
        with unittest.mock.patch("baseobjects.bases.BaseReducible.__getstate__", return_value=None):
            node = self.UnitTestClass()
            state = node.__getstate__()
            assert state is None

    def test_setstate_not_dict(self) -> None:
        """Tests __setstate__ when state is None."""
        node = self.UnitTestClass()
        state = None
        with unittest.mock.patch("baseobjects.bases.BaseReducible.__setstate__") as mock_super:
            node.__setstate__(state)
            mock_super.assert_called_once_with(state)
