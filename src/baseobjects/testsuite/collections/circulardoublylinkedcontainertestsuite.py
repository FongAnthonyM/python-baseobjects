"""circulardoublylinkedcontainertestsuite.py
Base class for test suites which test CircularDoublyLinkedContainer and its subclasses.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...collections import CircularDoublyLinkedContainer, LinkedNode
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class CircularDoublyLinkedContainerTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test CircularDoublyLinkedContainer.

    This class provides common functionality for test suites that test CircularDoublyLinkedContainer objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be CircularDoublyLinkedContainer or a
            subclass.
    """

    UnitTestClass: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer

    # Fixtures #
    @pytest.fixture
    def empty_container(self) -> CircularDoublyLinkedContainer:
        """Creates an empty CircularDoublyLinkedContainer for testing.

        Returns:
            CircularDoublyLinkedContainer: An empty CircularDoublyLinkedContainer.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def simple_container(self) -> CircularDoublyLinkedContainer:
        """Creates a CircularDoublyLinkedContainer with a few items for testing.

        Returns:
            CircularDoublyLinkedContainer: A CircularDoublyLinkedContainer with a few items.
        """
        container = self.UnitTestClass()
        container.append("A")
        container.append("B")
        container.append("C")
        return container

    @pytest.fixture
    def test_object(self) -> CircularDoublyLinkedContainer:
        """Creates a test object for testing.

        Returns:
            CircularDoublyLinkedContainer: A CircularDoublyLinkedContainer with a few items.
        """
        container = self.UnitTestClass()
        container.append("A")
        container.append("B")
        container.append("C")
        container.append("D")
        return container

    # Tests #
    # Magic Methods #
    def test_len(
        self,
        empty_container: CircularDoublyLinkedContainer,
        simple_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Tests the __len__ method.

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
        """Tests the __getitem__ method.

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
        """Tests the __iter__ method.

        This test verifies that the container can be iterated over.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Iterate and collect data
        data = [node.data for node in simple_container]

        # Verify data
        assert data == ["A", "B", "C"]

    @pytest.mark.parametrize(
        ("direction", "expected_data"),
        [
            ("forward", ["A", "B", "C"]),
            ("reverse", ["C", "B", "A"]),
        ],
    )
    def test_iter_variants(
        self,
        simple_container: CircularDoublyLinkedContainer,
        direction: str,
        expected_data: list[Any],
    ) -> None:
        """Tests forward_iter and reverse_iter.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items (A, B, C).
            direction: "forward" or "reverse".
            expected_data: Expected data order.
        """
        if direction == "forward":
            iterator = simple_container.forward_iter()
        else:
            iterator = simple_container.reverse_iter()

        data = [node.data for node in iterator]
        assert data == expected_data

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of CircularDoublyLinkedContainer can be created."""
        # Create an empty instance
        container = self.UnitTestClass()
        assert container is not None
        assert isinstance(container, self.UnitTestClass)
        assert container.first_node is None
        assert len(container.nodes) == 0
        assert container.is_empty is True

    # Copying #
    @pytest.mark.parametrize("use_method", [False, True], ids=["copy_func", "copy_method"])
    def test_copy(self, test_object: Any, use_method: bool) -> None:
        """Tests the copy behavior of the object.

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

        # Check that the nodes are the same (shallow copy)
        assert obj_copy.first_node is test_object.first_node
        assert len(obj_copy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        for node1, node2 in zip(obj_copy, test_object, strict=False):
            assert node1 is node2
            assert node1.data == node2.data

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the deepcopy method or deepcopy function.
            memo: A memo dictionary to pass to deepcopy.
        """
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

        # Check that the nodes are different (deep copy)
        assert obj_deepcopy.first_node is not test_object.first_node
        assert len(obj_deepcopy.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        # but the nodes should be different objects
        for node1, node2 in zip(obj_deepcopy, test_object, strict=False):
            assert node1 is not node2
            assert node1.data == node2.data

    def test_deepcopy_populated(self) -> None:
        """Tests deepcopy with populated container."""
        container = self.UnitTestClass()
        container.append(1)
        container.append(2)

        cp = copy.deepcopy(container)
        assert len(cp) == 2
        assert cp[0].data == 1
        assert cp[1].data == 2
        assert cp is not container
        assert cp[0] is not container[0]  # Nodes are copied

    def test_deepcopy_broken_state(self) -> None:
        """Tests deepcopy with broken state (nodes exist but first_node None)."""
        c = self.UnitTestClass()
        c.nodes.add(LinkedNode(1))
        # c.is_empty is False, but first_node is None
        cp = copy.deepcopy(c)
        assert len(cp) == 0  # Should skip copying nodes loop

    def test_deepcopy_nil_arg(self) -> None:
        """Tests deepcopy with explicit _nil argument."""
        c = self.UnitTestClass()
        c.append(1)
        cp = c.__deepcopy__(_nil=["marker"])
        assert len(cp) == 1

    def test_deepcopy_nil_recursion(self) -> None:
        """Tests deepcopy recursion handling."""
        c = self.UnitTestClass()
        nil = [c]
        new_c = c.__deepcopy__(_nil=nil)
        assert new_c is c

    def test_deepcopy_broken_chain(self) -> None:
        """Tests deepcopy with broken chain."""
        c = self.UnitTestClass()
        c.append(1)
        c.append(2)
        # Break the chain
        c.first_node.next = None  # type: ignore[union-attr]
        new_c = copy.deepcopy(c)
        assert len(new_c) == 1
        assert new_c.first_node.data == 1  # type: ignore[union-attr]

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

        # Check that the nodes are different objects
        assert unpickled.first_node is not test_object.first_node
        assert len(unpickled.nodes) == len(test_object.nodes)

        # Verify we can iterate through both containers and get the same data
        # but the nodes should be different objects
        data1 = [node.data for node in unpickled]
        data2 = [node.data for node in test_object]
        assert data1 == data2

    # Functionality #
    def test_is_empty_property(
        self,
        empty_container: CircularDoublyLinkedContainer,
        simple_container: CircularDoublyLinkedContainer,
    ) -> None:
        """Tests the is_empty property.

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
        """Tests the last_node property.

        This test verifies that the last_node property correctly returns the last node in the container.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
        """
        # Get the last node
        last_node = simple_container.last_node

        # Verify it's the last node
        assert last_node is not None
        assert last_node.data == "C"
        assert last_node.next is simple_container.first_node
        assert simple_container.first_node is not None
        assert simple_container.first_node.previous is last_node

    @pytest.mark.parametrize(
        ("items", "is_node"),
        [
            (["A", "B"], False),
            (["A", "B"], True),
        ],
        ids=["data", "node"],
    )
    def test_append(self, empty_container: CircularDoublyLinkedContainer, items: list[Any], is_node: bool) -> None:
        """Tests the append method with data and nodes.

        This test verifies that data/nodes can be appended to the container.

        Args:
            empty_container: An empty CircularDoublyLinkedContainer.
            items: Items to append.
            is_node: Whether items are nodes or data.
        """
        nodes = []
        for item in items:
            if is_node:
                node = LinkedNode(data=item)
                nodes.append(node)
                empty_container.append(node)
            else:
                node = empty_container.append(item)
                nodes.append(node)

        # Verify first node
        assert empty_container.first_node is nodes[0]
        assert len(empty_container) == len(items)

        # Verify data
        for i, node in enumerate(nodes):
            assert node.data == items[i]

        # Verify circular links (assuming 2 items for this specific check logic from original tests)
        if len(items) >= 2:
            node1 = nodes[0]
            node2 = nodes[1]
            assert node1.next is node2
            assert node2.next is node1
            assert node1.previous is node2
            assert node2.previous is node1

    @pytest.mark.parametrize(
        ("item", "index", "is_node", "expected_data"),
        [
            ("X", 0, False, ["X", "A", "B", "C"]),
            ("X", 0, True, ["X", "A", "B", "C"]),
            ("Y", 2, False, ["A", "B", "Y", "C"]),
        ],
        ids=["data_at_start", "node_at_start", "data_in_middle"],
    )
    def test_insert(
        self,
        simple_container: CircularDoublyLinkedContainer,
        item: Any,
        index: int,
        is_node: bool,
        expected_data: list[Any],
    ) -> None:
        """Tests the insert method with data and nodes.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
            item: Item to insert.
            index: Index to insert at.
            is_node: Whether item is a node or data.
            expected_data: Expected data in container after insertion.
        """
        if is_node:
            node = LinkedNode(data=item)
            simple_container.insert(node, index)
            assert simple_container[index] is node
        else:
            node = simple_container.insert(item, index)
            assert node.data == item

        assert len(simple_container) == len(expected_data)
        assert [n.data for n in simple_container] == expected_data

        if index == 0:
            assert simple_container.first_node is node

    def test_remove_node(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Tests the remove_node method.

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
        assert simple_container.first_node is not None
        assert simple_container.first_node.next is not None
        assert simple_container.first_node.next.data == "C"
        assert simple_container.first_node.previous is not None
        assert simple_container.first_node.previous.data == "C"

    @pytest.mark.parametrize(
        ("index", "expected_popped", "remaining_data"),
        [
            (1, "B", ["A", "C"]),
            (None, "C", ["A", "B"]),
            (0, "A", ["B", "C"]),
        ],
        ids=["middle", "end_default", "start"],
    )
    def test_pop(
        self,
        simple_container: CircularDoublyLinkedContainer,
        index: int | None,
        expected_popped: Any,
        remaining_data: list[Any],
    ) -> None:
        """Tests the pop method.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
            index: Index to pop.
            expected_popped: Expected data of popped node.
            remaining_data: Expected data in container after pop.
        """
        if index is None:
            node = simple_container.pop()
        else:
            node = simple_container.pop(index)

        assert node.data == expected_popped
        assert len(simple_container) == len(remaining_data)
        assert [n.data for n in simple_container] == remaining_data

    def test_clear(self, simple_container: CircularDoublyLinkedContainer) -> None:
        """Tests the clear method.

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

    @pytest.mark.parametrize(
        ("method", "index", "target", "expected_data"),
        [
            ("move_node_start", 2, None, ["C", "A", "B"]),
            ("move_node_end", 0, None, ["B", "C", "A"]),
            ("move_node", 0, 1, ["B", "A", "C"]),
            ("move_node_start", 0, None, ["A", "B", "C"]),
            ("move_node_end", 2, None, ["A", "B", "C"]),
            ("move_node_start", 1, None, ["B", "A", "C"]),
            ("move_node", 0, 0, ["A", "B", "C"]),
            ("move_node_end", 1, None, ["A", "C", "B"]),
        ],
        ids=["to_start", "to_end", "to_index", "start_same", "end_same", "start_middle", "index_same", "end_middle"],
    )
    def test_move_node_variants(
        self,
        simple_container: CircularDoublyLinkedContainer,
        method: str,
        index: int,
        target: Any,
        expected_data: list[Any],
    ) -> None:
        """Tests move_node methods.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items (A, B, C).
            method: Method name to call.
            index: Index of node to move.
            target: Target index for move_node, or None.
            expected_data: Expected data order.
        """
        node = simple_container[index]
        if method == "move_node_start":
            simple_container.move_node_start(node)
            if index != 0 and index != len(simple_container):
                assert simple_container.first_node is node
        elif method == "move_node_end":
            simple_container.move_node_end(node)
            if index != len(simple_container) - 1:
                assert simple_container.last_node is node
        else:
            simple_container.move_node(node, target)

        assert [n.data for n in simple_container] == expected_data

    @pytest.mark.parametrize(
        ("direction", "count", "use_operator", "expected_data"),
        [
            ("left", 1, False, ["B", "C", "A"]),
            ("left", 1, True, ["B", "C", "A"]),
            ("left", 2, False, ["C", "A", "B"]),
            ("right", 1, False, ["C", "A", "B"]),
            ("right", 1, True, ["C", "A", "B"]),
            ("right", 2, False, ["B", "C", "A"]),
            ("left", 0, False, ["A", "B", "C"]),
            ("right", 0, False, ["A", "B", "C"]),
        ],
        ids=["left_1", "left_1_op", "left_2", "right_1", "right_1_op", "right_2", "left_0", "right_0"],
    )
    def test_shift(
        self,
        simple_container: CircularDoublyLinkedContainer,
        direction: str,
        count: int,
        use_operator: bool,
        expected_data: list[Any],
    ) -> None:
        """Tests the shift methods and operators.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items.
            direction: Direction to shift ("left" or "right").
            count: Number of shifts.
            use_operator: Whether to use the shift operator (<< or >>).
            expected_data: Expected order of data after shift.
        """
        if direction == "left":
            if use_operator:
                simple_container << count
            else:
                simple_container.shift_left(count)
        else:
            if use_operator:
                simple_container >> count
            else:
                simple_container.shift_right(count)

        # Verify first node has changed
        assert simple_container.first_node is not None
        assert simple_container.first_node.data == expected_data[0]

        # Verify data order
        data = [n.data for n in simple_container]
        assert data == expected_data

    @pytest.mark.parametrize(
        ("direction", "expected_sequence"),
        [
            ("forward", ["A", "B", "C", "A", "B", "C"]),
            ("reverse", ["C", "B", "A", "C", "B", "A"]),
        ],
    )
    def test_cycle_variants(
        self,
        simple_container: CircularDoublyLinkedContainer,
        direction: str,
        expected_sequence: list[Any],
    ) -> None:
        """Tests forward_cycle and reverse_cycle.

        Args:
            simple_container: A CircularDoublyLinkedContainer with a few items (A, B, C).
            direction: "forward" or "reverse".
            expected_sequence: Expected data sequence (2 cycles).
        """
        if direction == "forward":
            cycle = simple_container.forward_cycle()
        else:
            cycle = simple_container.reverse_cycle()

        data = []
        for _ in range(len(expected_sequence)):
            node = next(cycle)
            data.append(node.data)

        assert data == expected_sequence

    def test_empty_container_operations(self, empty_container: CircularDoublyLinkedContainer) -> None:
        """Tests operations on an empty container.

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
        with pytest.raises(IndexError):
            empty_container.pop()

    def test_shift_more_than_one(self) -> None:
        """Tests shifting by more than 1."""
        container = self.UnitTestClass()
        container.append(1)
        container.append(2)
        container.append(3)

        container.shift_left(2)
        # 1,2,3 -> shift left 1 -> 2,3,1 -> shift left 2 -> 3,1,2
        assert container[0].data == 3

        container.shift_right(2)
        # 3,1,2 -> shift right 1 -> 2,3,1 -> shift right 2 -> 1,2,3
        assert container[0].data == 1

    def test_remove_last_node_leaving_empty(self) -> None:
        """Tests removing the only node."""
        container = self.UnitTestClass()
        container.append(1)
        node = container[0]

        container.remove_node(node)
        assert len(container) == 0
        assert container.first_node is None

    def test_move_node_general(self) -> None:
        """Tests move_node general cases."""
        container = self.UnitTestClass()
        container.append(1)
        container.append(2)
        container.append(3)
        node1 = container[0]

        # Move node1 to index 1 (between 2 and 3) -> 2, 1, 3
        container.move_node(node1, 1)
        assert container[0].data == 2
        assert container[1].data == 1
        assert container[2].data == 3

        # Move node1 back to 0
        # Current implementation inserts before first_node but doesn't update first_node pointer
        # So effectively it moves to the end of the sequence relative to iteration start
        container.move_node(node1, 0)

        # 2 is still first_node. 1 is inserted before 2.
        # 3 is after 2.
        # So: 2 -> 3 -> 1 -> (2)
        assert container[0].data == 2
        assert container[2].data == 1

    @pytest.mark.parametrize("is_node", [False, True])
    def test_insert_into_empty(self, is_node: bool) -> None:
        """Tests insert into empty container."""
        c = self.UnitTestClass()
        if is_node:
            item = LinkedNode(1)
            c.insert(item, 0)
            assert c[0] is item
        else:
            c.insert(1, 0)
            assert c[0].data == 1
        assert len(c) == 1

    @pytest.mark.parametrize("is_node", [False, True])
    def test_append_broken_last_node_is_none(self, is_node: bool) -> None:
        """Tests append when last_node is broken (None)."""
        c = self.UnitTestClass()
        c.append(1)
        c.first_node.previous = None  # type: ignore[union-attr]

        if is_node:
            node = LinkedNode(2)
            with pytest.raises(ValueError, match="Last node should not be None"):
                c.append(node)
        else:
            with pytest.raises(ValueError, match="Last node should not be None"):
                c.append(2)

    def test_forward_iter_broken_next_is_none(self) -> None:
        """Tests forward_iter when next link is broken."""
        c = self.UnitTestClass()
        c.append(1)
        c.append(2)
        c.first_node.next = None  # type: ignore[union-attr]
        iterator = c.forward_iter()
        assert next(iterator).data == 1
        with pytest.raises(StopIteration):
            next(iterator)

    def test_reverse_iter_broken_previous_is_none(self) -> None:
        """Tests reverse_iter when previous link is broken."""
        c = self.UnitTestClass()
        c.append(1)
        c.append(2)
        c.last_node.previous = None  # type: ignore[union-attr]
        iterator = c.reverse_iter()
        assert next(iterator).data == 2
        with pytest.raises(StopIteration):
            next(iterator)

    @pytest.mark.parametrize("direction", ["left", "right"])
    def test_shift_empty(self, direction: str) -> None:
        """Tests shift_left and shift_right on empty container."""
        c = self.UnitTestClass()
        if direction == "left":
            c.shift_left(1)
        else:
            c.shift_right(1)
        assert c.first_node is None

    @pytest.mark.parametrize("direction", ["forward", "reverse"])
    def test_cycle_empty(self, direction: str) -> None:
        """Tests forward_cycle and reverse_cycle on empty container."""
        c = self.UnitTestClass()
        if direction == "forward":
            iterator = c.forward_cycle()
        else:
            iterator = c.reverse_cycle()
        with pytest.raises(StopIteration):
            next(iterator)
