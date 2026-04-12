"""deepchainmaptestsuite.py
Base class for test suites which test DeepChainMap and its subclasses.

This module contains the base class for test suites which test DeepChainMap and its subclasses.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...collections import DeepChainMap
from ..bases import BaseObjectTestSuite


# Definitions #
# Classes #
class DeepChainMapTestSuite(BaseObjectTestSuite):
    """Base class for test suites which test DeepChainMap.

    This class provides common functionality for test suites that test DeepChainMap objects.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be DeepChainMap or a subclass.
    """

    UnitTestClass: type[DeepChainMap] = DeepChainMap

    # Fixtures #
    @pytest.fixture
    def empty_map(self) -> DeepChainMap:
        """Creates an empty DeepChainMap for testing.

        Returns:
            DeepChainMap: An empty DeepChainMap.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def single_map(self) -> DeepChainMap:
        """Creates a DeepChainMap with a single mapping for testing.

        Returns:
            DeepChainMap: A DeepChainMap with a single mapping.
        """
        return self.UnitTestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def multi_map(self) -> DeepChainMap:
        """Creates a DeepChainMap with multiple mappings for testing.

        Returns:
            DeepChainMap: A DeepChainMap with multiple mappings.
        """
        return self.UnitTestClass({"a": 1, "b": 2}, {"b": 20, "c": 30}, {"c": 300, "d": 400})

    @pytest.fixture
    def test_object(self) -> DeepChainMap:
        """Creates a test object for testing.

        Returns:
            DeepChainMap: A DeepChainMap with multiple mappings.
        """
        return self.UnitTestClass({"a": 1, "b": 2}, {"c": 3, "d": 4})

    # Magic Methods #
    @pytest.mark.parametrize(("key", "expected"), [("a", 1), ("b", 2), ("c", 30), ("d", 400)])
    def test_getitem(self, multi_map: DeepChainMap, key: str, expected: Any) -> None:
        """Tests the __getitem__ method of DeepChainMap.

        This test verifies that the __getitem__ method returns the value from the first mapping that contains the key.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
            key: The key to look up.
            expected: The expected value.
        """
        assert multi_map[key] == expected

    @pytest.mark.parametrize(("key", "value", "map_idx"), [("a", 10, 0), ("c", 300, 1), ("e", 500, 0)])
    def test_setitem(self, multi_map: DeepChainMap, key: str, value: Any, map_idx: int) -> None:
        """Tests the __setitem__ method of DeepChainMap.

        This test verifies that the __setitem__ method updates or adds the key-value pair to the appropriate mapping.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
            key: The key to set.
            value: The value to set.
            map_idx: The index of the map where the value should be set.
        """
        multi_map[key] = value
        assert multi_map[key] == value
        assert multi_map.maps[map_idx][key] == value

    @pytest.mark.parametrize(("key", "map_idx", "still_exists"), [("a", 0, False), ("c", 1, True)])
    def test_delitem(self, multi_map: DeepChainMap, key: str, map_idx: int, still_exists: bool) -> None:
        """Tests the __delitem__ method of DeepChainMap.

        This test verifies that the __delitem__ method removes the key from the first mapping that contains it.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
            key: The key to delete.
            map_idx: The index of the map from which the key should be deleted.
            still_exists: Whether the key should still exist in the chain (in another map).
        """
        del multi_map[key]
        assert key not in multi_map.maps[map_idx]
        if still_exists:
            assert key in multi_map
        else:
            with pytest.raises(KeyError):
                _ = multi_map[key]

    # Tests #
    # Instantiation #
    @pytest.mark.parametrize(
        "mappings",
        [
            (),
            ({"a": 1, "b": 2, "c": 3},),
            ({"a": 1, "b": 2}, {"b": 20, "c": 30}, {"c": 300, "d": 400}),
        ],
        ids=["empty", "single", "multiple"],
    )
    def test_instance_creation(self, mappings: tuple[dict[Any, Any], ...]) -> None:
        """Tests that instances of DeepChainMap can be created with various parameters.

        This test verifies that DeepChainMap instances can be created with no mappings, a single mapping,
        or multiple mappings.
        """
        dcm = self.UnitTestClass(*mappings)
        assert dcm is not None
        if not mappings:
            assert len(dcm.maps) == 1
            assert dcm.maps[0] == {}
        else:
            assert len(dcm.maps) == len(mappings)
            for i, m in enumerate(mappings):
                assert dcm.maps[i] == m

    # Copying #
    @pytest.mark.parametrize("use_method", [False, True], ids=["copy_func", "copy_method"])
    def test_copy(self, test_object: Any, use_method: bool) -> None:
        """Tests the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the copy method or copy function.
        """
        # Copy Object
        if use_method:
            obj_copy = test_object.copy()
        else:
            obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object
        assert isinstance(obj_copy, self.UnitTestClass)
        assert len(obj_copy.maps) == len(test_object.maps)

        # Checks that the maps are the same objects (shallow copy)
        # ChainMap copy logic copies the first map, but keeps the rest.
        assert obj_copy.maps[0] == test_object.maps[0]
        assert id(obj_copy.maps[0]) != id(test_object.maps[0])  # First map is copied

        for i, m in enumerate(obj_copy.maps[1:], start=1):
            assert m == test_object.maps[i]
            assert id(m) == id(test_object.maps[i])  # Others are same objects

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the deepcopy method or deepcopy function.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Deep Copy Object
        if memo is None:
            memo = {}

        if use_method:
            obj_deepcopy = test_object.deepcopy(memo=memo)
        else:
            obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.UnitTestClass)
        assert len(obj_deepcopy.maps) == len(test_object.maps)

        # Checks that the maps are the same but not the same objects
        for i, m in enumerate(obj_deepcopy.maps):
            assert m == test_object.maps[i]
            assert id(m) != id(test_object.maps[i])  # Different objects

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

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
        assert isinstance(unpickled, self.UnitTestClass)
        assert len(unpickled.maps) == len(test_object.maps)

        # Checks that the maps are the same
        for i, m in enumerate(unpickled.maps):
            assert m == test_object.maps[i]

        # Checks that the values are accessible
        assert unpickled["a"] == 1
        assert unpickled["b"] == 2
        assert unpickled["c"] == 3
        assert unpickled["d"] == 4
        assert unpickled["new_key"] == "new_value"

    # Functionality #
    def test_inheritance(self) -> None:
        """Tests that DeepChainMap inherits from both BaseObject and ChainMap.

        This test verifies that DeepChainMap instances are instances of both BaseObject and ChainMap.
        """
        dcm = self.UnitTestClass()
        assert isinstance(dcm, ChainMap)
        assert hasattr(dcm, "deepcopy")  # A method from BaseObject

    @pytest.mark.parametrize(
        ("operation", "key"),
        [
            ("getitem", "e"),
            ("delitem", "e"),
        ],
    )
    def test_invalid_key_operations(self, multi_map: DeepChainMap, operation: str, key: str) -> None:
        """Tests methods with nonexistent keys."""
        if operation == "getitem":
            with pytest.raises(KeyError):
                _ = multi_map[key]
        else:
            with pytest.raises(KeyError):
                del multi_map[key]

    def test_standard_chainmap_methods(self, multi_map: DeepChainMap) -> None:
        """Tests that standard ChainMap methods work with DeepChainMap.

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
        """Tests DeepChainMap with nested dictionaries.

        This test verifies that DeepChainMap works correctly with nested dictionaries.
        """
        # Creates a DeepChainMap with nested dictionaries
        nested_map = self.UnitTestClass({"a": {"x": 1, "y": 2}}, {"b": {"z": 3}}, {"a": {"w": 4}})

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
        """Tests DeepChainMap with empty mappings.

        This test verifies that DeepChainMap works correctly with empty mappings.
        """
        # Creates a DeepChainMap with empty mappings
        empty_maps = self.UnitTestClass({}, {}, {})

        # Test adding values
        empty_maps["a"] = 1
        assert empty_maps["a"] == 1
        assert empty_maps.maps[0]["a"] == 1

        # Test that other maps remain empty
        assert empty_maps.maps[1] == {}
        assert empty_maps.maps[2] == {}

    def test_update_method(self, multi_map: DeepChainMap) -> None:
        """Tests the update method of DeepChainMap.

        This test verifies that the update method updates existing keys in the appropriate mappings
        and adds new keys to the first mapping.

        Args:
            multi_map: A DeepChainMap with multiple mappings.
        """
        # Updates with a dictionary containing existing and new keys
        multi_map.update({"a": 100, "c": 300, "e": 500})

        # Checks existing keys were updated in the appropriate mappings
        assert multi_map["a"] == 100
        assert multi_map.maps[0]["a"] == 100

        assert multi_map["c"] == 300
        assert "c" not in multi_map.maps[0]
        assert multi_map.maps[1]["c"] == 300

        # Checks new keys were added to the first mapping
        assert multi_map["e"] == 500
        assert multi_map.maps[0]["e"] == 500
        assert "e" not in multi_map.maps[1]
        assert "e" not in multi_map.maps[2]
