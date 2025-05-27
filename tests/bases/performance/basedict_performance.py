#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basedict_performance.py
Performance tests for the BaseDict class in the baseobjects package.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.bases.collections import BaseDict
from .base_performance import BaseBaseObjectPerformanceTest


# Definitions #
# Base Dict
class TestBaseDict(BaseBaseObjectPerformanceTest):
    """Test the performance of the BaseDict class.

    This class tests the performance of the BaseDict class, which is a mixin of UserDict and BaseObject.
    """
    # Class Definitions #
    class BaseTestDict(BaseDict):
        """A subclass of BaseDict for testing purposes."""
        pass

    # Attributes #
    class_: Type[BaseTestDict] = BaseTestDict

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_dict(self) -> "TestBaseDict.BaseTestDict":
        """Create a test dictionary for use in tests.

        Returns:
            BaseTestDict: An instance of the test class.
        """
        return self.class_()

    @pytest.fixture
    def populated_test_dict(self) -> "TestBaseDict.BaseTestDict":
        """Create a populated test dictionary for use in tests.

        Returns:
            BaseTestDict: A populated instance of the test class.
        """
        return self.class_({f"key{i}": f"value{i}" for i in range(100)})

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
        return {f"key{i}": f"value{i}" for i in range(100)}

    # Tests
    def test_instance_creation(self, test_dict: "TestBaseDict.BaseTestDict") -> None:
        """Test that instances of BaseTestDict can be created efficiently.

        Args:
            test_dict: A fixture providing a BaseTestDict instance.
        """
        assert test_dict is not None

    def test_creation_speed_empty(self) -> None:
        """Test the performance of creating an empty BaseDict.

        This test compares the speed of creating an empty BaseDict with a normal dictionary.
        """
        def create_base() -> None:
            self.BaseTestDict()

        def create_normal() -> None:
            {}

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
        """Test the performance of creating a populated BaseDict.

        This test compares the speed of creating a populated BaseDict with a normal dictionary.
        """
        test_data = {f"key{i}": f"value{i}" for i in range(100)}

        def create_base() -> None:
            self.BaseTestDict(test_data)

        def create_normal() -> None:
            dict(test_data)

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

    def test_get_item_speed(self, populated_test_dict: "TestBaseDict.BaseTestDict", populated_normal_dict: dict) -> None:
        """Test the performance of getting an item from a BaseDict.

        This test compares the speed of getting an item from a BaseDict with a normal dictionary.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
            populated_normal_dict: A fixture providing a populated normal dictionary.
        """
        key = "key50"

        def get_base() -> None:
            populated_test_dict[key]

        def get_normal() -> None:
            populated_normal_dict[key]

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

    def test_set_item_speed(self, test_dict: "TestBaseDict.BaseTestDict", normal_dict: dict) -> None:
        """Test the performance of setting an item in a BaseDict.

        This test compares the speed of setting an item in a BaseDict with a normal dictionary.

        Args:
            test_dict: A fixture providing a BaseTestDict instance.
            normal_dict: A fixture providing a normal dictionary.
        """
        key = "test_key"
        value = "test_value"

        def set_base() -> None:
            test_dict[key] = value

        def set_normal() -> None:
            normal_dict[key] = value

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

    def test_delete_item_speed(self, populated_test_dict: "TestBaseDict.BaseTestDict", populated_normal_dict: dict) -> None:
        """Test the performance of deleting an item from a BaseDict.

        This test compares the speed of deleting an item from a BaseDict with a normal dictionary.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
            populated_normal_dict: A fixture providing a populated normal dictionary.
        """
        # Create copies to avoid modifying the fixtures
        base_dict = self.BaseTestDict(populated_test_dict)
        normal_dict = dict(populated_normal_dict)
        key = "key50"

        def delete_base() -> None:
            if key in base_dict:
                del base_dict[key]
                base_dict[key] = "value50"  # Add it back for next iteration

        def delete_normal() -> None:
            if key in normal_dict:
                del normal_dict[key]
                normal_dict[key] = "value50"  # Add it back for next iteration

        # Calculate the mean time in microseconds for the new implementation
        new_time = timeit.timeit(delete_base, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the old implementation
        old_time = timeit.timeit(delete_normal, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (delete item): {mean_new:.3f} μs ({percent:.3f}% of old function time)")
        assert percent < self.speed_tolerance

    def test_iteration_speed(self, populated_test_dict: "TestBaseDict.BaseTestDict", populated_normal_dict: dict) -> None:
        """Test the performance of iterating over a BaseDict.

        This test compares the speed of iterating over a BaseDict with a normal dictionary.

        Args:
            populated_test_dict: A fixture providing a populated BaseTestDict instance.
            populated_normal_dict: A fixture providing a populated normal dictionary.
        """
        def iterate_base() -> None:
            for key in populated_test_dict:
                pass

        def iterate_normal() -> None:
            for key in populated_normal_dict:
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