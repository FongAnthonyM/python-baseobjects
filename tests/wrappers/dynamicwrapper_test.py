#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dynamicwrapper_test.py
Tests for the DynamicWrapper class in the baseobjects package.
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
from typing import Any, List, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.wrappers import DynamicWrapper
from tests.wrappers.base_test_wrappers import BaseWrapperTest


# Definitions #
# Classes #
class TestDynamicWrapper(BaseWrapperTest):
    """Test the DynamicWrapper class.

    This class tests the functionality of the DynamicWrapper class, which is a wrapper that calls wrapped
    attributes/functions by changing the __getattr__ method.
    """

    # Class Definitions #
    class DynamicWrapperTestObject(DynamicWrapper):
        """A test class that inherits from DynamicWrapper.

        This class uses DynamicWrapper to wrap ExampleOne and ExampleTwo objects.
        """
        _wrap_attributes: List[str] = ["_first", "_second"]

        def __init__(self, first: Optional[Any] = None, second: Optional[Any] = None) -> None:
            """Initialize with wrapped objects.

            Args:
                first: The first object to wrap.
                second: The second object to wrap.
            """
            self._first = first
            self._second = second
            self.two = "wrapper"
            self.four = "wrapper"

        def wrap(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "wrapper"

    class DynamicWrapperWithGetAttr(DynamicWrapper):
        """A test class that inherits from DynamicWrapper and wraps an object with __getattr__.

        This class is used to test how DynamicWrapper handles objects with __getattr__.
        """
        _wrap_attributes: List[str] = ["_wrapped"]

        def __init__(self, wrapped: Optional[Any] = None) -> None:
            """Initialize with a wrapped object.

            Args:
                wrapped: The object to wrap.
            """
            self.existing = "wrapper_existing"
            self._wrapped = wrapped

    class NestedDynamicWrapper(DynamicWrapper):
        """A test class for nesting wrappers.

        This class wraps another wrapper.
        """
        _wrap_attributes: List[str] = ["_wrapped"]

        def __init__(self, wrapped: Optional[Any] = None) -> None:
            """Initialize with a wrapped wrapper.

            Args:
                wrapped: The wrapper to wrap.
            """
            self._wrapped = wrapped
            self.nested_attr = "nested"

    # Attributes #
    class_: Type[DynamicWrapper] = DynamicWrapperTestObject

    # Instance Methods #
    # Fixtures
    def new_object(self) -> DynamicWrapperTestObject:
        """Create a new DynamicWrapperTestObject instance.

        Returns:
            A new DynamicWrapperTestObject instance with ExampleOne and ExampleTwo objects.
        """
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.DynamicWrapperTestObject(first, second)

    def new_object_with_getattr(self) -> DynamicWrapperWithGetAttr:
        """Create a new DynamicWrapperWithGetAttr instance.

        Returns:
            A new DynamicWrapperWithGetAttr instance with an ExampleWithGetAttr object.
        """
        wrapped = self.ExampleWithGetAttr()
        return self.DynamicWrapperWithGetAttr(wrapped)

    @pytest.fixture(params=[new_object])
    def test_object(self, request: Any) -> Any:
        """Fixture that returns a test object.

        Args:
            request: The pytest request object.

        Returns:
            A test object created by the method specified in the request parameters.
        """
        return request.param(self)

    # Additional Tests
    def test_setattr_method(self) -> None:
        """Test the _setattr method.

        This test verifies that the _setattr method bypasses the dynamic attribute resolution and sets attributes
        directly on the wrapper.
        """
        obj = self.new_object()

        # Set an attribute in the wrapper object but is also present in the wrapped object
        obj._setattr("one", "direct_set")

        # Verify the attribute was set on the wrapper, not on the wrapped object
        assert obj._first.one == "one"  # Still gets from wrapped object
        assert obj.one == "direct_set"  # But also exists directly on wrapper

    def test_dynamic_attribute_creation(self) -> None:
        """Test how the wrapper handles objects that dynamically create attributes.

        This test verifies that attributes dynamically created by a wrapped object's __getattr__ are accessible through
        the wrapper.
        """
        obj = self.new_object_with_getattr()

        # Test accessing an existing attribute
        assert obj.existing == "wrapper_existing"  # From wrapper
        assert obj._wrapped.existing == "exists"  # From wrapped

        # Test accessing a dynamically created attribute
        assert obj.nonexistent == "dynamic_nonexistent"

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper,
        and that attribute access works correctly through multiple levels of wrapping.
        """
        inner = self.new_object()
        outer = self.NestedDynamicWrapper(inner)

        # Test access to inner wrapper's attributes
        assert outer.one == "one"
        assert outer.three == "two"

        # Test access to inner wrapper's wrapped objects' attributes
        assert outer._wrapped._first.one == "one"

        # Test access to outer wrapper's own attributes
        assert outer.nested_attr == "nested"

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects
        without raising exceptions during normal operations.
        """
        obj = self.DynamicWrapperTestObject(None, None)

        # Verify wrapper's own attributes are accessible
        assert obj.two == "wrapper"
        assert obj.four == "wrapper"

        # Verify accessing wrapped attributes raises AttributeError, not TypeError
        with pytest.raises(AttributeError):
            _ = obj.one


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])