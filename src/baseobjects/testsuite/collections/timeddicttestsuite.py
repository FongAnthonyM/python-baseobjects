"""timeddicttestsuite.py
Test suite for the TimedDict class.
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
import time
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...collections import TimedDict
from ..bases import BaseDictTestSuite


# Definitions #
# Classes #
class TimedDictTestSuite(BaseDictTestSuite):
    """Tests suite for the TimedDict class.

    This class provides common test functionality for TimedDict classes.
    """

    UnitTestClass: type[TimedDict]

    # Fixtures #
    @pytest.fixture
    def empty_dict(self) -> TimedDict:
        """Creates an empty TimedDict for testing.

        Returns:
            TimedDict: An empty TimedDict.
        """
        return self.UnitTestClass()

    @pytest.fixture
    def simple_dict(self) -> TimedDict:
        """Creates a TimedDict with a few items for testing.

        Returns:
            TimedDict: A TimedDict with a few items.
        """
        return self.UnitTestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def timed_dict(self) -> TimedDict:
        """Creates a TimedDict with a lifetime for testing.

        Returns:
            TimedDict: A TimedDict with a lifetime.
        """
        td = self.UnitTestClass({"a": 1, "b": 2, "c": 3})
        td.lifetime = 1.0  # 1 second lifetime
        return td

    @pytest.fixture
    def test_object(self) -> TimedDict:
        """Creates a test object for testing.

        Returns:
            TimedDict: A TimedDict with a few items.
        """
        # Use function scope to ensure a fresh object for each test
        return self.UnitTestClass({"a": 1, "b": 2, "c": 3, "d": 4})

    # Tests #
    # Instantiation #
    @pytest.mark.parametrize(
        ("args", "kwargs", "expected_len", "check_items"),
        [
            ((), {}, 0, False),
            (({"a": 1, "b": 2, "c": 3},), {}, 3, True),
            ((), {"a": 1, "b": 2, "c": 3}, 3, True),
        ],
        ids=["empty", "mapping", "kwargs"],
    )
    def test_instance_creation(self, args: tuple, kwargs: dict, expected_len: int, check_items: bool) -> None:  # type: ignore[type-arg]
        """Tests that instances of TimedDict can be created with various parameters."""
        td = self.UnitTestClass(*args, **kwargs)
        assert td is not None
        assert isinstance(td, self.UnitTestClass)
        assert len(td) == expected_len
        assert td.is_timed is True
        assert td.lifetime is None
        assert td.expiration is None
        if check_items:
            assert td["a"] == 1
            assert td["b"] == 2
            assert td["c"] == 3

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
        assert obj_copy.is_timed == test_object.is_timed
        assert obj_copy.lifetime == test_object.lifetime
        assert obj_copy.expiration == test_object.expiration

    @pytest.mark.parametrize("use_method", [False, True], ids=["deepcopy_func", "deepcopy_method"])
    def test_deepcopy(self, test_object: Any, use_method: bool, memo: dict[Any, Any] | None = None) -> None:
        """Tests the deep copy behavior of the object.

        Args:
            test_object: A fixture providing a test object instance.
            use_method: Boolean indicating whether to use the deepcopy method or deepcopy function.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set a lifetime to test copying of all attributes
        test_object.lifetime = 10.0

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
        assert obj_deepcopy.is_timed == test_object.is_timed
        assert obj_deepcopy.lifetime == test_object.lifetime
        assert obj_deepcopy.expiration is not None

        # Verify that modifying the deepcopy doesn't affect the original
        key = "deepcopy_key" if not use_method else "deepcopy_method_key"
        obj_deepcopy[key] = 300
        assert key in obj_deepcopy
        assert key not in test_object

    # Pickling #
    def test_pickling(self, test_object: Any) -> None:
        """Tests pickling and unpickling of the object.

        This test verifies that the object can be pickled and unpickled correctly.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Set a lifetime to test pickling of all attributes
        test_object.lifetime = 5.0
        test_object["e"] = 5

        # Pickle and Unpickle Object
        pickled = pickle.dumps(test_object)
        unpickled = pickle.loads(pickled)

        # Validate
        assert unpickled is not test_object
        assert isinstance(unpickled, self.UnitTestClass)
        assert unpickled == test_object
        assert unpickled.is_timed == test_object.is_timed
        assert unpickled.lifetime == test_object.lifetime
        assert unpickled.expiration is not None

        # Check that the values are accessible
        assert unpickled["a"] == 1
        assert unpickled["b"] == 2
        assert unpickled["c"] == 3
        assert unpickled["d"] == 4
        assert unpickled["e"] == 5

    # Functionality #
    def test_dict_set_item(self, empty_dict: TimedDict) -> None:  # type: ignore[override]
        """Tests setting items in BaseDict (overridden to use empty_dict)."""
        super().test_dict_set_item(empty_dict)

    def test_dict_update(self, empty_dict: TimedDict) -> None:  # type: ignore[override]
        """Tests updating BaseDict (overridden to use empty_dict)."""
        super().test_dict_update(empty_dict)

    def test_dict_pop(self, empty_dict: TimedDict) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict (overridden to use empty_dict)."""
        super().test_dict_pop(empty_dict)

    def test_dict_popitem(self, empty_dict: TimedDict) -> None:  # type: ignore[override]
        """Tests popping items from BaseDict (overridden to use empty_dict)."""
        super().test_dict_popitem(empty_dict)

    def test_lifetime_property(self, empty_dict: TimedDict) -> None:
        """Tests the lifetime property.

        This test verifies that the lifetime property can be set and retrieved correctly.

        Args:
            empty_dict: An empty TimedDict.
        """
        # Default value
        assert empty_dict.lifetime is None

        # Set lifetime
        empty_dict.lifetime = 10.0
        assert empty_dict.lifetime == 10.0
        assert empty_dict.expiration is not None  # Should be set when lifetime is set

        # Change lifetime
        empty_dict.lifetime = 5.0
        assert empty_dict.lifetime == 5.0
        assert empty_dict.expiration is not None  # Should be updated

        # Set to None
        empty_dict.lifetime = None
        assert empty_dict.lifetime is None

    def test_data_property(self, simple_dict: TimedDict) -> None:
        """Tests the data property.

        This test verifies that the data property returns the dictionary data.

        Args:
            simple_dict: A TimedDict with a few items.
        """
        # Check data property
        data = simple_dict.data
        assert isinstance(data, dict)
        assert len(data) == 3
        assert data["a"] == 1
        assert data["b"] == 2
        assert data["c"] == 3

        # Set data property
        new_data = {"x": 10}
        simple_dict.data = new_data  # type: ignore[assignment]
        assert simple_dict.data == new_data
        assert simple_dict["x"] == 10

    def test_clear(self, simple_dict: TimedDict) -> None:
        """Tests the clear method.

        This test verifies that the dictionary can be cleared and the expiration is reset.

        Args:
            simple_dict: A TimedDict with a few items.
        """
        # Set a lifetime
        simple_dict.lifetime = 10.0
        old_expiration = simple_dict.expiration

        # Clear dictionary
        simple_dict.clear()

        # Verify dictionary is empty
        assert len(simple_dict) == 0

        # Verify expiration was reset
        assert simple_dict.expiration is not None
        assert simple_dict.expiration != old_expiration

    def test_reset_expiration(self, timed_dict: TimedDict) -> None:
        """Tests the reset_expiration method.

        This test verifies that the expiration time is reset correctly.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Get initial expiration
        initial_expiration = timed_dict.expiration
        assert initial_expiration is not None

        # Wait a bit
        time.sleep(0.1)

        # Reset expiration
        timed_dict.reset_expiration()

        # Verify expiration was updated
        assert timed_dict.expiration is not None
        assert timed_dict.expiration > initial_expiration

    @pytest.mark.parametrize(
        ("manager_name", "has_lifetime"),
        [
            ("pause_timer", True),
            ("pause_timer", False),
            ("pause_reset_timer", True),
        ],
        ids=["pause_lifetime", "pause_no_lifetime", "pause_reset_lifetime"],
    )
    def test_context_managers(self, manager_name: str, has_lifetime: bool) -> None:
        """Tests context managers for pausing/resetting timer."""
        # Setup
        if has_lifetime:
            td = self.UnitTestClass({"a": 1})
            td.lifetime = 10.0
            initial_expiration = td.expiration
            assert initial_expiration is not None
        else:
            td = self.UnitTestClass({"a": 1})
            assert td.expiration is None
            initial_expiration = None

        # Execute context manager
        if manager_name == "pause_timer":
            cm = td.pause_timer()
        else:
            cm = td.pause_reset_timer()

        with cm:
            assert td.is_timed is False
            if manager_name == "pause_timer":
                assert td.expiration is None

            # Modify
            td["d"] = 4

        # Verify after
        assert td.is_timed is True
        if has_lifetime:  # type: ignore[unreachable]
            assert td.expiration is not None
            if manager_name == "pause_reset_timer":
                assert td.expiration > initial_expiration
        else:
            assert td.expiration is None

        assert td["d"] == 4

    def test_clear_condition(self, timed_dict: TimedDict) -> None:
        """Tests the clear_condition method.

        This test verifies that the clear_condition method returns the correct value.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Initially, condition should be False
        assert timed_dict.clear_condition() is False

        # Wait for expiration
        time.sleep(1.1)  # Slightly more than the 1.0 second lifetime

        # Now condition should be True
        assert timed_dict.clear_condition() is True

        # Disable timing
        timed_dict.is_timed = False
        assert timed_dict.clear_condition() is False

        # Re-enable timing
        timed_dict.is_timed = True
        assert timed_dict.clear_condition() is True

    def test_verify(self, timed_dict: TimedDict) -> None:
        """Tests the verify method.

        This test verifies that the dictionary is cleared when the expiration time is reached.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Initially, dictionary should have items
        assert len(timed_dict) == 3

        # Wait for expiration
        time.sleep(1.1)  # Slightly more than the 1.0 second lifetime

        # Call verify (this should clear the dictionary)
        timed_dict.verify()

        # Verify dictionary is now empty
        assert len(timed_dict) == 0

    def test_auto_clearing(self, timed_dict: TimedDict) -> None:
        """Tests that the dictionary automatically clears when accessed after expiration.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Initially, dictionary should have items
        assert len(timed_dict) == 3

        # Wait for expiration
        time.sleep(1.1)  # Slightly more than the 1.0 second lifetime

        # Access the data property (should trigger verify)
        data = timed_dict.data

        # Verify dictionary is now empty
        assert len(data) == 0
        assert len(timed_dict) == 0

    @pytest.mark.parametrize(("lifetime", "should_clear"), [(0, True), (-1, True), (None, False)])
    def test_lifetime_clearing(self, lifetime: float | None, should_clear: bool) -> None:
        """Tests the behavior with different lifetimes.

        Args:
            lifetime: The lifetime value to test.
            should_clear: Whether the dictionary should clear immediately or on verification.
        """
        # Create dictionary
        td = self.UnitTestClass({"a": 1, "b": 2})
        assert len(td) == 2

        # Set lifetime
        td.lifetime = lifetime

        if should_clear:
            # Dictionary should clear immediately
            assert len(td) == 0
        else:
            # Dictionary should not clear
            assert len(td) == 2
            td.verify()
            assert len(td) == 2
