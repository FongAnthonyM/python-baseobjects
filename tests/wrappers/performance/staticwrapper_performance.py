#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""staticwrapper_performance.py
Performance tests for the StaticWrapper class in the baseobjects.wrappers package.
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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.testsuite import WrapperPerformanceTestSuite
from src.baseobjects.wrappers import StaticWrapper


# Definitions #
# Classes #
class StaticWrapperTestObject(StaticWrapper):
    """A test class that inherits from StaticWrapper.

    This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects.
    """
    _wrapped_map_: list[[str, type[Any]], ...] = [
        ("_first", WrapperPerformanceTestSuite.ExampleOne),
        ("_second", WrapperPerformanceTestSuite.ExampleTwo)
    ]

    def __init__(self, first: Any = None, second: Any = None) -> None:
        """Initialize with wrapped objects.

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
        """
        self._first = first
        self._second = second
        self.two = "wrapper"
        self.four = "wrapper"
        self._wrap()

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class TestStaticWrapperPerformance(WrapperPerformanceTestSuite):
    """Test suite for assaying the performance of the StaticWrapper class.

    This test suite measures the performance of various operations on StaticWrapper objects
    and compares them with direct operations on the wrapped objects.

    Attributes:
        TestClass: The StaticWrapper test class to be assayed.
        timeit_runs: The number of runs to use for timeit measurements.
        speed_tolerance: The maximum percentage of time a new implementation can take compared to the old one.
    """
    # Attributes #
    TestClass = StaticWrapperTestObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(self) -> StaticWrapperTestObject:
        """Create a test object.

        Returns:
            A StaticWrapperTestObject with ExampleOne and ExampleTwo objects.
        """
        return self.TestClass(self.ExampleOne(), self.ExampleTwo())

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the StaticWrapper class.

        This test compares the speed of creating a StaticWrapper instance with creating a standard object.
        """
        def wrapper_creation() -> None:
            _ = self.TestClass(self.ExampleOne(), self.ExampleTwo())

        # Calculate the mean time in microseconds for the wrapper creation
        new_time = timeit.timeit(wrapper_creation, number=self.timeit_runs // 10)  # Reduce runs for creation
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Print the performance comparison
        print(f"\n{self.TestClass.__name__} creation: {mean_new:.3f} μ")
        # No assertion here, just measuring performance

    def test_wrap_method_performance(self, test_object: StaticWrapperTestObject) -> None:
        """Test the performance of the _wrap method.

        This test measures the performance of the _wrap method which is specific to StaticWrapper.

        Args:
            test_object: A fixture providing a StaticWrapperTestObject.
        """
        def wrap_method() -> None:
            test_object._wrap()

        # Calculate the mean time in microseconds for the wrap method
        time = timeit.timeit(wrap_method, number=self.timeit_runs // 10)  # Reduce runs for wrap
        mean = time / (self.timeit_runs // 10) * 1000000

        # Print the performance information
        print(f"\n{self.TestClass.__name__} _wrap method: {mean:.3f} μs")
        # No assertion here, just measuring performance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])