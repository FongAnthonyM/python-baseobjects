#!/usr/bin/env python
"""basedecorator_performance.py
Performance tests for the BaseDecorator class in the baseobjects.functions package.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions.basedecorator import BaseDecorator
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestBaseDecoratorPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseDecorator class.

    This test suite measures the performance of various operations on BaseDecorator objects
    and compares them with standard Python implementations.

    Attributes:
        timeit_runs: The number of times to run the timeit function.
        speed_tolerance: The maximum speed tolerance in microseconds.
        TestClass: The class being tested.
    """

    # Class Definitions #
    class BaseTestDecorator(BaseDecorator):
        """A subclass of BaseDecorator for testing purposes."""

        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    TestClass: Type[BaseTestDecorator] = BaseTestDecorator

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_decorator(self) -> "TestBaseDecoratorPerformance.BaseTestDecorator":
        """Create a test decorator instance for use in tests.

        Returns:
            BaseTestDecorator: An instance of the test class.
        """
        return self.TestClass()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTestDecorator can be created efficiently.

        This test compares the speed of creating BaseDecorator instances with creating
        standard Python functions.
        """

        def normal_decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        # Define the performance test functions
        def create_base_decorator() -> None:
            self.TestClass()

        def create_normal_function() -> None:
            normal_decorator(lambda x: x * 2)

        # Calculate the mean time in microseconds for the decorator creation
        new_time = timeit.timeit(create_base_decorator, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function creation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function creation: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"BaseDecorator creation: {mean_new:.3f} μs ({percent:.3f}% of normal function creation time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_decorator: "TestBaseDecoratorPerformance.BaseTestDecorator") -> None:
        """Test the performance of the __call__ method of BaseDecorator.

        This test compares the speed of BaseDecorator.__call__() with a normal function.

        Args:
            test_decorator: A fixture providing a BaseTestDecorator instance.
        """

        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        def wrapper(*args, **kwargs):
            return normal(*args, **kwargs)

        arg = 5

        # Define the performance test functions
        def call_base_decorator() -> None:
            test_decorator(arg)

        def call_normal() -> None:
            wrapper(arg)

        # Calculate the mean time in microseconds for the decorator call
        new_time = timeit.timeit(call_base_decorator, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the normal function call
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"BaseDecorator call: {mean_new:.3f} μs ({percent:.3f}% of normal function call time)")
        assert percent < self.speed_tolerance

    def test_wrap_speed(self) -> None:
        """Test the performance of the wrap spped of BaseDecorator.

        This test compares the wrap speed of BaseDecorator with a normal decorator.
        """

        # Create a normal decorator to compare against
        def normal_decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        def test_func(x):
            return x * 2

        # Define the performance test functions
        def construct_base_decorator() -> None:
            self.TestClass()

        def construct_normal_decorator() -> None:
            normal_decorator(test_func)

        # Calculate the mean time in microseconds for the decorator construction
        new_time = timeit.timeit(construct_base_decorator, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the normal decorator construction
        old_time = timeit.timeit(construct_normal_decorator, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNormal decorator wrap: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"BaseDecorator wrap: {mean_new:.3f} μs ({percent:.3f}% of normal decorator construction time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
