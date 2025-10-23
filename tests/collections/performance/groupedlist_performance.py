#!/usr/bin/env python
"""groupedlist_performance.py
Performance tests for the GroupedList class in the baseobjects.collections package.
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
from src.baseobjects.collections import GroupedList
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Classes #
class TestGroupedListPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the GroupedList class.

    This test suite measures the performance of various operations on GroupedList objects
    and compares them with standard Python list implementations.
    """

    # Attributes #
    timeit_runs: int = 10000  # Reduced for more complex operations
    speed_tolerance: float = 200.0  # Higher tolerance for complex structures

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_list(self) -> GroupedList:
        """Create a test GroupedList for use in tests.

        Returns:
            GroupedList: An instance of GroupedList.
        """
        return GroupedList()

    @pytest.fixture
    def populated_test_list(self) -> GroupedList:
        """Create a populated test GroupedList for use in tests.

        Returns:
            GroupedList: A populated instance of GroupedList.
        """
        result = GroupedList()
        for i in range(100):
            result.append(f"value{i}")
        return result

    @pytest.fixture
    def nested_test_list(self) -> GroupedList:
        """Create a nested test GroupedList for use in tests.

        Returns:
            GroupedList: A nested instance of GroupedList with groups.
        """
        result = GroupedList()
        # Add some direct items
        for i in range(20):
            result.append(f"value{i}")

        # Create a group and add items to it
        group1 = result.create_group("group1")
        for i in range(20, 40):
            group1.append(f"value{i}")

        # Create a nested group and add items to it
        group2 = group1.create_group("group2")
        for i in range(40, 60):
            group2.append(f"value{i}")

        # Create another top-level group
        group3 = result.create_group("group3")
        for i in range(60, 80):
            group3.append(f"value{i}")

        return result

    @pytest.fixture
    def normal_list(self) -> list:
        """Create a normal list for comparison.

        Returns:
            list: A standard Python list.
        """
        return []

    @pytest.fixture
    def populated_normal_list(self) -> list:
        """Create a populated normal list for comparison.

        Returns:
            list: A populated standard Python list.
        """
        return [f"value{i}" for i in range(100)]

    @pytest.fixture
    def nested_normal_list(self) -> list:
        """Create a nested normal list for comparison.

        Returns:
            list: A nested standard Python list.
        """
        result = []
        # Add some direct items
        for i in range(20):
            result.append(f"value{i}")

        # Add a sublist
        sublist1 = []
        for i in range(20, 40):
            sublist1.append(f"value{i}")

        # Add a nested sublist
        sublist2 = []
        for i in range(40, 60):
            sublist2.append(f"value{i}")
        sublist1.append(sublist2)

        result.append(sublist1)

        # Add another sublist
        sublist3 = []
        for i in range(60, 80):
            sublist3.append(f"value{i}")

        result.append(sublist3)

        return result

    # Tests
    def test_instance_creation_performance(self) -> None:
        """Test the performance of creating GroupedList instances.

        This test compares the speed of creating an empty GroupedList with a normal list.
        """

        def create_grouped() -> None:
            GroupedList()

        def create_list() -> None:
            []

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(create_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(create_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list creation: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"GroupedList creation: {mean_grouped:.3f} μs ({percent:.3f}% of standard list creation time)")
        assert percent < self.speed_tolerance

    def test_creation_speed_populated_performance(self) -> None:
        """Test the performance of creating a populated GroupedList.

        This test compares the speed of creating a populated GroupedList with a normal list.
        """
        test_data = [f"value{i}" for i in range(100)]

        def create_grouped() -> None:
            GroupedList(test_data)

        def create_list() -> None:
            list(test_data)

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(create_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(create_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list populated creation: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(
            f"GroupedList populated creation: {mean_grouped:.3f} μs ({percent:.3f}% of standard list populated creation time)",
        )
        assert percent < self.speed_tolerance

    def test_append_speed_performance(self, test_list: GroupedList, normal_list: list) -> None:
        """Test the performance of appending an item to a GroupedList.

        This test compares the speed of appending an item to a GroupedList with a normal list.

        Args:
            test_list: A fixture providing a GroupedList instance.
            normal_list: A fixture providing a normal list.
        """
        value = "test_value"

        def append_grouped() -> None:
            test_list.append(value)

        def append_list() -> None:
            normal_list.append(value)

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(append_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(append_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list append: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"GroupedList append: {mean_grouped:.3f} μs ({percent:.3f}% of standard list append time)")
        assert percent < self.speed_tolerance

    def test_get_item_speed_performance(self, populated_test_list: GroupedList, populated_normal_list: list) -> None:
        """Test the performance of getting an item from a GroupedList.

        This test compares the speed of getting an item from a GroupedList with a normal list.

        Args:
            populated_test_list: A fixture providing a populated GroupedList instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        index = 50

        def get_grouped() -> None:
            populated_test_list[index]

        def get_list() -> None:
            populated_normal_list[index]

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(get_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(get_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list get item: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"GroupedList get item: {mean_grouped:.3f} μs ({percent:.3f}% of standard list get item time)")
        assert percent < self.speed_tolerance

    def test_set_item_speed_performance(self, populated_test_list: GroupedList, populated_normal_list: list) -> None:
        """Test the performance of setting an item in a GroupedList.

        This test compares the speed of setting an item in a GroupedList with a normal list.

        Args:
            populated_test_list: A fixture providing a populated GroupedList instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        index = 50
        value = "new_value"

        def set_grouped() -> None:
            populated_test_list[index] = value

        def set_list() -> None:
            populated_normal_list[index] = value

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(set_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the list implementation
        list_time = timeit.timeit(set_list, number=self.timeit_runs)
        mean_list = list_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_list) * 100

        # Print the performance comparison
        print(
            f"\nStandard list set item: {mean_list:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"GroupedList set item: {mean_grouped:.3f} μs ({percent:.3f}% of standard list set item time)")
        assert percent < self.speed_tolerance

    def test_iteration_speed_performance(self, nested_test_list: GroupedList) -> None:
        """Test the performance of iterating over a nested GroupedList.

        This test compares the speed of iterating over a nested GroupedList with a flattened list.

        Args:
            nested_test_list: A fixture providing a nested GroupedList instance.
        """
        # Create a flattened list for comparison
        flat_list = nested_test_list.as_flat_list()

        def iterate_grouped() -> None:
            for _item in nested_test_list:
                pass

        def iterate_flat() -> None:
            for _item in flat_list:
                pass

        # Calculate the mean time in microseconds for the GroupedList implementation
        grouped_time = timeit.timeit(iterate_grouped, number=self.timeit_runs)
        mean_grouped = grouped_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the flat list implementation
        flat_time = timeit.timeit(iterate_flat, number=self.timeit_runs)
        mean_flat = flat_time / self.timeit_runs * 1000000
        percent = (mean_grouped / mean_flat) * 100

        # Print the performance comparison
        print(
            f"\nFlat list iteration: {mean_flat:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"GroupedList iteration: {mean_grouped:.3f} μs ({percent:.3f}% of flat list iteration time)")
        assert percent < self.speed_tolerance

    def test_create_group_speed_performance(self, test_list: GroupedList) -> None:
        """Test the performance of creating a group in a GroupedList.

        This test measures the speed of creating a group.

        Args:
            test_list: A fixture providing a GroupedList instance.
        """
        # We'll use different group names for each run to avoid KeyError
        group_names = [f"group{i}" for i in range(self.timeit_runs)]
        group_index = 0

        def create_group() -> None:
            nonlocal group_index
            group_name = group_names[group_index]
            group_index += 1
            test_list.create_group(group_name)

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(create_group, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nCreate group: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_require_group_speed_performance(self, test_list: GroupedList) -> None:
        """Test the performance of requiring a group in a GroupedList.

        This test measures the speed of requiring a group (get or create).

        Args:
            test_list: A fixture providing a GroupedList instance.
        """
        # Create a group that will be reused
        group_name = "test_group"
        test_list.create_group(group_name)

        def require_existing_group() -> None:
            test_list.require_group(group_name)

        # Calculate the mean time in microseconds for requiring an existing group
        existing_time = timeit.timeit(require_existing_group, number=self.timeit_runs)
        mean_existing = existing_time / self.timeit_runs * 1000000

        # We'll use different group names for each run to test creating new groups
        new_group_names = [f"new_group{i}" for i in range(self.timeit_runs)]
        group_index = 0

        def require_new_group() -> None:
            nonlocal group_index
            group_name = new_group_names[group_index]
            group_index += 1
            test_list.require_group(group_name)

        # Calculate the mean time in microseconds for requiring a new group
        new_time = timeit.timeit(require_new_group, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Print the performance measurements
        print(
            f"\nRequire existing group: {mean_existing:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)",
        )
        print(f"Require new group: {mean_new:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_as_flat_list_speed_performance(self, nested_test_list: GroupedList) -> None:
        """Test the performance of flattening a nested GroupedList.

        This test measures the speed of converting a nested GroupedList to a flat list.

        Args:
            nested_test_list: A fixture providing a nested GroupedList instance.
        """

        def as_flat_list() -> None:
            nested_test_list.as_flat_list()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(as_flat_list, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nAs flat list: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_as_flat_tuple_speed_performance(self, nested_test_list: GroupedList) -> None:
        """Test the performance of flattening a nested GroupedList to a tuple.

        This test measures the speed of converting a nested GroupedList to a flat tuple.

        Args:
            nested_test_list: A fixture providing a nested GroupedList instance.
        """

        def as_flat_tuple() -> None:
            nested_test_list.as_flat_tuple()

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(as_flat_tuple, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nAs flat tuple: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_get_group_speed_performance(self, nested_test_list: GroupedList) -> None:
        """Test the performance of getting a group from a GroupedList.

        This test measures the speed of getting a group by name.

        Args:
            nested_test_list: A fixture providing a nested GroupedList instance.
        """
        group_name = "group1"

        def get_group() -> None:
            nested_test_list[group_name]

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(get_group, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nGet group: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time

    def test_nested_get_item_speed_performance(self, nested_test_list: GroupedList) -> None:
        """Test the performance of getting an item from a nested group in a GroupedList.

        This test measures the speed of getting an item from a nested group.

        Args:
            nested_test_list: A fixture providing a nested GroupedList instance.
        """

        # Get an item from a nested group
        def get_nested_item() -> None:
            nested_test_list.get_item(30)  # This should be in group1

        # Calculate the mean time in microseconds
        time_taken = timeit.timeit(get_nested_item, number=self.timeit_runs)
        mean_time = time_taken / self.timeit_runs * 1000000

        # Print the performance measurement
        print(f"\nGet nested item: {mean_time:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        # No comparison here, just measuring the absolute time


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
