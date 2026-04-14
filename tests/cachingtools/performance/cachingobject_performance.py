#!/usr/bin/env python
"""cachingobject_performance.py
Performance tests for the CachingObject class in the baseobjects.cachingtools package.
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

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools import CachingObject, timed_cache
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class ExampleCachingObject(CachingObject):
    """An example class for testing CachingObject performance."""

    # Attributes #
    _is_caching: bool = True

    @timed_cache(lifetime=10)
    def cached_method(self) -> int:
        """A cached method.

        Returns:
            int: A constant value.
        """
        return 1


class TestCachingObjectPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the CachingObject class.

    This test suite measures the performance of CachingObject instantiation and property switching.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def caching_object(self) -> ExampleCachingObject:
        """Create a test ExampleCachingObject for use in tests.

        Returns:
            ExampleCachingObject: An instance of the test class.
        """
        return ExampleCachingObject()

    # Tests
    def test_instantiation_performance(self) -> None:
        """Test the performance of creating CachingObject instances.

        This test measures the speed of creating a CachingObject.
        """

        def create_object() -> None:
            ExampleCachingObject()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(create_object, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nCachingObject creation: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )
        # No comparison here, just measuring the absolute time

    def test_property_switching_performance(self, caching_object: ExampleCachingObject) -> None:
        """Test the performance of switching the is_caching property.

        This test measures the speed of enabling and disabling caching.

        Args:
            caching_object: A fixture providing a CachingObject instance.
        """

        def switch_property() -> None:
            if caching_object.any_caching:
                caching_object.disable_caching()
            else:
                caching_object.enable_caching()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(switch_property, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nCachingObject is_caching switch: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
