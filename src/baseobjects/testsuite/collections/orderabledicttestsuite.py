"""orderabledicttestsuite.py
Test suite for the OrderableDict class.
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
from ...collections import OrderableDict
from ..bases import BaseDictTestSuite


# Definitions #
# Classes #
class OrderableDictTestSuite(BaseDictTestSuite):
    """Tests suite for the OrderableDict class.

    This class provides common test functionality for OrderableDict classes.
    """

    UnitTestClass: type[OrderableDict]

    # Fixtures #
    @pytest.fixture
    def empty_dict(self) -> OrderableDict:
        """Creates an empty OrderableDict for testing.

        Returns:
            OrderableDict: An empty OrderableDict.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def simple_dict(self) -> OrderableDict:
        """Creates an OrderableDict with a few items for testing.

        Returns:
            OrderableDict: An OrderableDict with a few items.
        """
        return self.UnitTestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def test_object(self) -> OrderableDict:
        """Creates a test object for testing.

        Returns:
            OrderableDict: An OrderableDict with a few items.
        """
        # Use function scope to ensure a fresh object for each test
        return self.UnitTestClass({"a": 1, "b": 2, "c": 3, "d": 4})

    # Tests #
    # Magic Methods #
    def test_setitem_getitem(self, empty_dict: OrderableDict) -> None:
        """Tests the __setitem__ and __getitem__ methods."""
        # Sets items
        empty_dict["a"] = 1
        empty_dict["b"] = 2
        empty_dict["c"] = 3

        # Verifies items and order
        assert empty_dict["a"] == 1
        assert empty_dict["b"] == 2
        assert empty_dict["c"] == 3
        assert empty_dict.order == ["a", "b", "c"]

        # Updates an existing item
        empty_dict["b"] = 20
        assert empty_dict["b"] == 20
        assert empty_dict.order == ["a", "b", "c"]  # Order unchanged

    def test_delitem(self, simple_dict: OrderableDict) -> None:
        """Tests the __delitem__ method."""
        # Deletes an item
        del simple_dict["b"]

        # Verifies item is removed and order is updated
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Try to delete a non-existent item
        with pytest.raises(KeyError):
            del simple_dict["z"]

    def test_iter(self, simple_dict: OrderableDict) -> None:
        """Tests the __iter__ method."""
        # Iterate and collect keys
        keys = list(simple_dict)

        # Verifies keys match the order
        assert keys == simple_dict.order
        assert keys == ["a", "b", "c"]

    # Instantiation #
    @pytest.mark.parametrize(
        ("args", "kwargs", "expected_len", "expected_order"),
        [
            ((), {}, 0, []),
            (({"a": 1, "b": 2, "c": 3},), {}, 3, ["a", "b", "c"]),
            ((), {"a": 1, "b": 2, "c": 3}, 3, ["a", "b", "c"]),
        ],
        ids=["empty", "mapping", "kwargs"],
    )
    def test_instance_creation(self, args: tuple, kwargs: dict, expected_len: int, expected_order: list) -> None:  # type: ignore[type-arg]
        """Tests that instances of OrderableDict can be created with various parameters."""
        od = self.UnitTestClass(*args, **kwargs)
        assert od is not None
        assert isinstance(od, self.UnitTestClass)
        assert len(od) == expected_len
        assert set(od.order) == set(expected_order)
        if expected_len > 0:
            assert od["a"] == 1
            assert od["b"] == 2
            assert od["c"] == 3

    # Copying #
    @pytest.mark.parametrize("use_method", [False, True], ids=["copy_func", "copy_method"])
    def test_copy(self, test_object: Any, use_method: bool) -> None:
        """Tests the copy behavior of the object.

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
        assert obj_copy is not test_object  # Different objects
        assert isinstance(obj_copy, self.UnitTestClass)  # Same type
        assert obj_copy == test_object  # Equal values
        assert obj_copy.order == test_object.order  # Same order

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

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
        assert obj_deepcopy == test_object
        assert obj_deepcopy.order == test_object.order
        assert id(obj_deepcopy.order) != id(test_object.order)  # Different list objects

        # Verifies that modifying the deepcopy doesn't affect the original
        key = "deepcopy_key" if not use_method else "deepcopy_method_key"
        obj_deepcopy[key] = 300
        assert key in obj_deepcopy
        assert key not in test_object
        assert len(obj_deepcopy.order) == len(test_object.order) + 1

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object."""
        # Modify the test object
        test_object["e"] = 5

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)
        assert unpickled == test_object
        assert unpickled.order == test_object.order

        # Checks that the values are accessible
        assert unpickled["a"] == 1
        assert unpickled["b"] == 2
        assert unpickled["c"] == 3
        assert unpickled["d"] == 4
        assert unpickled["e"] == 5

    # Functionality #
    def test_dict_set_item(self, empty_dict: OrderableDict) -> None:  # type: ignore[override]
        """Tests setting items in BaseDict (overridden to use empty_dict)."""
        super().test_dict_set_item(empty_dict)

    def test_dict_update(self, empty_dict: OrderableDict) -> None:  # type: ignore[override]
        """Tests updating BaseDict (overridden to use empty_dict)."""
        super().test_dict_update(empty_dict)

    def test_dict_pop(self, empty_dict: OrderableDict) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict (overridden to use empty_dict)."""
        super().test_dict_pop(empty_dict)

    def test_dict_popitem(self, empty_dict: OrderableDict) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict (overridden to use empty_dict)."""
        super().test_dict_popitem(empty_dict)

    def test_get_index(self, simple_dict: OrderableDict) -> None:
        """Tests the get_index method."""
        # Gets values by index
        assert simple_dict.get_index(0) == 1  # Value at key "a"
        assert simple_dict.get_index(1) == 2  # Value at key "b"
        assert simple_dict.get_index(2) == 3  # Value at key "c"

        # Test with default value
        assert simple_dict.get_index(10, default=None) is None

        # Test without default value (should raise IndexError)
        with pytest.raises(IndexError):
            simple_dict.get_index(10)

    def test_set_index(self, simple_dict: OrderableDict) -> None:
        """Tests the set_index method."""
        # Sets values by index
        simple_dict.set_index(0, 10)  # Set value at key "a"
        simple_dict.set_index(1, 20)  # Set value at key "b"

        # Verifies values were updated
        assert simple_dict["a"] == 10
        assert simple_dict["b"] == 20
        assert simple_dict["c"] == 3  # Unchanged
        assert simple_dict.order == ["a", "b", "c"]  # Order unchanged

    def test_setdefault(self, simple_dict: OrderableDict) -> None:
        """Tests the setdefault method."""
        # Test with existing key
        value = simple_dict.setdefault("a", 100)
        assert value == 1  # Original value returned
        assert simple_dict["a"] == 1  # Value unchanged

        # Test with new key
        value = simple_dict.setdefault("d", 4)
        assert value == 4  # Default value returned
        assert simple_dict["d"] == 4  # New key-value added
        assert simple_dict.order == ["a", "b", "c", "d"]  # Order updated

    @pytest.mark.parametrize(
        ("index", "key", "value", "expected_order"),
        [
            (0, "d", 4, ["d", "a", "b", "c"]),
            (2, "e", 5, ["a", "b", "e", "c"]),
            (5, "f", 6, ["a", "b", "c", "f"]),
        ],
    )
    def test_insert(self, simple_dict: OrderableDict, index: int, key: str, value: Any, expected_order: list) -> None:  # type: ignore[type-arg]
        """Tests the insert method.

        Args:
            simple_dict: A fixture providing a simple dictionary.
            index: The index to insert at.
            key: The key to insert.
            value: The value to insert.
            expected_order: The expected order of keys after insertion.
        """
        simple_dict.insert(index, key, value)
        assert simple_dict.order == expected_order
        assert simple_dict[key] == value

    def test_insert_error(self, simple_dict: OrderableDict) -> None:
        """Tests insert with existing key."""
        with pytest.raises(KeyError):
            simple_dict.insert(0, "a", 10)

    @pytest.mark.parametrize(
        ("index", "key", "value", "expected_order"),
        [
            (0, "d", 4, ["d", "a", "b", "c"]),
            (3, "d", 4, ["a", "b", "c", "d"]),
            (0, "c", 30, ["c", "a", "b"]),
            (1, "b", 20, ["a", "b", "c"]),
            (2, "b", 21, ["a", "b", "c"]),
            (2, "a", 10, ["b", "a", "c"]),
        ],
        ids=["new_start", "new_end", "move_to_start", "same_index", "index_plus_one", "move_forward_skip"],
    )
    def test_insert_move_variants(
        self,
        simple_dict: OrderableDict,
        index: int,
        key: str,
        value: Any,
        expected_order: list,  # type: ignore[type-arg]
    ) -> None:
        """Tests the insert_move method.

        Args:
            simple_dict: A fixture providing a simple dictionary.
            index: The index to insert/move to.
            key: The key to insert/move.
            value: The value to set.
            expected_order: The expected order of keys.
        """
        simple_dict.insert_move(index, key, value)
        assert simple_dict.order == expected_order
        assert simple_dict[key] == value

    def test_append(self, simple_dict: OrderableDict) -> None:
        """Tests the append method."""
        # Append new key
        simple_dict.append("d", 4)
        assert simple_dict.order == ["a", "b", "c", "d"]
        assert simple_dict["d"] == 4

        # Append existing key (should update value but not change order)
        simple_dict.append("b", 20)
        assert simple_dict.order == ["a", "b", "c", "d"]
        assert simple_dict["b"] == 20

    def test_update(self) -> None:
        """Tests the update method."""
        # Creates a fresh dictionary for this test
        test_dict = self.UnitTestClass({"a": 1, "b": 2, "c": 3})

        # Updates with dictionary
        test_dict.update({"b": 20, "d": 4, "e": 5})
        assert test_dict["a"] == 1  # Unchanged
        assert test_dict["b"] == 20  # Updated
        assert test_dict["c"] == 3  # Unchanged
        assert test_dict["d"] == 4  # New
        assert test_dict["e"] == 5  # New
        assert set(test_dict.order) == {"a", "b", "c", "d", "e"}

        # Creates a new dictionary for this test
        kw_dict = self.UnitTestClass()
        kw_dict.update({"x": 1, "y": 2})
        assert kw_dict["x"] == 1
        assert kw_dict["y"] == 2
        assert set(kw_dict.order) == {"x", "y"}

    @pytest.mark.parametrize(
        ("key", "expected_val", "expected_order"),
        [("b", 2, ["a", "c"]), ("a", 1, ["b", "c"]), ("c", 3, ["a", "b"])],
    )
    def test_pop(self, simple_dict: OrderableDict, key: str, expected_val: Any, expected_order: list) -> None:  # type: ignore[type-arg]
        """Tests the pop method.

        Args:
            simple_dict: A fixture providing a simple dictionary.
            key: The key to pop.
            expected_val: The expected value.
            expected_order: The expected order of keys after pop.
        """
        value = simple_dict.pop(key)
        assert value == expected_val
        assert key not in simple_dict
        assert simple_dict.order == expected_order

    def test_pop_error(self, simple_dict: OrderableDict) -> None:
        """Tests pop with non-existent key."""
        with pytest.raises(KeyError):
            simple_dict.pop("z")

    def test_pop_default(self, simple_dict: OrderableDict) -> None:
        """Tests popping a non-existent key with a default value."""
        assert simple_dict.pop("z", "default") == "default"
        assert "z" not in simple_dict

    @pytest.mark.parametrize(
        ("index", "expected_val", "expected_key", "expected_order"),
        [(1, 2, "b", ["a", "c"]), (None, 3, "c", ["a", "b"]), (0, 1, "a", ["b", "c"]), (-1, 3, "c", ["a", "b"])],
    )
    def test_pop_index(
        self,
        simple_dict: OrderableDict,
        index: int | None,
        expected_val: Any,
        expected_key: str,
        expected_order: list,  # type: ignore[type-arg]
    ) -> None:
        """Tests the pop_index method.

        Args:
            simple_dict: A fixture providing a simple dictionary.
            index: The index to pop.
            expected_val: The expected value.
            expected_key: The expected key that was popped.
            expected_order: The expected order of keys after pop.
        """
        if index is None:
            value = simple_dict.pop_index()
        else:
            value = simple_dict.pop_index(index)

        assert value == expected_val
        assert expected_key not in simple_dict
        assert simple_dict.order == expected_order

    def test_pop_index_empty(self, empty_dict: OrderableDict) -> None:
        """Tests pop_index from empty dictionary."""
        with pytest.raises(IndexError):
            empty_dict.pop_index()

    def test_popitem(self, simple_dict: OrderableDict) -> None:
        """Tests the popitem method."""
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
        """Tests the remove method."""
        # Removes existing key
        simple_dict.remove("b")
        assert "b" not in simple_dict
        assert simple_dict.order == ["a", "c"]

        # Try to remove non-existent key
        with pytest.raises(KeyError):
            simple_dict.remove("z")

    def test_clear(self, simple_dict: OrderableDict) -> None:
        """Tests the clear method."""
        # Clear dictionary
        simple_dict.clear()
        assert len(simple_dict) == 0
        assert simple_dict.order == []

    def test_reverse(self, simple_dict: OrderableDict) -> None:
        """Tests the reverse method."""
        # Reverse order
        simple_dict.reverse()
        assert simple_dict.order == ["c", "b", "a"]

        # Verifies values are still accessible
        assert simple_dict["a"] == 1
        assert simple_dict["b"] == 2
        assert simple_dict["c"] == 3
