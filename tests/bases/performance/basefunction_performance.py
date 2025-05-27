#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basefunction_performance.py
Performance tests for the BaseFunction class in the baseobjects package.
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
from src.baseobjects.bases import BaseFunction
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Function
class TestBaseFunction(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseFunction class.

    This class tests the performance of the BaseFunction class, which is a subclass of BaseCallable for creating
    function-like objects.
    """
    # Class Definitions #
    class BaseTestFunction(BaseFunction):
        """A subclass of BaseFunction for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

    class ExampleClass:
        """A class to own methods for testing."""

        base_function = BaseFunction(lambda self, x: x * 2)

        def normal_function(self, x):
            """A normal method."""
            return x * 2

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[BaseTestFunction] = BaseTestFunction

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function(self) -> "TestBaseFunction.BaseTestFunction":
        """Create a test function instance for use in tests.

        Returns:
            BaseTestFunction: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self, test_function: "TestBaseFunction.BaseTestFunction") -> None:
        """Test that instances of BaseTestFunction can be created efficiently.

        Args:
            test_function: A fixture providing a BaseTestFunction instance.
        """
        assert test_function is not None

    def test_call_speed(self, test_function: "TestBaseFunction.BaseTestFunction") -> None:
        """Test the performance of the __call__ method of BaseFunction.

        This test compares the speed of BaseFunction.__call__() with a normal function-like object.

        Args:
            test_function: A fixture providing a BaseTestFunction instance.
        """
        # Create a normal function-like object to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_base() -> None:
            test_function(arg)

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
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_bind_speed(self) -> None:
        """Test the performance of the bind method of BaseFunction.

        This test compares the speed of BaseFunction.bind() with a normal function binding.
        """
        example_class = self.ExampleClass()
        arg = 2

        def bind_base() -> None:
            getattr(example_class, "base_function")(arg)

        def bind_normal() -> None:
            getattr(example_class, "normal_function")(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(bind_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(bind_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])