#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" orderabledict_test.py
Tests for the OrderableDict class in the baseobjects package.
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
import datetime
from typing import Dict, Tuple, Type, Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import OrderableDict
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestOrderableDict(ClassTest):
    """Test the OrderableDict class.

    This class tests the functionality of the OrderableDict class, which is a dictionary with an adjustable
    order and additional supporting methods.
    """

    # Attributes #
    class_: Type[OrderableDict] = OrderableDict
    zero_time: datetime.timedelta = datetime.timedelta(0)

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize("items", ({"a": 1, "b": 2, "c": 3}, {"c": 3, "b": 2, "a": 1}))
    def test_instance_creation(self, items: Dict[str, int]) -> None:
        """Test that instances of OrderableDict can be created with various item orders.

        This test verifies that OrderableDict instances can be created with dictionaries having different key orders.

        Args:
            items: The dictionary items to initialize the OrderableDict with.
        """
        instance = self.class_(items)
        assert instance is not None
        assert len(instance) == len(items)

    def test_setitem(self) -> None:
        """Test the __setitem__ method of OrderableDict.

        This test verifies that setting an item adds it to the dictionary and appends the key to the order list
        if it wasn't already present.
        """
        od = OrderableDict()
        od["a"] = 1
        assert od.data["a"] == 1
        assert od.order == ["a"]

        # Test updating an existing key
        od["a"] = 2
        assert od.data["a"] == 2
        assert od.order == ["a"]  # Order should not change

    def test_delitem(self) -> None:
        """Test the __delitem__ method of OrderableDict.

        This test verifies that deleting an item removes it from both the dictionary and the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        del od["b"]
        assert "b" not in od.data
        assert od.order == ["a", "c"]

    def test_iter(self) -> None:
        """Test iterating over an OrderableDict.

        This test verifies that iterating over an OrderableDict returns keys in the order specified by the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od) == ["c", "b", "a"]

    def test_get_index(self) -> None:
        """Test the get_index method of OrderableDict.

        This test verifies that get_index returns the value at the specified index in the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        assert od.get_index(0) == 1
        assert od.get_index(1) == 2
        assert od.get_index(2) == 3

        # Test with default value
        assert od.get_index(3, default=0) == 0

        # Test with out of range index
        with pytest.raises(IndexError):
            od.get_index(3)

    def test_set_index(self) -> None:
        """Test the set_index method of OrderableDict.

        This test verifies that set_index sets the value at the specified index in the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.set_index(1, 5)
        assert od.data["b"] == 5
        assert od.order == ["a", "b", "c"]

    def test_setdefault(self) -> None:
        """Test the setdefault method of OrderableDict.

        This test verifies that setdefault returns the value for a key if it exists, otherwise adds the key
        with the default value and returns that value.
        """
        od = OrderableDict({"a": 1, "b": 2})

        # Test existing key
        value = od.setdefault("a", 10)
        assert value == 1
        assert od.data["a"] == 1
        assert od.order == ["a", "b"]

        # Test new key
        value = od.setdefault("c", 3)
        assert value == 3
        assert od.data["c"] == 3
        assert od.order == ["a", "b", "c"]

    def test_insert(self) -> None:
        """Test the insert method of OrderableDict.

        This test verifies that insert adds a key-value pair at the specified index in the order list,
        or raises an error if the key already exists.
        """
        od = OrderableDict({"a": 1, "c": 3})

        # Test inserting a new key
        od.insert(1, "b", 2)
        assert od.data["b"] == 2
        assert od.order == ["a", "b", "c"]

        # Test inserting an existing key
        with pytest.raises(KeyError):
            od.insert(0, "a", 10)

    def test_insert_move(self) -> None:
        """Test the insert_move method of OrderableDict.

        This test verifies that insert_move adds a key-value pair at the specified index in the order list,
        or moves the key if it already exists.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})

        # Test inserting a new key
        od.insert_move(1, "d", 4)
        assert od.data["d"] == 4
        assert "d" in od.order
        assert od.order == ["a", "d", "b", "c"]

        # Test moving an existing key to an earlier position
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.insert_move(0, "c", 30)
        assert od.data["c"] == 30
        assert od.order == ["c", "a", "b"]

        # Test moving an existing key to a later position
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.insert_move(3, "a", 10)
        assert od.data["a"] == 10
        assert od.order == ["b", "c", "a"]

    def test_append(self) -> None:
        """Test the append method of OrderableDict.

        This test verifies that append adds a key-value pair to the end of the order list.
        """
        od = OrderableDict({"a": 1, "b": 2})
        od.append("c", 3)
        assert od.data["c"] == 3
        assert od.order == ["a", "b", "c"]

        # Test appending an existing key
        od.append("a", 10)
        assert od.data["a"] == 10
        assert od.order == ["a", "b", "c"]  # Order should not change

    def test_keys(self) -> None:
        """Test the keys method of OrderableDict.

        This test verifies that the keys method returns keys in the order specified by the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.keys()) == ["c", "b", "a"]

    def test_values(self) -> None:
        """Test the values method of OrderableDict.

        This test verifies that the values method returns values in the order specified by the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.values()) == [3, 2, 1]

    def test_items(self) -> None:
        """Test the items method of OrderableDict.

        This test verifies that the items method returns key-value pairs in the order specified by the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.order.reverse()
        assert list(od.items()) == [("c", 3), ("b", 2), ("a", 1)]

    def test_clear(self) -> None:
        """Test the clear method of OrderableDict.

        This test verifies that the clear method removes all items from the dictionary and clears the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.clear()
        assert not od.data
        assert not od.order

    def test_pop(self) -> None:
        """Test the pop method of OrderableDict.

        This test verifies that the pop method removes an item by key and returns its value, and that the key is also
        removed from the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        value = od.pop("b")
        assert value == 2
        assert list(od.data.keys()) == ["a", "c"]
        assert od.order == ["a", "c"]

    def test_pop_index(self) -> None:
        """Test the pop_index method of OrderableDict.

        This test verifies that pop_index removes and returns the value at the specified index in the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})

        # Test with positive index
        value = od.pop_index(1)
        assert value == 2
        assert list(od.data.keys()) == ["a", "c"]
        assert od.order == ["a", "c"]

        # Test with negative index
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        value = od.pop_index(-1)
        assert value == 3
        assert list(od.data.keys()) == ["a", "b"]
        assert od.order == ["a", "b"]

    def test_popitem(self) -> None:
        """Test the popitem method of OrderableDict.

        This test verifies that the popitem method removes and returns the last key-value pair
        based on the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        item = od.popitem()
        assert item == ("c", 3)
        assert list(od.data.keys()) == ["a", "b"]
        assert od.order == ["a", "b"]

    def test_remove(self) -> None:
        """Test the remove method of OrderableDict.

        This test verifies that the remove method removes an item by key from both the dictionary and the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.remove("b")
        assert "b" not in od.data
        assert od.order == ["a", "c"]

    @pytest.mark.parametrize("param", ({"d": 4, "e": 5}, (("d", 4), ("e", 5))))
    def test_update(self, param: dict[str, int] | list[tuple[str, int]]) -> None:
        """Test the update method of OrderableDict.

        This test verifies that the update method adds new key-value pairs to the dictionary
        and appends new keys to the order list.

        Args:
            param: The parameter to pass to the update method, either a dictionary or a list of key-value pairs.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.update(param)
        assert list(od.data.keys()) == ["a", "b", "c", "d", "e"]
        assert od.order == ["a", "b", "c", "d", "e"]

    def test_reverse(self) -> None:
        """Test the reverse method of OrderableDict.

        This test verifies that the reverse method reverses the order of the keys in the order list.
        """
        od = OrderableDict({"a": 1, "b": 2, "c": 3})
        od.reverse()
        assert od.order == ["c", "b", "a"]
        assert list(od.keys()) == ["c", "b", "a"]


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
