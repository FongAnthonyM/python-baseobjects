"""baselist_test.py
Tests for the BaseList class in the baseobjects package.

This module contains tests for the BaseList class, which is an abstract base class that inherits from both BaseObject
and UserList. It combines the list-like behavior of UserList with the enhanced functionality of BaseObject,
such as proper copying and deep copying support.
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
from src.baseobjects.bases.collections import BaseList
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Classes #
class BaseTestList(BaseList):
    """A subclass of BaseList for testing purposes."""


# Tests #
class TestBaseList(BaseObjectTestSuite):
    """Test the BaseList class.

    This class tests the functionality of the BaseList class, which is a mixin of UserList and BaseObject.
    It creates a test subclass of BaseList to test with.
    """

    # Attributes #
    TestClass: type[BaseList] = BaseTestList

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseList.BaseTestList":
        """Create a test list instance for use in tests.

        Returns:
            BaseTestList: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def populated_test_list(self) -> "TestBaseList.BaseTestList":
        """Create a populated test list for use in tests.

        Returns:
            BaseTestList: A populated instance of the test class.
        """
        result = self.TestClass()
        result.extend([f"value{i}" for i in range(5)])
        return result

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of BaseTestList can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, BaseList)
        assert isinstance(obj.data, list)

    def test_copy(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test the copy behavior of BaseList.

        This test verifies that the copy method creates a new list with references to the same items
        (shallow copy).

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        # Copy Object
        new = copy.copy(populated_test_list)

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            assert id(new[i]) == id(populated_test_list[i])

    def test_copy_method(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test the copy method of BaseList.

        This test verifies that the copy method creates a new list with references to the same items
        (shallow copy).

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        # Copy Object
        new = populated_test_list.copy()

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            assert id(new[i]) == id(populated_test_list[i])

    def test_deepcopy(self, populated_test_list: "TestBaseList.BaseTestList", memo: dict | None = None) -> None:
        """Test the deepcopy behavior of BaseList.

        This test verifies that the deepcopy method creates a new list with new copies of mutable items
        but references to the same immutable items.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = copy.deepcopy(populated_test_list, memo=memo)

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[i]) == id(populated_test_list[i])

    def test_deepcopy_method(self, populated_test_list: "TestBaseList.BaseTestList", memo: dict | None = None) -> None:
        """Test the deepcopy method of BaseList.

        This test verifies that the deepcopy method creates a new list with new copies of mutable items
        but references to the same immutable items.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = populated_test_list.deepcopy(memo=memo)

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[i]) == id(populated_test_list[i])

    def test_pickling(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(populated_test_list)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not populated_test_list
        assert isinstance(unpickled, type(populated_test_list))
        assert len(unpickled) == len(populated_test_list)
        for i in range(len(unpickled)):
            assert unpickled[i] == populated_test_list[i]

    def test_list_operations(self, test_object: "TestBaseList.BaseTestList") -> None:
        """Test basic list operations on BaseList.

        This test verifies that BaseList supports standard list operations like append, extend, etc.

        Args:
            test_object: A fixture providing a BaseTestList instance.
        """
        # Test append
        test_object.append("item1")
        assert len(test_object) == 1
        assert test_object[0] == "item1"

        # Test extend
        test_object.extend(["item2", "item3"])
        assert len(test_object) == 3
        assert test_object[1] == "item2"
        assert test_object[2] == "item3"

        # Test insert
        test_object.insert(1, "inserted")
        assert len(test_object) == 4
        assert test_object[1] == "inserted"

        # Test remove
        test_object.remove("inserted")
        assert len(test_object) == 3
        assert "inserted" not in test_object

        # Test pop
        popped = test_object.pop()
        assert popped == "item3"
        assert len(test_object) == 2

        # Test clear
        test_object.clear()
        assert len(test_object) == 0

    def test_list_initialization(self) -> None:
        """Test initialization of BaseList with a list."""
        # Initialize with a list
        init_list = ["item1", "item2", "item3"]
        test_list = self.TestClass(init_list)

        # Validate
        assert len(test_list) == 3
        assert test_list[0] == "item1"
        assert test_list[1] == "item2"
        assert test_list[2] == "item3"

    def test_list_indexing(self, populated_test_list: "TestBaseList.BaseTestList") -> None:
        """Test indexing operations on BaseList.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
        """
        # Test positive indexing
        assert populated_test_list[0] == "value0"
        assert populated_test_list[4] == "value4"

        # Test negative indexing
        assert populated_test_list[-1] == "value4"
        assert populated_test_list[-5] == "value0"

        # Test slicing
        assert populated_test_list[1:3] == ["value1", "value2"]
        assert populated_test_list[::2] == ["value0", "value2", "value4"]
        assert populated_test_list[::-1] == ["value4", "value3", "value2", "value1", "value0"]

    def test_list_s(self) -> None:
        """Test edge cases for BaseList."""
        # Test empty list
        empty_list = self.TestClass()
        assert len(empty_list) == 0

        # Test list with one item
        single_item_list = self.TestClass(["single"])
        assert len(single_item_list) == 1
        assert single_item_list[0] == "single"

        # Test nested lists
        nested_list = self.TestClass([["nested1"], ["nested2"]])
        assert len(nested_list) == 2
        assert nested_list[0] == ["nested1"]
        assert nested_list[1] == ["nested2"]

        # Test list with different types
        mixed_list = self.TestClass([1, "string", 3.14, None, True])
        assert len(mixed_list) == 5
        assert mixed_list[0] == 1
        assert mixed_list[1] == "string"
        assert mixed_list[2] == 3.14
        assert mixed_list[3] is None
        assert mixed_list[4] is True


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
