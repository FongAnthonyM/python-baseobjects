#!/usr/bin/env python
"""basecallable_performance.py
Performance tests for the BaseCallable class in the baseobjects.bases package.
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
from collections.abc import Callable
from types import MethodType
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseCallable
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def simple_function(x: int) -> int:
    """A simple function that doubles its input."""
    return x * 2


def simple_coroutine_function(x: int) -> int:
    """A simple coroutine function that doubles its input."""

    async def inner():
        return x * 2

    return inner()


class NormalCallable:
    """A normal Python callable object for comparison with BaseCallable."""

    def __init__(self, func: Callable | None = None) -> None:
        """Initialize with a function."""
        self.func = func or simple_function

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the wrapped function."""
        return self.func(*args, **kwargs)


class TestBaseCallablePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseCallable class.

    This test suite measures the performance of various operations on BaseCallable objects
    and compares them with standard Python implementations.
    """

    # Class Definitions #
    class TestCallable(BaseCallable):
        """A subclass of BaseCallable for testing purposes."""

        def __init__(self, func: Callable | None = None) -> None:
            """Initialize with a function."""
            super().__init__(func or simple_function)

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_callable(self) -> "TestBaseCallablePerformance.TestCallable":
        """Create a test callable instance for use in tests.

        Returns:
            TestCallable: An instance of the test class.
        """
        return self.TestCallable()

    @pytest.fixture
    def test_normal_callable(self) -> NormalCallable:
        """Create a normal callable instance for comparison.

        Returns:
            NormalCallable: A standard Python callable object.
        """
        return NormalCallable()

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the BaseCallable class.

        This test compares the speed of creating BaseCallable instances with creating
        standard Python callable objects.
        """

        def create_base_callable() -> None:
            self.TestCallable(simple_function)

        # Calculate the mean time in microseconds for BaseCallable
        base_time = timeit.timeit(create_base_callable, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Print the performance comparison
        print(f"\nBaseCallable instance creation: {mean_base:.3f} μs or {mean_base / self.call_speed:.3f} cu")

    def test_call_performance(
        self,
        test_callable: "TestBaseCallablePerformance.TestCallable",
        test_normal_callable: NormalCallable,
    ) -> None:
        """Test the performance of the __call__ method of BaseCallable.

        This test compares the speed of BaseCallable.__call__() with a normal callable object.

        Args:
            test_callable: A fixture providing a TestCallable instance.
            test_normal_callable: A fixture providing a NormalCallable instance.
        """
        arg = 5

        def call_base() -> None:
            test_callable(arg)

        def call_normal() -> None:
            test_normal_callable(arg)

        # Calculate the mean time in microseconds for BaseCallable
        base_time = timeit.timeit(call_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for NormalCallable
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"BaseCallable.__call__: {mean_base:.3f} μs ({percent:.3f}% of normal callable time)")
        assert percent < self.speed_tolerance

    def test_func_property_performance(self, test_callable: "TestBaseCallablePerformance.TestCallable") -> None:
        """Test the performance of the __func__ property of BaseCallable.

        This test measures the time it takes to get and set the __func__ property.

        Args:
            test_callable: A fixture providing a TestCallable instance.
        """

        def get_func() -> None:
            _ = test_callable.__func__

        def set_func() -> None:
            test_callable.__func__ = simple_function

        # Calculate the mean time in microseconds for getting __func__
        get_time = timeit.timeit(get_func, number=self.timeit_runs)
        mean_get = get_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for setting __func__
        set_time = timeit.timeit(set_func, number=self.timeit_runs)
        mean_set = set_time / self.timeit_runs * 1000000

        # Print the performance results
        print(f"\nBaseCallable.__func__ getter: {mean_get:.3f} μs or {mean_get / self.call_speed:.3f} cu")
        print(f"BaseCallable.__func__ setter: {mean_set:.3f} μs or {mean_set / self.call_speed:.3f} cu")

        # No direct comparison, just ensure they're reasonably fast
        assert mean_get < 10  # 10 microseconds is a reasonable threshold for property access
        assert mean_set < 100  # 100 microseconds is a reasonable threshold for property setting

    def test_as_function_performance(self, test_callable: "TestBaseCallablePerformance.TestCallable") -> None:
        """Test the performance of the as_function method of BaseCallable.

        This test measures the time it takes to convert a BaseCallable to a function.

        Args:
            test_callable: A fixture providing a TestCallable instance.
        """

        def convert_to_function() -> None:
            test_callable.as_function()

        # Calculate the mean time in microseconds for the as_function method
        conversion_time = timeit.timeit(convert_to_function, number=self.timeit_runs)
        mean_conversion = conversion_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseCallable.as_function: {mean_conversion:.3f} μs or {mean_conversion / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_conversion < 100  # 100 microseconds is a reasonable threshold

    def test_bind_builtin_performance(self, test_callable: "TestBaseCallablePerformance.TestCallable") -> None:
        """Test the performance of the bind_builtin method of BaseCallable.

        This test compares the speed of BaseCallable.bind_builtin() with creating a method using MethodType.

        Args:
            test_callable: A fixture providing a TestCallable instance.
        """

        class TestObject:
            def example_method(self, x: int) -> int:
                return x * 2

        obj = TestObject()

        def bind_base() -> None:
            test_callable.bind_builtin(obj)

        def bind_standard() -> None:
            obj.example_method

        # Calculate the mean time in microseconds for BaseCallable.bind_builtin
        base_time = timeit.timeit(bind_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for standard method binding
        standard_time = timeit.timeit(bind_standard, number=self.timeit_runs)
        mean_standard = standard_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_standard) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_standard:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"BaseCallable.bind_builtin: {mean_base:.3f} μs ({percent:.3f}% of standard method binding time)")
        assert percent < 200

    def test_bind_wrapped_performance(self, test_callable: "TestBaseCallablePerformance.TestCallable") -> None:
        """Test the performance of the bind_wrapped method of BaseCallable.

        This test measures the time it takes to bind the wrapped function to an instance.

        Args:
            test_callable: A fixture providing a TestCallable instance.
        """

        class TestObject:
            pass

        obj = TestObject()

        def bind_wrapped() -> None:
            test_callable.bind_wrapped(obj)

        # Calculate the mean time in microseconds for BaseCallable.bind_wrapped
        bind_time = timeit.timeit(bind_wrapped, number=self.timeit_runs)
        mean_bind = bind_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseCallable.bind_wrapped: {mean_bind:.3f} μs or {mean_bind / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_bind < 100  # 100 microseconds is a reasonable threshold

    def test_coroutine_detection_performance(self) -> None:
        """Test the performance of coroutine detection in BaseCallable.

        This test measures the time it takes to create a BaseCallable with a coroutine function
        compared to a regular function.
        """

        def create_with_regular() -> None:
            self.TestCallable(simple_function)

        def create_with_coroutine() -> None:
            self.TestCallable(simple_coroutine_function)

        # Calculate the mean time in microseconds for regular function
        regular_time = timeit.timeit(create_with_regular, number=self.timeit_runs)
        mean_regular = regular_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for coroutine function
        coroutine_time = timeit.timeit(create_with_coroutine, number=self.timeit_runs)
        mean_coroutine = coroutine_time / self.timeit_runs * 1000000
        percent = (mean_coroutine / mean_regular) * 100

        # Print the performance comparison
        print(f"\nOld: {mean_coroutine:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"BaseCallable with coroutine: {mean_coroutine:.3f} μs ({percent:.3f}% of regular function time)")
        # Coroutine detection might be slower, but should still be within reasonable bounds
        assert percent < 200  # 200% is a reasonable threshold for coroutine detection overhead


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
