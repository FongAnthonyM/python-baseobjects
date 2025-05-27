#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basecallable_performance.py
Performance tests for the BaseCallable class in the baseobjects package.
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
import timeit
from typing import Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases import BaseCallable
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Callable
class TestBaseCallable(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseCallable class.

    This class tests the performance of the BaseCallable class, which is the base class for callable objects in the
    baseobjects package. It creates test subclasses of BaseCallable to test with.
    """
    # Class Definitions #
    class BaseTestCallable(BaseCallable):
        """A subclass of BaseCallable for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

    class NormalCallable:
        """A normal Python callable object for comparison with BaseCallable."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            self.func = lambda x: x * 2

        def __call__(self, *args, **kwargs):
            """Call the wrapped function."""
            return self.func(*args, **kwargs)

    # Attributes #
    class_: Type[BaseTestCallable] = BaseTestCallable

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_callable(self) -> "TestBaseCallable.BaseTestCallable":
        """Create a test callable instance for use in tests.

        Returns:
            BaseTestCallable: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self, test_callable: "TestBaseCallable.BaseTestCallable") -> None:
        """Test that instances of BaseTestCallable can be created efficiently.

        Args:
            test_callable: A fixture providing a BaseTestCallable instance.
        """
        assert test_callable is not None

    def test_call_speed(self, test_callable: "TestBaseCallable.BaseTestCallable") -> None:
        """Test the performance of the __call__ method of BaseCallable.

        This test compares the speed of BaseCallable.__call__() with a normal callable object.

        Args:
            test_callable: A fixture providing a BaseTestCallable instance.
        """
        normal = self.NormalCallable()
        arg = 5

        def call_base() -> None:
            test_callable(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_as_function_speed(self, test_callable: "TestBaseCallable.BaseTestCallable") -> None:
        """Test the performance of the as_function method of BaseCallable.

        This test measures the time it takes to convert a BaseCallable to a function.

        Args:
            test_callable: A fixture providing a BaseTestCallable instance.
        """
        # Calculate the mean time in microseconds for the as_function method
        conversion_time = timeit.timeit(test_callable.as_function, number=self.timeit_runs)
        mean_conversion = conversion_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nConversion to function: {mean_conversion:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_conversion < 100  # 100 microseconds is a reasonable threshold



# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
