"""basedict_test.py
Tests for the BaseDict class in the baseobjects package.

This module contains tests for the BaseDict class, which is an abstract base class that inherits from both BaseObject
and UserDict. It combines the dictionary-like behavior of UserDict with the enhanced functionality of BaseObject,
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
from src.baseobjects.bases.collections import BaseDict
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Classes #
class TestBaseDict(BaseObjectTestSuite):
    """Test the BaseDict class.

    This class tests the functionality of the BaseDict class, which is a mixin of UserDict and BaseObject.
    It creates a test subclass of BaseDict to test with.
    """

    # Class Definitions #
    class BaseTestDict(BaseDict):
        """A subclass of BaseDict for testing purposes."""

    # Attributes #
    TestClass: Type[BaseDict] = BaseTestDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseDict.BaseTestDict":
        """Create a test dictionary instance for use in tests.

        Returns:
            BaseTestDict: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def populated_test_dict(self) -> "TestBaseDict.BaseTestDict":
        """Create a populated test dictionary for use in tests.

        Returns:
            BaseTestDict: A populated instance of the test class.
        """
        return self.TestClass({f"key{i}": f"value{i}" for i in range(5)})

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of BaseTestDict can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create Object
        obj = self.TestClass(*args, **kwargs)

        # Validate
        assert isinstance(obj, self.TestClass)
        assert isinstance(obj, BaseDict)
        assert isinstance(obj.data, dict)

    def test_copy(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test the copy behavior of BaseDict.

        This test verifies that the copy method creates a new dictionary with references to the same items
        (shallow copy).

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
        """
        # Copy Object
        new = copy.copy(populated_test_dict)

        # Validate
        assert id(new) != id(populated_test_dict)
        assert isinstance(new, type(populated_test_dict))
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            assert id(new[key]) == id(populated_test_dict[key])

    def test_copy_method(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test the copy method of BaseDict.

        This test verifies that the copy method creates a new dictionary with references to the same items
        (shallow copy).

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
        """
        # Copy Object
        new = populated_test_dict.copy()

        # Validate
        assert id(new) != id(populated_test_dict)
        assert isinstance(new, type(populated_test_dict))
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            assert id(new[key]) == id(populated_test_dict[key])

    def test_deepcopy(self, populated_test_dict: "TestBaseDict.BaseTestDict", memo: dict | None = None) -> None:
        """Test the deepcopy behavior of BaseDict.

        This test verifies that the deepcopy method creates a new dictionary with new copies of mutable values
        but references to the same immutable values.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
        new = copy.deepcopy(populated_test_dict, memo=memo)

        # Validate
        assert id(new) != id(populated_test_dict)
        assert isinstance(new, type(populated_test_dict))
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[key]) == id(populated_test_dict[key])

    def test_deepcopy_method(self, populated_test_dict: "TestBaseDict.BaseTestDict", memo: dict | None = None) -> None:
        """Test the deepcopy method of BaseDict.

        This test verifies that the deepcopy method creates a new dictionary with new copies of mutable values
        but references to the same immutable values.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}
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

    def test_pickling(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
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

    def test_dict_operations(self, test_object: "TestBaseDict.BaseTestDict") -> None:
        """Test basic dictionary operations on BaseDict.

        This test verifies that BaseDict supports standard dictionary operations like setting items,
        getting items, etc.

        Args:
            test_object: A fixture providing a BaseTestDict instance.
        """
        # Test setting items
        test_object["key1"] = "value1"
        assert len(test_object) == 1
        assert test_object["key1"] == "value1"

        # Test updating
        test_object.update({"key2": "value2", "key3": "value3"})
        assert len(test_object) == 3
        assert test_object["key2"] == "value2"
        assert test_object["key3"] == "value3"

        # Test get
        assert test_object.get("key1") == "value1"
        assert test_object.get("nonexistent", "default") == "default"

        # Test pop
        popped = test_object.pop("key2")
        assert popped == "value2"
        assert len(test_object) == 2
        assert "key2" not in test_object

        # Test popitem
        key, value = test_object.popitem()
        assert len(test_object) == 1
        assert key in ["key1", "key3"]
        assert value == f"value{key[-1]}"

        # Test clear
        test_object.clear()
        assert len(test_object) == 0

    def test_dict_initialization(self) -> None:
        """Test initialization of BaseDict with a dictionary."""
        # Initialize with a dictionary
        init_dict = {"key1": "value1", "key2": "value2"}
        test_dict = self.TestClass(init_dict)

        # Validate
        assert len(test_dict) == 2
        assert test_dict["key1"] == "value1"
        assert test_dict["key2"] == "value2"

    def test_dict_initialization_with_kwargs(self) -> None:
        """Test initialization of BaseDict with keyword arguments."""
        # Initialize with keyword arguments
        test_dict = self.TestClass(key1="value1", key2="value2")

        # Validate
        assert len(test_dict) == 2
        assert test_dict["key1"] == "value1"
        assert test_dict["key2"] == "value2"

    def test_dict_iteration(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test iteration over BaseDict.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
