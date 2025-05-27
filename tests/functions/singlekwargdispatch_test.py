#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" singlekwargdispatch_test.py
Tests for the singlekwargdispatch decorator in the baseobjects package.
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
import pickle
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import singlekwargdispatch
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestSingleKwargDispatch(ClassTest):
    """Test the singlekwargdispatch decorator.

    This class tests the functionality of the singlekwargdispatch decorator, which extends singledispatch
    to allow keyword arguments to be used for dispatching.
    """

    # Class Definitions #
    class DispatchTestClass:
        """A class with methods for testing."""
        @singlekwargdispatch
        def dispatch_arg(self, arg: int | str, **kwargs):
            """Default implementation."""
            return f"Default: {arg}"

        @dispatch_arg.register
        def _(self, arg: int, **kwargs):
            """Process an integer."""
            return f"Integer: {arg}"

        @dispatch_arg.register(str)
        def _(self, arg: str, **kwargs):
            """Process a string."""
            return f"String: {arg}"

        @singlekwargdispatch(kwarg="kwarg")
        def dispatch_kwarg(self, arg: Any = None, kwarg: int | str | None = None, **kwargs):
            """Default implementation with specific kwarg."""
            return f"Default: {kwarg}"

        @dispatch_kwarg.register
        def _(self, arg: Any = None, kwarg: int = 0, **kwargs):
            """Process an integer value."""
            return f"Integer: {kwarg}"

        @dispatch_kwarg.register(str)
        def _(self, arg: Any = None, kwarg: int | str | None = None, **kwargs):
            """Process a string value."""
            return f"String: {kwarg}"

    # Instance Methods #
    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of singlekwargdispatch can be created.

        This test verifies that singlekwargdispatch instances can be created with various parameters.
        """
        # Create with no parameters
        decorator1 = singlekwargdispatch()
        assert decorator1 is not None

        # Create with kwarg parameter
        decorator2 = singlekwargdispatch(kwarg="test_param")
        assert decorator2 is not None

        # Create and apply to a function
        @singlekwargdispatch
        def test_func(x: Any) -> Any:
            return x

        assert test_func is not None
        assert hasattr(test_func, "registry")

        # Create and apply to a function
        @singlekwargdispatch(kwarg="x")
        def test_func(x: Any) -> Any:
            return x

        assert test_func is not None
        assert hasattr(test_func, "registry")

    def test_method_arg(self) -> None:
        """Test dispatching based on positional arguments.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of the first argument.
        """
        test_object = self.DispatchTestClass()
        assert test_object.dispatch_arg(1) == "Integer: 1"
        assert test_object.dispatch_arg("Any") == "String: Any"

    def test_method_pickling(self) -> None:
        """Test pickling and unpickling of objects with singlekwargdispatch methods.

        This test verifies that objects with singlekwargdispatch methods can be pickled and unpickled correctly,
        preserving the dispatch functionality.
        """
        test_object = self.DispatchTestClass()
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)
        assert new_obj is not test_object
        assert set(dir(new_obj)) == set(dir(test_object))
        assert test_object.dispatch_arg(1) == "Integer: 1"
        assert test_object.dispatch_arg("Any") == "String: Any"

    def test_first_kwarg(self) -> None:
        """Test dispatching based on the first keyword argument.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of the first keyword
        argument when no positional arguments are provided.
        """
        test_object = self.DispatchTestClass()
        assert test_object.dispatch_kwarg(1) == "Default: None"
        assert test_object.dispatch_kwarg("Any") == "Default: None"

    def test_specific_kwarg(self) -> None:
        """Test dispatching based on a specific keyword argument.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of a specific keyword
        argument when configured with the kwarg parameter.
        """
        test_object = self.DispatchTestClass()
        assert test_object.dispatch_kwarg("not", kwarg=1) == "Integer: 1"
        assert test_object.dispatch_kwarg(-1, kwarg="Any") == "String: Any"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
