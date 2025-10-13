#!/usr/bin/env python
"""timeddict_performance.py
Performance tests for the TimedDict class in the baseobjects.collections package.
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
from typing import Any, ClassVar, Dict, List

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.collections import TimedDict
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestTimedDictPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the TimedDict class.

    This test suite measures the performance of various operations on TimedDict objects
    and compares them with standard Python dictionary implementations.
    """

    # Class Definitions #
    class NormalDict(dict):
        """A normal Python dictionary for comparison with TimedDict."""

        pass

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dict(self) -> TimedDict:
        """Create a test TimedDict for use in tests.

        Returns:
            TimedDict: An instance of TimedDict.
        """
        return TimedDict()

    @pytest.fixture
    def populated_test_dict(self) -> TimedDict:
        """Create a populated test TimedDict for use in tests.

        Returns:
            TimedDict: A populated instance of TimedDict.
        """
        result = TimedDict()
        for i in range(100):
            result[f"key{i}"] = f"value{i}"
        return result

    @pytest.fixture
    def normal_dict(self) -> dict:
        """Create a normal dictionary for comparison.

        Returns:
            dict: A standard Python dictionary.
        """
        return {}

    @pytest.fixture
    def populated_normal_dict(self) -> dict:
        """Create a populated normal dictionary for comparison.

        Returns:
            dict: A populated standard Python dictionary.
        """
        result = {}
        for i in range(100):
            result[f"key{i}"] = f"value{i}"
        return result

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating TimedDict instances.

        This test compares the speed of creating an empty TimedDict with a normal dict.
        """

        def create_timed() -> None:
            TimedDict()

        def create_normal() -> None:
            dict()

        # Calculate the mean time in microseconds for the TimedDict implementation
        timed_time = timeit.timeit(create_timed, number=self.timeit_runs)
        mean_timed = timed_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_timed / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict creation: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"TimedDict creation: {mean_timed:.3f} μs ({percent:.3f}% of standard dict creation time)")
        assert percent < self.speed_tolerance

    def test_creation_speed_populated_performance(self) -> None:
        """Test the performance of creating a populated TimedDict.

        This test compares the speed of creating a populated TimedDict with a normal dict.
        """
        test_data = {f"key{i}": f"value{i}" for i in range(100)}

        def create_timed() -> None:
            TimedDict(test_data)

        def create_normal() -> None:
            dict(test_data)

        # Calculate the mean time in microseconds for the TimedDict implementation
        timed_time = timeit.timeit(create_timed, number=self.timeit_runs)
        mean_timed = timed_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_timed / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict populated creation: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"TimedDict populated creation: {mean_timed:.3f} μs ({percent:.3f}% of standard dict populated creation time)"
        )
        assert percent < self.speed_tolerance

    def test_get_item_speed_performance(self, populated_test_dict: TimedDict, populated_normal_dict: dict) -> None:
        """Test the performance of getting an item from a TimedDict.

        This test compares the speed of getting an item from a TimedDict with a normal dict.

        Args:
            populated_test_dict: A fixture providing a populated TimedDict instance.
            populated_normal_dict: A fixture providing a populated normal dict.
        """
        key = "key50"

        def get_timed() -> None:
            populated_test_dict[key]

        def get_normal() -> None:
            populated_normal_dict[key]

        # Calculate the mean time in microseconds for the TimedDict implementation
        timed_time = timeit.timeit(get_timed, number=self.timeit_runs)
        mean_timed = timed_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(get_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_timed / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict get item: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"TimedDict get item: {mean_timed:.3f} μs ({percent:.3f}% of standard dict get item time)")
        assert percent < self.speed_tolerance

    def test_set_item_speed_performance(self, test_dict: TimedDict, normal_dict: dict) -> None:
        """Test the performance of setting an item in a TimedDict.

        This test compares the speed of setting an item in a TimedDict with a normal dict.

        Args:
            test_dict: A fixture providing a TimedDict instance.
            normal_dict: A fixture providing a normal dict.
        """
        key = "test_key"
        value = "test_value"

        def set_timed() -> None:
            test_dict[key] = value

        def set_normal() -> None:
            normal_dict[key] = value

        # Calculate the mean time in microseconds for the TimedDict implementation
        timed_time = timeit.timeit(set_timed, number=self.timeit_runs)
        mean_timed = timed_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(set_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_timed / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict set item: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"TimedDict set item: {mean_timed:.3f} μs ({percent:.3f}% of standard dict set item time)")
        assert percent < self.speed_tolerance

    def test_clear_speed_performance(self, populated_test_dict: TimedDict, populated_normal_dict: dict) -> None:
        """Test the performance of clearing a TimedDict.

        This test compares the speed of clearing a TimedDict with a normal dict.

        Args:
            populated_test_dict: A fixture providing a populated TimedDict instance.
            populated_normal_dict: A fixture providing a populated normal dict.
        """

        def clear_timed() -> None:
            populated_test_dict.clear()

        def clear_normal() -> None:
            populated_normal_dict.clear()

        # Calculate the mean time in microseconds for the TimedDict implementation
        timed_time = timeit.timeit(clear_timed, number=self.timeit_runs)
        mean_timed = timed_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(clear_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_timed / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict clear: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"TimedDict clear: {mean_timed:.3f} μs ({percent:.3f}% of standard dict clear time)")
        assert percent < self.speed_tolerance

    def test_reset_expiration_speed_performance(self, test_dict: TimedDict) -> None:
        """Test the performance of resetting the expiration time of a TimedDict.

        This test measures the speed of resetting the expiration time.

        Args:
            test_dict: A fixture providing a TimedDict instance.
        """
        # Set up the test dictionary with a lifetime
        test_dict.lifetime = 60

        def reset_expiration() -> None:
            test_dict.reset_expiration()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(reset_expiration, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nReset expiration: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_verify_speed_performance(self, test_dict: TimedDict) -> None:
        """Test the performance of verifying a TimedDict.

        This test measures the speed of verifying if a TimedDict should be cleared.

        Args:
            test_dict: A fixture providing a TimedDict instance.
        """
        # Set up the test dictionary with a lifetime that won't expire during the test
        test_dict.lifetime = 3600
        test_dict.reset_expiration()

        def verify() -> None:
            test_dict.verify()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(verify, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nVerify: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
