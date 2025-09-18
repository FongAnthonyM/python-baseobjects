"""timeddict_test.py
Tests for the TimedDict class in the baseobjects package.

This module provides tests for the TimedDict class, which extends BaseDict to implement a dictionary
that clears its contents after a specified time has elapsed.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import TimedDict
from src.baseobjects.testsuite.bases import BaseObjectTestSuite


# Definitions #
# Tests #
class TestTimedDict(BaseObjectTestSuite):
    """Test the TimedDict class.

    This class tests the functionality of the TimedDict class, which extends BaseDict to implement a dictionary
    that clears its contents after a specified time has elapsed.
    """

    # Attributes #
    TestClass: Type[TimedDict] = TimedDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_dict(self) -> TimedDict:
        """Create an empty TimedDict for testing.

        Returns:
            TimedDict: An empty TimedDict.
        """
        return self.TestClass()

    @pytest.fixture
    def simple_dict(self) -> TimedDict:
        """Create a TimedDict with a few items for testing.

        Returns:
            TimedDict: A TimedDict with a few items.
        """
        return self.TestClass({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def timed_dict(self) -> TimedDict:
        """Create a TimedDict with a lifetime for testing.

        Returns:
            TimedDict: A TimedDict with a lifetime.
        """
        td = self.TestClass({"a": 1, "b": 2, "c": 3})
        td.lifetime = 1.0  # 1 second lifetime
        return td

    @pytest.fixture
    def test_object(self) -> TimedDict:
        """Create a test object for testing.

        Returns:
            TimedDict: A TimedDict with a few items.
        """
        # Use function scope to ensure a fresh object for each test
        return self.TestClass({"a": 1, "b": 2, "c": 3, "d": 4})

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedDict can be created with various parameters.

        This test verifies that TimedDict instances can be created with no arguments,
        a dictionary, or keyword arguments.
        """
        # Create an empty instance
        td = self.TestClass()
        assert td is not None
        assert isinstance(td, self.TestClass)
        assert len(td) == 0
        assert td.is_timed is True
        assert td.lifetime is None
        assert td.expiration is None

        # Create an instance with a dictionary
        mapping = {"a": 1, "b": 2, "c": 3}
        td = self.TestClass(mapping)
        assert td is not None
        assert isinstance(td, self.TestClass)
        assert len(td) == 3
        assert td["a"] == 1
        assert td["b"] == 2
        assert td["c"] == 3

        # Create an instance with keyword arguments
        td = self.TestClass(a=1, b=2, c=3)
        assert td is not None
        assert isinstance(td, self.TestClass)
        assert len(td) == 3
        assert td["a"] == 1
        assert td["b"] == 2
        assert td["c"] == 3

    def test_copy(self, test_object: TimedDict) -> None:
        """Test the copy behavior of the object.

        This test verifies that copy creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = copy.copy(test_object)

        # Validate
        assert obj_copy is not test_object  # Different objects
        assert isinstance(obj_copy, self.TestClass)  # Same type
        assert obj_copy == test_object  # Equal values
        assert obj_copy.is_timed == test_object.is_timed
        assert obj_copy.lifetime == test_object.lifetime
        assert obj_copy.expiration == test_object.expiration

    def test_copy_method(self, test_object: TimedDict) -> None:
        """Test the copy method behavior of the object.

        This test verifies that the copy method creates a new object with the same attributes.

        Args:
            test_object: A fixture providing a test object instance.
        """
        # Copy Object
        obj_copy = test_object.copy()

        # Validate
        assert obj_copy is not test_object  # Different objects
        assert isinstance(obj_copy, self.TestClass)  # Same type
        assert obj_copy == test_object  # Equal values
        assert obj_copy.is_timed == test_object.is_timed
        assert obj_copy.lifetime == test_object.lifetime
        assert obj_copy.expiration == test_object.expiration

    def test_deepcopy(self, test_object: TimedDict, memo: dict | None = None) -> None:
        """Test the deep copy behavior of the object.

        This test verifies that deepcopy creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set a lifetime to test copying of all attributes
        test_object.lifetime = 10.0

        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = copy.deepcopy(test_object, memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy == test_object
        assert obj_deepcopy.is_timed == test_object.is_timed
        assert obj_deepcopy.lifetime == test_object.lifetime
        assert obj_deepcopy.expiration is not None

        # Verify that modifying the deepcopy doesn't affect the original
        obj_deepcopy["deepcopy_key"] = 300
        assert "deepcopy_key" in obj_deepcopy
        assert "deepcopy_key" not in test_object

    def test_deepcopy_method(self, test_object: TimedDict, memo: dict | None = None) -> None:
        """Test the deepcopy method behavior of the object.

        This test verifies that the deepcopy method creates a new object with new mutable attributes.

        Args:
            test_object: A fixture providing a test object instance.
            memo: A memo dictionary to pass to deepcopy.
        """
        # Set a lifetime to test copying of all attributes
        test_object.lifetime = 10.0

        # Deep Copy Object
        if memo is None:
            memo = {}
        obj_deepcopy = test_object.deepcopy(memo=memo)

        # Validate
        assert obj_deepcopy is not test_object
        assert isinstance(obj_deepcopy, self.TestClass)
        assert obj_deepcopy == test_object
        assert obj_deepcopy.is_timed == test_object.is_timed
        assert obj_deepcopy.lifetime == test_object.lifetime
        assert obj_deepcopy.expiration is not None

        # Verify that modifying the deepcopy doesn't affect the original
        obj_deepcopy["deepcopy_method_key"] = 400
        assert "deepcopy_method_key" in obj_deepcopy
        assert "deepcopy_method_key" not in test_object

    def test_pickling(self, test_object: TimedDict) -> None:
        """Test pickling and unpickling of the object.

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
        assert isinstance(unpickled, self.TestClass)
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

    def test_lifetime_property(self, empty_dict: TimedDict) -> None:
        """Test the lifetime property.

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
        """Test the data property.

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

    def test_clear(self, simple_dict: TimedDict) -> None:
        """Test the clear method.

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
        """Test the reset_expiration method.

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

    def test_pause_timer(self, timed_dict: TimedDict) -> None:
        """Test the pause_timer context manager.

        This test verifies that the timer is paused within the context manager.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Get initial expiration
        initial_expiration = timed_dict.expiration
        assert initial_expiration is not None

        # Use pause_timer context manager
        with timed_dict.pause_timer():
            assert timed_dict.is_timed is False
            assert timed_dict.expiration is None

            # Modify dictionary during pause
            timed_dict["d"] = 4

        # Verify timer is resumed after context
        assert timed_dict.is_timed is True
        assert timed_dict.expiration is not None
        assert timed_dict["d"] == 4

    def test_pause_reset_timer(self, timed_dict: TimedDict) -> None:
        """Test the pause_reset_timer context manager.

        This test verifies that the timer is paused within the context manager and reset afterward.

        Args:
            timed_dict: A TimedDict with a lifetime.
        """
        # Get initial expiration
        initial_expiration = timed_dict.expiration
        assert initial_expiration is not None

        # Use pause_reset_timer context manager
        with timed_dict.pause_reset_timer():
            assert timed_dict.is_timed is False

            # Modify dictionary during pause
            timed_dict["d"] = 4

        # Verify timer is resumed and reset after context
        assert timed_dict.is_timed is True
        assert timed_dict.expiration is not None
        assert timed_dict.expiration > initial_expiration
        assert timed_dict["d"] == 4

    def test_clear_condition(self, timed_dict: TimedDict) -> None:
        """Test the clear_condition method.

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
        """Test the verify method.

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
        """Test that the dictionary automatically clears when accessed after expiration.

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

    def test_edge_case_zero_lifetime(self) -> None:
        """Test the behavior with a zero lifetime."""
        # Create dictionary with zero lifetime
        td = self.TestClass({"a": 1, "b": 2})

        # Dictionary should clear immediately when lifetime is set to zero
        # because setting lifetime calls reset_expiration which sets expiration to current time + lifetime
        # and when lifetime is 0, expiration is set to current time, making clear_condition() return True
        assert len(td) == 2
        td.lifetime = 0

        # Dictionary should already be empty after setting lifetime to zero
        assert len(td) == 0

    def test_edge_case_negative_lifetime(self) -> None:
        """Test the behavior with a negative lifetime."""
        # Create dictionary with negative lifetime
        td = self.TestClass({"a": 1, "b": 2})

        # Dictionary should clear immediately when lifetime is set to a negative value
        # because setting lifetime calls reset_expiration which sets expiration to current time + lifetime
        # and when lifetime is negative, expiration is set to a time in the past, making clear_condition() return True
        assert len(td) == 2
        td.lifetime = -1

        # Dictionary should already be empty after setting lifetime to a negative value
        assert len(td) == 0

    def test_edge_case_none_lifetime(self) -> None:
        """Test the behavior with a None lifetime."""
        # Create dictionary with None lifetime
        td = self.TestClass({"a": 1, "b": 2})
        td.lifetime = None

        # Dictionary should not clear when verified
        assert len(td) == 2
        td.verify()
        assert len(td) == 2


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
