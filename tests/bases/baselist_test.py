#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baselist_test.py
Tests for the BaseList class in the baseobjects package.
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
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases.collections import BaseList
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseList(BaseBaseObjectTest):
    """Test the BaseList class.

    This class tests the functionality of the BaseList class, which is a mixin of UserList and BaseObject.
    It creates a test subclass of BaseList to test with.
    """

    # Class Definitions #
    class BaseTestList(BaseList):
        """A subclass of BaseList for testing purposes."""

    class NormalList(list):
        """A normal Python list for comparison with BaseList."""

    # Attributes #
    class_: Type[BaseTestList] = BaseTestList

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_list(self) -> "TestBaseList.BaseTestList":
        """Create a test list instance for use in tests.

        Returns:
            BaseTestList: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def populated_test_list(self) -> "TestBaseList.BaseTestList":
        """Create a populated test list for use in tests.

        Returns:
            BaseTestList: A populated instance of the test class.
        """
        result = self.class_()
        result.extend([f"value{i}" for i in range(5)])
        return result

    # Tests
    def test_instance_creation(self, test_list: "TestBaseList.BaseTestList") -> None:
        """Test that instances of BaseTestList can be created.

        Args:
            test_list: A fixture providing a BaseTestList instance.
        """
        assert test_list is not None

    def test_copy(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test the copy method of BaseList.

        This test verifies that the copy method creates a new list with references to the same items
        (shallow copy).

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        new: "TestBaseList.BaseTestList" = populated_test_list.copy()
        assert id(new) != id(populated_test_list)
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            assert id(new[i]) == id(populated_test_list[i])

    def test_deepcopy(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test the deepcopy method of BaseList.

        This test verifies that the deepcopy method creates a new list with new copies of mutable items
        but references to the same immutable items.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        new: "TestBaseList.BaseTestList" = populated_test_list.deepcopy()
        assert id(new) != id(populated_test_list)
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[i]) == id(populated_test_list[i])

    def test_list_operations(self, test_list: "TestBaseList.BaseTestList") -> None:
        """Test basic list operations on BaseList.

        This test verifies that BaseList supports standard list operations like append, extend, etc.

        Args:
            test_list: A fixture providing a BaseTestList instance.
        """
        # Test append
        test_list.append("item1")
        assert len(test_list) == 1
        assert test_list[0] == "item1"

        # Test extend
        test_list.extend(["item2", "item3"])
        assert len(test_list) == 3
        assert test_list[1] == "item2"
        assert test_list[2] == "item3"

        # Test insert
        test_list.insert(1, "inserted")
        assert len(test_list) == 4
        assert test_list[1] == "inserted"

        # Test remove
        test_list.remove("inserted")
        assert len(test_list) == 3
        assert "inserted" not in test_list

        # Test pop
        popped = test_list.pop()
        assert popped == "item3"
        assert len(test_list) == 2

        # Test clear
        test_list.clear()
        assert len(test_list) == 0


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])