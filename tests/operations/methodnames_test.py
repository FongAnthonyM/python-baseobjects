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
from collections.abc import Callable, Generator
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.operations import (
    get_method_names,
    get_public_method_names,
    iter_method_names,
    iter_public_method_names,
)


# Definitions #
# Classes #
class TestMethodNames:
    """Tests the method name functions.

    This class tests the functionality of the functions that retrieve method names from objects.
    """

    # Class Definitions #
    class UnitTestClass:
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
    @pytest.mark.parametrize(
        ("func", "return_type"),
        [
            (iter_method_names, Generator),
            (get_method_names, tuple),
        ],
    )
    def test_all_method_names(
        self,
        func: Callable[[Any], Generator[str, None, None] | tuple[str, ...]],
        return_type: type,
    ) -> None:
        """Tests getting all method names.

        This test verifies that the method name functions correctly retrieve all method names of an object, including
        public, private, and dunder methods.
        """
        # Create an instance of the test class
        test_obj = self.UnitTestClass()

        # Get the method names
        result = func(test_obj)
        method_names = list(result)

        # Verify that all methods are included
        assert "public_method" in method_names
        assert "another_public_method" in method_names
        assert "_private_method" in method_names
        assert "__dunder_method__" in method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in method_names

        # Verify the return type
        assert isinstance(result, return_type)

    @pytest.mark.parametrize(
        ("func", "return_type"),
        [
            (iter_public_method_names, Generator),
            (get_public_method_names, tuple),
        ],
    )
    def test_public_method_names(
        self,
        func: Callable[[Any], Generator[str, None, None] | tuple[str, ...]],
        return_type: type,
    ) -> None:
        """Tests getting public method names.

        This test verifies that the public method name functions correctly retrieve only public method names of an
        object (those not starting with '_').
        """
        # Create an instance of the test class
        test_obj = self.UnitTestClass()

        # Get the public method names
        result = func(test_obj)
        public_method_names = list(result)

        # Verify that only public methods are included
        assert "public_method" in public_method_names
        assert "another_public_method" in public_method_names

        # Private and dunder methods should not be included
        assert "_private_method" not in public_method_names
        assert "__dunder_method__" not in public_method_names

        # Non-callable attributes should not be included
        assert "non_callable_attr" not in public_method_names

        # Verify the return type
        assert isinstance(result, return_type)

    @pytest.mark.parametrize(
        ("obj", "methods_to_check"),
        [
            ([1, 2, 3], ["append", "extend"]),
            ({"a": 1, "b": 2}, ["keys", "values"]),
        ],
    )
    def test_with_builtin_objects(self, obj: Any, methods_to_check: list[str]) -> None:
        """Tests with built-in objects.

        This test verifies that the method name functions work correctly with built-in objects.
        """
        list_methods = get_method_names(obj)
        list_public_methods = get_public_method_names(obj)

        # Verify some common methods are included
        for method in methods_to_check:
            assert method in list_methods
            assert method in list_public_methods


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
