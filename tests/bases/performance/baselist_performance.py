#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""baselist_performance.py
Performance tests for the BaseList class in the baseobjects.bases.collections package.
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
import timeit
from collections import UserList
from typing import Any, List

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.testsuite import BasePerformanceTestSuite
from src.baseobjects.bases.collections import BaseList


# Definitions #
# Classes #
class TestBaseListPerformance(BasePerformanceTestSuite):
    """Test suite for assaying the performance of the BaseList class.

    This test suite measures the performance of various operations on BaseList objects
    and compares them with standard Python lists and UserList.
    """
    # Class Definitions #
    class TestList(BaseList):
        """A concrete subclass of BaseList for testing purposes."""
        pass

    # Attributes #
    timeit_runs: int = 100000
    list_size: int = 100  # Size of lists for performance tests

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_list(self) -> "TestBaseListPerformance.TestList":
        """Create a test list instance for use in tests.

        Returns:
            TestList: An instance of the test class with some initial data.
        """
        return self.TestList([f"item_{i}" for i in range(self.list_size)])

    @pytest.fixture
    def test_user_list(self) -> UserList:
        """Create a UserList instance for comparison.

        Returns:
            UserList: A UserList instance with the same initial data as test_list.
        """
        return UserList([f"item_{i}" for i in range(self.list_size)])

    @pytest.fixture
    def test_std_list(self) -> List[str]:
        """Create a standard list for comparison.

        Returns:
            List[str]: A standard list with the same initial data as test_list.
        """
        return [f"item_{i}" for i in range(self.list_size)]

    # Tests
    def test_creation_performance(self) -> None:
        """Test the performance of creating BaseList instances.

        This test compares the speed of creating BaseList instances with creating
        standard Python lists and UserList instances.
        """
        init_data = [f"item_{i}" for i in range(self.list_size)]

        def create_base_list() -> None:
            self.TestList(init_data)

        def create_user_list() -> None:
            UserList(init_data)

        def create_std_list() -> None:
            list(init_data)

        # Calculate the mean time in microseconds for BaseList creation
        base_time = timeit.timeit(create_base_list, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList creation
        user_time = timeit.timeit(create_user_list, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list creation
        std_time = timeit.timeit(create_std_list, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list creation: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList creation: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList creation: {mean_base:.3f} μs ({percent_user:.3f}% of UserList creation time, {percent_std:.3f}% of standard list creation time)")
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserList
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard list

    def test_get_item_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of getting items from lists.

        This test compares the speed of getting items from BaseList with getting items from
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        # Use an index that exists in all lists
        index = 50

        def get_base_list_item() -> None:
            _ = test_list[index]

        def get_user_list_item() -> None:
            _ = test_user_list[index]

        def get_std_list_item() -> None:
            _ = test_std_list[index]

        # Calculate the mean time in microseconds for BaseList item access
        base_time = timeit.timeit(get_base_list_item, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList item access
        user_time = timeit.timeit(get_user_list_item, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list item access
        std_time = timeit.timeit(get_std_list_item, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list item access: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList item access: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList item access: {mean_base:.3f} μs ({percent_user:.3f}% of UserList item access time, {percent_std:.3f}% of standard list item access time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_set_item_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of setting items in lists.

        This test compares the speed of setting items in BaseList with setting items in
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        # Use an index that exists in all lists
        index = 50
        value = "new_value"

        def set_base_list_item() -> None:
            test_list[index] = value

        def set_user_list_item() -> None:
            test_user_list[index] = value

        def set_std_list_item() -> None:
            test_std_list[index] = value

        # Calculate the mean time in microseconds for BaseList item setting
        base_time = timeit.timeit(set_base_list_item, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList item setting
        user_time = timeit.timeit(set_user_list_item, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list item setting
        std_time = timeit.timeit(set_std_list_item, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list item setting: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList item setting: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList item setting: {mean_base:.3f} μs ({percent_user:.3f}% of UserList item setting time, {percent_std:.3f}% of standard list item setting time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_append_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of appending items to lists.

        This test compares the speed of appending items to BaseList with appending items to
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        value = "appended_value"

        def append_to_base_list() -> None:
            test_list.append(value)
            test_list.pop()  # Remove the appended item to keep the list size constant

        def append_to_user_list() -> None:
            test_user_list.append(value)
            test_user_list.pop()  # Remove the appended item to keep the list size constant

        def append_to_std_list() -> None:
            test_std_list.append(value)
            test_std_list.pop()  # Remove the appended item to keep the list size constant

        # Calculate the mean time in microseconds for BaseList append
        base_time = timeit.timeit(append_to_base_list, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList append
        user_time = timeit.timeit(append_to_user_list, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list append
        std_time = timeit.timeit(append_to_std_list, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list append: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList append: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList append: {mean_base:.3f} μs ({percent_user:.3f}% of UserList append time, {percent_std:.3f}% of standard list append time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_extend_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of extending lists.

        This test compares the speed of extending BaseList with extending
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        extension = ["ext_1", "ext_2", "ext_3"]

        def extend_base_list() -> None:
            test_list.extend(extension)
            for _ in range(len(extension)):
                test_list.pop()  # Remove the extended items to keep the list size constant

        def extend_user_list() -> None:
            test_user_list.extend(extension)
            for _ in range(len(extension)):
                test_user_list.pop()  # Remove the extended items to keep the list size constant

        def extend_std_list() -> None:
            test_std_list.extend(extension)
            for _ in range(len(extension)):
                test_std_list.pop()  # Remove the extended items to keep the list size constant

        # Calculate the mean time in microseconds for BaseList extend
        base_time = timeit.timeit(extend_base_list, number=self.timeit_runs // 10)  # Reduce runs for extend operations
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for UserList extend
        user_time = timeit.timeit(extend_user_list, number=self.timeit_runs // 10)  # Reduce runs for extend operations
        mean_user = user_time / (self.timeit_runs // 10) * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list extend
        std_time = timeit.timeit(extend_std_list, number=self.timeit_runs // 10)  # Reduce runs for extend operations
        mean_std = std_time / (self.timeit_runs // 10) * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list extend: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList extend: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList extend: {mean_base:.3f} μs ({percent_user:.3f}% of UserList extend time, {percent_std:.3f}% of standard list extend time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_insert_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of inserting items into lists.

        This test compares the speed of inserting items into BaseList with inserting items into
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        index = 50
        value = "inserted_value"

        def insert_into_base_list() -> None:
            test_list.insert(index, value)
            test_list.pop(index)  # Remove the inserted item to keep the list size constant

        def insert_into_user_list() -> None:
            test_user_list.insert(index, value)
            test_user_list.pop(index)  # Remove the inserted item to keep the list size constant

        def insert_into_std_list() -> None:
            test_std_list.insert(index, value)
            test_std_list.pop(index)  # Remove the inserted item to keep the list size constant

        # Calculate the mean time in microseconds for BaseList insert
        base_time = timeit.timeit(insert_into_base_list, number=self.timeit_runs // 10)  # Reduce runs for insert operations
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for UserList insert
        user_time = timeit.timeit(insert_into_user_list, number=self.timeit_runs // 10)  # Reduce runs for insert operations
        mean_user = user_time / (self.timeit_runs // 10) * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list insert
        std_time = timeit.timeit(insert_into_std_list, number=self.timeit_runs // 10)  # Reduce runs for insert operations
        mean_std = std_time / (self.timeit_runs // 10) * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list insert: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList insert: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList insert: {mean_base:.3f} μs ({percent_user:.3f}% of UserList insert time, {percent_std:.3f}% of standard list insert time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_iteration_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of iterating over lists.

        This test compares the speed of iterating over BaseList with iterating over
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        def iterate_base_list() -> None:
            for _ in test_list:
                pass

        def iterate_user_list() -> None:
            for _ in test_user_list:
                pass

        def iterate_std_list() -> None:
            for _ in test_std_list:
                pass

        # Calculate the mean time in microseconds for BaseList iteration
        base_time = timeit.timeit(iterate_base_list, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList iteration
        user_time = timeit.timeit(iterate_user_list, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list iteration
        std_time = timeit.timeit(iterate_std_list, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list iteration: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList iteration: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList iteration: {mean_base:.3f} μs ({percent_user:.3f}% of UserList iteration time, {percent_std:.3f}% of standard list iteration time)")
        assert percent_user < self.speed_tolerance * 1.5  # Allow some overhead compared to UserList
        assert percent_std < self.speed_tolerance * 2  # Allow more overhead compared to standard list

    def test_copy_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of copying lists.

        This test compares the speed of copying BaseList with copying
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        def copy_base_list() -> None:
            test_list.copy()

        def copy_user_list() -> None:
            copy.copy(test_user_list)

        def copy_std_list() -> None:
            test_std_list.copy()

        # Calculate the mean time in microseconds for BaseList copy
        base_time = timeit.timeit(copy_base_list, number=self.timeit_runs)
        mean_base = base_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for UserList copy
        user_time = timeit.timeit(copy_user_list, number=self.timeit_runs)
        mean_user = user_time / self.timeit_runs * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list copy
        std_time = timeit.timeit(copy_std_list, number=self.timeit_runs)
        mean_std = std_time / self.timeit_runs * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list copy: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList copy: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList copy: {mean_base:.3f} μs ({percent_user:.3f}% of UserList copy time, {percent_std:.3f}% of standard list copy time)")
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserList
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard list

    def test_deepcopy_performance(
        self,
        test_list: "TestBaseListPerformance.TestList",
        test_user_list: UserList,
        test_std_list: List[str],
    ) -> None:
        """Test the performance of deep copying lists.

        This test compares the speed of deep copying BaseList with deep copying
        standard Python lists and UserList instances.

        Args:
            test_list: A fixture providing a TestList instance.
            test_user_list: A fixture providing a UserList instance.
            test_std_list: A fixture providing a standard list.
        """
        def deepcopy_base_list() -> None:
            test_list.deepcopy()

        def deepcopy_user_list() -> None:
            copy.deepcopy(test_user_list)

        def deepcopy_std_list() -> None:
            copy.deepcopy(test_std_list)

        # Calculate the mean time in microseconds for BaseList deepcopy
        base_time = timeit.timeit(deepcopy_base_list, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_base = base_time / (self.timeit_runs // 10) * 1000000

        # Calculate the mean time in microseconds for UserList deepcopy
        user_time = timeit.timeit(deepcopy_user_list, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_user = user_time / (self.timeit_runs // 10) * 1000000
        percent_user = (mean_base / mean_user) * 100

        # Calculate the mean time in microseconds for standard list deepcopy
        std_time = timeit.timeit(deepcopy_std_list, number=self.timeit_runs // 10)  # Reduce runs for deepcopy
        mean_std = std_time / (self.timeit_runs // 10) * 1000000
        percent_std = (mean_base / mean_std) * 100

        # Print the performance comparison
        print(f"\nStandard list deepcopy: {mean_std:.3f} μs ({self.call_speed:.3f} is the speed of a simple function call)")
        print(f"UserList deepcopy: {mean_user:.3f} μs ({mean_user / mean_std:.3f}x standard list)")
        print(f"BaseList deepcopy: {mean_base:.3f} μs ({percent_user:.3f}% of UserList deepcopy time, {percent_std:.3f}% of standard list deepcopy time)")
        assert percent_user < self.speed_tolerance * 2  # Allow more overhead compared to UserList
        assert percent_std < self.speed_tolerance * 3  # Allow more overhead compared to standard list


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])