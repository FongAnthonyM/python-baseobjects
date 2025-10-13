#!/usr/bin/env python
"""orderabledict_performance.py
Performance tests for the OrderableDict class in the baseobjects.collections package.
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
from src.baseobjects.collections import OrderableDict
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestOrderableDictPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the OrderableDict class.

    This test suite measures the performance of various operations on OrderableDict objects
    and compares them with standard Python dictionary implementations.
    """

    # Attributes #
    timeit_runs: int = 100000
    speed_tolerance: float = 150.0

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dict(self) -> OrderableDict:
        """Create a test OrderableDict for use in tests.

        Returns:
            OrderableDict: An instance of OrderableDict.
        """
        return OrderableDict()

    @pytest.fixture
    def populated_test_dict(self) -> OrderableDict:
        """Create a populated test OrderableDict for use in tests.

        Returns:
            OrderableDict: A populated instance of OrderableDict.
        """
        result = OrderableDict()
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
        """Test the performance of creating OrderableDict instances.

        This test compares the speed of creating an empty OrderableDict with a normal dict.
        """

        def create_orderable() -> None:
            OrderableDict()

        def create_normal() -> None:
            dict()

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(create_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict creation: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"OrderableDict creation: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict creation time)")
        assert percent < self.speed_tolerance

    def test_creation_speed_populated_performance(self) -> None:
        """Test the performance of creating a populated OrderableDict.

        This test compares the speed of creating a populated OrderableDict with a normal dict.
        """
        test_data = {f"key{i}": f"value{i}" for i in range(100)}

        def create_orderable() -> None:
            OrderableDict(test_data)

        def create_normal() -> None:
            dict(test_data)

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(create_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict populated creation: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(
            f"OrderableDict populated creation: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict populated creation time)"
        )
        assert percent < self.speed_tolerance

    def test_get_item_speed_performance(self, populated_test_dict: OrderableDict, populated_normal_dict: dict) -> None:
        """Test the performance of getting an item from an OrderableDict.

        This test compares the speed of getting an item from an OrderableDict with a normal dict.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
            populated_normal_dict: A fixture providing a populated normal dict.
        """
        key = "key50"

        def get_orderable() -> None:
            populated_test_dict[key]

        def get_normal() -> None:
            populated_normal_dict[key]

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(get_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(get_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict get item: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"OrderableDict get item: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict get item time)")
        assert percent < self.speed_tolerance

    def test_set_item_speed_performance(self, test_dict: OrderableDict, normal_dict: dict) -> None:
        """Test the performance of setting an item in an OrderableDict.

        This test compares the speed of setting an item in an OrderableDict with a normal dict.

        Args:
            test_dict: A fixture providing an OrderableDict instance.
            normal_dict: A fixture providing a normal dict.
        """
        key = "test_key"
        value = "test_value"

        def set_orderable() -> None:
            test_dict[key] = value

        def set_normal() -> None:
            normal_dict[key] = value

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(set_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(set_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict set item: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"OrderableDict set item: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict set item time)")
        assert percent < self.speed_tolerance

    def test_del_item_speed_performance(self, populated_test_dict: OrderableDict, populated_normal_dict: dict) -> None:
        """Test the performance of deleting an item from an OrderableDict.

        This test compares the speed of deleting an item from an OrderableDict with a normal dict.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
            populated_normal_dict: A fixture providing a populated normal dict.
        """
        # We'll use different keys for each run to avoid KeyError after deletion
        keys = [f"key{i}" for i in range(50, 60)]
        key_index = 0

        def del_orderable() -> None:
            nonlocal key_index
            key = keys[key_index % len(keys)]
            key_index += 1
            try:
                del populated_test_dict[key]
            except KeyError:
                pass

        def del_normal() -> None:
            nonlocal key_index
            key = keys[key_index % len(keys)]
            key_index += 1
            try:
                del populated_normal_dict[key]
            except KeyError:
                pass

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(del_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(del_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict delete item: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"OrderableDict delete item: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict delete item time)")
        assert percent < self.speed_tolerance

    def test_iteration_speed_performance(self, populated_test_dict: OrderableDict, populated_normal_dict: dict) -> None:
        """Test the performance of iterating over an OrderableDict.

        This test compares the speed of iterating over an OrderableDict with a normal dict.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
            populated_normal_dict: A fixture providing a populated normal dict.
        """

        def iterate_orderable() -> None:
            for key in populated_test_dict:
                pass

        def iterate_normal() -> None:
            for key in populated_normal_dict:
                pass

        # Calculate the mean time in microseconds for the OrderableDict implementation
        orderable_time = timeit.timeit(iterate_orderable, number=self.timeit_runs)
        mean_orderable = orderable_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the dict implementation
        dict_time = timeit.timeit(iterate_normal, number=self.timeit_runs)
        mean_dict = dict_time / self.timeit_runs * 1000000
        percent = (mean_orderable / mean_dict) * 100

        # Print the performance comparison
        print(
            f"\nStandard dict iteration: {mean_dict:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)"
        )
        print(f"OrderableDict iteration: {mean_orderable:.3f} μs ({percent:.3f}% of standard dict iteration time)")
        assert percent < self.speed_tolerance

    def test_get_index_speed_performance(self, populated_test_dict: OrderableDict) -> None:
        """Test the performance of getting an item by index from an OrderableDict.

        This test measures the speed of getting an item by index.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
        """
        index = 50

        def get_index() -> None:
            populated_test_dict.get_index(index)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(get_index, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nGet index: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_set_index_speed_performance(self, populated_test_dict: OrderableDict) -> None:
        """Test the performance of setting an item by index in an OrderableDict.

        This test measures the speed of setting an item by index.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
        """
        index = 50
        value = "new_value"

        def set_index() -> None:
            populated_test_dict.set_index(index, value)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(set_index, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nSet index: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_insert_speed_performance(self, test_dict: OrderableDict) -> None:
        """Test the performance of inserting an item at a specific position in an OrderableDict.

        This test measures the speed of inserting an item at a specific position.

        Args:
            test_dict: A fixture providing an OrderableDict instance.
        """
        # We'll use different keys for each run to avoid KeyError
        keys = [f"insert_key{i}" for i in range(self.timeit_runs)]
        key_index = 0
        index = 0
        value = "insert_value"

        def insert() -> None:
            nonlocal key_index
            key = keys[key_index]
            key_index += 1
            try:
                test_dict.insert(index, key, value)
            except KeyError:
                pass

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(insert, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nInsert: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_insert_move_speed_performance(self, populated_test_dict: OrderableDict) -> None:
        """Test the performance of insert_move in an OrderableDict.

        This test measures the speed of insert_move, which inserts or moves an item.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
        """
        # We'll alternate between existing and new keys
        existing_key = "key25"
        new_key = "new_insert_key"
        index = 0
        value = "insert_move_value"
        use_existing = [True, False]
        call_index = 0

        def insert_move() -> None:
            nonlocal call_index
            key = existing_key if use_existing[call_index % len(use_existing)] else new_key
            call_index += 1
            populated_test_dict.insert_move(index, key, value)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(insert_move, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nInsert move: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_pop_index_speed_performance(self, populated_test_dict: OrderableDict) -> None:
        """Test the performance of popping an item by index from an OrderableDict.

        This test measures the speed of popping an item by index.

        Args:
            populated_test_dict: A fixture providing a populated OrderableDict instance.
        """

        # We need to repopulate the dict after each pop to avoid IndexError
        def pop_and_repopulate() -> None:
            try:
                populated_test_dict.pop_index(0)
            except IndexError:
                # Repopulate if empty
                for i in range(100):
                    populated_test_dict[f"key{i}"] = f"value{i}"

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(pop_and_repopulate, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nPop index: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
