#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" deepchainmap_test.py
Tests for the DeepChainMap class in the baseobjects package.
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
from collections import ChainMap
from typing import Dict, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import DeepChainMap
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestDeepChainMap(ClassTest):
    """Test the DeepChainMap class.

    This class tests the functionality of the DeepChainMap class, which is a ChainMap that updates
    and deletes items from the first mapping that contains the key.
    """

    # Attributes #
    class_: Type[DeepChainMap] = DeepChainMap

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_map(self) -> DeepChainMap:
        """Create an empty DeepChainMap for testing.

        Returns:
            An empty DeepChainMap.
        """
        return self.class_()

    @pytest.fixture
    def single_map(self) -> DeepChainMap:
        """Create a DeepChainMap with a single mapping for testing.

        Returns:
            A DeepChainMap with a single mapping.
        """
        return self.class_({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def multi_map(self) -> DeepChainMap:
        """Create a DeepChainMap with multiple mappings for testing.

        Returns:
            A DeepChainMap with multiple mappings.
        """
        return self.class_({"a": 1, "b": 2}, {"b": 20, "c": 30}, {"c": 300, "d": 400})

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of DeepChainMap can be created with various parameters.

        This test verifies that DeepChainMap instances can be created with no mappings, a single mapping,
        or multiple mappings.
        """
        # Create an empty instance
        dcm = self.class_()
        assert dcm is not None
        assert len(dcm.maps) == 1
        assert dcm.maps[0] == {}

        # Create an instance with a single mapping
        mapping = {"a": 1, "b": 2, "c": 3}
        dcm = self.class_(mapping)
        assert dcm is not None
        assert len(dcm.maps) == 1
        assert dcm.maps[0] == mapping

        # Create an instance with multiple mappings
        mapping1 = {"a": 1, "b": 2}
        mapping2 = {"b": 20, "c": 30}
        mapping3 = {"c": 300, "d": 400}
        dcm = self.class_(mapping1, mapping2, mapping3)
        assert dcm is not None
        assert len(dcm.maps) == 3
        assert dcm.maps[0] == mapping1
        assert dcm.maps[1] == mapping2
        assert dcm.maps[2] == mapping3

    def test_inheritance(self) -> None:
        """Test that DeepChainMap inherits from both BaseObject and ChainMap.

        This test verifies that DeepChainMap instances are instances of both BaseObject and ChainMap.
        """
        dcm = self.class_()
        assert isinstance(dcm, ChainMap)
        assert hasattr(dcm, "deepcopy")  # A method from BaseObject

    def test_getitem(self, multi_map: DeepChainMap) -> None:
        """Test the __getitem__ method of DeepChainMap.

        This test verifies that the __getitem__ method returns the value from the first mapping that contains the key.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        assert multi_map["a"] == 1  # From first mapping
        assert multi_map["b"] == 2  # From first mapping, not second
        assert multi_map["c"] == 30  # From second mapping, not third
        assert multi_map["d"] == 400  # From third mapping

        # Test key not found
        with pytest.raises(KeyError):
            _ = multi_map["e"]

    def test_setitem_existing_key(self, multi_map: DeepChainMap) -> None:
        """Test the __setitem__ method of DeepChainMap with an existing key.

        This test verifies that the __setitem__ method updates the value in the first mapping that contains the key.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        # Update key in first mapping
        multi_map["a"] = 10
        assert multi_map["a"] == 10
        assert multi_map.maps[0]["a"] == 10

        # Update key in second mapping
        multi_map["c"] = 300
        assert multi_map["c"] == 300
        assert "c" not in multi_map.maps[0]
        assert multi_map.maps[1]["c"] == 300
        assert multi_map.maps[2]["c"] == 300  # Unchanged in third mapping

    def test_setitem_new_key(self, multi_map: DeepChainMap) -> None:
        """Test the __setitem__ method of DeepChainMap with a new key.

        This test verifies that the __setitem__ method adds the key-value pair to the first mapping.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        multi_map["e"] = 500
        assert multi_map["e"] == 500
        assert multi_map.maps[0]["e"] == 500
        assert "e" not in multi_map.maps[1]
        assert "e" not in multi_map.maps[2]

    def test_delitem_existing_key(self, multi_map: DeepChainMap) -> None:
        """Test the __delitem__ method of DeepChainMap with an existing key.

        This test verifies that the __delitem__ method removes the key from the first mapping that contains it.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        # Delete key from first mapping
        del multi_map["a"]
        assert "a" not in multi_map.maps[0]
        with pytest.raises(KeyError):
            _ = multi_map["a"]

        # Delete key from second mapping
        del multi_map["c"]
        assert "c" not in multi_map.maps[1]
        assert multi_map["c"] == 300  # Still accessible from third mapping

    def test_delitem_nonexistent_key(self, multi_map: DeepChainMap) -> None:
        """Test the __delitem__ method of DeepChainMap with a nonexistent key.

        This test verifies that the __delitem__ method raises a KeyError when the key is not found in any mapping.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        with pytest.raises(KeyError):
            del multi_map["e"]

    def test_standard_chainmap_methods(self, multi_map: DeepChainMap) -> None:
        """Test that standard ChainMap methods work with DeepChainMap.

        This test verifies that DeepChainMap inherits and correctly implements standard ChainMap methods.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        # Test new_child
        child = multi_map.new_child({"e": 500})
        assert isinstance(child, DeepChainMap)
        assert child["e"] == 500
        assert child["a"] == 1

        # Test parents
        parents = multi_map.parents
        assert isinstance(parents, DeepChainMap)
        assert len(parents.maps) == 2
        assert parents.maps[0] == multi_map.maps[1]
        assert parents.maps[1] == multi_map.maps[2]

        # Test keys, values, items
        assert set(multi_map.keys()) == {"a", "b", "c", "d"}
        assert set(multi_map.values()) == {1, 2, 30, 400}
        assert set(multi_map.items()) == {("a", 1), ("b", 2), ("c", 30), ("d", 400)}


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
