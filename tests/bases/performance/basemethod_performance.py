#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basemethod_performance.py
Performance tests for the BaseMethod class in the baseobjects package.
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
from src.baseobjects.bases import BaseMethod
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Method
class TestBaseMethod(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseMethod class.

    This class tests the performance of the BaseMethod class, which is a subclass of BaseCallable for creating
    method-like objects.
    """
    # Class Definitions #
    class MethodOwner:
        """A class to own methods for testing."""
        def test_method(self, x):
            """A test method."""
            return x * 2

    class BaseTestMethod(BaseMethod):
        """A subclass of BaseMethod for testing purposes."""
        # Magic Methods #
        def __init__(self, instance=None) -> None:
            """Initialize with a simple function and optional instance."""
            super().__init__(lambda self, x: x * 2, instance=instance)

    class NormalMethod:
        """A normal Python method-like object for comparison."""
        # Magic Methods #
        def __init__(self, instance=None) -> None:
            """Initialize with a simple function and optional instance."""
            self.instance = instance
            self.func = lambda self, x: x * 2
            
        def __call__(self, *args, **kwargs):
            """Call the wrapped function with the instance."""
            return self.func(self.instance, *args, **kwargs)

    # Attributes #
    class_: Type[BaseTestMethod] = BaseTestMethod

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def method_owner(self) -> "TestBaseMethod.MethodOwner":
        """Create a method owner instance for testing.

        Returns:
            MethodOwner: An instance to own methods.
        """
        return self.MethodOwner()

    @pytest.fixture
    def test_method(self, method_owner) -> "TestBaseMethod.BaseTestMethod":
        """Create a test method instance for use in tests.

        Args:
            method_owner: The instance to bind the method to.

        Returns:
            BaseTestMethod: An instance of the test class.
        """
        return self.class_(instance=method_owner)

    # Tests
    def test_instance_creation(self, test_method: "TestBaseMethod.BaseTestMethod") -> None:
        """Test that instances of BaseTestMethod can be created efficiently.

        Args:
            test_method: A fixture providing a BaseTestMethod instance.
        """
        assert test_method is not None

    def test_call_speed(self, test_method: "TestBaseMethod.BaseTestMethod", method_owner) -> None:
        """Test the performance of the __call__ method of BaseMethod.

        This test compares the speed of BaseMethod.__call__() with a normal method-like object.

        Args:
            test_method: A fixture providing a BaseTestMethod instance.
            method_owner: The instance the method is bound to.
        """
        normal = self.NormalMethod(instance=method_owner)
        arg = 5

        def call_base() -> None:
            test_method(arg)

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

    def test_bind_speed(self, method_owner) -> None:
        """Test the performance of the bind method of BaseMethod.

        This test measures the time it takes to bind a BaseMethod to an instance.

        Args:
            method_owner: The instance to bind the method to.
        """
        method = self.BaseTestMethod()

        def bind_method() -> None:
            method.bind(instance=method_owner)

        # Calculate the mean time in microseconds for the bind method
        bind_time = timeit.timeit(bind_method, number=self.timeit_runs)
        mean_bind = bind_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBinding method: {mean_bind:.3f} μs")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_bind < 100  # 100 microseconds is a reasonable threshold


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])