"""basedicttestsuite.py
Base class for test suites which test BaseDict and its subclasses.

This module provides a base test suite for testing the BaseDict class and its subclasses. It includes tests for
dictionary operations, copying, and pickling.
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
from ...bases import BaseDict
from .baseobjecttestsuite import BaseObjectTestSuite


# Definitions #
# Classes #
class BaseDictTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test BaseDict and its subclasses.

    This class provides common functionality for test suites that test dictionary objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseDict or a subclass.
    """

    # Attributes #
    UnitTestClass: type[BaseDict]

    # Fixtures #
    @pytest.fixture
    def populated_test_dict(self) -> BaseDict:
        """Creates a populated test dictionary for use in tests.

        Returns:
            BaseDict: A populated instance of the test class.
        """
        # Creates a dictionary with some initial data
        data = {f"key{i}": f"value{i}" for i in range(5)}
        return self.UnitTestClass(data)

    # Tests #
    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Creates Object
        obj = self.UnitTestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.UnitTestClass)
        assert isinstance(obj, BaseDict)
        # Checks if it behaves like a dict
        assert hasattr(obj, "data")
        assert isinstance(obj.data, dict)

    # Copying #
    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_copy_operations(self, populated_test_dict: BaseDict, method: str) -> None:  # type: ignore[override]
        """Tests the copy behavior of BaseDict.

        This test verifies that the copy method creates a new dictionary with references to the same items
        (shallow copy).

        Args:
            populated_test_dict: A fixture providing a populated BaseDict instance.
            method: The method to use for copying ('copy' or 'method').
        """
        # Copy Object
        if method == "copy":
            new = copy.copy(populated_test_dict)
        else:
            new = populated_test_dict.copy()

        # Validate
        assert id(new) != id(populated_test_dict)
        assert isinstance(new, type(populated_test_dict))
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            assert id(new[key]) == id(populated_test_dict[key])

    @pytest.mark.parametrize("method", ["copy", "method"])
    def test_deepcopy_operations(
        self,
        populated_test_dict: BaseDict,
        method: str,
        memo: dict[Any, Any] | None = None,
    ) -> None:
        """Tests the deepcopy behavior of BaseDict.

        This test verifies that the deepcopy method creates a new dictionary with new copies of mutable values
        but references to the same immutable values.

        Args:
            populated_test_dict: A fixture providing a populated BaseDict instance.
            method: The method to use for deep copying ('copy' or 'method').
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if method == "copy":
            new = copy.deepcopy(populated_test_dict, memo=memo)
        else:
            new = populated_test_dict.deepcopy(memo=memo)

        # Validate
        assert id(new) != id(populated_test_dict)
        assert isinstance(new, type(populated_test_dict))
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[key]) == id(populated_test_dict[key])

    # Pickling #
    def test_pickling(self, populated_test_dict: BaseDict) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            populated_test_dict: A fixture providing a populated BaseDict instance.
        """
        # Pickle and Unpickle Object
        pickled = pickle.dumps(populated_test_dict)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not populated_test_dict
        assert isinstance(unpickled, type(populated_test_dict))
        assert len(unpickled) == len(populated_test_dict)
        for key in unpickled:
            assert key in populated_test_dict
            assert unpickled[key] == populated_test_dict[key]

    # Functionality #
    def test_dict_set_item(self, test_object: BaseDict) -> None:
        """Tests setting items in BaseDict.

        This test verifies that BaseDict supports setting items using bracket notation.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object["key1"] = "value1"
        assert len(test_object) == 1
        assert test_object["key1"] == "value1"

    def test_dict_update(self, test_object: BaseDict) -> None:
        """Tests updating BaseDict with multiple items.

        This test verifies that BaseDict supports the update method to add multiple items.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object.update({"key2": "value2", "key3": "value3"})
        assert len(test_object) == 2
        assert test_object["key2"] == "value2"
        assert test_object["key3"] == "value3"

    def test_dict_get(self, test_object: BaseDict) -> None:
        """Tests getting items from BaseDict.

        This test verifies that BaseDict supports the get method with default values.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object["key1"] = "value1"
        assert test_object.get("key1") == "value1"
        assert test_object.get("nonexistent", "default") == "default"

    def test_dict_pop(self, test_object: BaseDict) -> None:
        """Tests popping items from BaseDict.

        This test verifies that BaseDict supports the pop method to remove and return items.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object["key1"] = "value1"
        test_object["key2"] = "value2"

        popped = test_object.pop("key2")
        assert popped == "value2"
        assert len(test_object) == 1
        assert "key2" not in test_object

    def test_dict_popitem(self, test_object: BaseDict) -> None:
        """Tests popping an arbitrary item from BaseDict.

        This test verifies that BaseDict supports the popitem method.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object["key1"] = "value1"
        test_object["key3"] = "value3"

        key, value = test_object.popitem()
        assert len(test_object) == 1
        assert key in ["key1", "key3"]
        assert value == f"value{key[-1]}"

    def test_dict_clear(self, test_object: BaseDict) -> None:
        """Tests clearing BaseDict.

        This test verifies that BaseDict supports the clear method to remove all items.

        Args:
            test_object: A fixture providing a BaseDict instance.
        """
        test_object["key1"] = "value1"
        test_object["key2"] = "value2"

        test_object.clear()
        assert len(test_object) == 0

    def test_dict_initialization(self) -> None:
        """Tests initialization of BaseDict with a dictionary."""
        # Initializes with a dictionary
        init_dict = {"key1": "value1", "key2": "value2"}
        test_dict = self.UnitTestClass(init_dict)

        # Validate
        assert len(test_dict) == 2
        assert test_dict["key1"] == "value1"
        assert test_dict["key2"] == "value2"

    def test_dict_initialization_with_kwargs(self) -> None:
        """Tests initialization of BaseDict with keyword arguments."""
        # Initializes with keyword arguments
        test_dict = self.UnitTestClass(key1="value1", key2="value2")

        # Validate
        assert len(test_dict) == 2
        assert test_dict["key1"] == "value1"
        assert test_dict["key2"] == "value2"

    def test_dict_iteration(self, populated_test_dict: BaseDict) -> None:
        """Tests iteration over BaseDict.

        Args:
            populated_test_dict: A fixture providing a populated BaseDict instance.
        """
        # Test keys
        keys = list(populated_test_dict.keys())
        assert len(keys) == 5
        for i in range(5):
            assert f"key{i}" in keys

        # Test values
        values = list(populated_test_dict.values())
        assert len(values) == 5
        for i in range(5):
            assert f"value{i}" in values

        # Test items
        items = list(populated_test_dict.items())
        assert len(items) == 5
        for i in range(5):
            assert (f"key{i}", f"value{i}") in items
