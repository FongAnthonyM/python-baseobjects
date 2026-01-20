#!/usr/bin/env python
"""timedcache_performance.py
Performance tests for the TimedCache classes in the baseobjects.cachingtools package.
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
from baseobjects.cachingtools import timed_cache, timed_lru_cache, timed_single_cache
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class ExampleTimedCache:
    """An example class for testing TimedCache performance."""

    def simple_method(self) -> int:
        """A simple method.

        Returns:
            int: A constant value.
        """
        return 1

    @timed_single_cache(lifetime=10)
    def single_cache_method(self) -> int:
        """A method with a single value cache.

        Returns:
            int: A constant value.
        """
        return 1

    @timed_cache(lifetime=10)
    def unlimited_cache_method(self) -> int:
        """A method with an unlimited cache.

        Returns:
            int: A constant value.
        """
        return 1

    @timed_cache(lifetime=10, maxsize=10)
    def limited_cache_method(self, arg: int) -> int:
        """A method with a limited cache.

        Args:
            arg: The argument to return.

        Returns:
            int: The argument.
        """
        return arg

    @timed_lru_cache(lifetime=10)
    def unlimited_lru_cache_method(self) -> int:
        """A method with an unlimited LRU cache.

        Returns:
            int: A constant value.
        """
        return 1

    @timed_lru_cache(lifetime=10, maxsize=10)
    def limited_lru_cache_method(self, arg: int) -> int:
        """A method with a limited LRU cache.

        Args:
            arg: The argument to return.

        Returns:
            int: The argument.
        """
        return arg


class TestTimedCachePerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the TimedCache classes.

    This test suite measures the performance of cache hits for various TimedCache implementations.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def example_object(self) -> ExampleTimedCache:
        """Create a test ExampleTimedCache for use in tests.

        Returns:
            ExampleTimedCache: An instance of the test class.
        """
        return ExampleTimedCache()

    # Tests
    def test_single_cache_hit_performance(self, example_object: ExampleTimedCache) -> None:
        """Test the performance of TimedSingleCache hits.

        Args:
            example_object: A fixture providing a ExampleTimedCache instance.
        """
        # Warm up
        example_object.single_cache_method()

        def call_method() -> None:
            example_object.single_cache_method()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(call_method, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nTimedSingleCache hit: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_unlimited_cache_hit_performance(self, example_object: ExampleTimedCache) -> None:
        """Test the performance of TimedCache (unlimited) hits.

        Args:
            example_object: A fixture providing a ExampleTimedCache instance.
        """
        # Warm up
        example_object.unlimited_cache_method()

        def call_method() -> None:
            example_object.unlimited_cache_method()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(call_method, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nTimedCache (unlimited) hit: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_limited_cache_hit_performance(self, example_object: ExampleTimedCache) -> None:
        """Test the performance of TimedCache (limited) hits.

        Args:
            example_object: A fixture providing a ExampleTimedCache instance.
        """
        # Warm up with some values
        for i in range(5):
            example_object.limited_cache_method(i)

        def call_method() -> None:
            example_object.limited_cache_method(0)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(call_method, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nTimedCache (limited) hit: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_unlimited_lru_cache_hit_performance(self, example_object: ExampleTimedCache) -> None:
        """Test the performance of TimedLRUCache (unlimited) hits.

        Args:
            example_object: A fixture providing a ExampleTimedCache instance.
        """
        # Warm up
        example_object.unlimited_lru_cache_method()

        def call_method() -> None:
            example_object.unlimited_lru_cache_method()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(call_method, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nTimedLRUCache (unlimited) hit: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )

    def test_limited_lru_cache_hit_performance(self, example_object: ExampleTimedCache) -> None:
        """Test the performance of TimedLRUCache (limited) hits.

        Args:
            example_object: A fixture providing a ExampleTimedCache instance.
        """
        # Warm up with some values
        for i in range(5):
            example_object.limited_lru_cache_method(i)

        def call_method() -> None:
            example_object.limited_lru_cache_method(0)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(call_method, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(
            f"\nTimedLRUCache (limited) hit: {mean_time:.3f} us ({self.call_speed:.3f} "
            f"is the speed of a simple function call)",
        )


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
