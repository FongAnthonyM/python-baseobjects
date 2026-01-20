#!/usr/bin/env python
"""sentinelobject_performance.py
Performance tests for the SentinelObject class in the baseobjects.bases package.
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
import copy
import pickle
import timeit
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import SentinelObject
from baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class NormalSentinel:
    """A normal Python object implementing a sentinel pattern for comparison."""

    # Class Attributes #
    registry: ClassVar[dict[str, "NormalSentinel"]] = {}

    # Attributes #
    identity: str

    def __new__(cls, id_: str) -> "NormalSentinel":
        """Create a new sentinel object or return an existing one with the same ID.

        Returns:
            NormalSentinel: The sentinel.
        """
        if (sentinel := cls.registry.get(id_, None)) is None:
            cls.registry[id_] = sentinel = super().__new__(cls)
        return sentinel

    def __init__(self, id_: str) -> None:
        """Initialize the sentinel object with the given ID."""
        self.identity = id_

    def __reduce__(self) -> tuple[Any, tuple[Any]]:
        """Reduce the sentinel object for pickling.

        Returns:
            tuple[Any, tuple[Any]]: The pickling state.
        """
        return self.__class__, (self.identity,)


class TestSentinelObjectPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the SentinelObject class.

    This test suite measures the performance of various operations on SentinelObject objects
    and compares them with standard Python implementations.
    """

    # Attributes #
    timeit_runs: int = 100000

    # Instance Methods #
    # Tests
    def test_creation_performance(self) -> None:
        """Test the performance of creating SentinelObject instances.

        This test compares the speed of creating SentinelObject instances with creating
        standard Python sentinel objects.
        """

        def create_sentinel_object() -> None:
            SentinelObject("test_sentinel")

        def create_normal_sentinel() -> None:
            NormalSentinel("test_sentinel")

        # Calculate the mean time in microseconds for SentinelObject creation
        sentinel_time = timeit.timeit(create_sentinel_object, number=self.timeit_runs)
        mean_sentinel = sentinel_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal sentinel creation
        normal_time = timeit.timeit(create_normal_sentinel, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel creation: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject creation: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel creation time)")
        assert percent < self.speed_tolerance * 1.5  # Allow some overhead for SentinelObject creation

    def test_registry_lookup_performance(self) -> None:
        """Test the performance of looking up existing sentinel objects in the registry.

        This test compares the speed of retrieving existing SentinelObject instances with retrieving
        standard Python sentinel objects.
        """
        # Create sentinel objects first to ensure they're in the registry
        sentinel_id = "existing_sentinel"
        SentinelObject(sentinel_id)
        NormalSentinel(sentinel_id)

        def lookup_sentinel_object() -> None:
            SentinelObject(sentinel_id)

        def lookup_normal_sentinel() -> None:
            NormalSentinel(sentinel_id)

        # Calculate the mean time in microseconds for SentinelObject lookup
        sentinel_time = timeit.timeit(lookup_sentinel_object, number=self.timeit_runs)
        mean_sentinel = sentinel_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal sentinel lookup
        normal_time = timeit.timeit(lookup_normal_sentinel, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel lookup: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject lookup: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel lookup time)")
        assert percent < self.speed_tolerance  # Should be very similar to normal sentinel lookup

    def test_copy_performance(self) -> None:
        """Test the performance of copying SentinelObject instances.

        This test compares the speed of copying SentinelObject instances with copying
        standard Python sentinel objects.
        """
        sentinel_object = SentinelObject("copy_test")
        normal_sentinel = NormalSentinel("copy_test")

        def copy_sentinel_object() -> None:
            sentinel_object.copy()

        def copy_normal_sentinel() -> None:
            copy.copy(normal_sentinel)

        # Calculate the mean time in microseconds for SentinelObject.copy
        sentinel_time = timeit.timeit(copy_sentinel_object, number=self.timeit_runs)
        mean_sentinel = sentinel_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for copy.copy on normal sentinel
        normal_time = timeit.timeit(copy_normal_sentinel, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel copy: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject.copy: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel copy time)")
        assert percent < self.speed_tolerance  # Should be very fast since it just returns self

    def test_deepcopy_performance(self) -> None:
        """Test the performance of deep copying SentinelObject instances.

        This test compares the speed of deep copying SentinelObject instances with deep copying
        standard Python sentinel objects.
        """
        sentinel_object = SentinelObject("deepcopy_test")
        normal_sentinel = NormalSentinel("deepcopy_test")

        def deepcopy_sentinel_object() -> None:
            sentinel_object.deepcopy()

        def deepcopy_normal_sentinel() -> None:
            copy.deepcopy(normal_sentinel)

        # Calculate the mean time in microseconds for SentinelObject.deepcopy
        sentinel_time = timeit.timeit(deepcopy_sentinel_object, number=self.timeit_runs)
        mean_sentinel = sentinel_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for copy.deepcopy on normal sentinel
        normal_time = timeit.timeit(deepcopy_normal_sentinel, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel deepcopy: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject.deepcopy: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel deepcopy time)")
        assert percent < self.speed_tolerance  # Should be very fast since it just returns self

    def test_pickle_performance(self) -> None:
        """Test the performance of pickling and unpickling SentinelObject instances.

        This test compares the speed of pickling and unpickling SentinelObject instances with
        standard Python sentinel objects.
        """
        sentinel_object = SentinelObject("pickle_test")
        normal_sentinel = NormalSentinel("pickle_test")

        def pickle_sentinel_object() -> None:
            pickle.dumps(sentinel_object)

        def pickle_normal_sentinel() -> None:
            pickle.dumps(normal_sentinel)

        # Calculate the mean time in microseconds for pickling SentinelObject
        sentinel_time = timeit.timeit(pickle_sentinel_object, number=self.timeit_runs // 10)  # Reduce runs for pickling
        mean_sentinel = sentinel_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for pickling normal sentinel
        normal_time = timeit.timeit(pickle_normal_sentinel, number=self.timeit_runs // 10)  # Reduce runs for pickling
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel pickling: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject pickling: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel pickling time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for pickling operations

        # Now test unpickling
        sentinel_pickle = pickle.dumps(sentinel_object)
        normal_pickle = pickle.dumps(normal_sentinel)

        def unpickle_sentinel_object() -> None:
            pickle.loads(sentinel_pickle)

        def unpickle_normal_sentinel() -> None:
            pickle.loads(normal_pickle)

        # Calculate the mean time in microseconds for unpickling SentinelObject
        sentinel_time = timeit.timeit(
            unpickle_sentinel_object,
            number=self.timeit_runs // 10,
        )  # Reduce runs for unpickling
        mean_sentinel = sentinel_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for unpickling normal sentinel
        normal_time = timeit.timeit(
            unpickle_normal_sentinel,
            number=self.timeit_runs // 10,
        )  # Reduce runs for unpickling
        mean_normal = normal_time / (self.timeit_runs // 10) * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel unpickling: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"SentinelObject unpickling: {mean_sentinel:.3f} μs ({percent:.3f}% of normal sentinel unpickling time)")
        assert percent < self.speed_tolerance * 2  # Allow more overhead for unpickling operations

    def test_identity_comparison_performance(self) -> None:
        """Test the performance of identity comparisons with SentinelObject instances.

        This test compares the speed of identity comparisons with SentinelObject instances vs
        standard Python sentinel objects.
        """
        # Create two instances with the same ID (should be the same object)
        sentinel1 = SentinelObject("compare_test")
        sentinel2 = SentinelObject("compare_test")
        normal1 = NormalSentinel("compare_test")
        normal2 = NormalSentinel("compare_test")

        def compare_sentinel_objects() -> None:
            _ = sentinel1 is sentinel2

        def compare_normal_sentinels() -> None:
            _ = normal1 is normal2

        # Calculate the mean time in microseconds for SentinelObject identity comparison
        sentinel_time = timeit.timeit(compare_sentinel_objects, number=self.timeit_runs)
        mean_sentinel = sentinel_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for normal sentinel identity comparison
        normal_time = timeit.timeit(compare_normal_sentinels, number=self.timeit_runs)
        mean_normal = normal_time / self.timeit_runs * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nNormal sentinel identity comparison: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"SentinelObject identity comparison: {mean_sentinel:.3f} μs "
            f"({percent:.3f}% of normal sentinel identity comparison time)",
        )
        assert percent < self.speed_tolerance  # Should be very similar to normal identity comparison

    def test_multiple_sentinel_creation_performance(self) -> None:
        """Test the performance of creating multiple SentinelObject instances with different IDs.

        This test measures the time it takes to create multiple SentinelObject instances with
        different IDs and compares it with creating multiple standard Python sentinel objects.
        """

        def create_multiple_sentinel_objects() -> None:
            for i in range(10):
                SentinelObject(f"multi_test_{i}")

        def create_multiple_normal_sentinels() -> None:
            for i in range(10):
                NormalSentinel(f"multi_test_{i}")

        # Calculate the mean time in microseconds for creating multiple SentinelObjects
        sentinel_time = timeit.timeit(
            create_multiple_sentinel_objects,
            number=self.timeit_runs // 100,
        )  # Reduce runs for multiple creations
        mean_sentinel = sentinel_time / (self.timeit_runs // 100) * 1000000

        # Calculate the mean time in microseconds for creating multiple normal sentinels
        normal_time = timeit.timeit(
            create_multiple_normal_sentinels,
            number=self.timeit_runs // 100,
        )  # Reduce runs for multiple creations
        mean_normal = normal_time / (self.timeit_runs // 100) * 1000000
        percent = (mean_sentinel / mean_normal) * 100

        # Print the performance comparison
        print(
            f"\nMultiple normal sentinel creation: {mean_normal:.3f} μs "
            f"({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"Multiple SentinelObject creation: {mean_sentinel:.3f} μs "
            f"({percent:.3f}% of multiple normal sentinel creation time)",
        )
        assert percent < self.speed_tolerance * 2  # Allow more overhead for multiple creations


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
