#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" grouplist_test.py
Tests for the GroupedList class in the baseobjects package.
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
import datetime
from typing import Iterable, List, Tuple, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import GroupedList
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestGroupedList(ClassTest):
    """Test the GroupedList class.

    This class tests the functionality of the GroupedList class, which is a list that can contain nested GroupedList
    instances, and the contents of those nested lists are treated as if they are elements of the parent list.
    """
    # Attributes #
    class_: Type[GroupedList] = GroupedList
    zero_time: datetime.timedelta = datetime.timedelta(0)

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize("items", ([1, 2, 3], (1, 2, 3)))
    def test_instance_creation(self, items: List[int] | Tuple[int, ...]) -> None:
        """Test that instances of GroupedList can be created with various item types.

        This test verifies that GroupedList instances can be created with both list and tuple items.

        Args:
            items: The items to initialize the GroupedList with, either a list or tuple.
        """
        instance = self.class_(items=items)
        assert instance is not None
        assert len(instance) == len(items)

    def test_create_group(self) -> None:
        """Test creating a group in a GroupedList.

        This test verifies that a group can be created in a GroupedList and is properly registered.
        """
        gl = GroupedList()
        gl.create_group("name", [1])
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_require_group_create(self) -> None:
        """Test requiring a group that doesn't exist yet.

        This test verifies that requiring a non-existent group creates it.
        """
        gl = GroupedList()
        gl.require_group("name")
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_require_group_retrieve(self) -> None:
        """Test requiring a group that already exists.

        This test verifies that requiring an existing group returns the existing group.
        """
        gl = GroupedList()
        group_1 = gl.create_group("name")
        group_2 = gl.require_group("name")
        assert group_1 is group_2

    def test_add_group(self) -> None:
        """Test adding an existing GroupedList as a group.

        This test verifies that an existing GroupedList can be added as a group.
        """
        gl = GroupedList()
        gl.add_group(GroupedList([1]), "name")
        assert len(gl.data) == 1 and "name" in gl.groups

    def test_remove_group(self) -> None:
        """Test removing a group by name.

        This test verifies that a group can be removed by its name.
        """
        gl = GroupedList()
        group_1 = gl.create_group("name", [1])
        gl.remove_group("name")
        assert len(gl) == 0

    def test_remove_group_object(self) -> None:
        """Test removing a group by object reference.

        This test verifies that a group can be removed by its object reference.
        """
        gl = GroupedList()
        group_1 = gl.create_group("name", [1])
        gl.remove_group(group_1)
        assert len(gl) == 0

    def test_check_if_child(self) -> None:
        """Test checking if a group is a child of another GroupedList.

        This test verifies that the check_if_child method correctly identifies child groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        child = gl.create_group("name", [4, 5, 6])
        assert gl.check_if_child(child)

    def test_check_if_parent(self) -> None:
        """Test checking if a group is a parent of another GroupedList.

        This test verifies that the check_if_parent method correctly identifies parent groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        child = gl.create_group("name", [4, 5, 6])
        assert child.check_if_parent(gl)

    def test_add_parent_to_children(self) -> None:
        """Test adding a parent to all children of a GroupedList.

        This test verifies that the add_parent_to_children method correctly adds a parent to all child groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        first = gl.create_group("first", [4, 5, 6])
        second = gl.create_group("second", [7, 8, 9, 10])
        new = GroupedList([-1])
        gl.add_parent_to_children(new)
        assert first.check_if_parent(new) and second.check_if_parent(new)

    def test_remove_parent_from_children(self) -> None:
        """Test removing a parent from all children of a GroupedList.

        This test verifies that the remove_parent_from_children method correctly removes a parent from all child groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        first = gl.create_group("first", [4, 5, 6])
        second = gl.create_group("second", [7, 8, 9, 10])
        new = GroupedList([-1])
        gl.add_parent_to_children(new)
        gl.remove_parent_from_children(new)
        assert not first.check_if_parent(new) and not second.check_if_parent(new)

    def test_lengths(self) -> None:
        """Test getting the lengths of groups in a GroupedList.

        This test verifies that the get_group_lengths method correctly returns the lengths of groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.get_group_lengths() == (4, (3, 7))

    def test_lengths_recurse(self) -> None:
        """Test getting the lengths of groups in a GroupedList recursively.

        This test verifies that the get_group_lengths method with recurse=True correctly returns the lengths of groups
        and their nested groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.get_group_lengths(recurse=True) == (4, ((3, ()), (4, ((3, ()),))))

    def test_len(self) -> None:
        """Test the len method of GroupedList.

        This test verifies that the len method correctly returns the total number of items in the GroupedList, including
        items in groups.
        """
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("name", [4, 5, 6])
        assert len(gl) == 7

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_get_item(self, index: int) -> None:
        """Test getting items from a GroupedList by index.

        This test verifies that items can be accessed by index, including items in nested groups, and that both positive
        and negative indices work correctly.

        Args:
            index: The index to test, which can be positive or negative.
        """
        answer = tuple(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        assert gl[index] == answer[index]

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_set_item(self, index: int) -> None:
        """Test setting items in a GroupedList by index.

        This test verifies that items can be set by index, including items in nested groups, and that both positive and
        negative indices work correctly.

        Args:
            index: The index to test, which can be positive or negative.
        """
        answer = list(range(15))
        answer[index] = 0
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        gl[index] = 0
        assert gl == answer

    @pytest.mark.parametrize("index", (tuple(range(15)) + tuple(range(-1, -15, -1))))
    def test_del_item(self, index: int) -> None:
        """Test deleting items from a GroupedList by index.

        This test verifies that items can be deleted by index, including items in nested groups, and that both positive
        and negative indices work correctly.

        Args:
            index: The index to test, which can be positive or negative.
        """
        answer = list(range(15))
        del answer[index]
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        del gl[index]
        assert gl == answer

    def test_append(self) -> None:
        """Test appending an item to a GroupedList.

        This test verifies that items can be appended to a GroupedList and are correctly included in the flat list.
        """
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        assert gl == answer

    def test_append_group_name(self) -> None:
        """Test appending an item to a specific group in a GroupedList.

        This test verifies that items can be appended to a specific group in a GroupedList and are correctly included in
        the flat list.
        """
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14, "second")
        assert gl == answer

    def test_as_flat_list(self) -> None:
        """Test converting a GroupedList to a flat list.

        This test verifies that the as_flat_list method correctly returns a flat list of all items in the GroupedList,
        including items in nested groups.
        """
        answer = list(range(14))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.as_flat_list() == answer

    def test_as_flat_tuple(self) -> None:
        """Test converting a GroupedList to a flat tuple.

        This test verifies that the as_flat_tuple method correctly returns a flat tuple of all items in the GroupedList,
        including items in nested groups.
        """
        answer = tuple(range(14))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        assert gl.as_flat_tuple() == answer

    def test_copy(self) -> None:
        """Test copying a GroupedList.

        This test verifies that the copy method correctly creates a copy of a GroupedList with all its groups and items.
        """
        answer = list(range(15))
        gl = GroupedList([0, 1, 2, 3])
        gl.create_group("first", [4, 5, 6])
        level_1 = gl.create_group("second", [7, 8, 9, 10])
        level_2 = level_1.create_group("inner", [11, 12, 13])
        gl.append(14)
        gl_2 = gl.copy()
        assert gl_2 == answer

    def test_empty_group(self) -> None:
        """Test creating and working with empty groups.

        This test verifies that empty groups can be created and manipulated correctly.
        """
        gl = GroupedList([1, 2, 3])
        empty_group = gl.create_group("empty")

        # Verify the empty group doesn't affect the length
        assert len(gl) == 3

        # Add an item to the empty group
        empty_group.append(4)
        assert len(gl) == 4
        assert gl[3] == 4

    def test_duplicate_group_names(self) -> None:
        """Test handling of duplicate group names.

        This test verifies that attempting to require a group with a name that already exists returns the existing group
        rather than creating a new one. It also verifies that creating a group with a name that already exists will
        raise an error.
        """
        gl = GroupedList([1, 2, 3])
        group1 = gl.create_group("duplicate", [4, 5])
        group2 = gl.require_group("duplicate", [6, 7]) # Should return the existing group

        # Verify that group1 and group2 are the same object
        assert group1 is group2

        # Verify that the items weren't added twice
        assert len(gl) == 5
        assert gl.as_flat_list() == [1, 2, 3, 4, 5]

        # Using Create Group on an existing group should raise an error
        with pytest.raises(KeyError):
            group2 = gl.create_group("duplicate", [6, 7])  # Should return the existing group

    def test_circular_reference(self) -> None:
        """Test handling of circular references.

        This test verifies that circular references (a group containing itself or its parent) are handled correctly and
        don't cause infinite recursion.
        """
        gl = GroupedList([1, 2, 3])
        group = gl.create_group("group", [4, 5])

        # Try to add the parent as a child of the group (which would create a circular reference)
        with pytest.raises(ValueError):
            group.add_group(gl, "parent")

        # Try to add the group to itself (which would also create a circular reference)
        with pytest.raises(ValueError):
            group.add_group(group, "self")

    def test_extend(self) -> None:
        """Test extending a GroupedList with another iterable.

        This test verifies that the extend method correctly adds all items from another iterable to the GroupedList.
        """
        gl = GroupedList([1, 2, 3])
        gl.extend([4, 5, 6])

        assert gl.as_flat_list() == [1, 2, 3, 4, 5, 6]

        # Test extending a specific group
        group = gl.create_group("group", [7, 8])
        gl.extend([9, 10], "group")

        assert group.as_flat_list() == [7, 8, 9, 10]
        assert gl.as_flat_list() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def test_insert(self) -> None:
        """Test inserting items into a GroupedList.

        This test verifies that the insert method correctly inserts items at specific positions in the GroupedList,
        including in nested groups.
        """
        gl = GroupedList([1, 3, 4])
        gl.insert(1, 2)  # Insert 2 between 1 and 3

        assert gl.as_flat_list() == [1, 2, 3, 4]

        # Test inserting into a specific group
        group = gl.create_group("group", [5, 7])
        gl.insert(5, 6, "group")  # Insert 6 between 5 and 7 in the group

        assert group.as_flat_list() == [5, 6, 7]
        assert gl.as_flat_list() == [1, 2, 3, 4, 5, 6, 7]

    def test_slicing(self) -> None:
        """Test slicing operations on a GroupedList.

        This test verifies that slicing operations work correctly on a GroupedList, including getting, setting, and
        deleting slices.
        """
        gl = GroupedList(range(10))

        # Test getting a slice
        assert gl[2:5] == [2, 3, 4]

        # Test setting a slice
        gl[2:5] = [20, 30, 40]
        assert gl.as_flat_list() == [0, 1, 20, 30, 40, 5, 6, 7, 8, 9]

        # Test deleting a slice
        del gl[2:5]
        assert gl.as_flat_list() == [0, 1, 5, 6, 7, 8, 9]

    def test_iteration(self) -> None:
        """Test iteration over a GroupedList.

        This test verifies that a GroupedList can be iterated over correctly, yielding all items in the flat list.
        """
        gl = GroupedList([1, 2, 3])
        gl.create_group("group", [4, 5, 6])

        # Test iteration using a for loop
        items = []
        for item in gl:
            items.append(item)

        assert items == [1, 2, 3, 4, 5, 6]

        # Test iteration using list comprehension
        items = [item for item in gl]
        assert items == [1, 2, 3, 4, 5, 6]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
