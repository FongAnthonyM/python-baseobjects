#!/usr/bin/env python
"""methodnames_test.py
Tests for the method name functions in the baseobjects package.
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
from collections.abc import Generator

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.operations import (
    get_method_names,
    get_public_method_names,
    iter_method_names,
    iter_public_method_names,
)


# Definitions #
# Classes #
class TestMethodNames:
    """Test the method name functions.

    This class tests the functionality of the functions that retrieve method names from objects.
    """

    # Class Definitions #
    class TestClass:
        """A test class with various methods for testing method name functions."""

        def public_method(self) -> None:
            """A public method."""

        def another_public_method(self) -> None:
            """Another public method."""

        def _private_method(self) -> None:
            """A private method."""

        def __dunder_method__(self) -> None:
            """A dunder method."""

        @property
        def some_property(self) -> str:
            """A property."""
            return "property"

        # A non-callable attribute
        non_callable_attr = "not a method"

    # Instance Methods #
    # Tests
    def test_iter_method_names(self) -> None:
        """Test iterating over method names.

        This test verifies that the iter_method_names function correctly yields all method names of an object, including
        public, private, and dunder methods.
        """
        # Create an instance of the test class
        test_obj = self.TestClass()

        # Get the method names
        method_names = list(iter_method_names(test_obj))

        # Verify that all methods are included
        assert "public_method" in method_names
        assert "another_public_method" in method_names
        assert "_private_method" in method_names
        assert "__dunder_method__" in method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in method_names

        # Verify the return type is a generator
        assert isinstance(iter_method_names(test_obj), Generator)

    def test_iter_public_method_names(self) -> None:
        """Test iterating over public method names.

        This test verifies that the iter_public_method_names function correctly yields only public method names of an
        object (those not starting with '_').
        """
        # Create an instance of the test class
        test_obj = self.TestClass()

        # Get the public method names
        public_method_names = list(iter_public_method_names(test_obj))

        # Verify that only public methods are included
        assert "public_method" in public_method_names
        assert "another_public_method" in public_method_names

        # Private and dunder methods should not be included
        assert "_private_method" not in public_method_names
        assert "__dunder_method__" not in public_method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in public_method_names

        # Verify the return type is a generator
        assert isinstance(iter_public_method_names(test_obj), Generator)

    def test_get_method_names(self) -> None:
        """Test getting method names as a tuple.

        This test verifies that the get_method_names function correctly returns a tuple of all method names of an
        object.
        """
        # Create an instance of the test class
        test_obj = self.TestClass()

        # Get the method names
        method_names = get_method_names(test_obj)

        # Verify that all methods are included
        assert "public_method" in method_names
        assert "another_public_method" in method_names
        assert "_private_method" in method_names
        assert "__dunder_method__" in method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in method_names

        # Verify the return type is a tuple
        assert isinstance(method_names, tuple)

    def test_get_public_method_names(self) -> None:
        """Test getting public method names as a tuple.

        This test verifies that the get_public_method_names function correctly returns a tuple of public method names of
        an object.
        """
        # Create an instance of the test class
        test_obj = self.TestClass()

        # Get the public method names
        public_method_names = get_public_method_names(test_obj)

        # Verify that only public methods are included
        assert "public_method" in public_method_names
        assert "another_public_method" in public_method_names

        # Private and dunder methods should not be included
        assert "_private_method" not in public_method_names
        assert "__dunder_method__" not in public_method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in public_method_names

        # Verify the return type is a tuple
        assert isinstance(public_method_names, tuple)

    def test_with_builtin_objects(self) -> None:
        """Test with built-in objects.

        This test verifies that the method name functions work correctly with built-in objects.
        """
        # Test with a list
        list_obj = [1, 2, 3]
        list_methods = get_method_names(list_obj)
        list_public_methods = get_public_method_names(list_obj)

        # Verify some common list methods are included
        assert "append" in list_methods
        assert "append" in list_public_methods
        assert "extend" in list_methods
        assert "extend" in list_public_methods

        # Test with a dict
        dict_obj = {"a": 1, "b": 2}
        dict_methods = get_method_names(dict_obj)
        dict_public_methods = get_public_method_names(dict_obj)

        # Verify some common dict methods are included
        assert "keys" in dict_methods
        assert "keys" in dict_public_methods
        assert "values" in dict_methods
        assert "values" in dict_public_methods


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
