#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basedict_test.py
Tests for the BaseDict class in the baseobjects package.
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
from src.baseobjects.bases.collections import BaseDict
from .base_test import BaseBaseObjectTest


# Classes #
class TestBaseDict(BaseBaseObjectTest):
    """Test the BaseDict class.

    This class tests the functionality of the BaseDict class, which is a mixin of UserDict and BaseObject.
    It creates a test subclass of BaseDict to test with.
    """

    # Class Definitions #
    class BaseTestDict(BaseDict):
        """A subclass of BaseDict for testing purposes."""

    class NormalDict(dict):
        """A normal Python dictionary for comparison with BaseDict."""

    # Attributes #
    class_: Type[BaseTestDict] = BaseTestDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dict(self) -> "TestBaseDict.BaseTestDict":
        """Create a test dictionary instance for use in tests.

        Returns:
            BaseTestDict: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def populated_test_dict(self) -> "TestBaseDict.BaseTestDict":
        """Create a populated test dictionary for use in tests.

        Returns:
            BaseTestDict: A populated instance of the test class.
        """
        return self.class_({f"key{i}": f"value{i}" for i in range(5)})

    # Tests
    def test_instance_creation(self, test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test that instances of BaseTestDict can be created.

        Args:
            test_dict: A fixture providing a BaseTestDict instance.
        """
        assert test_dict is not None

    def test_copy(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test the copy method of BaseDict.

        This test verifies that the copy method creates a new dictionary with references to the same items
        (shallow copy).

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
        """
        new: "TestBaseDict.BaseTestDict" = populated_test_dict.copy()
        assert id(new) != id(populated_test_dict)
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            assert id(new[key]) == id(populated_test_dict[key])

    def test_deepcopy(self, populated_test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test the deepcopy method of BaseDict.

        This test verifies that the deepcopy method creates a new dictionary with new copies of mutable values
        but references to the same immutable values.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
        """
        new: "TestBaseDict.BaseTestDict" = populated_test_dict.deepcopy()
        assert id(new) != id(populated_test_dict)
        assert len(new) == len(populated_test_dict)
        for key in new:
            assert key in populated_test_dict
            assert new[key] == populated_test_dict[key]
            # Since our test values are strings (immutable), the ids should be the same
            assert id(new[key]) == id(populated_test_dict[key])

    def test_dict_operations(self, test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test basic dictionary operations on BaseDict.

        This test verifies that BaseDict supports standard dictionary operations like setting items,
        getting items, etc.

        Args:
            test_dict: A fixture providing a BaseTestDict instance.
        """
        # Test setting items
        test_dict["key1"] = "value1"
        assert len(test_dict) == 1
        assert test_dict["key1"] == "value1"

        # Test updating
        test_dict.update({"key2": "value2", "key3": "value3"})
        assert len(test_dict) == 3
        assert test_dict["key2"] == "value2"
        assert test_dict["key3"] == "value3"

        # Test get
        assert test_dict.get("key1") == "value1"
        assert test_dict.get("nonexistent", "default") == "default"

        # Test pop
        popped = test_dict.pop("key2")
        assert popped == "value2"
        assert len(test_dict) == 2
        assert "key2" not in test_dict

        # Test popitem
        key, value = test_dict.popitem()
        assert len(test_dict) == 1
        assert key in ["key1", "key3"]
        assert value == f"value{key[-1]}"

        # Test clear
        test_dict.clear()
        assert len(test_dict) == 0


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])