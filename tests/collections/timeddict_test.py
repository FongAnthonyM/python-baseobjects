#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timeddict_test.py
Tests for the TimedDict class in the baseobjects package.
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
import time
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.collections import TimedDict
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestTimedDict(ClassTest):
    """Test the TimedDict class.

    This class tests the functionality of the TimedDict class, which is a dictionary that clears its contents after a
    specified time has passed.
    """

    # Attributes #
    class_: Type[TimedDict] = TimedDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def empty_dict(self) -> TimedDict:
        """Create an empty TimedDict for testing.

        Returns:
            An empty TimedDict.
        """
        return self.class_()

    @pytest.fixture
    def populated_dict(self) -> TimedDict:
        """Create a TimedDict with items for testing.

        Returns:
            A TimedDict with items.
        """
        return self.class_({"a": 1, "b": 2, "c": 3})

    @pytest.fixture
    def short_lived_dict(self) -> TimedDict:
        """Create a TimedDict with a short lifetime for testing.

        Returns:
            A TimedDict with a short lifetime.
        """
        d = self.class_({"a": 1, "b": 2, "c": 3})
        d.lifetime = 0.1  # 100 milliseconds
        d.reset_expiration()
        return d

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of TimedDict can be created with various parameters.

        This test verifies that TimedDict instances can be created with no items, a dictionary, or keyword arguments.
        """
        # Create an empty instance
        td = self.class_()
        assert td is not None
        assert len(td) == 0
        assert td.is_timed is True
        assert td.lifetime is None
        assert td.expiration is None

        # Create an instance with a dictionary
        items = {"a": 1, "b": 2, "c": 3}
        td = self.class_(items)
        assert td is not None
        assert len(td) == 3
        assert td["a"] == 1
        assert td["b"] == 2
        assert td["c"] == 3

        # Create an instance with keyword arguments
        td = self.class_(a=1, b=2, c=3)
        assert td is not None
        assert len(td) == 3
        assert td["a"] == 1
        assert td["b"] == 2
        assert td["c"] == 3

    def test_data_property(self, populated_dict: TimedDict) -> None:
        """Test the data property of TimedDict.

        This test verifies that the data property returns the dictionary data and calls verify.

        Args:
            populated_dict: A TimedDict with items.
        """
        assert populated_dict.data == {"a": 1, "b": 2, "c": 3}
        
        # Test that verify is called
        populated_dict.lifetime = 0
        populated_dict.expiration = 0  # Set to expire immediately
        assert populated_dict.data == {}  # Should be cleared by verify

    def test_clear(self, populated_dict: TimedDict) -> None:
        """Test the clear method of TimedDict.

        This test verifies that the clear method removes all items from the dictionary and resets the expiration.

        Args:
            populated_dict: A TimedDict with items.
        """
        # Set a lifetime and expiration
        populated_dict.lifetime = 10
        populated_dict.reset_expiration()
        initial_expiration = populated_dict.expiration
        
        # Clear the dictionary
        populated_dict.clear()
        assert len(populated_dict) == 0
        assert populated_dict.expiration != initial_expiration  # Expiration should be reset

    def test_reset_expiration(self) -> None:
        """Test the reset_expiration method of TimedDict.

        This test verifies that the reset_expiration method updates the expiration to a new future time.
        """
        td = self.class_()
        
        # Test with no lifetime
        td.reset_expiration()
        assert td.expiration is None
        
        # Test with a lifetime
        td.lifetime = 10
        td.reset_expiration()
        assert td.expiration is not None
        assert td.expiration > time.perf_counter()  # Expiration should be in the future

    def test_pause_timer(self, short_lived_dict: TimedDict) -> None:
        """Test the pause_timer context manager of TimedDict.

        This test verifies that the pause_timer context manager stops the timer while active and resumes it with the
        remaining time when exited.

        Args:
            short_lived_dict: A TimedDict with a short lifetime.
        """
        # Get initial expiration
        initial_expiration = short_lived_dict.expiration
        
        # Pause the timer
        with short_lived_dict.pause_timer():
            assert short_lived_dict.is_timed is False
            assert short_lived_dict.expiration is None
            
            # Sleep for longer than the lifetime
            time.sleep(0.2)
            
            # Dictionary should not be cleared
            assert len(short_lived_dict) == 3
        
        # Timer should be resumed
        unpaused_expiration = short_lived_dict.expiration
        assert short_lived_dict.is_timed is True
        assert unpaused_expiration is not None
        
        # Expiration should be close to the original (accounting for the time spent in the context manager)
        # This is approximate since we can't know exactly how much time passed (time.sleep may not be accurate)
        assert abs(unpaused_expiration - (initial_expiration + 0.2)) < 0.001

    def test_pause_reset_timer(self, short_lived_dict: TimedDict) -> None:
        """Test the pause_reset_timer context manager of TimedDict.

        This test verifies that the pause_reset_timer context manager stops the timer while active
        and resets it when exited.

        Args:
            short_lived_dict: A TimedDict with a short lifetime.
        """
        # Get initial expiration
        initial_expiration = short_lived_dict.expiration
        
        # Pause the timer
        with short_lived_dict.pause_reset_timer():
            assert short_lived_dict.is_timed is False
            
            # Sleep for longer than the lifetime
            time.sleep(0.2)
            
            # Dictionary should not be cleared
            assert len(short_lived_dict) == 3
        
        # Timer should be resumed and reset
        assert short_lived_dict.is_timed is True
        assert short_lived_dict.expiration is not None
        assert short_lived_dict.expiration > initial_expiration  # New expiration should be later

    def test_clear_condition(self) -> None:
        """Test the clear_condition method of TimedDict.

        This test verifies that the clear_condition method returns True when the dictionary should be cleared.
        """
        td = self.class_()
        
        # Test with no lifetime
        assert td.clear_condition() is False
        
        # Test with a future expiration
        td.lifetime = 10
        td.reset_expiration()
        assert td.clear_condition() is False
        
        # Test with a past expiration
        td.expiration = time.perf_counter() - 1  # Set to expire 1 second ago
        assert td.clear_condition() is True
        
        # Test with is_timed=False
        td.is_timed = False
        assert td.clear_condition() is False

    def test_verify(self, short_lived_dict: TimedDict) -> None:
        """Test the verify method of TimedDict.

        This test verifies that the verify method clears the dictionary when the expiration has passed.

        Args:
            short_lived_dict: A TimedDict with a short lifetime.
        """
        # Dictionary should not be cleared initially
        short_lived_dict.verify()
        assert len(short_lived_dict) == 3
        
        # Sleep for longer than the lifetime
        time.sleep(0.2)
        
        # Dictionary should be cleared after verify
        short_lived_dict.verify()
        assert len(short_lived_dict) == 0

    def test_automatic_clearing(self, short_lived_dict: TimedDict) -> None:
        """Test that the dictionary is automatically cleared when accessed after expiration.

        This test verifies that accessing the dictionary after the expiration time has passed
        automatically clears it.

        Args:
            short_lived_dict: A TimedDict with a short lifetime.
        """
        # Dictionary should not be cleared initially
        assert len(short_lived_dict) == 3
        
        # Sleep for longer than the lifetime
        time.sleep(0.2)
        
        # Dictionary should be cleared when accessed
        assert len(short_lived_dict) == 0

    def test_standard_dict_methods(self, populated_dict: TimedDict) -> None:
        """Test that standard dictionary methods work with TimedDict.

        This test verifies that TimedDict inherits and correctly implements standard dictionary methods.

        Args:
            populated_dict: A TimedDict with items.
        """
        # Test __getitem__
        assert populated_dict["a"] == 1
        
        # Test __setitem__
        populated_dict["d"] = 4
        assert populated_dict["d"] == 4
        
        # Test __delitem__
        del populated_dict["a"]
        assert "a" not in populated_dict
        
        # Test keys, values, items
        assert set(populated_dict.keys()) == {"b", "c", "d"}
        assert set(populated_dict.values()) == {2, 3, 4}
        assert set(populated_dict.items()) == {("b", 2), ("c", 3), ("d", 4)}
        
        # Test update
        populated_dict.update({"e": 5, "f": 6})
        assert populated_dict["e"] == 5
        assert populated_dict["f"] == 6
        
        # Test pop
        value = populated_dict.pop("b")
        assert value == 2
        assert "b" not in populated_dict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])