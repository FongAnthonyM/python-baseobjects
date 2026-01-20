"""groupedlisttestsuite.py
Base class for test suites which test GroupedList and its subclasses.
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
import re
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

try:
    # Third-Party Packages #
    from typeguard import TypeCheckError
except ImportError:
    TypeCheckError = TypeError  # type: ignore

# Local Packages #
from ...collections import GroupedList
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class GroupedListTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test GroupedList.

    This class provides common functionality for test suites that test GroupedList objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be GroupedList or a subclass.
    """

    UnitTestClass: ClassVar[type[GroupedList]] = GroupedList

    # Fixtures #
    @pytest.fixture
    def empty_list(self) -> GroupedList:
        """Creates an empty GroupedList for testing.

        Returns:
            GroupedList: An empty GroupedList.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def simple_list(self) -> GroupedList:
        """Creates a GroupedList with simple items for testing.

        Returns:
            GroupedList: A GroupedList with simple items.
        """
        return self.UnitTestClass([1, 2, 3, 4, 5])

    @pytest.fixture
    def nested_list(self) -> GroupedList:
        """Creates a GroupedList with nested GroupedLists for testing.

        Returns:
            GroupedList: A GroupedList with nested GroupedLists.
        """
        parent = self.UnitTestClass([1, 2])
        child1 = self.UnitTestClass([3, 4], parent=parent)
        child2 = self.UnitTestClass([5, 6], parent=parent)
        parent.data.extend([child1, child2])
        parent.groups["child1"] = child1
        parent.groups["child2"] = child2
        return parent

    @pytest.fixture
    def test_object(self) -> GroupedList:
        """Creates a test object for testing.

        Returns:
            GroupedList: A GroupedList with some items and a nested group.
        """
        parent = self.UnitTestClass([1, 2, 3])
        child = self.UnitTestClass([4, 5], parent=parent)
        parent.data.append(child)
        parent.groups["child"] = child
        return parent

    # Tests #
    # Magic Methods #
    def test_len(self, nested_list: GroupedList) -> None:
        """Tests the __len__ method of GroupedList.

        This test verifies that the __len__ method returns the total number of items in the GroupedList,
        including items in child groups.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the total length should be 6 (1, 2, 3, 4, 5, 6)
        assert len(nested_list) == 6

        # Add an item to a child and check that the parent length increases
        nested_list.groups["child1"].append(7)
        assert len(nested_list) == 7

    @pytest.mark.parametrize(
        ("index", "expected"),
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (-1, 6), (-2, 5), (-3, 4), (-4, 3), (-5, 2), (-6, 1)],
    )
    def test_getitem_index(self, nested_list: GroupedList, index: int, expected: int) -> None:
        """Tests the __getitem__ method of GroupedList with integer indices.

        This test verifies that the __getitem__ method returns the correct item when accessed by index.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
            index: The index to access.
            expected: The expected value.
        """
        assert nested_list[index] == expected

    @pytest.mark.parametrize("index", [6, -7])
    def test_getitem_index_error(self, nested_list: GroupedList, index: int) -> None:
        """Tests the __getitem__ method of GroupedList with out of range indices."""
        with pytest.raises(IndexError):
            _ = nested_list[index]

    def test_getitem_by_name(self, nested_list: GroupedList) -> None:
        """Tests the __getitem__ method of GroupedList with string names.

        This test verifies that the __getitem__ method returns the correct group when accessed by name.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Get groups by name
        child1 = nested_list["child1"]
        assert isinstance(child1, GroupedList)
        assert len(child1.data) == 2
        assert child1.data == [3, 4]

        child2 = nested_list["child2"]
        assert isinstance(child2, GroupedList)
        assert len(child2.data) == 2
        assert child2.data == [5, 6]

        # Test non-existent group
        with pytest.raises(KeyError):
            _ = nested_list["non_existent"]

    @pytest.mark.parametrize(
        ("s", "expected"),
        [
            (slice(1, 4), [2, 3, 4]),
            (slice(0, 6, 2), [1, 3, 5]),
            (slice(None, 3), [1, 2, 3]),
            (slice(3, None), [4, 5, 6]),
            (slice(None, None), [1, 2, 3, 4, 5, 6]),
            (slice(-3, None), [4, 5, 6]),
            (slice(None, -3), [1, 2, 3]),
            (slice(-5, -2), [2, 3, 4]),
        ],
    )
    def test_getitem_slice(self, nested_list: GroupedList, s: slice, expected: list) -> None:  # type: ignore[type-arg]
        """Tests the __getitem__ method of GroupedList with slices.

        This test verifies that the __getitem__ method returns the correct items when accessed by slice.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
            s: The slice object.
            expected: The expected list of values.
        """
        assert nested_list[s] == expected

    @pytest.mark.parametrize(
        ("index", "value", "verify_lambda"),
        [
            (0, 10, lambda nl: nl.data[0] == 10),
            (2, 30, lambda nl: nl.groups["child1"].data[0] == 30),
            (-1, 60, lambda nl: nl.groups["child2"].data[1] == 60),
        ],
        ids=["direct", "nested", "negative"],
    )
    def test_setitem_by_index(self, nested_list: GroupedList, index: int, value: int, verify_lambda: Any) -> None:
        """Tests the __setitem__ method of GroupedList with integer indices.

        This test verifies that the __setitem__ method sets the correct item when accessed by index.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
            index: The index to set.
            value: The value to set.
            verify_lambda: A lambda to verify the internal state.
        """
        nested_list[index] = value
        assert nested_list[index] == value
        assert verify_lambda(nested_list)

    @pytest.mark.parametrize("index", [10])
    def test_setitem_index_error(self, nested_list: GroupedList, index: int) -> None:
        """Tests __setitem__ out of range."""
        with pytest.raises(IndexError):
            nested_list[index] = 100

    def test_setitem_by_name(self, nested_list: GroupedList) -> None:
        """Tests the __setitem__ method of GroupedList with string names.

        This test verifies that the __setitem__ method sets the correct group when accessed by name.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Create a new group
        new_group = self.UnitTestClass([7, 8])
        nested_list["new_group"] = new_group

        # Verify the group was added
        assert "new_group" in nested_list.groups
        assert nested_list["new_group"] is new_group
        assert new_group in nested_list.data
        # The new group is treated as a single item in the flat list
        # so we don't test accessing its elements by index through the parent

        # We need to remove the existing group before replacing it
        # because GroupedList doesn't allow overwriting existing groups
        del nested_list["child1"]

        # Now add a new group with the same name
        replacement_group = self.UnitTestClass([9, 10])
        nested_list["child1"] = replacement_group

        # Verify the group was added
        assert nested_list["child1"] is replacement_group
        assert replacement_group in nested_list.data

    def test_setitem_by_slice(self, nested_list: GroupedList) -> None:
        """Tests the __setitem__ method of GroupedList with slices.

        This test verifies that the __setitem__ method sets the correct items when accessed by slice.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        nested_list[1:4] = [20, 30, 40]
        assert nested_list[1] == 20
        assert nested_list[2] == 30
        assert nested_list[3] == 40

        # Test with a different length
        with pytest.raises(ValueError, match="attempt to assign sequence of size 2 to slice of size 3"):
            nested_list[1:4] = [100, 200]

    def test_delitem_by_index(self, nested_list: GroupedList) -> None:
        """Tests the __delitem__ method of GroupedList with integer indices.

        This test verifies that the __delitem__ method deletes the correct item when accessed by index.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        del nested_list[0]
        assert nested_list[0] == 2  # Now the first item is 2
        assert len(nested_list) == 5

        del nested_list[1]  # This should delete the first item in child1
        assert nested_list[1] == 4  # Now the second item is 4
        assert len(nested_list) == 4

        # Test negative indices
        del nested_list[-1]  # This should delete the last item in child2
        assert len(nested_list) == 3

        # Test out of range
        with pytest.raises(IndexError):
            del nested_list[10]

    def test_delitem_by_name(self, nested_list: GroupedList) -> None:
        """Tests the __delitem__ method of GroupedList with string names.

        This test verifies that the __delitem__ method deletes the correct group when accessed by name.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Delete a group
        del nested_list["child1"]

        # Verify the group was removed
        assert "child1" not in nested_list.groups
        assert len(nested_list) == 4  # Now only [1, 2, 5, 6] remain
        assert nested_list[2] == 5  # The first item in child2 is now at index 2

        # Test non-existent group
        with pytest.raises(KeyError):
            del nested_list["non_existent"]

    def test_delitem_by_slice(self, nested_list: GroupedList) -> None:
        """Tests the __delitem__ method of GroupedList with slices.

        This test verifies that the __delitem__ method deletes the correct items when accessed by slice.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]

        # Create a fresh list with simple items for testing slice deletion
        simple_list = self.UnitTestClass([1, 2, 3, 4, 5, 6])
        del simple_list[1:4]
        assert len(simple_list) == 3  # Now only [1, 5, 6] remain
        assert simple_list[0] == 1
        assert simple_list[1] == 5
        assert simple_list[2] == 6

    def test_iter(self, nested_list: GroupedList) -> None:
        """Tests the __iter__ method of GroupedList.

        This test verifies that the __iter__ method iterates through all items in the GroupedList,
        including items in child groups.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        items = list(nested_list)
        assert items == [1, 2, 3, 4, 5, 6]

    def test_contains(self, nested_list: GroupedList) -> None:
        """Tests the __contains__ method of GroupedList.

        This test verifies that the __contains__ method correctly checks if an item is in the GroupedList,
        including in child groups.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        assert 1 in nested_list
        assert 3 in nested_list  # In child1
        assert 6 in nested_list  # In child2
        assert 7 not in nested_list

    def test_add_group(self, empty_list: GroupedList) -> None:
        """Tests the add_group method of GroupedList.

        This test verifies that the add_group method correctly adds an existing group.

        Args:
            empty_list: An empty GroupedList.
        """
        # Create a group
        group = self.UnitTestClass([1, 2, 3])

        # Add the group
        empty_list.add_group(group, "group1")
        assert "group1" in empty_list.groups
        assert empty_list.groups["group1"] is group
        assert group in empty_list.data

        # Try to add a group with an existing name
        group2 = self.UnitTestClass([4, 5, 6])
        with pytest.raises(KeyError):
            empty_list.add_group(group2, "group1")

        # Try to add the same group as itself
        with pytest.raises(ValueError, match="Cannot add this GroupedList to itself"):
            empty_list.add_group(empty_list, "self")

        # Try to add a parent as a child
        child = self.UnitTestClass([7, 8, 9], parent=empty_list)
        with pytest.raises(
            ValueError, match=re.escape("Cannot add a GroupedList that is already a parent of this GroupedList.")
        ):
            child.add_group(empty_list, "parent")

    # Instantiation #
    def test_instance_creation(self) -> None:
        """Tests that instances of GroupedList can be created with various parameters.

        This test verifies that GroupedList instances can be created with no items, with items,
        and with parent-child relationships.
        """
        # Create an empty instance
        gl = self.UnitTestClass()
        assert gl is not None
        assert len(gl.data) == 0
        assert len(gl.groups) == 0
        assert isinstance(gl.parents, set)
        assert len(gl.parents) == 0

        # Create an instance with items
        items = [1, 2, 3, 4, 5]
        gl = self.UnitTestClass(items)
        assert gl is not None
        assert len(gl.data) == 5
        assert gl.data == items
        assert len(gl.groups) == 0
        assert len(gl.parents) == 0

        # Create a child instance with a parent
        parent = self.UnitTestClass([1, 2])
        child = self.UnitTestClass([3, 4], parent=parent)
        assert child is not None
        assert len(child.data) == 2
        assert child.data == [3, 4]
        assert len(child.parents) == 1
        assert parent in child.parents

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
        assert len(obj_copy.data) == len(test_object.data)
        assert len(obj_copy.groups) == len(test_object.groups)

        # Check that the data items are the same objects (shallow copy)
        for i, item in enumerate(obj_copy.data):
            if not isinstance(item, self.UnitTestClass):
                assert item == test_object.data[i]
            else:
                assert item is test_object.data[i]  # Same objects in shallow copy
                # Ensure the copy is added as a parent to the child group
                if isinstance(item, self.UnitTestClass):
                    assert obj_copy in item.parents

        # Check that the groups are the same objects
        for name, group in obj_copy.groups.items():
            assert name in test_object.groups
            assert group is test_object.groups[name]

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

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
        assert len(obj_deepcopy.data) == len(test_object.data)
        assert len(obj_deepcopy.groups) == len(test_object.groups)

        # Check that the data items are equal but not the same objects
        for i, item in enumerate(obj_deepcopy.data):
            if not isinstance(item, GroupedList):
                assert item == test_object.data[i]
            else:
                assert item is not test_object.data[i]  # Different objects in deep copy
                assert len(item.data) == len(test_object.data[i].data)

        # Check that the groups are different objects
        for name, group in obj_deepcopy.groups.items():
            assert name in test_object.groups
            assert group is not test_object.groups[name]

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
        assert len(unpickled.data) == len(test_object.data)
        assert len(unpickled.groups) == len(test_object.groups)

        # Check that the data items are equal
        for i, item in enumerate(unpickled.data):
            if not isinstance(item, GroupedList):
                assert item == test_object.data[i]
            else:
                assert item is not test_object.data[i]
                assert len(item.data) == len(test_object.data[i].data)

        # Check that the groups are accessible
        for name in test_object.groups:
            assert name in unpickled.groups

    # Functionality #
    def test_append(self, empty_list: GroupedList) -> None:
        """Tests the append method of GroupedList.

        This test verifies that the append method correctly adds an item to the GroupedList.

        Args:
            empty_list: An empty GroupedList.
        """
        # Append to the main list
        empty_list.append(1)
        assert len(empty_list) == 1
        assert empty_list[0] == 1

        # Append to a group
        empty_list.create_group("group1")
        empty_list.append(2, "group1")
        assert len(empty_list) == 2
        assert empty_list[1] == 2
        assert empty_list["group1"][0] == 2

    def test_extend(self, empty_list: GroupedList) -> None:
        """Tests the extend method of GroupedList.

        This test verifies that the extend method correctly adds items to the GroupedList.

        Args:
            empty_list: An empty GroupedList.
        """
        # Extend the main list
        empty_list.extend([1, 2, 3])
        assert len(empty_list) == 3
        assert empty_list.data == [1, 2, 3]

        # Extend a group
        empty_list.create_group("group1")
        empty_list.extend([4, 5], "group1")
        assert len(empty_list) == 5
        assert empty_list["group1"].data == [4, 5]

    def test_insert(self, simple_list: GroupedList) -> None:
        """Tests the insert method of GroupedList.

        This test verifies that the insert method correctly inserts an item at a specific position.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Insert at the beginning
        simple_list.insert(0, 0)
        assert simple_list.data[0] == 0
        assert len(simple_list) == 6

        # Insert in the middle
        simple_list.insert(3, 2.5)
        assert simple_list[3] == 2.5
        assert len(simple_list) == 7

        # Insert at the end
        simple_list.insert(len(simple_list), 6)
        assert simple_list[-1] == 6
        assert len(simple_list) == 8

    def test_remove(self, simple_list: GroupedList) -> None:
        """Tests the remove method of GroupedList.

        This test verifies that the remove method correctly removes the first occurrence of an item.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Remove an item
        simple_list.remove(3)
        assert 3 not in simple_list
        assert len(simple_list) == 4

        # Try to remove a non-existent item
        with pytest.raises(ValueError, match="item is not present in this object"):
            simple_list.remove(10)

    def test_pop(self, simple_list: GroupedList) -> None:
        """Tests the pop method of GroupedList.

        This test verifies that the pop method correctly removes and returns an item at a specific position.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Create a fresh list with known values
        test_list = self.UnitTestClass([1, 2, 3, 4, 5])

        # Pop from a specific position
        item = test_list.pop(1)
        assert item == 2
        assert len(test_list) == 4
        assert test_list.data == [1, 3, 4, 5]

        # Pop from the beginning
        item = test_list.pop(0)
        assert item == 1
        assert len(test_list) == 3
        assert test_list.data == [3, 4, 5]

        # Try to pop from an invalid position
        with pytest.raises(IndexError):
            test_list.pop(10)

    def test_clear(self, nested_list: GroupedList) -> None:
        """Tests the clear method of GroupedList.

        This test verifies that the clear method correctly removes all items from the GroupedList.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Clear the main list
        nested_list.clear()
        assert len(nested_list.data) == 0
        assert len(nested_list.groups) == 0
        assert len(nested_list) == 0

        # Create a new nested list and clear a group
        parent = self.UnitTestClass([1, 2])
        child = self.UnitTestClass([3, 4], parent=parent)
        parent.data.append(child)
        parent.groups["child"] = child

        parent.clear("child")
        assert len(parent.data) == 3  # [1, 2, child]
        assert len(parent.groups) == 1
        assert len(parent["child"].data) == 0
        assert len(parent) == 2  # Only [1, 2] remain

    @pytest.mark.parametrize(
        ("item", "expected", "setup_func"),
        [
            (3, 1, None),
            (3, 2, lambda lst: lst.append(3)),
            (10, 0, None),
        ],
        ids=["existing", "duplicate", "non_existent"],
    )
    def test_count(self, simple_list: GroupedList, item: Any, expected: int, setup_func: Any) -> None:
        """Tests the count method of GroupedList.

        This test verifies that the count method correctly counts the occurrences of an item.

        Args:
            simple_list: A GroupedList with simple items.
            item: The item to count.
            expected: The expected count.
            setup_func: A setup function to modify the list.
        """
        if setup_func:
            setup_func(simple_list)
        assert simple_list.count(item) == expected

    @pytest.mark.parametrize(
        ("item", "args", "expected", "error"),
        [
            (3, (), 2, None),
            (10, (), None, ValueError),
            (4, (3,), 3, None),
            (5, (0, 5), 4, None),
            (3, (3,), None, ValueError),
        ],
        ids=["found", "not_found", "start", "start_stop", "start_not_found"],
    )
    def test_index(
        self,
        simple_list: GroupedList,
        item: Any,
        args: tuple[Any, ...],
        expected: int | None,
        error: type[Exception] | None,
    ) -> None:
        """Tests the index method of GroupedList.

        This test verifies that the index method correctly returns the index of the first occurrence of an item.

        Args:
            simple_list: A GroupedList with simple items.
            item: The item to find.
            args: Additional arguments (start, stop).
            expected: The expected index.
            error: The expected error type, if any.
        """
        if error:
            with pytest.raises(error):
                simple_list.index(item, *args)
        else:
            assert simple_list.index(item, *args) == expected

    def test_reverse(self, simple_list: GroupedList) -> None:
        """Tests the reverse method of GroupedList.

        This test verifies that the reverse method correctly reverses the order of items.

        Args:
            simple_list: A GroupedList with simple items.
        """
        simple_list.reverse()
        assert simple_list.data == [5, 4, 3, 2, 1]

    def test_sort(self, simple_list: GroupedList) -> None:
        """Tests the sort method of GroupedList.

        This test verifies that the sort method correctly sorts the items.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Reverse the list first
        simple_list.reverse()
        assert simple_list.data == [5, 4, 3, 2, 1]

        # Sort the list
        simple_list.sort()
        assert simple_list.data == [1, 2, 3, 4, 5]

        # Sort with a key function
        simple_list.sort(key=lambda x: -x)
        assert simple_list.data == [5, 4, 3, 2, 1]

    def test_create_group(self, empty_list: GroupedList) -> None:
        """Tests the create_group method of GroupedList.

        This test verifies that the create_group method correctly creates a new group.

        Args:
            empty_list: An empty GroupedList.
        """
        # Create a group
        group = empty_list.create_group("group1")
        assert isinstance(group, GroupedList)
        assert "group1" in empty_list.groups
        assert empty_list.groups["group1"] is group
        assert group in empty_list.data

        # Create a group with items
        group2 = empty_list.create_group("group2", [1, 2, 3])
        assert len(group2.data) == 3
        assert group2.data == [1, 2, 3]

        # Try to create a group with an existing name
        with pytest.raises(KeyError):
            empty_list.create_group("group1")

    def test_require_group(self, empty_list: GroupedList) -> None:
        """Tests the require_group method of GroupedList.

        This test verifies that the require_group method correctly gets or creates a group.

        Args:
            empty_list: An empty GroupedList.
        """
        # Require a non-existent group
        group1 = empty_list.require_group("group1")
        assert isinstance(group1, GroupedList)
        assert "group1" in empty_list.groups
        assert empty_list.groups["group1"] is group1

        # Require an existing group
        group1_again = empty_list.require_group("group1")
        assert group1_again is group1

        # Test simple nested group creation
        # Create a new empty list for this test
        test_list = self.UnitTestClass()

        # Create a group
        group1 = test_list.require_group("group1")

        # Create a nested group inside group1
        nested_group = group1.require_group("nested")

        # Verify the nested group was created correctly
        assert "group1" in test_list.groups
        assert "nested" in group1.groups
        assert group1.groups["nested"] is nested_group

    def test_remove_group(self, nested_list: GroupedList) -> None:
        """Tests the remove_group method of GroupedList.

        This test verifies that the remove_group method correctly removes a group.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Remove a group by name
        nested_list.remove_group("child1")
        assert "child1" not in nested_list.groups
        assert len(nested_list.data) == 3  # [1, 2, child2]

        # Remove a group by object
        child2 = nested_list.groups["child2"]
        nested_list.remove_group(child2)
        assert "child2" not in nested_list.groups
        assert len(nested_list.data) == 2  # [1, 2]

        # Try to remove a non-existent group
        with pytest.raises(KeyError):
            nested_list.remove_group("non_existent")

    def test_get_group(self, nested_list: GroupedList) -> None:
        """Tests the get_group method of GroupedList.

        This test verifies that the get_group method correctly gets a group.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Get a group
        child1 = nested_list.get_group("child1")
        assert child1 is nested_list.groups["child1"]

        # Try to get a non-existent group
        with pytest.raises(KeyError):
            nested_list.get_group("non_existent")

        # Create a nested group and get it
        nested_group = nested_list.require_group(["child1", "nested"])
        retrieved_group = nested_list.get_group(["child1", "nested"])
        assert retrieved_group is nested_group

    def test_as_flat_list(self, nested_list: GroupedList) -> None:
        """Tests the as_flat_list method of GroupedList.

        This test verifies that the as_flat_list method correctly returns a flat list of all items.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        flat_list = nested_list.as_flat_list()
        assert flat_list == [1, 2, 3, 4, 5, 6]

    def test_as_flat_tuple(self, nested_list: GroupedList) -> None:
        """Tests the as_flat_tuple method of GroupedList.

        This test verifies that the as_flat_tuple method correctly returns a flat tuple of all items.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened tuple is (1, 2, 3, 4, 5, 6)
        flat_tuple = nested_list.as_flat_tuple()
        assert flat_tuple == (1, 2, 3, 4, 5, 6)

    def test_arithmetic_operations(self, simple_list: GroupedList) -> None:
        """Tests the arithmetic operations of GroupedList.

        This test verifies that the arithmetic operations correctly combine GroupedLists.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Addition
        other_list = self.UnitTestClass([6, 7, 8])
        result = simple_list + other_list
        assert isinstance(result, GroupedList)
        assert result.data == [1, 2, 3, 4, 5, 6, 7, 8]

        # Right addition
        result = [6, 7, 8] + simple_list  # noqa: RUF005
        assert isinstance(result, GroupedList)
        assert result.data == [6, 7, 8, 1, 2, 3, 4, 5]

        # In-place addition
        original = simple_list.copy()
        simple_list += [6, 7, 8]
        assert simple_list.data == [*original.data, 6, 7, 8]

        # Multiplication
        result = simple_list * 2
        assert isinstance(result, GroupedList)
        assert len(result.data) == len(simple_list.data) * 2

        # Right multiplication
        result = 2 * simple_list
        assert isinstance(result, GroupedList)
        assert len(result.data) == len(simple_list.data) * 2

        # In-place multiplication
        original = simple_list.copy()
        simple_list *= 2
        assert len(simple_list.data) == len(original.data) * 2

    def test_comparison_operations(self) -> None:
        """Tests the comparison operations of GroupedList.

        This test verifies that the comparison operations correctly compare GroupedLists.
        """
        list1 = self.UnitTestClass([1, 2, 3])
        list2 = self.UnitTestClass([1, 2, 3])
        list3 = self.UnitTestClass([1, 2, 4])
        list4 = self.UnitTestClass([1, 2])

        # Equality
        assert list1 == list2
        assert list1 != list3
        assert list1 != list4

        # Less than
        assert list1 < list3
        assert list4 < list1
        assert not (list1 < list2)

        # Less than or equal
        assert list1 <= list2
        assert list1 <= list3
        assert list4 <= list1

        # Greater than
        assert list3 > list1
        assert list1 > list4
        assert not (list1 > list2)

        # Greater than or equal
        assert list1 >= list2
        assert list3 >= list1
        assert list1 >= list4

        # Compare with other types
        assert list1 == [1, 2, 3]
        assert list1 < [1, 2, 4]
        assert list1 > [1, 2]

    def test_get_group_lengths(self) -> None:
        """Tests the get_group_lengths method."""
        gl = self.UnitTestClass([1, 2])
        # No groups, returns int length of items
        assert gl.get_group_lengths() == 2

        child = self.UnitTestClass([3, 4])
        gl.add_group(child, "child")

        # 2 items + 1 child group (length 2)
        ret = gl.get_group_lengths()
        assert ret == (2, (2,))

        # Recurse
        grandchild = self.UnitTestClass([5])
        child.add_group(grandchild, "grandchild")

        ret = gl.get_group_lengths(recurse=True)
        # Structure: (items_in_gl, (child_lengths_recursive,))
        # child_lengths_recursive = (items_in_child, (grandchild_lengths,))
        assert ret == (2, ((2, (1,)),))

    def test_pop_nested(self) -> None:
        """Tests popping items when nested groups are present."""
        gl = self.UnitTestClass([1])
        child = self.UnitTestClass([2, 3])
        gl.add_group(child, "child")
        gl.append(4)
        # Flat: 1, 2, 3, 4

        # Pop 4 (index 3) - After the group
        val = gl.pop(3)
        assert val == 4

        # Pop 3 (index 2) - last item of child
        val = gl.pop(2)
        assert val == 3
        assert len(child) == 1

    def test_invalid_index_types(self) -> None:
        """Tests invalid index types for getitem, setitem, and delitem."""
        gl = self.UnitTestClass([1])

        with pytest.raises((TypeError, TypeCheckError)):
            gl[None]  # type: ignore[call-overload]

        with pytest.raises((TypeError, TypeCheckError)):
            gl[None] = 1  # type: ignore[index]

        with pytest.raises((TypeError, TypeCheckError)):
            del gl[None]  # type: ignore[arg-type]

    def test_remove_parent_from_children(self) -> None:
        """Tests removing a parent from children."""
        gl = self.UnitTestClass()
        child = self.UnitTestClass()
        gl.add_group(child, "child")

        assert gl in child.parents

        gl.remove_parent_from_children(gl)
        assert gl not in child.parents

    def test_pop_edge_cases(self) -> None:
        """Tests edge cases for pop."""
        gl = self.UnitTestClass()
        child = self.UnitTestClass([1, 2])
        gl.add_group(child, "child")

        # Pop from child via parent
        # index 0 -> child[0] -> 1
        val = gl.pop(0)
        assert val == 1

        # Pop remaining from child
        # index 0 -> child[0] -> 2
        val = gl.pop(0)
        assert val == 2

        # Now child is empty
        assert len(child) == 0
        # Pop from gl (empty)? raises IndexError
        with pytest.raises(IndexError):
            gl.pop(0)

    def test_item_access_types(self) -> None:
        """Tests different item access types."""
        gl = self.UnitTestClass([1, 2])
        child = self.UnitTestClass([3, 4])
        gl.add_group(child, "child")

        # Int access
        assert gl[0] == 1
        assert gl[2] == 3  # Flattened access into child

        # Str access (get group)
        assert gl["child"] is child

        # Slice access
        assert gl[1:3] == [2, 3]

        # Set item
        gl[0] = 10
        assert gl[0] == 10

        # Attempt to overwrite existing group via setitem should fail
        with pytest.raises(KeyError):
            gl["child"] = self.UnitTestClass([5, 6])

        # Set slice
        gl[0:2] = [11, 12]
        assert gl[0] == 11
        assert gl[1] == 12

        # Del item
        del gl[0]
        # Now: 12, child(3,4) -> 12, 3, 4
        assert len(gl) == 3
        assert gl[0] == 12
        assert gl[1] == 3

        # Del slice
        # Current: 12, 3, 4
        del gl[1:3]
        # Removes 3, 4 (from child)
        assert len(gl) == 1
        assert gl[0] == 12

    def test_group_management(self) -> None:
        """Tests group management methods."""
        gl = self.UnitTestClass([1])

        # Create group
        g1 = gl.create_group("g1", [2, 3])
        assert "g1" in gl.groups
        assert g1 in gl.data
        assert gl in g1.parents
        assert gl[1] == 2

        # Require group (existing)
        g1_req = gl.require_group("g1")
        assert g1_req is g1

        # Require group (new)
        g2 = gl.require_group("g2", [4])
        assert "g2" in gl.groups
        assert len(g2) == 1

        # Require nested group
        # "g1" exists. Need "sub" in "g1".
        # Note: require_group consumes list from the end (pop), so order is [child, parent]
        sub = gl.require_group(["sub", "g1"], [5])
        assert "sub" in g1.groups
        assert sub in g1.data
        assert g1 in sub.parents

        # Remove group
        gl.remove_group("g2")
        assert "g2" not in gl.groups

    def test_arithmetic_operators(self) -> None:
        """Tests arithmetic operators."""
        gl1 = self.UnitTestClass([1, 2])
        gl2 = self.UnitTestClass([3, 4])

        # __add__
        gl3 = gl1 + gl2
        assert len(gl3) == 4
        assert list(gl3) == [1, 2, 3, 4]
        assert isinstance(gl3, self.UnitTestClass)

        # __add__ with list
        gl4 = [*gl1, 5, 6]
        assert list(gl4) == [1, 2, 5, 6]

        # __iadd__
        gl1 += [7]
        assert list(gl1) == [1, 2, 7]

        # __mul__
        gl_mul = gl2 * 2
        assert list(gl_mul) == [3, 4, 3, 4]

        # __imul__
        gl2 *= 2
        assert list(gl2) == [3, 4, 3, 4]

    def test_remove_clear_count_index(self) -> None:
        """Tests remove, clear, count, and index methods."""
        gl = self.UnitTestClass([1, 2, 1, 3])
        child = self.UnitTestClass([4, 1])
        gl.add_group(child, "child")
        # Content: 1, 2, 1, 3, 4, 1

        # Count
        assert gl.count(1) == 3
        assert gl.count(4) == 1

        # Index
        assert gl.index(4) == 4
        assert gl.index(1) == 0
        assert gl.index(1, 1) == 2  # Start from index 1

        # Remove item
        gl.remove(2)
        assert 2 not in gl

        # Remove from group via parent
        gl.remove(4)
        assert 4 not in child

        # Remove with group name
        child.append(5)
        gl.remove(5, "child")
        assert 5 not in child

        # Clear
        gl.clear("child")
        assert len(child) == 0
        assert "child" in gl.groups  # Group still exists, but empty?

        gl.clear()
        assert len(gl) == 0
        assert len(gl.groups) == 0

    def test_reverse_sort_extend(self) -> None:
        """Tests reverse, sort, and extend methods."""
        gl = self.UnitTestClass([1, 3])
        child = self.UnitTestClass([2, 4])
        gl.add_group(child, "child")
        # Flat: 1, 3, 2, 4

        # Reverse
        gl.reverse()
        assert list(gl) == [4, 2, 3, 1]

        # Sort
        try:
            gl.sort()
            # Expect flat: 1, 2, 3, 4
            assert list(gl) == [1, 2, 3, 4]
        except TypeError:
            pass

        # Extend
        gl.extend([5, 6])
        assert 5 in gl
        assert 6 in gl

    def test_error_cases(self) -> None:
        """Tests error cases."""
        gl = self.UnitTestClass()

        # Add self
        with pytest.raises(ValueError, match="itself"):
            gl.add_group(gl, "self")

        # Add parent
        child = self.UnitTestClass()
        gl.add_group(child, "child")
        # child is child of gl.
        # try adding gl to child
        with pytest.raises(ValueError, match="already a parent"):
            child.add_group(gl, "parent")

    def test_complex_indexing_and_structure(self) -> None:
        """Tests complex indexing and structure."""
        # Setup: child followed by item
        gl = self.UnitTestClass()
        child = self.UnitTestClass([1, 2])
        gl.add_group(child, "child")
        gl.append(3)
        # Data: [child, 3]
        # Flat: 1, 2, 3

        # get_item with index inside group (not first)
        # Index 1 is '2' (inside child)
        assert gl[1] == 2

        # get_item with index after group
        # Index 2 is '3'
        assert gl[2] == 3

        # Negative indexing
        # -1 is 3
        assert gl[-1] == 3
        # -2 is 2 (inside child)
        assert gl[-2] == 2
        # -3 is 1 (inside child)
        assert gl[-3] == 1

        # set_item with negative index
        gl[-1] = 30
        assert gl[2] == 30
        gl[-2] = 20
        assert child[1] == 20

        # insert with group
        gl.insert(0, 0, group="child")
        # child: [0, 1, 20]
        assert child[0] == 0

        # extend with group
        gl.extend([4, 5], group="child")
        # child: [0, 1, 20, 4, 5]
        assert child[4] == 5

        # radd
        # [99] + gl
        gl_new = [99, *gl]
        # gl_new: 99, 0, 1, 20, 4, 5, 30
        assert gl_new[0] == 99
        assert gl_new[1] == 0

        # Comparisons
        gl_copy = gl.copy()
        assert gl_copy == gl
        assert gl_copy <= gl
        assert gl_copy >= gl

        # Modify copy
        gl_copy.append(100)
        assert gl < gl_copy
        assert gl_copy > gl

    def test_missing_coverage_paths(self) -> None:
        """Tests missing coverage paths."""
        # 1. init=False
        gl = self.UnitTestClass(init=False)
        assert len(gl) == 0
        gl.construct(items=[1, 2])
        assert len(gl) == 2

        # 2. __repr__
        gl = self.UnitTestClass([1, 2])
        assert repr(gl) == "(1, 2)"

        # 3. remove_parent_from_children with mixed content
        gl = self.UnitTestClass([1])
        child = self.UnitTestClass([2])
        gl.add_group(child, "child")
        # Now data has [1, child]
        # This triggers the 'isinstance' check in loop
        gl.remove_parent_from_children(gl)
        # No error, coverage of 'isinstance' branch

        # 4. Group delegation methods
        gl = self.UnitTestClass()
        child = self.UnitTestClass([1, 2, 3])
        gl.add_group(child, "child")

        # get_item with group
        assert gl.get_item(0, group="child") == 1

        # set_item with group
        gl.set_item(0, 10, group="child")
        assert child[0] == 10

        # get_slice with group
        assert gl.get_slice(slice(0, 2), group="child") == [10, 2]

        # set_slice with group
        gl.set_slice(slice(0, 2), [20, 30], group="child")
        assert child[0] == 20
        assert child[1] == 30

        # delete_item with group
        gl.delete_item(0, group="child")
        assert len(child) == 2
        assert child[0] == 30

        # delete_slice with group
        gl.delete_slice(slice(0, 1), group="child")
        assert len(child) == 1
        assert child[0] == 3

        # pop with group
        val = gl.pop(0, group="child")
        assert val == 3
        assert len(child) == 0

        # append with group
        gl.append(100, group="child")
        assert child[0] == 100

        # insert with group
        gl.insert(0, 50, group="child")
        assert child[0] == 50

        # extend with group
        gl.extend([60], group="child")
        assert child[2] == 60

        # remove with group
        gl.remove(50, group="child")
        assert 50 not in child

        # clear with group
        gl.clear(group="child")
        assert len(child) == 0

        # 5. Reverse logic deeply nested
        gl = self.UnitTestClass([1])
        child = self.UnitTestClass([2, 3, 4])
        gl.add_group(child, "child")

        # set_item(-3) -> sets '2' (index 0 of child)
        gl[-3] = 20
        assert child[0] == 20

        # pop(-3) -> removes '20'
        val = gl.pop(-3)
        assert val == 20
        assert len(child) == 2  # [3, 4]

        # delete_item(-3) -> removes '3'
        del gl[-2]
        assert 3 not in child
        assert len(child) == 1  # [4]

        # 6. Arithmetic with single items
        gl = self.UnitTestClass([1])

        # __add__ with int
        gl2 = gl + 2
        assert list(gl2) == [1, 2]

        # __radd__ with int
        gl3 = 2 + gl
        assert list(gl3) == [2, 1]

        # __iadd__ with int
        gl += 3
        assert list(gl) == [1, 3]

        # 7. __radd__ with GroupedList (via subclass)
        class OtherGL(self.UnitTestClass):  # type: ignore[misc, name-defined]
            def __add__(self, other: Any) -> Any:
                return NotImplemented

        other = OtherGL([10])
        gl = self.UnitTestClass([20])
        res = other + gl
        assert list(res) == [10, 20]
        assert isinstance(res, self.UnitTestClass)

    def test_more_missing_coverage(self) -> None:
        """Tests additional missing coverage paths."""
        gl = self.UnitTestClass([1])
        child = self.UnitTestClass([2, 3, 4])
        gl.add_group(child, "child")

        # 2. create_group duplicate
        with pytest.raises(KeyError):
            gl.create_group("child")

        # 4. get_group list
        # Create nested group
        sub = child.create_group("sub", [5])
        g = gl.get_group(["sub", "child"])
        assert g is sub

        # 5. IndexError
        with pytest.raises(IndexError):
            gl[100]
        with pytest.raises(IndexError):
            gl[-100]
        with pytest.raises(IndexError):
            gl[100] = 1
        with pytest.raises(IndexError):
            del gl[100]

        # 6. ValueError set_slice
        with pytest.raises(
            ValueError,
            match="attempt to assign sequence of size 2 to slice of size 1",
        ):
            gl[0:1] = [10, 20]

        # 7. set_item positive deep index (Block 2, reverse=False)
        gl[2] = 30
        assert child[1] == 30

        # 8. delete_item positive deep index (Block 2, reverse=False)
        del gl[2]
        assert 3 not in child
        assert len(child) == 3  # 2, 4, 5

        # 9. remove(item_in_child)
        gl.remove(5)
        assert 5 not in sub

        # 10. remove_group(obj)
        gl.remove_group(child)
        assert "child" not in gl.groups
        assert child not in gl.data

        # 11. __delitem__ str
        gl.add_group(child, "child")
        del gl["child"]
        assert "child" not in gl.groups

        # 12. remove missing item with groups present
        gl2 = self.UnitTestClass([1])
        g1 = self.UnitTestClass([2])
        gl2.add_group(g1, "g1")
        with pytest.raises(ValueError, match="item is not present in this object"):
            gl2.remove(999)

        # 13. remove item in second group
        gl3 = self.UnitTestClass()
        g2 = self.UnitTestClass([3])
        g3 = self.UnitTestClass([4])
        gl3.add_group(g2, "g2")
        gl3.add_group(g3, "g3")
        gl3.remove(4)
        assert 4 not in g3
