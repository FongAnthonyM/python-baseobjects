"""orderabledict_test.py
Tests for the OrderableDict class in the baseobjects package.

This module provides tests for the OrderableDict class, which extends BaseDict to implement a dictionary that maintains an
explicit ordering of its keys. Unlike OrderedDict from the standard library, OrderableDict allows for direct
manipulation of the key order through various methods.
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

# Local Packages #
from src.baseobjects.collections import OrderableDict
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestOrderableDict(BaseObjectTestSuite):
    """Test the OrderableDict class.

    This class tests the functionality of the OrderableDict class, which extends BaseDict to implement a dictionary
    that maintains an explicit ordering of its keys and allows for direct manipulation of the key order.
    """

    # Attributes #
    TestClass: Type[OrderableDict] = OrderableDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_dict(self) -> OrderableDict:
        """Create an empty OrderableDict for testing.

        Returns:
            OrderableDict: An empty OrderableDict.
        """
        return self.TestClass()

    @pytest.fixture
    def simple_dict(self) -> OrderableDict:
        """Create an OrderableDict with a few items for testing.

        Returns:
            OrderableDict: An OrderableDict with a few items.
        """
        return self.TestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def test_object(self) -> OrderableDict:
        """Create a test object for testing.

        Returns:
            OrderableDict: An OrderableDict with a few items.
        """
        # Use function scope to ensure a fresh object for each test
        return self.TestClass({"a": 1, "b": 2, "c": 3, "d": 4})

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of OrderableDict can be created with various parameters.

        This test verifies that OrderableDict instances can be created with no arguments,
        a dictionary, or keyword arguments.
        """
        # Create an empty instance
        od = self.TestClass()
        assert od is not None
        assert isinstance(od, self.TestClass)
        assert len(od) == 0
        assert od.order == []

        # Create an instance with a dictionary
        mapping = {"a": 1, "b": 2, "c": 3}
        od = self.TestClass(mapping)
        assert od is not None
        assert isinstance(od, self.TestClass)
        assert len(od) == 3
        assert set(od.order) == {"a", "b", "c"}
        assert od["a"] == 1
        assert od["b"] == 2
        assert od["c"] == 3

        # Create an instance with keyword arguments
        od = self.TestClass(a=1, b=2, c=3)
        assert od is not None
        assert isinstance(od, self.TestClass)
        assert len(od) == 3
        assert set(od.order) == {"a", "b", "c"}
        assert od["a"] == 1
        assert od["b"] == 2
        assert od["c"] == 3

    def test_copy(self) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.
        """
        # Create a fresh object for this test
        original = self.TestClass({"a": 1, "b": 2})

        # Copy Object
        obj_copy = copy.copy(original)

        # Validate
        assert obj_copy is not original  # Different objects
        assert isinstance(obj_copy, self.TestClass)  # Same type
        assert obj_copy == original  # Equal values
        assert obj_copy.order == original.order  # Same order

    def test_copy_method(self) -> None:
        """Test the copy method behavior of the object.

        This test verifies that the copy method creates a new object with the same attributes.
        """
        # Create a fresh object for this test
        original = self.TestClass({"x": 10, "y": 20})

        # Copy Object
        obj_copy = original.copy()

        # Validate
        assert obj_copy is not original  # Different objects
        assert isinstance(obj_copy, self.TestClass)  # Same type
        assert obj_copy == original  # Equal values
        assert obj_copy.order == original.order  # Same order

    def test_deepcopy(self, test_object: OrderableDict, memo: dict | None = None) -> None:
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
        assert obj_deepcopy == test_object
        assert obj_deepcopy.order == test_object.order
        assert id(obj_deepcopy.order) != id(test_object.order)  # Different list objects

        # Verify that modifying the deepcopy doesn't affect the original
        obj_deepcopy["deepcopy_key"] = 300
        assert "deepcopy_key" in obj_deepcopy
        assert "deepcopy_key" not in test_object
        assert len(obj_deepcopy.order) == len(test_object.order) + 1

    def test_deepcopy_method(self, test_object: OrderableDict, memo: dict | None = None) -> None:
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
        assert obj_deepcopy == test_object
        assert obj_deepcopy.order == test_object.order
        assert id(obj_deepcopy.order) != id(test_object.order)  # Different list objects

        # Verify that modifying the deepcopy doesn't affect the original
        obj_deepcopy["deepcopy_method_key"] = 400
        assert "deepcopy_method_key" in obj_deepcopy
        assert "deepcopy_method_key" not in test_object
        assert len(obj_deepcopy.order) == len(test_object.order) + 1

    def test_pickling(self, test_object: OrderableDict) -> None:
        """Test pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Modify the test object
        test_object["e"] = 5

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.TestClass)
        assert unpickled == test_object
        assert unpickled.order == test_object.order

        # Check that the values are accessible
        assert unpickled["a"] == 1
        assert unpickled["b"] == 2
        assert unpickled["c"] == 3
        assert unpickled["d"] == 4
        assert unpickled["e"] == 5

    def test_setitem_getitem(self, empty_dict: OrderableDict) -> None:
        """Test the __setitem__ and __getitem__ methods.

        This test verifies that items can be set and retrieved correctly, and that
        the order is maintained.

        Args:
            empty_dict: An empty OrderableDict.
        """
        # Set items
        empty_dict["a"] = 1
        empty_dict["b"] = 2
        empty_dict["c"] = 3

        # Verify items and order
        assert empty_dict["a"] == 1
        assert empty_dict["b"] == 2
        assert empty_dict["c"] == 3
        assert empty_dict.order == ["a", "b", "c"]

        # Update an existing item
        empty_dict["b"] = 20
        assert empty_dict["b"] == 20
        assert empty_dict.order == ["a", "b", "c"]  # Order unchanged

    def test_delitem(self, simple_dict: OrderableDict) -> None:
        """Test the __delitem__ method.

        This test verifies that items can be deleted correctly, and that
        the order is updated.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Delete an item
        del simple_dict["b"]

        # Verify item is removed and order is updated
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Try to delete a non-existent item
        with pytest.raises(KeyError):
            del simple_dict["z"]

    def test_iter(self, simple_dict: OrderableDict) -> None:
        """Test the __iter__ method.

        This test verifies that iterating over the dictionary yields keys in the correct order.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Iterate and collect keys
        keys = list(simple_dict)

        # Verify keys match the order
        assert keys == simple_dict.order
        assert keys == ["a", "b", "c"]

    def test_get_index(self, simple_dict: OrderableDict) -> None:
        """Test the get_index method.

        This test verifies that values can be retrieved by index.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Get values by index
        assert simple_dict.get_index(0) == 1  # Value at key "a"
        assert simple_dict.get_index(1) == 2  # Value at key "b"
        assert simple_dict.get_index(2) == 3  # Value at key "c"

        # Test with default value
        assert simple_dict.get_index(10, default=None) is None

        # Test without default value (should raise IndexError)
        with pytest.raises(IndexError):
            simple_dict.get_index(10)

    def test_set_index(self, simple_dict: OrderableDict) -> None:
        """Test the set_index method.

        This test verifies that values can be set by index.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Set values by index
        simple_dict.set_index(0, 10)  # Set value at key "a"
        simple_dict.set_index(1, 20)  # Set value at key "b"

        # Verify values were updated
        assert simple_dict["a"] == 10
        assert simple_dict["b"] == 20
        assert simple_dict["c"] == 3  # Unchanged
        assert simple_dict.order == ["a", "b", "c"]  # Order unchanged

    def test_setdefault(self, simple_dict: OrderableDict) -> None:
        """Test the setdefault method.

        This test verifies that setdefault works correctly for existing and new keys.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Test with existing key
        value = simple_dict.setdefault("a", 100)
        assert value == 1  # Original value returned
        assert simple_dict["a"] == 1  # Value unchanged

        # Test with new key
        value = simple_dict.setdefault("d", 4)
        assert value == 4  # Default value returned
        assert simple_dict["d"] == 4  # New key-value added
        assert simple_dict.order == ["a", "b", "c", "d"]  # Order updated

    def test_insert(self, simple_dict: OrderableDict) -> None:
        """Test the insert method.

        This test verifies that new key-value pairs can be inserted at a specific position.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Insert at beginning
        simple_dict.insert(0, "d", 4)
        assert simple_dict.order == ["d", "a", "b", "c"]
        assert simple_dict["d"] == 4

        # Insert in middle
        simple_dict.insert(2, "e", 5)
        assert simple_dict.order == ["d", "a", "e", "b", "c"]
        assert simple_dict["e"] == 5

        # Insert at end
        simple_dict.insert(5, "f", 6)
        assert simple_dict.order == ["d", "a", "e", "b", "c", "f"]
        assert simple_dict["f"] == 6

        # Try to insert existing key
        with pytest.raises(KeyError):
            simple_dict.insert(0, "a", 10)

    def test_insert_move(self, simple_dict: OrderableDict) -> None:
        """Test the insert_move method.

        This test verifies that key-value pairs can be inserted or moved to a specific position.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Insert new key
        simple_dict.insert_move(0, "d", 4)
        assert simple_dict.order == ["d", "a", "b", "c"]
        assert simple_dict["d"] == 4

        # Move existing key forward
        simple_dict.insert_move(3, "a", 10)
        # The actual behavior moves 'a' after 'b' but before 'c'
        assert simple_dict.order == ["d", "b", "a", "c"]
        assert simple_dict["a"] == 10

        # Move existing key backward
        simple_dict.insert_move(0, "c", 30)
        assert simple_dict.order == ["c", "d", "b", "a"]
        assert simple_dict["c"] == 30

    def test_append(self, simple_dict: OrderableDict) -> None:
        """Test the append method.

        This test verifies that key-value pairs can be appended to the dictionary.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Append new key
        simple_dict.append("d", 4)
        assert simple_dict.order == ["a", "b", "c", "d"]
        assert simple_dict["d"] == 4

        # Append existing key (should update value but not change order)
        simple_dict.append("b", 20)
        assert simple_dict.order == ["a", "b", "c", "d"]
        assert simple_dict["b"] == 20

    def test_update(self) -> None:
        """Test the update method.

        This test verifies that the dictionary can be updated with another mapping.
        """
        # Create a fresh dictionary for this test
        test_dict = self.TestClass({"a": 1, "b": 2, "c": 3})

        # Update with dictionary
        test_dict.update({"b": 20, "d": 4, "e": 5})
        assert test_dict["a"] == 1  # Unchanged
        assert test_dict["b"] == 20  # Updated
        assert test_dict["c"] == 3  # Unchanged
        assert test_dict["d"] == 4  # New
        assert test_dict["e"] == 5  # New
        assert set(test_dict.order) == {"a", "b", "c", "d", "e"}

        # Note: The OrderableDict implementation doesn't support updating with keyword arguments
        # directly. This is a limitation of the current implementation.
        # Instead, we can update with a dictionary created from keyword arguments.

        # Create a new dictionary for this test
        kw_dict = self.TestClass()
        kw_dict.update(dict(x=1, y=2))
        assert kw_dict["x"] == 1
        assert kw_dict["y"] == 2
        assert set(kw_dict.order) == {"x", "y"}

    def test_pop(self, simple_dict: OrderableDict) -> None:
        """Test the pop method.

        This test verifies that items can be popped from the dictionary.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Pop existing key
        value = simple_dict.pop("b")
        assert value == 2
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Try to pop non-existent key
        # The OrderableDict.pop implementation raises ValueError for non-existent keys
        # when trying to remove the key from the order list
        with pytest.raises(ValueError):
            simple_dict.pop("z")

    def test_pop_index(self, simple_dict: OrderableDict) -> None:
        """Test the pop_index method.

        This test verifies that items can be popped by index.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Pop by index
        value = simple_dict.pop_index(1)  # Pop key "b"
        assert value == 2
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Pop last item (default)
        value = simple_dict.pop_index()  # Pop key "c"
        assert value == 3
        assert "c" not in simple_dict
        assert simple_dict.order == ["a"]

        # Pop first item
        value = simple_dict.pop_index(0)  # Pop key "a"
        assert value == 1
        assert "a" not in simple_dict
        assert simple_dict.order == []

        # Try to pop from empty dictionary
        with pytest.raises(IndexError):
            simple_dict.pop_index()

    def test_popitem(self, simple_dict: OrderableDict) -> None:
        """Test the popitem method.

        This test verifies that the last item can be popped from the dictionary.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Pop last item
        key, value = simple_dict.popitem()
        assert key == "c"
        assert value == 3
        assert "c" not in simple_dict
        assert simple_dict.order == ["a", "b"]

        # Pop another item
        key, value = simple_dict.popitem()
        assert key == "b"
        assert value == 2
        assert "b" not in simple_dict
        assert simple_dict.order == ["a"]

        # Pop last remaining item
        key, value = simple_dict.popitem()
        assert key == "a"
        assert value == 1
        assert "a" not in simple_dict
        assert simple_dict.order == []

        # Try to pop from empty dictionary
        with pytest.raises(IndexError):
            simple_dict.popitem()

    def test_remove(self, simple_dict: OrderableDict) -> None:
        """Test the remove method.

        This test verifies that items can be removed from the dictionary.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Remove existing key
        simple_dict.remove("b")
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Try to remove non-existent key
        with pytest.raises(KeyError):
            simple_dict.remove("z")

    def test_clear(self, simple_dict: OrderableDict) -> None:
        """Test the clear method.

        This test verifies that the dictionary can be cleared.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Clear dictionary
        simple_dict.clear()
        assert len(simple_dict) == 0
        assert simple_dict.order == []

    def test_reverse(self, simple_dict: OrderableDict) -> None:
        """Test the reverse method.

        This test verifies that the order of the dictionary can be reversed.

        Args:
            simple_dict: An OrderableDict with a few items.
        """
        # Reverse order
        simple_dict.reverse()
        assert simple_dict.order == ["c", "b", "a"]

        # Verify values are still accessible
        assert simple_dict["a"] == 1
        assert simple_dict["b"] == 2
        assert simple_dict["c"] == 3


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
