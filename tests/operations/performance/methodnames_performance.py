#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""methodnames_performance.py
Performance tests_old_ for the method name functions in the baseobjects.operations package.
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
from typing import Any, Generator, List, Tuple

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.testsuite import BasePerformanceTestSuite
from src.baseobjects.operations import (
    iter_method_names,
    iter_public_method_names,
    get_method_names,
    get_public_method_names,
)


# Definitions #
# Functions #
def standard_iter_method_names(obj: Any) -> Generator[str, None, None]:
    """Standard implementation of iter_method_names using a for loop.

    Args:
        obj: The object to iterate the method names from.

    Returns:
        The iterator as a generator which iterates over the method names of an object.
    """
    for name in dir(obj):
        attr = getattr(obj, name, None)
        if callable(attr):
            yield name


def standard_iter_public_method_names(obj: Any) -> Generator[str, None, None]:
    """Standard implementation of iter_public_method_names using a for loop.

    Args:
        obj: The object to iterate the public method names from.

    Returns:
        The iterator as a generator which iterates over the public method names of an object.
    """
    for name in dir(obj):
        attr = getattr(obj, name, None)
        if callable(attr) and name[0] != '_':
            yield name


def standard_get_method_names(obj: Any) -> Tuple[str, ...]:
    """Standard implementation of get_method_names using a list comprehension.

    Args:
        obj: The object to get the method names from.

    Returns:
        The method names of an object.
    """
    return tuple(name for name in dir(obj) if callable(getattr(obj, name, None)))


def standard_get_public_method_names(obj: Any) -> Tuple[str, ...]:
    """Standard implementation of get_public_method_names using a list comprehension.

    Args:
        obj: The object to get the public method names from.

    Returns:
        The public method names of an object.
    """
    return tuple(name for name in dir(obj) if callable(getattr(obj, name, None)) and name[0] != '_')


# Classes #
class TestMethodNames(BasePerformanceTestSuite):
    """Test the performance of the method name functions.

    This class tests_old_ the performance of the functions that retrieve method names from objects.
    """
    # Class Definitions #
    class TestClass:
        """A test class with various methods for testing method name functions."""

        def public_method(self) -> None:
            """A public method."""
            pass

        def another_public_method(self) -> None:
            """Another public method."""
            pass

        def third_public_method(self) -> None:
            """A third public method."""
            pass

        def _private_method(self) -> None:
            """A private method."""
            pass

        def _another_private_method(self) -> None:
            """Another private method."""
            pass

        def __dunder_method__(self) -> None:
            """A dunder method."""
            pass

        def __another_dunder_method__(self) -> None:
            """Another dunder method."""
            pass

        @property
        def some_property(self) -> str:
            """A property."""
            return "property"

        @property
        def another_property(self) -> str:
            """Another property."""
            return "another property"

        # Non-callable attributes
        non_callable_attr1 = "not a method 1"
        non_callable_attr2 = "not a method 2"
        non_callable_attr3 = "not a method 3"

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: int = 150

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> "TestMethodNames.TestClass":
        """Create a test object for use in tests_old_.

        Returns:
            TestClass: An instance of the test class.
        """
        return self.TestClass()

    @pytest.fixture
    def builtin_object(self) -> List[int]:
        """Create a built-in object for use in tests_old_.

        Returns:
            List[int]: A list object.
        """
        return [1, 2, 3, 4, 5]

    # Tests
    def test_iter_method_names_speed(self, test_object: "TestMethodNames.TestClass") -> None:
        """Test the performance of iter_method_names.

        This test compares the speed of iter_method_names with a standard implementation.

        Args:
            test_object: A fixture providing a test object.
        """
        def custom_implementation() -> None:
            list(iter_method_names(test_object))

        def standard_implementation() -> None:
            list(standard_iter_method_names(test_object))

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (iter_method_names): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_iter_public_method_names_speed(self, test_object: "TestMethodNames.TestClass") -> None:
        """Test the performance of iter_public_method_names.

        This test compares the speed of iter_public_method_names with a standard implementation.

        Args:
            test_object: A fixture providing a test object.
        """
        def custom_implementation() -> None:
            list(iter_public_method_names(test_object))

        def standard_implementation() -> None:
            list(standard_iter_public_method_names(test_object))

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (iter_public_method_names): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_get_method_names_speed(self, test_object: "TestMethodNames.TestClass") -> None:
        """Test the performance of get_method_names.

        This test compares the speed of get_method_names with a standard implementation.

        Args:
            test_object: A fixture providing a test object.
        """
        def custom_implementation() -> None:
            get_method_names(test_object)

        def standard_implementation() -> None:
            standard_get_method_names(test_object)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (get_method_names): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_get_public_method_names_speed(self, test_object: "TestMethodNames.TestClass") -> None:
        """Test the performance of get_public_method_names.

        This test compares the speed of get_public_method_names with a standard implementation.

        Args:
            test_object: A fixture providing a test object.
        """
        def custom_implementation() -> None:
            get_public_method_names(test_object)

        def standard_implementation() -> None:
            standard_get_public_method_names(test_object)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (get_public_method_names): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_with_builtin_object_speed(self, builtin_object: List[int]) -> None:
        """Test the performance of method name functions with a built-in object.

        This test compares the speed of the method name functions with a built-in object.

        Args:
            builtin_object: A fixture providing a built-in object.
        """
        def iter_method_names_impl() -> None:
            list(iter_method_names(builtin_object))

        def iter_public_method_names_impl() -> None:
            list(iter_public_method_names(builtin_object))

        def get_method_names_impl() -> None:
            get_method_names(builtin_object)

        def get_public_method_names_impl() -> None:
            get_public_method_names(builtin_object)

        # Calculate the mean time for each function
        iter_time = timeit.timeit(iter_method_names_impl, number=self.timeit_runs)
        iter_public_time = timeit.timeit(iter_public_method_names_impl, number=self.timeit_runs)
        get_time = timeit.timeit(get_method_names_impl, number=self.timeit_runs)
        get_public_time = timeit.timeit(get_public_method_names_impl, number=self.timeit_runs)

        # Convert to microseconds
        mean_iter = iter_time / self.timeit_runs * 1000000
        mean_iter_public = iter_public_time / self.timeit_runs * 1000000
        mean_get = get_time / self.timeit_runs * 1000000
        mean_get_public = get_public_time / self.timeit_runs * 1000000

        # Print the performance measurements
        print(f"\niter_method_names with built-in object: {mean_iter:.3f} μs")
        print(f"iter_public_method_names with built-in object: {mean_iter_public:.3f} μs")
        print(f"get_method_names with built-in object: {mean_get:.3f} μs")
        print(f"get_public_method_names with built-in object: {mean_get_public:.3f} μs")
        # No assertion here, just measuring absolute performance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])