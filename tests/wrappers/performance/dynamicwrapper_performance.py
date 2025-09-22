#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dynamicwrapper_performance.py
Performance tests for the DynamicWrapper class in the baseobjects.wrappers package.
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
from src.baseobjects.wrappers import DynamicWrapper


# Definitions #
# Classes #
class DynamicWrapperTestObject(DynamicWrapper):
    """A test class that inherits from DynamicWrapper.

    This class uses DynamicWrapper to wrap ExampleOne and ExampleTwo objects.
    """

    _wrapped_map_ = ["_first", "_second"]

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

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class TestDynamicWrapperPerformance(WrapperPerformanceTestSuite):
    """Test suite for assaying the performance of the DynamicWrapper class.

    This test suite measures the performance of various operations on DynamicWrapper objects
    and compares them with direct operations on the wrapped objects.

    Attributes:
        TestClass: The DynamicWrapper test class to be assayed.
        timeit_runs: The number of runs to use for timeit measurements.
        speed_tolerance: The maximum percentage of time a new implementation can take compared to the old one.
    """

    # Attributes #
    TestClass = DynamicWrapperTestObject

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_object(
        self,
        test_example_one: "WrapperPerformanceTestSuite.ExampleOne",
        test_example_two: "WrapperPerformanceTestSuite.ExampleTwo",
    ) -> DynamicWrapperTestObject:
        """Create a test object.

         Args:
            test_example_one: A fixture providing an ExampleOne object.
            test_example_two: A fixture providing an ExampleTwo object.

        Returns:
            A DynamicWrapperTestObject with ExampleOne and ExampleTwo objects.
        """
        return self.TestClass(self.ExampleOne(), self.ExampleTwo())

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating instances of the DynamicWrapper class.

        This test compares the speed of creating a DynamicWrapper instance with creating a standard object.
        """

        def wrapper_creation() -> None:
            _ = self.TestClass(self.ExampleOne(), self.ExampleTwo())

        # Calculate the mean time in microseconds for the wrapper creation
        new_time = timeit.timeit(wrapper_creation, number=self.timeit_runs // 10)  # Reduce runs for creation
        mean_new = new_time / (self.timeit_runs // 10) * 1000000

        # Print the performance comparison
        print(f"\n{self.TestClass.__name__} creation: {mean_new:.3f} μs")
        # No assertion here, just measuring performance

    def test_getattr_performance(
        self, test_object: DynamicWrapperTestObject, test_example_one: "WrapperPerformanceTestSuite.ExampleOne"
    ) -> None:
        """Test the performance of the __getattr__ method.

        This test compares the speed of accessing attributes through __getattr__ with direct attribute access.

        Args:
            test_object: A fixture providing a DynamicWrapperTestObject.
            test_example_one: A fixture providing an ExampleOne object.
        """

        def dynamic_access() -> None:
            _ = test_object.one

        def direct_access() -> None:
            _ = test_example_one.one

        # Calculate the mean time in microseconds for dynamic access
        new_time = timeit.timeit(dynamic_access, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for direct access
        old_time = timeit.timeit(direct_access, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\n{self.TestClass.__name__} __getattr__: {mean_new:.3f} μs ({percent:.3f}% of direct access time)")
        assert percent < self.speed_tolerance

    def test_setattr_performance(
        self, test_object: DynamicWrapperTestObject, test_example_one: "WrapperPerformanceTestSuite.ExampleOne"
    ) -> None:
        """Test the performance of the __setattr__ method.

        This test compares the speed of setting attributes through __setattr__ with direct attribute setting.

        Args:
            test_object: A fixture providing a DynamicWrapperTestObject.
            test_example_one: A fixture providing an ExampleOne object.
        """

        def dynamic_set() -> None:
            test_object.one = "test"

        def direct_set() -> None:
            test_example_one.one = "test"

        # Calculate the mean time in microseconds for dynamic set
        new_time = timeit.timeit(dynamic_set, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for direct set
        old_time = timeit.timeit(direct_set, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\n{self.TestClass.__name__} __setattr__: {mean_new:.3f} μs ({percent:.3f}% of direct set time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
