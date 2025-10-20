"""deepchainmap_test.py
Tests for the DeepChainMap class in the baseobjects package.

This module provides tests for the DeepChainMap class, which is a ChainMap that updates and deletes items from the first
mapping that contains the key.
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
from collections import ChainMap
from typing import Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.collections import DeepChainMap
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestDeepChainMap(BaseObjectTestSuite):
    """Test the DeepChainMap class.

    This class tests the functionality of the DeepChainMap class, which is a ChainMap that updates
    and deletes items from the first mapping that contains the key.
    """

    # Attributes #
    TestClass: type[DeepChainMap] = DeepChainMap

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_map(self) -> DeepChainMap:
        """Create an empty DeepChainMap for testing.

        Returns:
            DeepChainMap: An empty DeepChainMap.
        """
        return self.TestClass()

    @pytest.fixture
    def single_map(self) -> DeepChainMap:
        """Create a DeepChainMap with a single mapping for testing.

        Returns:
            DeepChainMap: A DeepChainMap with a single mapping.
        """
        return self.TestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def multi_map(self) -> DeepChainMap:
        """Create a DeepChainMap with multiple mappings for testing.

        Returns:
            DeepChainMap: A DeepChainMap with multiple mappings.
        """
        return self.TestClass({"a": 1, "b": 2}, {"b": 20, "c": 30}, {"c": 300, "d": 400})

    @pytest.fixture
    def test_object(self) -> DeepChainMap:
        """Create a test object for testing.

        Returns:
            DeepChainMap: A DeepChainMap with multiple mappings.
        """
        return self.TestClass({"a": 1, "b": 2}, {"c": 3, "d": 4})

    # Tests
    def test_copy(self, test_object: DeepChainMap) -> None:
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
        assert len(obj_copy.maps) == len(test_object.maps)

        # Check that the maps are the same objects (shallow copy)
        for i, m in enumerate(obj_copy.maps):
            assert m == test_object.maps[i]
            assert id(m) == id(test_object.maps[i])  # Same objects in shallow copy

    def test_copy_method(self, test_object: DeepChainMap) -> None:
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
        assert len(obj_copy.maps) == len(test_object.maps)

        # Check that the maps are the same objects (shallow copy)
        for i, m in enumerate(obj_copy.maps):
            assert m == test_object.maps[i]
            assert id(m) == id(test_object.maps[i])  # Same objects in shallow copy

    def test_deepcopy(self, test_object: DeepChainMap, memo: dict | None = None) -> None:
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
        assert len(obj_deepcopy.maps) == len(test_object.maps)

        # Check that the maps are the same but not the same objects
        for i, m in enumerate(obj_deepcopy.maps):
            assert m == test_object.maps[i]
            assert id(m) != id(test_object.maps[i])  # Different objects

    def test_deepcopy_method(self, test_object: DeepChainMap, memo: dict | None = None) -> None:
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
        assert len(obj_deepcopy.maps) == len(test_object.maps)

        # Check that the maps are the same but not the same objects
        for i, m in enumerate(obj_deepcopy.maps):
            assert m == test_object.maps[i]
            assert id(m) != id(test_object.maps[i])  # Different objects

    def test_pickling(self, test_object: DeepChainMap) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify the test object
        test_object["new_key"] = "new_value"

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)
        assert len(unpickled.maps) == len(test_object.maps)

        # Check that the maps are the same
        for i, m in enumerate(unpickled.maps):
            assert m == test_object.maps[i]

        # Check that the values are accessible
        assert unpickled["a"] == 1
        assert unpickled["b"] == 2
        assert unpickled["c"] == 3
        assert unpickled["d"] == 4
        assert unpickled["new_key"] == "new_value"

    def test_inheritance(self) -> None:
        """Test that DeepChainMap inherits from both BaseObject and ChainMap.

        This test verifies that DeepChainMap instances are instances of both BaseObject and ChainMap.
        """
        dcm = self.TestClass()
        assert isinstance(dcm, ChainMap)
        assert hasattr(dcm, "deepcopy")  # A method from BaseObject

    def test_instance_creation(self) -> None:
        """Test that instances of DeepChainMap can be created with various parameters.

        This test verifies that DeepChainMap instances can be created with no mappings, a single mapping,
        or multiple mappings.
        """
        # Create an empty instance
        dcm = self.TestClass()
        assert dcm is not None
        assert len(dcm.maps) == 1
        assert dcm.maps[0] == {}

        # Create an instance with a single mapping
        mapping = {"a": 1, "b": 2, "c": 3}
        dcm = self.TestClass(mapping)
        assert dcm is not None
        assert len(dcm.maps) == 1
        assert dcm.maps[0] == mapping

        # Create an instance with multiple mappings
        mapping1 = {"a": 1, "b": 2}
        mapping2 = {"b": 20, "c": 30}
        mapping3 = {"c": 300, "d": 400}
        dcm = self.TestClass(mapping1, mapping2, mapping3)
        assert dcm is not None
        assert len(dcm.maps) == 3
        assert dcm.maps[0] == mapping1
        assert dcm.maps[1] == mapping2
        assert dcm.maps[2] == mapping3

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

    def test_nested_maps(self) -> None:
        """Test DeepChainMap with nested dictionaries.

        This test verifies that DeepChainMap works correctly with nested dictionaries.
        """
        # Create a DeepChainMap with nested dictionaries
        nested_map = self.TestClass({"a": {"x": 1, "y": 2}}, {"b": {"z": 3}}, {"a": {"w": 4}})

        # Test accessing nested values
        assert nested_map["a"] == {"x": 1, "y": 2}  # From first mapping
        assert nested_map["b"] == {"z": 3}  # From second mapping

        # Test updating nested values
        nested_map["a"]["x"] = 10
        assert nested_map["a"]["x"] == 10
        assert nested_map.maps[0]["a"]["x"] == 10

        # Test adding new nested values
        nested_map["a"]["v"] = 5
        assert nested_map["a"]["v"] == 5
        assert nested_map.maps[0]["a"]["v"] == 5

    def test_empty_maps(self) -> None:
        """Test DeepChainMap with empty mappings.

        This test verifies that DeepChainMap works correctly with empty mappings.
        """
        # Create a DeepChainMap with empty mappings
        empty_maps = self.TestClass({}, {}, {})

        # Test adding values
        empty_maps["a"] = 1
        assert empty_maps["a"] == 1
        assert empty_maps.maps[0]["a"] == 1

        # Test that other maps remain empty
        assert empty_maps.maps[1] == {}
        assert empty_maps.maps[2] == {}

    def test_update_method(self, multi_map: DeepChainMap) -> None:
        """Test the update method of DeepChainMap.

        This test verifies that the update method updates existing keys in the appropriate mappings
        and adds new keys to the first mapping.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        # Update with a dictionary containing existing and new keys
        multi_map.update({"a": 100, "c": 300, "e": 500})

        # Check existing keys were updated in the appropriate mappings
        assert multi_map["a"] == 100
        assert multi_map.maps[0]["a"] == 100

        assert multi_map["c"] == 300
        assert "c" not in multi_map.maps[0]
        assert multi_map.maps[1]["c"] == 300

        # Check new keys were added to the first mapping
        assert multi_map["e"] == 500
        assert multi_map.maps[0]["e"] == 500
        assert "e" not in multi_map.maps[1]
        assert "e" not in multi_map.maps[2]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
