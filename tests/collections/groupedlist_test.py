"""groupedlist_test.py
Tests for the GroupedList class in the baseobjects package.

This module provides tests for the GroupedList class, which is a list that contains any item, but nested GroupLists'
contents are treated as if they are elements of this list.
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
from src.baseobjects.collections import GroupedList
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestGroupedList(BaseObjectTestSuite):
    """Test the GroupedList class.

    This class tests the functionality of the GroupedList class, which is a list that contains any item,
    but nested GroupLists' contents are treated as if they are elements of this list.
    """

    # Attributes #
    TestClass: type[GroupedList] = GroupedList

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_list(self) -> GroupedList:
        """Create an empty GroupedList for testing.

        Returns:
            GroupedList: An empty GroupedList.
        """
        return self.TestClass()

    @pytest.fixture
    def simple_list(self) -> GroupedList:
        """Create a GroupedList with simple items for testing.

        Returns:
            GroupedList: A GroupedList with simple items.
        """
        return self.TestClass([1, 2, 3, 4, 5])

    @pytest.fixture
    def nested_list(self) -> GroupedList:
        """Create a GroupedList with nested GroupedLists for testing.

        Returns:
            GroupedList: A GroupedList with nested GroupedLists.
        """
        parent = self.TestClass([1, 2])
        child1 = self.TestClass([3, 4], parent=parent)
        child2 = self.TestClass([5, 6], parent=parent)
        parent.data.extend([child1, child2])
        parent.groups["child1"] = child1
        parent.groups["child2"] = child2
        return parent

    @pytest.fixture
    def test_object(self) -> GroupedList:
        """Create a test object for testing.

        Returns:
            GroupedList: A GroupedList with some items and a nested group.
        """
        parent = self.TestClass([1, 2, 3])
        child = self.TestClass([4, 5], parent=parent)
        parent.data.append(child)
        parent.groups["child"] = child
        return parent

    # Tests
    def test_copy(self, test_object: GroupedList) -> None:
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
        assert len(obj_copy.data) == len(test_object.data)
        assert len(obj_copy.groups) == len(test_object.groups)

        # Check that the data items are the same objects (shallow copy)
        for i, item in enumerate(obj_copy.data):
            if not isinstance(item, GroupedList):
                assert item == test_object.data[i]
            else:
                assert item is test_object.data[i]  # Same objects in shallow copy

        # Check that the groups are the same objects
        for name, group in obj_copy.groups.items():
            assert name in test_object.groups
            assert group is test_object.groups[name]

    def test_copy_method(self, test_object: GroupedList) -> None:
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
        assert len(obj_copy.data) == len(test_object.data)
        assert len(obj_copy.groups) == len(test_object.groups)

        # Check that the data items are the same objects (shallow copy)
        for i, item in enumerate(obj_copy.data):
            if not isinstance(item, GroupedList):
                assert item == test_object.data[i]
            else:
                assert item is test_object.data[i]  # Same objects in shallow copy

        # Check that the groups are the same objects
        for name, group in obj_copy.groups.items():
            assert name in test_object.groups
            assert group is test_object.groups[name]

    def test_deepcopy(self, test_object: GroupedList, memo: dict | None = None) -> None:
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

    def test_deepcopy_method(self, test_object: GroupedList, memo: dict | None = None) -> None:
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

    def test_pickling(self, test_object: GroupedList) -> None:
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

    def test_instance_creation(self) -> None:
        """Test that instances of GroupedList can be created with various parameters.

        This test verifies that GroupedList instances can be created with no items, with items,
        and with parent-child relationships.
        """
        # Create an empty instance
        gl = self.TestClass()
        assert gl is not None
        assert len(gl.data) == 0
        assert len(gl.groups) == 0
        assert isinstance(gl.parents, set)
        assert len(gl.parents) == 0

        # Create an instance with items
        items = [1, 2, 3, 4, 5]
        gl = self.TestClass(items)
        assert gl is not None
        assert len(gl.data) == 5
        assert gl.data == items
        assert len(gl.groups) == 0
        assert len(gl.parents) == 0

        # Create a child instance with a parent
        parent = self.TestClass([1, 2])
        child = self.TestClass([3, 4], parent=parent)
        assert child is not None
        assert len(child.data) == 2
        assert child.data == [3, 4]
        assert len(child.parents) == 1
        assert parent in child.parents

    def test_len(self, nested_list: GroupedList) -> None:
        """Test the __len__ method of GroupedList.

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

    def test_getitem_by_index(self, nested_list: GroupedList) -> None:
        """Test the __getitem__ method of GroupedList with integer indices.

        This test verifies that the __getitem__ method returns the correct item when accessed by index.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        assert nested_list[0] == 1
        assert nested_list[1] == 2
        assert nested_list[2] == 3
        assert nested_list[3] == 4
        assert nested_list[4] == 5
        assert nested_list[5] == 6

        # Test negative indices
        assert nested_list[-1] == 6
        assert nested_list[-2] == 5
        assert nested_list[-3] == 4
        assert nested_list[-4] == 3
        assert nested_list[-5] == 2
        assert nested_list[-6] == 1

        # Test out of range
        with pytest.raises(IndexError):
            _ = nested_list[6]
        with pytest.raises(IndexError):
            _ = nested_list[-7]

    def test_getitem_by_name(self, nested_list: GroupedList) -> None:
        """Test the __getitem__ method of GroupedList with string names.

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

    def test_getitem_by_slice(self, nested_list: GroupedList) -> None:
        """Test the __getitem__ method of GroupedList with slices.

        This test verifies that the __getitem__ method returns the correct items when accessed by slice.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        assert nested_list[1:4] == [2, 3, 4]
        assert nested_list[0:6:2] == [1, 3, 5]
        assert nested_list[:3] == [1, 2, 3]
        assert nested_list[3:] == [4, 5, 6]
        assert nested_list[:] == [1, 2, 3, 4, 5, 6]

        # Test negative indices in slices
        assert nested_list[-3:] == [4, 5, 6]
        assert nested_list[:-3] == [1, 2, 3]
        assert nested_list[-5:-2] == [2, 3, 4]

    def test_setitem_by_index(self, nested_list: GroupedList) -> None:
        """Test the __setitem__ method of GroupedList with integer indices.

        This test verifies that the __setitem__ method sets the correct item when accessed by index.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        nested_list[0] = 10
        assert nested_list[0] == 10
        assert nested_list.data[0] == 10

        nested_list[2] = 30  # This should modify the first item in child1
        assert nested_list[2] == 30
        assert nested_list.groups["child1"].data[0] == 30

        # Test negative indices
        nested_list[-1] = 60  # This should modify the last item in child2
        assert nested_list[-1] == 60
        assert nested_list.groups["child2"].data[1] == 60

        # Test out of range
        with pytest.raises(IndexError):
            nested_list[10] = 100

    def test_setitem_by_name(self, nested_list: GroupedList) -> None:
        """Test the __setitem__ method of GroupedList with string names.

        This test verifies that the __setitem__ method sets the correct group when accessed by name.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # Create a new group
        new_group = self.TestClass([7, 8])
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
        replacement_group = self.TestClass([9, 10])
        nested_list["child1"] = replacement_group

        # Verify the group was added
        assert nested_list["child1"] is replacement_group
        assert replacement_group in nested_list.data

    def test_setitem_by_slice(self, nested_list: GroupedList) -> None:
        """Test the __setitem__ method of GroupedList with slices.

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
        with pytest.raises(ValueError):
            nested_list[1:4] = [100, 200]

    def test_delitem_by_index(self, nested_list: GroupedList) -> None:
        """Test the __delitem__ method of GroupedList with integer indices.

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
        """Test the __delitem__ method of GroupedList with string names.

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
        """Test the __delitem__ method of GroupedList with slices.

        This test verifies that the __delitem__ method deletes the correct items when accessed by slice.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]

        # Create a fresh list with simple items for testing slice deletion
        simple_list = self.TestClass([1, 2, 3, 4, 5, 6])
        del simple_list[1:4]
        assert len(simple_list) == 3  # Now only [1, 5, 6] remain
        assert simple_list[0] == 1
        assert simple_list[1] == 5
        assert simple_list[2] == 6

    def test_iter(self, nested_list: GroupedList) -> None:
        """Test the __iter__ method of GroupedList.

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
        """Test the __contains__ method of GroupedList.

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

    def test_append(self, empty_list: GroupedList) -> None:
        """Test the append method of GroupedList.

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
        """Test the extend method of GroupedList.

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
        """Test the insert method of GroupedList.

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
        """Test the remove method of GroupedList.

        This test verifies that the remove method correctly removes the first occurrence of an item.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Remove an item
        simple_list.remove(3)
        assert 3 not in simple_list
        assert len(simple_list) == 4

        # Try to remove a non-existent item
        with pytest.raises(ValueError):
            simple_list.remove(10)

    def test_pop(self, simple_list: GroupedList) -> None:
        """Test the pop method of GroupedList.

        This test verifies that the pop method correctly removes and returns an item at a specific position.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Create a fresh list with known values
        test_list = self.TestClass([1, 2, 3, 4, 5])

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
        """Test the clear method of GroupedList.

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
        parent = self.TestClass([1, 2])
        child = self.TestClass([3, 4], parent=parent)
        parent.data.append(child)
        parent.groups["child"] = child

        parent.clear("child")
        assert len(parent.data) == 3  # [1, 2, child]
        assert len(parent.groups) == 1
        assert len(parent["child"].data) == 0
        assert len(parent) == 2  # Only [1, 2] remain

    def test_count(self, simple_list: GroupedList) -> None:
        """Test the count method of GroupedList.

        This test verifies that the count method correctly counts the occurrences of an item.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Count an existing item
        assert simple_list.count(3) == 1

        # Add a duplicate and count again
        simple_list.append(3)
        assert simple_list.count(3) == 2

        # Count a non-existent item
        assert simple_list.count(10) == 0

    def test_index(self, simple_list: GroupedList) -> None:
        """Test the index method of GroupedList.

        This test verifies that the index method correctly returns the index of the first occurrence of an item.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Find the index of an existing item
        assert simple_list.index(3) == 2

        # Try to find the index of a non-existent item
        with pytest.raises(ValueError):
            simple_list.index(10)

        # Test with start and stop parameters
        assert simple_list.index(4, 3) == 3
        assert simple_list.index(5, 0, 5) == 4

        with pytest.raises(ValueError):
            simple_list.index(3, 3)

    def test_reverse(self, simple_list: GroupedList) -> None:
        """Test the reverse method of GroupedList.

        This test verifies that the reverse method correctly reverses the order of items.

        Args:
            simple_list: A GroupedList with simple items.
        """
        simple_list.reverse()
        assert simple_list.data == [5, 4, 3, 2, 1]

    def test_sort(self, simple_list: GroupedList) -> None:
        """Test the sort method of GroupedList.

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
        """Test the create_group method of GroupedList.

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
        """Test the require_group method of GroupedList.

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
        test_list = self.TestClass()

        # Create a group
        group1 = test_list.require_group("group1")

        # Create a nested group inside group1
        nested_group = group1.require_group("nested")

        # Verify the nested group was created correctly
        assert "group1" in test_list.groups
        assert "nested" in group1.groups
        assert group1.groups["nested"] is nested_group

    def test_remove_group(self, nested_list: GroupedList) -> None:
        """Test the remove_group method of GroupedList.

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
        """Test the get_group method of GroupedList.

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

    def test_add_group(self, empty_list: GroupedList) -> None:
        """Test the add_group method of GroupedList.

        This test verifies that the add_group method correctly adds an existing group.

        Args:
            empty_list: An empty GroupedList.
        """
        # Create a group
        group = self.TestClass([1, 2, 3])

        # Add the group
        empty_list.add_group(group, "group1")
        assert "group1" in empty_list.groups
        assert empty_list.groups["group1"] is group
        assert group in empty_list.data

        # Try to add a group with an existing name
        group2 = self.TestClass([4, 5, 6])
        with pytest.raises(KeyError):
            empty_list.add_group(group2, "group1")

        # Try to add the same group as itself
        with pytest.raises(ValueError):
            empty_list.add_group(empty_list, "self")

        # Try to add a parent as a child
        child = self.TestClass([7, 8, 9], parent=empty_list)
        with pytest.raises(ValueError):
            child.add_group(empty_list, "parent")

    def test_as_flat_list(self, nested_list: GroupedList) -> None:
        """Test the as_flat_list method of GroupedList.

        This test verifies that the as_flat_list method correctly returns a flat list of all items.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened list is [1, 2, 3, 4, 5, 6]
        flat_list = nested_list.as_flat_list()
        assert flat_list == [1, 2, 3, 4, 5, 6]

    def test_as_flat_tuple(self, nested_list: GroupedList) -> None:
        """Test the as_flat_tuple method of GroupedList.

        This test verifies that the as_flat_tuple method correctly returns a flat tuple of all items.

        Args:
            nested_list: A GroupedList with nested GroupedLists.
        """
        # The nested_list has [1, 2, child1, child2] where child1 is [3, 4] and child2 is [5, 6]
        # So the flattened tuple is (1, 2, 3, 4, 5, 6)
        flat_tuple = nested_list.as_flat_tuple()
        assert flat_tuple == (1, 2, 3, 4, 5, 6)

    def test_arithmetic_operations(self, simple_list: GroupedList) -> None:
        """Test the arithmetic operations of GroupedList.

        This test verifies that the arithmetic operations correctly combine GroupedLists.

        Args:
            simple_list: A GroupedList with simple items.
        """
        # Addition
        other_list = self.TestClass([6, 7, 8])
        result = simple_list + other_list
        assert isinstance(result, GroupedList)
        assert result.data == [1, 2, 3, 4, 5, 6, 7, 8]

        # Right addition
        result = [6, 7, 8] + simple_list
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
        """Test the comparison operations of GroupedList.

        This test verifies that the comparison operations correctly compare GroupedLists.
        """
        list1 = self.TestClass([1, 2, 3])
        list2 = self.TestClass([1, 2, 3])
        list3 = self.TestClass([1, 2, 4])
        list4 = self.TestClass([1, 2])

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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
