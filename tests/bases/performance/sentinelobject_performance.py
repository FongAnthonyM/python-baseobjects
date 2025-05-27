#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" sentinelobject_performance.py
Performance tests for the SentinelObject class in the baseobjects package.
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
from src.baseobjects.bases import SentinelObject
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Sentinel Object
class TestSentinelObject(BaseBaseObjectPerformanceTest):
    """Test the performance of the SentinelObject class.

    This class tests the performance of the SentinelObject class, which is used to create sentinel objects in the
    baseobjects package.
    """
    # Class Definitions #
    class NormalSentinel:
        """A normal Python sentinel object for comparison with SentinelObject."""
        # Magic Methods #
        def __init__(self, id_: str | bytes | int) -> None:
            """Initialize with an ID."""
            if isinstance(id_, str):
                self.id_number = int.from_bytes(id_.encode("utf-8"), "big")
            elif isinstance(id_, bytes):
                self.id_number = int.from_bytes(id_, "big")
            else:
                self.id_number = id_

        def __hash__(self) -> int:
            """Return the hash of the object."""
            return self.id_number

        def __eq__(self, other) -> bool:
            """Compare two sentinel objects."""
            return isinstance(other, self.__class__) and self.id_number == other.id_number

    # Attributes #
    class_: Type[SentinelObject] = SentinelObject

    # Instance Methods #
    # Tests
    def test_instance_creation_string(self) -> None:
        """Test the performance of creating a SentinelObject with a string ID.

        This test compares the speed of creating a SentinelObject with a string ID with a normal sentinel object.
        """
        string_id = "test_sentinel"

        def create_base() -> None:
            SentinelObject(string_id)

        def create_normal() -> None:
            self.NormalSentinel(string_id)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (string ID): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_instance_creation_bytes(self) -> None:
        """Test the performance of creating a SentinelObject with a bytes ID.

        This test compares the speed of creating a SentinelObject with a bytes ID with a normal sentinel object.
        """
        bytes_id = b"test_sentinel"

        def create_base() -> None:
            SentinelObject(bytes_id)

        def create_normal() -> None:
            self.NormalSentinel(bytes_id)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (bytes ID): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_instance_creation_int(self) -> None:
        """Test the performance of creating a SentinelObject with an int ID.

        This test compares the speed of creating a SentinelObject with an int ID with a normal sentinel object.
        """
        int_id = 12345

        def create_base() -> None:
            SentinelObject(int_id)

        def create_normal() -> None:
            self.NormalSentinel(int_id)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (int ID): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_hash_speed(self) -> None:
        """Test the performance of hashing a SentinelObject.

        This test compares the speed of hashing a SentinelObject with a normal sentinel object.
        """
        base_sentinel = SentinelObject("test_sentinel")
        normal_sentinel = self.NormalSentinel("test_sentinel")

        def hash_base() -> None:
            hash(base_sentinel)

        def hash_normal() -> None:
            hash(normal_sentinel)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(hash_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(hash_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (hash): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_equality_speed_same(self) -> None:
        """Test the performance of comparing equal SentinelObjects.

        This test compares the speed of comparing equal SentinelObjects with normal sentinel objects.
        """
        base_sentinel1 = SentinelObject("test_sentinel")
        base_sentinel2 = SentinelObject("test_sentinel")
        normal_sentinel1 = self.NormalSentinel("test_sentinel")
        normal_sentinel2 = self.NormalSentinel("test_sentinel")

        def compare_base() -> None:
            base_sentinel1 == base_sentinel2

        def compare_normal() -> None:
            normal_sentinel1 == normal_sentinel2

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(compare_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(compare_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (equality, same): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_equality_speed_different(self) -> None:
        """Test the performance of comparing different SentinelObjects.

        This test compares the speed of comparing different SentinelObjects with normal sentinel objects.
        """
        base_sentinel1 = SentinelObject("test_sentinel1")
        base_sentinel2 = SentinelObject("test_sentinel2")
        normal_sentinel1 = self.NormalSentinel("test_sentinel1")
        normal_sentinel2 = self.NormalSentinel("test_sentinel2")

        def compare_base() -> None:
            base_sentinel1 == base_sentinel2

        def compare_normal() -> None:
            normal_sentinel1 == normal_sentinel2

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(compare_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(compare_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (equality, different): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
