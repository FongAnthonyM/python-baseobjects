"""baselisttestsuite.py
Base class for test suites which test BaseList and its subclasses.

This module provides a base test suite for testing the BaseList class and its subclasses. It includes tests for list
operations, copying, and pickling.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseList
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseListTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test BaseList and its subclasses.

    This class provides common functionality for test suites that test list objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseList or a subclass.
    """

    UnitTestClass: ClassVar[type[BaseList]]

    # Fixtures #
    @pytest.fixture
    def populated_test_list(self) -> BaseList:
        """Creates a populated test list for use in tests.

        Returns:
            BaseList: A populated instance of the test class.
        """
        result = self.UnitTestClass()
        result.extend([f"value{i}" for i in range(5)])
        return result

    # Tests #
    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.UnitTestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.UnitTestClass)
        assert isinstance(obj, BaseList)
        # Check if it behaves like a list
        assert hasattr(obj, "data")
        assert isinstance(obj.data, list)

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, populated_test_list: BaseList, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of BaseList.

        This test verifies that the copy method creates a new list with references to the same items
        (shallow copy).

        Args:
            populated_test_list: A fixture providing a populated BaseList instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            new = copy.copy(populated_test_list)
        else:
            new = populated_test_list.copy()

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            assert id(new[i]) == id(populated_test_list[i])

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        populated_test_list: BaseList,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deepcopy behavior of BaseList.

        This test verifies that the deepcopy method creates a new list with new copies of mutable items
        but references to the same immutable items.

        Args:
            populated_test_list: A fixture providing a populated BaseList instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            new = copy.deepcopy(populated_test_list, memo=memo)
        else:
            new = populated_test_list.deepcopy(memo=memo)

        # Validate
        assert id(new) != id(populated_test_list)
        assert isinstance(new, type(populated_test_list))
        assert len(new) == len(populated_test_list)
        for i in range(len(new)):
            assert new[i] == populated_test_list[i]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[i]) == id(populated_test_list[i])

    # Pickling #
    def test_pickling(self, populated_test_list: BaseList) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            populated_test_list: A fixture providing a populated BaseList instance.
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

    # Functionality #
    def test_list_initialization(self) -> None:
        """Tests initialization of BaseList with a list."""
        # Initialize with a list
        init_list = ["item1", "item2", "item3"]
        test_list = self.UnitTestClass(init_list)

        # Validate
        assert len(test_list) == 3
        assert test_list[0] == "item1"
        assert test_list[1] == "item2"
        assert test_list[2] == "item3"

    def test_append(self, test_object: BaseList) -> None:
        """Tests the append operation on BaseList.

        This test verifies that BaseList supports the append operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.append("item1")
        assert len(test_object) == 1
        assert test_object[0] == "item1"

    def test_extend(self, test_object: BaseList) -> None:
        """Tests the extend operation on BaseList.

        This test verifies that BaseList supports the extend operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.append("item1")
        test_object.extend(["item2", "item3"])
        assert len(test_object) == 3
        assert test_object[0] == "item1"
        assert test_object[1] == "item2"
        assert test_object[2] == "item3"

    def test_insert(self, test_object: BaseList) -> None:
        """Tests the insert operation on BaseList.

        This test verifies that BaseList supports the insert operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.extend(["item1", "item2", "item3"])
        test_object.insert(1, "inserted")
        assert len(test_object) == 4
        assert test_object[1] == "inserted"

    def test_remove(self, test_object: BaseList) -> None:
        """Tests the remove operation on BaseList.

        This test verifies that BaseList supports the remove operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.extend(["item1", "inserted", "item2"])
        test_object.remove("inserted")
        assert len(test_object) == 2
        assert "inserted" not in test_object

    def test_pop(self, test_object: BaseList) -> None:
        """Tests the pop operation on BaseList.

        This test verifies that BaseList supports the pop operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.extend(["item1", "item2", "item3"])
        popped = test_object.pop()
        assert popped == "item3"
        assert len(test_object) == 2

    def test_clear(self, test_object: BaseList) -> None:
        """Tests the clear operation on BaseList.

        This test verifies that BaseList supports the clear operation correctly.

        Args:
            test_object: A fixture providing a BaseList instance.
        """
        test_object.extend(["item1", "item2"])
        test_object.clear()
        assert len(test_object) == 0

    @pytest.mark.parametrize(
        ("index", "expected"),
        [
            # Test positive indexing
            (0, "value0"),
            (4, "value4"),
            # Test negative indexing
            (-1, "value4"),
            (-5, "value0"),
            # Test slicing
            (slice(1, 3), ["value1", "value2"]),
            (slice(None, None, 2), ["value0", "value2", "value4"]),
            (slice(None, None, -1), ["value4", "value3", "value2", "value1", "value0"]),
        ],
    )
    def test_list_indexing(self, populated_test_list: BaseList, index: int | slice, expected: str | list[str]) -> None:
        """Tests indexing operations on BaseList.

        Args:
            populated_test_list: A fixture providing a populated BaseList instance.
            index: The index or slice to test.
            expected: The expected value at that index/slice.
        """
        assert populated_test_list[index] == expected

    def test_empty_list(self) -> None:
        """Tests empty BaseList."""
        empty_list = self.UnitTestClass()
        assert len(empty_list) == 0

    def test_single_item_list(self) -> None:
        """Tests BaseList with one item."""
        single_item_list = self.UnitTestClass(["single"])
        assert len(single_item_list) == 1
        assert single_item_list[0] == "single"

    def test_nested_lists(self) -> None:
        """Tests BaseList with nested lists."""
        nested_list = self.UnitTestClass([["nested1"], ["nested2"]])
        assert len(nested_list) == 2
        assert nested_list[0] == ["nested1"]
        assert nested_list[1] == ["nested2"]

    def test_mixed_types_list(self) -> None:
        """Tests BaseList with different types."""
        mixed_list = self.UnitTestClass([1, "string", 3.14, None, True])
        assert len(mixed_list) == 5
        assert mixed_list[0] == 1
        assert mixed_list[1] == "string"
        assert mixed_list[2] == 3.14
        assert mixed_list[3] is None
        assert mixed_list[4] is True
