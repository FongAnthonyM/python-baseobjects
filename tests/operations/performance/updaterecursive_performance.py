#!/usr/bin/env python
"""updaterecursive_performance.py
Performance tests for the update_recursive function in the baseobjects.operations package.
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
from collections.abc import Mapping
from typing import Any, Dict

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations import update_recursive
from src.baseobjects.testsuite import BasePerformanceTestSuite


# Definitions #
# Functions #
def standard_update_recursive(d: dict[str, Any], updates: Mapping) -> dict[str, Any]:
    """Standard implementation of update_recursive using a recursive function.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    for key, value in updates.items():
        if key in d and isinstance(d[key], Mapping) and isinstance(value, Mapping):
            standard_update_recursive(d[key], value)
        else:
            d[key] = value
    return d


def standard_update_non_recursive(d: dict[str, Any], updates: Mapping) -> dict[str, Any]:
    """Standard implementation of update_recursive using a non-recursive approach.

    This implementation only handles one level of nesting and is used for comparison.

    Args:
        d: The mapping type to update recursively.
        updates: The mapping updates.

    Returns:
        The original mapping that has been updated.
    """
    d.update(updates)
    return d


# Classes #
class TestUpdateRecursive(BasePerformanceTestSuite):
    """Test the performance of the update_recursive function.

    This class tests the performance of the update_recursive function, which updates a mapping object and its contained
    mappings based on another mapping.
    """

    # Attributes #
    timeit_runs: int = 10000  # Reduced for more complex operations
    speed_tolerance: int = 150

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def simple_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create simple dictionaries for use in tests.

        Returns:
            tuple: A tuple containing two simple dictionaries.
        """
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"d": 4, "e": 5, "f": 6}
        return d1.copy(), d2

    @pytest.fixture
    def overlapping_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create dictionaries with overlapping keys for use in tests.

        Returns:
            tuple: A tuple containing two dictionaries with overlapping keys.
        """
        d1 = {"a": 1, "b": 2, "c": 3, "d": 4}
        d2 = {"c": 30, "d": 40, "e": 50, "f": 60}
        return d1.copy(), d2

    @pytest.fixture
    def nested_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create dictionaries with nested dictionaries for use in tests.

        Returns:
            tuple: A tuple containing two dictionaries with nested dictionaries.
        """
        d1 = {"a": 1, "b": {"x": 10, "y": 20}, "c": 3}
        d2 = {"d": 4, "b": {"y": 200, "z": 300}, "e": 5}
        return d1.copy(), d2

    @pytest.fixture
    def deeply_nested_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create dictionaries with deeply nested dictionaries for use in tests.

        Returns:
            tuple: A tuple containing two dictionaries with deeply nested dictionaries.
        """
        d1 = {"a": {"b": {"c": {"d": 1, "e": 2}}}, "f": 3}
        d2 = {"a": {"b": {"c": {"e": 20, "g": 30}}}, "h": 4}
        return d1.copy(), d2

    @pytest.fixture
    def mixed_type_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create dictionaries with mixed value types for use in tests.

        Returns:
            tuple: A tuple containing two dictionaries with mixed value types.
        """
        d1 = {"a": 1, "b": [1, 2, 3], "c": {"x": 10, "y": 20}}
        d2 = {"d": (4, 5, 6), "e": "string", "c": {"z": 30}}
        return d1.copy(), d2

    @pytest.fixture
    def large_dicts(self) -> tuple[dict[str, Any], dict[str, Any]]:
        """Create large dictionaries for use in tests.

        Returns:
            tuple: A tuple containing two large dictionaries.
        """
        d1 = {f"key{i}": i for i in range(100)}
        d2 = {f"key{i + 50}": i + 100 for i in range(100)}
        return d1.copy(), d2

    # Tests
    def test_update_recursive_simple_speed(self, simple_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with simple dictionaries.

        This test compares the speed of update_recursive with a standard implementation for simple dictionaries.

        Args:
            simple_dicts: A fixture providing simple dictionaries.
        """
        d1, d2 = simple_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (update_recursive simple): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_update_recursive_overlapping_speed(self, overlapping_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with dictionaries that have overlapping keys.

        This test compares the speed of update_recursive with a standard implementation for dictionaries with overlapping keys.

        Args:
            overlapping_dicts: A fixture providing dictionaries with overlapping keys.
        """
        d1, d2 = overlapping_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (update_recursive overlapping): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)",
        )
        assert percent < self.speed_tolerance

    def test_update_recursive_nested_speed(self, nested_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with dictionaries that have nested dictionaries.

        This test compares the speed of update_recursive with a standard implementation for dictionaries with nested dictionaries.

        Args:
            nested_dicts: A fixture providing dictionaries with nested dictionaries.
        """
        d1, d2 = nested_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (update_recursive nested): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance

    def test_update_recursive_deeply_nested_speed(
        self, deeply_nested_dicts: tuple[dict[str, Any], dict[str, Any]],
    ) -> None:
        """Test the performance of update_recursive with dictionaries that have deeply nested dictionaries.

        This test compares the speed of update_recursive with a standard implementation for dictionaries with deeply nested dictionaries.

        Args:
            deeply_nested_dicts: A fixture providing dictionaries with deeply nested dictionaries.
        """
        d1, d2 = deeply_nested_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (update_recursive deeply nested): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)",
        )
        assert percent < self.speed_tolerance

    def test_update_recursive_mixed_types_speed(self, mixed_type_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with dictionaries that have mixed value types.

        This test compares the speed of update_recursive with a standard implementation for dictionaries with mixed value types.

        Args:
            mixed_type_dicts: A fixture providing dictionaries with mixed value types.
        """
        d1, d2 = mixed_type_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (update_recursive mixed types): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)",
        )
        assert percent < self.speed_tolerance

    def test_update_recursive_vs_non_recursive(self, nested_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive compared to a non-recursive update.

        This test compares the speed of update_recursive with a non-recursive implementation to measure the overhead of recursion.

        Args:
            nested_dicts: A fixture providing dictionaries with nested dictionaries.
        """
        d1, d2 = nested_dicts

        def recursive_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def non_recursive_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_non_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the recursive implementation
        recursive_time = timeit.timeit(recursive_implementation, number=self.timeit_runs)
        mean_recursive = recursive_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the non-recursive implementation
        non_recursive_time = timeit.timeit(non_recursive_implementation, number=self.timeit_runs)
        mean_non_recursive = non_recursive_time / self.timeit_runs * 1000000
        percent = (mean_recursive / mean_non_recursive) * 100

        # Print the performance comparison
        print(f"\nRecursive: {mean_recursive:.3f} μs ({percent:.3f}% of non-recursive implementation time)")
        # No assertion here, just measuring the overhead of recursion

    def test_update_recursive_large_dicts_speed(self, large_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with large dictionaries.

        This test compares the speed of update_recursive with a standard implementation for large dictionaries.

        Args:
            large_dicts: A fixture providing large dictionaries.
        """
        d1, d2 = large_dicts

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, d2)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            standard_update_recursive(d1_copy, d2)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(
            f"\nNew (update_recursive large dicts): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)",
        )
        assert percent < self.speed_tolerance

    def test_update_recursive_iterable_speed(self, overlapping_dicts: tuple[dict[str, Any], dict[str, Any]]) -> None:
        """Test the performance of update_recursive with an iterable of key-value pairs.

        This test compares the speed of update_recursive with a standard implementation when using an iterable of key-value pairs.

        Args:
            overlapping_dicts: A fixture providing dictionaries with overlapping keys.
        """
        d1, d2 = overlapping_dicts
        items = list(d2.items())

        def custom_implementation() -> None:
            d1_copy = d1.copy()
            update_recursive(d1_copy, items)

        def standard_implementation() -> None:
            d1_copy = d1.copy()
            d1_copy.update(items)

        # Calculate the mean time in microseconds for the custom implementation
        new_time = timeit.timeit(custom_implementation, number=self.timeit_runs)
        mean_new = new_time / self.timeit_runs * 1000000

        # Calculate the mean time in microseconds for the standard implementation
        old_time = timeit.timeit(standard_implementation, number=self.timeit_runs)
        mean_old = old_time / self.timeit_runs * 1000000
        percent = (mean_new / mean_old) * 100

        # Print the performance comparison
        print(f"\nNew (update_recursive iterable): {mean_new:.3f} μs ({percent:.3f}% of standard implementation time)")
        assert percent < self.speed_tolerance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
