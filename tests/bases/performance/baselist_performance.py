#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" baselist_performance.py
Performance tests for the BaseList class in the baseobjects package.
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
from src.baseobjects.bases.collections import BaseList
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base List
class TestBaseList(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseList class.

    This class tests the performance of the BaseList class, which is a mixin of UserList and BaseObject.
    """
    # Class Definitions #
    class BaseTestList(BaseList):
        """A subclass of BaseList for testing purposes."""
        pass

    # Attributes #
    class_: Type[BaseTestList] = BaseTestList

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_list(self) -> "TestBaseList.BaseTestList":
        """Create a test list for use in tests.

        Returns:
            BaseTestList: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def populated_test_list(self) -> "TestBaseList.BaseTestList":
        """Create a populated test list for use in tests.

        Returns:
            BaseTestList: A populated instance of the test class.
        """
        result = self.class_()
        result.extend([f"value{i}" for i in range(100)])
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

    # Tests
    def test_instance_creation(self, test_list: "TestBaseList.BaseTestList") -> None:
        """Test that instances of BaseTestList can be created efficiently.

        Args:
            test_list: A fixture providing a BaseTestList instance.
        """
        assert test_list is not None

    def test_creation_speed_empty(self) -> None:
        """Test the performance of creating an empty BaseList.

        This test compares the speed of creating an empty BaseList with a normal list.
        """
        def create_base() -> None:
            self.BaseTestList()

        def create_normal() -> None:
            []

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (empty creation): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_creation_speed_populated(self) -> None:
        """Test the performance of creating a populated BaseList.

        This test compares the speed of creating a populated BaseList with a normal list.
        """
        test_data = [f"value{i}" for i in range(100)]

        def create_base() -> None:
            base_list = self.BaseTestList()
            base_list.extend(test_data)

        def create_normal() -> None:
            list(test_data)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(create_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(create_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (populated creation): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_get_item_speed(self, populated_test_list: "TestBaseList.BaseTestList", populated_normal_list: list) -> None:
        """Test the performance of getting an item from a BaseList.

        This test compares the speed of getting an item from a BaseList with a normal list.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        index = 50

        def get_base() -> None:
            populated_test_list[index]

        def get_normal() -> None:
            populated_normal_list[index]

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(get_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(get_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (get item): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_set_item_speed(self, populated_test_list: "TestBaseList.BaseTestList", populated_normal_list: list) -> None:
        """Test the performance of setting an item in a BaseList.

        This test compares the speed of setting an item in a BaseList with a normal list.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        index = 50
        value = "new_value"

        def set_base() -> None:
            populated_test_list[index] = value

        def set_normal() -> None:
            populated_normal_list[index] = value

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(set_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(set_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (set item): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_append_speed(self, test_list: "TestBaseList.BaseTestList", normal_list: list) -> None:
        """Test the performance of appending an item to a BaseList.

        This test compares the speed of appending an item to a BaseList with a normal list.

        Args:
            test_list: A fixture providing a BaseTestList instance.
            normal_list: A fixture providing a normal list.
        """
        value = "test_value"

        def append_base() -> None:
            test_list.append(value)

        def append_normal() -> None:
            normal_list.append(value)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(append_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(append_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (append): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_extend_speed(self, test_list: "TestBaseList.BaseTestList", normal_list: list) -> None:
        """Test the performance of extending a BaseList.

        This test compares the speed of extending a BaseList with a normal list.

        Args:
            test_list: A fixture providing a BaseTestList instance.
            normal_list: A fixture providing a normal list.
        """
        values = ["value1", "value2", "value3", "value4", "value5"]

        def extend_base() -> None:
            test_list.extend(values)

        def extend_normal() -> None:
            normal_list.extend(values)

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(extend_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(extend_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (extend): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_iteration_speed(self, populated_test_list: "TestBaseList.BaseTestList", populated_normal_list: list) -> None:
        """Test the performance of iterating over a BaseList.

        This test compares the speed of iterating over a BaseList with a normal list.

        Args:
            populated_test_list: A fixture providing a populated BaseTestList instance.
            populated_normal_list: A fixture providing a populated normal list.
        """
        def iterate_base() -> None:
            for item in populated_test_list:
                pass

        def iterate_normal() -> None:
            for item in populated_normal_list:
                pass

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(iterate_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(iterate_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (iteration): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])