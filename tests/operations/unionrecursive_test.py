#!/usr/bin/env python
"""unionrecursive_test.py
Tests for the union_recursive function in the baseobjects package.
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
from collections.abc import Mapping
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.operations import union_recursive


# Definitions #
# Classes #
class TestUnionRecursive:
    """Tests the union_recursive function.

    This class tests the functionality of the union_recursive function, which unions a mapping object and its contained
    mappings within another mapping.
    """

    # Instance Methods #
    # Tests
    @pytest.mark.parametrize(
        ("d1", "d2", "expected"),
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
        ],
    )
    def test_union_recursive(self, d1: dict[str, Any], d2: dict[str, Any], expected: dict[str, Any]) -> None:
        """Tests union_recursive with various scenarios.

        This test verifies that the union_recursive function correctly unions dictionaries in various scenarios,
        including simple merge, overlapping keys, nested dictionaries, mixed types, and empty dictionaries.
        """
        d1_copy = copy.deepcopy(d1)
        d2_copy = copy.deepcopy(d2)

        result = union_recursive(d1_copy, d2_copy)

        # Verify the result
        assert isinstance(result, Mapping)
        assert result == expected

        # Verify the original dictionaries are unchanged
        assert d1_copy == d1
        assert d2_copy == d2


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
