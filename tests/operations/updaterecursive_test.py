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

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations import update_recursive


# Definitions #
# Classes #
class TestUpdateRecursive:
    """Test the update_recursive function.

    This class tests the functionality of the update_recursive function, which updates a mapping object and its
    contained mappings based on another mapping.
    """

    # Instance Methods #
    # Tests
    def test_update_recursive_simple(self) -> None:
        """Test updating a simple dictionary.

        This test verifies that the update_recursive function correctly updates a dictionary with values from another
        dictionary without nested mappings.
        """
        # Test with two simple dictionaries
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        result = update_recursive(d1, d2)

        # Verify the result is the updated first dictionary
        assert result is d1
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

        # Verify the second dictionary is unchanged
        assert d2 == {"c": 3, "d": 4}

    def test_update_recursive_overlapping_keys(self) -> None:
        """Test updating a dictionary with overlapping keys.

        This test verifies that the update_recursive function correctly updates a dictionary with values from another
        dictionary, with values from the second dictionary taking precedence.
        """
        # Test with dictionaries that have overlapping keys
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"b": 20, "c": 30, "d": 40}
        result = update_recursive(d1, d2)

        # Verify the result has all keys with values from d2 taking precedence for overlapping keys
        assert result is d1
        assert result == {"a": 1, "b": 20, "c": 30, "d": 40}

        # Verify the second dictionary is unchanged
        assert d2 == {"b": 20, "c": 30, "d": 40}

    def test_update_recursive_nested(self) -> None:
        """Test updating a dictionary with nested dictionaries.

        This test verifies that the update_recursive function correctly updates a dictionary with nested dictionaries,
        recursively merging the nested dictionaries.
        """
        # Test with dictionaries that have nested dictionaries
        d1 = {"a": 1, "b": {"x": 10, "y": 20}}
        d2 = {"c": 3, "b": {"y": 200, "z": 300}}
        result = update_recursive(d1, d2)

        # Verify the result has recursively merged the nested dictionaries
        assert result is d1
        assert result == {"a": 1, "b": {"x": 10, "y": 200, "z": 300}, "c": 3}

        # Verify the second dictionary is unchanged
        assert d2 == {"c": 3, "b": {"y": 200, "z": 300}}

    def test_update_recursive_deeply_nested(self) -> None:
        """Test updating a dictionary with deeply nested dictionaries.

        This test verifies that the update_recursive function correctly updates a dictionary with deeply nested
        dictionaries, recursively merging at all levels.
        """
        # Test with dictionaries that have deeply nested dictionaries
        d1 = {"a": {"b": {"c": {"d": 1}}}}
        d2 = {"a": {"b": {"c": {"e": 2}}}}
        result = update_recursive(d1, d2)

        # Verify the result has recursively merged the deeply nested dictionaries
        assert result is d1
        assert result == {"a": {"b": {"c": {"d": 1, "e": 2}}}}

        # Verify the second dictionary is unchanged
        assert d2 == {"a": {"b": {"c": {"e": 2}}}}

    def test_update_recursive_mixed_types(self) -> None:
        """Test updating a dictionary with mixed value types.

        This test verifies that the update_recursive function correctly handles dictionaries with mixed value types,
        including lists, tuples, and other non-mapping types.
        """
        # Test with dictionaries that have mixed value types
        d1 = {"a": 1, "b": [1, 2, 3], "c": {"x": 10}}
        d2 = {"d": (4, 5, 6), "c": {"y": 20}}
        result = update_recursive(d1, d2)

        # Verify the result has correctly merged the dictionaries
        assert result is d1
        assert result == {"a": 1, "b": [1, 2, 3], "c": {"x": 10, "y": 20}, "d": (4, 5, 6)}

        # Verify the second dictionary is unchanged
        assert d2 == {"d": (4, 5, 6), "c": {"y": 20}}

    def test_update_recursive_non_mapping_values(self) -> None:
        """Test updating a dictionary where nested values are replaced with non-mapping values.

        This test verifies that the update_recursive function correctly handles cases where a nested mapping in the
        first dictionary is replaced with a non-mapping value in the second.
        """
        # Test with a nested mapping being replaced by a non-mapping value
        d1 = {"a": {"b": {"c": 1}}}
        d2 = {"a": {"b": 2}}
        result = update_recursive(d1, d2)

        # Verify the result has replaced the nested mapping with the non-mapping value
        assert result is d1
        assert result == {"a": {"b": 2}}

        # Verify the second dictionary is unchanged
        assert d2 == {"a": {"b": 2}}

    def test_update_recursive_empty_dicts(self) -> None:
        """Test updating with empty dictionaries.

        This test verifies that the update_recursive function correctly handles empty dictionaries.
        """
        # Test with an empty first dictionary
        d1 = {}
        d2 = {"a": 1, "b": 2}
        result = update_recursive(d1, d2)
        assert result is d1
        assert result == {"a": 1, "b": 2}

        # Test with an empty second dictionary
        d1 = {"a": 1, "b": 2}
        d2 = {}
        result = update_recursive(d1, d2)
        assert result is d1
        assert result == {"a": 1, "b": 2}

        # Test with both dictionaries empty
        d1 = {}
        d2 = {}
        result = update_recursive(d1, d2)
        assert result is d1
        assert result == {}

    def test_update_recursive_with_iterable(self) -> None:
        """Test updating a dictionary with an iterable of key-value pairs.

        This test verifies that the update_recursive function correctly updates a dictionary with an iterable of
        key-value pairs.
        """
        # Test with an iterable of key-value pairs
        d1 = {"a": 1, "b": {"x": 10}}
        updates = [("c", 3), ("b", {"y": 20})]
        result = update_recursive(d1, updates)

        # Verify the result has correctly merged the dictionary with the iterable
        assert result is d1
        assert result == {"a": 1, "b": {"x": 10, "y": 20}, "c": 3}


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
