#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basereducible_performance.py
Performance tests for the BaseReducible class in the baseobjects package.
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
import pickle
import timeit
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseReducible
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Reducible
class TestBaseReducible(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseReducible class.

    This class tests the performance of the BaseReducible class, which is the base class for objects that implement
    custom pickling behavior in the baseobjects package.
    """
    # Class Definitions #
    class BaseTestReducible(BaseReducible):
        """A subclass of BaseReducible for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            super().__init__()
            self.immutable: int = 0
            self.mutable: dict = {"key": "value"}
            self.nested: list = [1, 2, {"nested_key": "nested_value"}]

    class NormalObject(object):
        """A normal Python object for comparison with BaseReducible."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with immutable and mutable attributes."""
            self.immutable: int = 0
            self.mutable: dict = {"key": "value"}
            self.nested: list = [1, 2, {"nested_key": "nested_value"}]

    # Attributes #
    class_: Type[BaseTestReducible] = BaseTestReducible

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestBaseReducible.BaseTestReducible":
        """Create a test object instance for use in tests.

        Returns:
            BaseTestReducible: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self, test_object: "TestBaseReducible.BaseTestReducible") -> None:
        """Test that instances of BaseTestReducible can be created efficiently.

        Args:
            test_object: A fixture providing a BaseTestReducible instance.
        """
        assert test_object is not None

    def test_pickle_speed(self, test_object: "TestBaseReducible.BaseTestReducible") -> None:
        """Test the performance of pickling a BaseReducible object.

        This test compares the speed of pickling a BaseReducible object with a normal Python object.

        Args:
            test_object: A fixture providing a BaseTestReducible instance.
        """
        normal = self.NormalObject()

        def pickle_base() -> None:
            pickle.dumps(test_object)

        def pickle_normal() -> None:
            pickle.dumps(normal)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(pickle_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(pickle_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_unpickle_speed(self, test_object: "TestBaseReducible.BaseTestReducible") -> None:
        """Test the performance of unpickling a BaseReducible object.

        This test compares the speed of unpickling a BaseReducible object with a normal Python object.

        Args:
            test_object: A fixture providing a BaseTestReducible instance.
        """
        normal = self.NormalObject()
        
        # Pickle the objects first
        pickled_base = pickle.dumps(test_object)
        pickled_normal = pickle.dumps(normal)

        def unpickle_base() -> None:
            pickle.loads(pickled_base)

        def unpickle_normal() -> None:
            pickle.loads(pickled_normal)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(unpickle_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(unpickle_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_getstate_speed(self, test_object: "TestBaseReducible.BaseTestReducible") -> None:
        """Test the performance of the __getstate__ method of BaseReducible.

        This test measures the time it takes to get the state of a BaseReducible object.

        Args:
            test_object: A fixture providing a BaseTestReducible instance.
        """
        # Calculate the mean time in microseconds for the __getstate__ method
        getstate_time = timeit.timeit(test_object.__getstate__, number=self.timeit_runs)
        mean_getstate = getstate_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\n__getstate__: {mean_getstate:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_getstate < 100  # 100 microseconds is a reasonable threshold

    def test_setstate_speed(self, test_object: "TestBaseReducible.BaseTestReducible") -> None:
        """Test the performance of the __setstate__ method of BaseReducible.

        This test measures the time it takes to set the state of a BaseReducible object.

        Args:
            test_object: A fixture providing a BaseTestReducible instance.
        """
        # Get the state to use for setting
        state = test_object.__getstate__()

        def setstate() -> None:
            # Create a new instance and set its state
            obj = self.class_()
            obj.__setstate__(state)

        # Calculate the mean time in microseconds for the __setstate__ method
        setstate_time = timeit.timeit(setstate, number=self.timeit_runs)
        mean_setstate = setstate_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\n__setstate__: {mean_setstate:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_setstate < 100  # 100 microseconds is a reasonable threshold


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])