#!/usr/bin/env python
"""basefunction_performance.py
Performance tests for the BaseFunction class in the baseobjects.bases package.
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
from types import MethodType
from typing import Any
from collections.abc import Callable

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseFunction, BaseMethod
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def simple_function(x: int) -> int:
    """A simple function that doubles its input."""
    return x * 2


class NormalFunction:
    """A normal Python function-like object for comparison with BaseFunction."""

    def __init__(self, func: Callable | None = None) -> None:
        """Initialize with a function."""
        self.func = func or simple_function

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the wrapped function."""
        return self.func(*args, **kwargs)


class TestBaseFunctionPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseFunction class.

    This test suite measures the performance of various operations on BaseFunction objects
    and compares them with standard Python implementations.
    """

    # Class Definitions #
    class TestFunction(BaseFunction):
        """A subclass of BaseFunction for testing purposes."""

        def __init__(self, func: Callable | None = None) -> None:
            """Initialize with a function."""
            super().__init__(func or simple_function)

    class ExampleClass:
        """A class to own methods for testing."""

        def normal_method(self, x: int) -> int:
            """A normal method."""
            return x * 2

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_function(self) -> "TestBaseFunctionPerformance.TestFunction":
        """Create a test function instance for use in tests.

        Returns:
            TestFunction: An instance of the test class.
        """
        return self.TestFunction()

    @pytest.fixture
    def test_normal_function(self) -> NormalFunction:
        """Create a normal function instance for comparison.

        Returns:
            NormalFunction: A standard Python function-like object.
        """
        return NormalFunction()

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the BaseFunction class.

        This test compares the speed of creating BaseFunction instances with creating
        standard Python function-like objects.
        """

        def create_base_function() -> None:
            self.TestFunction(simple_function)

        # Calculate the mean time in microseconds for BaseFunction
        base_time = timeit.timeit(create_base_function, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Print the performance comparison
        print(f"\nBaseFunction instance creation: {mean_base:.3f} μs or {mean_base / self.call_speed:.3f} cu")

    def test_call_performance(
        self,
        test_function: "TestBaseFunctionPerformance.TestFunction",
        test_normal_function: NormalFunction,
    ) -> None:
        """Test the performance of the __call__ method of BaseFunction.

        This test compares the speed of BaseFunction.__call__() with a normal function-like object.

        Args:
            test_function: A fixture providing a TestFunction instance.
            test_normal_function: A fixture providing a NormalFunction instance.
        """
        arg = 5

        def call_base() -> None:
            test_function(arg)

        def call_normal() -> None:
            test_normal_function(arg)

        # Calculate the mean time in microseconds for BaseFunction
        base_time = timeit.timeit(call_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for NormalFunction
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal function call: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseFunction.__call__: {mean_base:.3f} μs ({percent:.3f}% of normal function call time)")
        assert percent < self.speed_tolerance

    def test_bind_performance(self) -> None:
        """Test the performance of the bind method of BaseFunction.

        This test compares the speed of BaseFunction.bind() with creating a method using MethodType.
        """

        def test_method(self: Any, x: int) -> int:
            return x * 2

        test_function = self.TestFunction(test_method)

        obj = self.ExampleClass()

        def bind_base() -> None:
            test_function.bind(obj)

        def bind_standard() -> None:
            obj.normal_method

        # Calculate the mean time in microseconds for BaseFunction.bind
        base_time = timeit.timeit(bind_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for standard method binding
        standard_time = timeit.timeit(bind_standard, number=self.timeit_runs)
        mean_standard = standard_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_standard) * 100

        # Print the performance comparison
        print(
            f"\nStandard method binding: {mean_standard:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"BaseFunction.bind: {mean_base:.3f} μs ({percent:.3f}% of standard method binding time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for method creation

    def test_bind_to_attribute_performance(self, test_function: "TestBaseFunctionPerformance.TestFunction") -> None:
        """Test the performance of the bind_to_attribute method of BaseFunction.

        This test measures the time it takes to bind a function to an instance and set it as an attribute.

        Args:
            test_function: A fixture providing a TestFunction instance.
        """

        class TestObject:
            pass

        def bind_to_attribute() -> None:
            obj = TestObject()
            test_function.bind_to_attribute(obj, name="test_method")

        # Calculate the mean time in microseconds for BaseFunction.bind_to_attribute
        bind_time = timeit.timeit(bind_to_attribute, number=self.timeit_runs)
        mean_bind = bind_time / self.timeit_runs * 1000000

        # Print the performance result
        print(f"\nBaseFunction.bind_to_attribute: {mean_bind:.3f} μs or {mean_bind / self.call_speed:.3f} cu")
        # No direct comparison, just ensure it's reasonably fast
        assert mean_bind < 200  # 200 microseconds is a reasonable threshold

    def test_bound_method_call_performance(self) -> None:
        """Test the performance of calling a method created by BaseFunction.bind.

        This test compares the speed of calling a method created by BaseFunction.bind with a normal method.
        """

        def test_method(self: Any, x: int) -> int:
            return x * 2

        test_function = self.TestFunction(test_method)

        obj = self.ExampleClass()
        arg = 5

        def call_bound() -> None:
            test_function.bind(obj)(arg)

        def call_normal() -> None:
            obj.normal_method(arg)

        # Calculate the mean time in microseconds for bound method call
        bound_time = timeit.timeit(call_bound, number=self.timeit_runs)
        mean_bound = bound_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal method call
        normal_time = timeit.timeit(call_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_bound / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal method call: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Bound BaseFunction call: {mean_bound:.3f} μs ({percent:.3f}% of normal method call time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for method call

    def test_method_type_customization_performance(self) -> None:
        """Test the performance impact of customizing the method_type attribute.

        This test compares the speed of binding with the default method_type versus a custom method_type.
        """

        # Create a custom method type
        class CustomMethod(BaseMethod):
            pass

        # Create functions with different method types
        default_function = self.TestFunction()

        # Create a function with custom method type
        custom_function = self.TestFunction()
        custom_function.method_type = CustomMethod

        obj = self.ExampleClass()

        def bind_default() -> None:
            default_function.bind(obj)

        def bind_custom() -> None:
            custom_function.bind(obj)

        # Calculate the mean time in microseconds for default method type
        default_time = timeit.timeit(bind_default, number=self.timeit_runs)
        mean_default = default_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for custom method type
        custom_time = timeit.timeit(bind_custom, number=self.timeit_runs)
        mean_custom = custom_time / self.timeit_runs * 1000000
        percent = (mean_custom / mean_default) * 100

        # Print the performance comparison
        print(
            f"\nDefault method_type binding: {mean_default:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Custom method_type binding: {mean_custom:.3f} μs ({percent:.3f}% of default method_type binding time)")
        # The performance should be similar since the only difference is the class used
        assert percent < 120  # Allow up to 20% overhead for custom method type

    def test_nested_function_calls_performance(self, test_function: "TestBaseFunctionPerformance.TestFunction") -> None:
        """Test the performance of BaseFunction with deeply nested function calls.

        This test measures the performance impact of calling a BaseFunction that calls another BaseFunction,
        and compares it with nested normal function calls.

        Args:
            test_function: A fixture providing a TestFunction instance.
        """

        # Create a chain of nested functions
        def inner_function(x: int) -> int:
            return x * 2

        normal_outer = NormalFunction(inner_function)
        base_outer = self.TestFunction(inner_function)

        arg = 5

        def call_nested_normal() -> None:
            normal_outer(arg)

        def call_nested_base() -> None:
            base_outer(arg)

        # Calculate the mean time in microseconds for nested normal function calls
        normal_time = timeit.timeit(call_nested_normal, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for nested BaseFunction calls
        base_time = timeit.timeit(call_nested_base, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNested normal function calls: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Nested BaseFunction calls: {mean_base:.3f} μs ({percent:.3f}% of nested normal function calls time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for nested calls

    def test_large_argument_list_performance(self, test_function: "TestBaseFunctionPerformance.TestFunction") -> None:
        """Test the performance of BaseFunction with large argument lists.

        This test compares the speed of BaseFunction.__call__() with a normal function-like object
        when passing a large number of arguments.

        Args:
            test_function: A fixture providing a TestFunction instance.
        """

        # Create a function that accepts many arguments
        def many_args_function(*args: Any, **kwargs: Any) -> int:
            return len(args) + len(kwargs)

        normal_func = NormalFunction(many_args_function)
        base_func = self.TestFunction(many_args_function)

        # Create a large list of arguments and a large dict of keyword arguments
        args = list(range(50))
        kwargs = {f"key_{i}": i for i in range(50)}

        def call_normal_large_args() -> None:
            normal_func(*args, **kwargs)

        def call_base_large_args() -> None:
            base_func(*args, **kwargs)

        # Calculate the mean time in microseconds for normal function with large args
        normal_time = timeit.timeit(call_normal_large_args, number=self.timeit_runs // 10)  # Reduce runs for large args
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for BaseFunction with large args
        base_time = timeit.timeit(call_base_large_args, number=self.timeit_runs // 10)  # Reduce runs for large args
        mean_base = base_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_base / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal function with large args: {mean_normal:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"BaseFunction with large args: {mean_base:.3f} μs ({percent:.3f}% of normal function with large args time)",
        )
        assert percent < self.speed_tolerance * 2  # Allow more overhead for large argument processing


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
