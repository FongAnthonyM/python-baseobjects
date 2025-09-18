#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" unionrecursive_test.py
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
from collections.abc import Mapping

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.operations import union_recursive


# Definitions #
# Classes #
class TestUnionRecursive:
    """Test the union_recursive function.

    This class tests_old_ the functionality of the union_recursive function, which unions a mapping object and its contained
    mappings within another mapping.
    """

    # Instance Methods #
    # Tests
    def test_union_recursive_simple(self) -> None:
        """Test unioning two simple dictionaries.

        This test verifies that the union_recursive function correctly unions two simple dictionaries without nested
        mappings.
        """
        # Test with two simple dictionaries
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        result = union_recursive(d1, d2)
        
        # Verify the result is a new dictionary with all keys from both dictionaries
        assert isinstance(result, Mapping)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": 1, "b": 2}
        assert d2 == {"c": 3, "d": 4}

    def test_union_recursive_overlapping_keys(self) -> None:
        """Test unioning dictionaries with overlapping keys.

        This test verifies that the union_recursive function correctly unions dictionaries with overlapping keys, with
        values from the second dictionary taking precedence.
        """
        # Test with dictionaries that have overlapping keys
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"b": 20, "c": 30, "d": 40}
        result = union_recursive(d1, d2)
        
        # Verify the result has all keys with values from d2 taking precedence for overlapping keys
        assert result == {"a": 1, "b": 20, "c": 30, "d": 40}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": 1, "b": 2, "c": 3}
        assert d2 == {"b": 20, "c": 30, "d": 40}

    def test_union_recursive_nested(self) -> None:
        """Test unioning dictionaries with nested dictionaries.

        This test verifies that the union_recursive function correctly unions dictionaries with nested dictionaries,
        recursively merging the nested dictionaries.
        """
        # Test with dictionaries that have nested dictionaries
        d1 = {"a": 1, "b": {"x": 10, "y": 20}}
        d2 = {"c": 3, "b": {"y": 200, "z": 300}}
        result = union_recursive(d1, d2)
        
        # Verify the result has recursively merged the nested dictionaries
        assert result == {"a": 1, "b": {"x": 10, "y": 200, "z": 300}, "c": 3}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": 1, "b": {"x": 10, "y": 20}}
        assert d2 == {"c": 3, "b": {"y": 200, "z": 300}}

    def test_union_recursive_deeply_nested(self) -> None:
        """Test unioning dictionaries with deeply nested dictionaries.

        This test verifies that the union_recursive function correctly unions dictionaries with deeply nested
        dictionaries, recursively merging at all levels.
        """
        # Test with dictionaries that have deeply nested dictionaries
        d1 = {"a": {"b": {"c": {"d": 1}}}}
        d2 = {"a": {"b": {"c": {"e": 2}}}}
        result = union_recursive(d1, d2)
        
        # Verify the result has recursively merged the deeply nested dictionaries
        assert result == {"a": {"b": {"c": {"d": 1, "e": 2}}}}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": {"b": {"c": {"d": 1}}}}
        assert d2 == {"a": {"b": {"c": {"e": 2}}}}

    def test_union_recursive_mixed_types(self) -> None:
        """Test unioning dictionaries with mixed value types.

        This test verifies that the union_recursive function correctly handles dictionaries with mixed value types,
        including lists, tuples, and other non-mapping types.
        """
        # Test with dictionaries that have mixed value types
        d1 = {"a": 1, "b": [1, 2, 3], "c": {"x": 10}}
        d2 = {"d": (4, 5, 6), "c": {"y": 20}}
        result = union_recursive(d1, d2)
        
        # Verify the result has correctly merged the dictionaries
        assert result == {"a": 1, "b": [1, 2, 3], "c": {"x": 10, "y": 20}, "d": (4, 5, 6)}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": 1, "b": [1, 2, 3], "c": {"x": 10}}
        assert d2 == {"d": (4, 5, 6), "c": {"y": 20}}

    def test_union_recursive_non_mapping_values(self) -> None:
        """Test unioning dictionaries where nested values are replaced with non-mapping values.

        This test verifies that the union_recursive function correctly handles cases where a nested mapping in the first
        dictionary is replaced with a non-mapping value in the second.
        """
        # Test with a nested mapping being replaced by a non-mapping value
        d1 = {"a": {"b": {"c": 1}}}
        d2 = {"a": {"b": 2}}
        result = union_recursive(d1, d2)
        
        # Verify the result has replaced the nested mapping with the non-mapping value
        assert result == {"a": {"b": 2}}
        
        # Verify the original dictionaries are unchanged
        assert d1 == {"a": {"b": {"c": 1}}}
        assert d2 == {"a": {"b": 2}}

    def test_union_recursive_empty_dicts(self) -> None:
        """Test unioning with empty dictionaries.

        This test verifies that the union_recursive function correctly handles empty dictionaries.
        """
        # Test with an empty first dictionary
        d1 = {}
        d2 = {"a": 1, "b": 2}
        result = union_recursive(d1, d2)
        assert result == {"a": 1, "b": 2}
        
        # Test with an empty second dictionary
        d1 = {"a": 1, "b": 2}
        d2 = {}
        result = union_recursive(d1, d2)
        assert result == {"a": 1, "b": 2}
        
        # Test with both dictionaries empty
        d1 = {}
        d2 = {}
        result = union_recursive(d1, d2)
        assert result == {}


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])