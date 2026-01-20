#!/usr/bin/env python
"""updaterecursive_test.py
Tests for the update_recursive function in the baseobjects package.
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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.operations import update_recursive


# Definitions #
# Classes #
class TestUpdateRecursive:
    """Tests the update_recursive function.

    This class tests the functionality of the update_recursive function, which updates a mapping object and its
    contained mappings based on another mapping.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("d1", "updates", "expected"),
        [
            (
                {"a": 1, "b": 2},
                {"c": 3, "d": 4},
                {"a": 1, "b": 2, "c": 3, "d": 4},
            ),
            (
                {"a": 1, "b": 2, "c": 3},
                {"b": 20, "c": 30, "d": 40},
                {"a": 1, "b": 20, "c": 30, "d": 40},
            ),
            (
                {"a": 1, "b": {"x": 10, "y": 20}},
                {"c": 3, "b": {"y": 200, "z": 300}},
                {"a": 1, "b": {"x": 10, "y": 200, "z": 300}, "c": 3},
            ),
            (
                {"a": {"b": {"c": {"d": 1}}}},
                {"a": {"b": {"c": {"e": 2}}}},
                {"a": {"b": {"c": {"d": 1, "e": 2}}}},
            ),
            (
                {"a": 1, "b": [1, 2, 3], "c": {"x": 10}},
                {"d": (4, 5, 6), "c": {"y": 20}},
                {"a": 1, "b": [1, 2, 3], "c": {"x": 10, "y": 20}, "d": (4, 5, 6)},
            ),
            (
                {"a": {"b": {"c": 1}}},
                {"a": {"b": 2}},
                {"a": {"b": 2}},
            ),
            ({}, {"a": 1, "b": 2}, {"a": 1, "b": 2}),
            ({"a": 1, "b": 2}, {}, {"a": 1, "b": 2}),
            ({}, {}, {}),
            (
                {"a": 1, "b": {"x": 10}},
                [("c", 3), ("b", {"y": 20})],
                {"a": 1, "b": {"x": 10, "y": 20}, "c": 3},
            ),
        ],
    )
    def test_update_recursive(self, d1: dict[str, Any], updates: Any, expected: dict[str, Any]) -> None:
        """Tests update_recursive with various scenarios.

        This test verifies that the update_recursive function correctly updates dictionaries in various scenarios,
        including simple merge, overlapping keys, nested dictionaries, mixed types, empty dictionaries, and iterable
        inputs.
        """
        # Standard Libraries #
        import copy

        # Deepcopy d1 because it is modified in place
        d1_copy = copy.deepcopy(d1)
        # Deepcopy updates if it is a dict, to verify it's unchanged.
        # If it's a list (iterable), deepcopying is also fine.
        updates_copy = copy.deepcopy(updates)

        result = update_recursive(d1_copy, updates_copy)

        # Verify the result is the updated first dictionary
        assert result is d1_copy
        assert result == expected

        # Verify the updates object is unchanged (if it was a dict)
        if isinstance(updates, dict):
            assert updates_copy == updates


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
