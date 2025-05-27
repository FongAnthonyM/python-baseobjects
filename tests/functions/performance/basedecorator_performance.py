#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basedecorator_performance.py
Performance tests for the BaseDecorator class in the baseobjects package.
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
from typing import Type, Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions.basedecorator import BaseDecorator
from tests.bases.performance.base_performance import ClassPerformanceTest


# Definitions #
# Base Decorator
class TestBaseDecorator(ClassPerformanceTest):
    """Test the performance of the BaseDecorator class.

    This class tests the performance of the BaseDecorator class, which is an abstract class
    that implements the basic structure for creating decorators.
    """
    # Class Definitions #
    class BaseTestDecorator(BaseDecorator):
        """A subclass of BaseDecorator for testing purposes."""
        # Magic Methods #
        def __init__(self) -> None:
            """Initialize with a simple function."""
            super().__init__(lambda x: x * 2)

        def call(self, *args: Any, **kwargs: Any) -> Any:
            """The wrapper method for this decorator."""
            return self.func(*args, **kwargs)

    # Attributes #
    timeit_runs: int = 1000000
    speed_tolerance: int = 400

    class_: Type[BaseTestDecorator] = BaseTestDecorator

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_decorator(self) -> "TestBaseDecorator.BaseTestDecorator":
        """Create a test decorator instance for use in tests.

        Returns:
            BaseTestDecorator: An instance of the test class.
        """
        return self.class_()

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of BaseTestDecorator can be created efficiently."""
        # Define the performance test functions
        def create_base_decorator() -> None:
            self.class_()

        def create_normal_function() -> None:
            lambda x: x * 2

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base_decorator, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal_function, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_call_speed(self, test_decorator: "TestBaseDecorator.BaseTestDecorator") -> None:
        """Test the performance of the __call__ method of BaseDecorator.

        This test compares the speed of BaseDecorator.__call__() with a normal function.

        Args:
            test_decorator: A fixture providing a BaseTestDecorator instance.
        """
        # Create a normal function to compare against
        def normal(x: int) -> int:
            return x * 2

        arg = 5

        # Define the performance test functions
        def call_base_decorator() -> None:
            test_decorator(arg)

        def call_normal() -> None:
            normal(arg)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(call_base_decorator, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_construct_call_speed(self) -> None:
        """Test the performance of the construct_call method of BaseDecorator.

        This test compares the speed of BaseDecorator.construct_call() with a normal decorator.
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
            decorator = self.class_()
            decorator.construct_call(test_func)

        def construct_normal_decorator() -> None:
            normal_decorator(test_func)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(construct_base_decorator, number=self.timeit_runs // 10)
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(construct_normal_decorator, number=self.timeit_runs // 10)
        mean_old = old_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_old:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"New: {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])