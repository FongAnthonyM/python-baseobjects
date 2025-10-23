#!/usr/bin/env python
"""dynamicwrapper_test.py
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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.testsuite.wrappers.wrappertestsuite import WrapperTestSuite
from src.baseobjects.wrappers import DynamicWrapper


# Definitions #
# Classes #
class TestDynamicWrapper(DynamicWrapper):
    """A test class that inherits from DynamicWrapper.

    This class uses DynamicWrapper to wrap ExampleOne and ExampleTwo objects.
    """

    _wrapped_map_: list[str] = ["_first", "_second"]

    def __init__(self, first: Any = None, second: Any = None) -> None:
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


class TestDynamicWrapperWithGetAttr(DynamicWrapper):
    """A test class that inherits from DynamicWrapper and wraps an object with __getattr__.

    This class is used to test how DynamicWrapper handles objects with __getattr__.
    """

    _wrapped_map_: list[str] = ["_wrapped_obj"]

    def __init__(self, wrapped: Any = None) -> None:
        """Initialize with a wrapped object.

        Args:
            wrapped: The object to wrap.
        """
        self.existing = "wrapper_existing"
        self._wrapped_obj = wrapped


class NestedDynamicWrapper(DynamicWrapper):
    """A test class for nesting wrappers.

    This class wraps another wrapper.
    """

    _wrapped_map_: list[str] = ["_wrapped_obj"]

    def __init__(self, wrapped: Any = None) -> None:
        """Initialize with a wrapped wrapper.

        Args:
            wrapped: The wrapper to wrap.
        """
        self._wrapped_obj = wrapped
        self.nested_attr = "nested"


# Tests #
class TestDynamicWrapperTests(WrapperTestSuite):
    """Test the DynamicWrapper class.

    This class tests the functionality of the DynamicWrapper class, which is a wrapper that
    calls wrapped attributes/functions by changing the __getattr__ method.
    """

    # Class Attributes #
    TestClass = TestDynamicWrapper

    # Instance Methods #
    # Additional Tests
    def test_setattr_method(self) -> None:
        """Test the _setattr method.

        This test verifies that the _setattr method bypasses the dynamic attribute resolution and sets attributes
        directly on the wrapper.
        """
        # Create a test object
        obj = self.TestClass(self.ExampleOne(), self.ExampleTwo())

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

        # Create a test object with an object that has __getattr__
        class ExampleWithGetAttr:
            """An example class with a __getattr__ method."""

            def __init__(self) -> None:
                """Initialize with attributes."""
                self.existing = "exists"

            def __getattr__(self, name: str) -> str:
                """Return a dynamic attribute."""
                return f"dynamic_{name}"

        obj = TestDynamicWrapperWithGetAttr(ExampleWithGetAttr())

        # Test accessing an existing attribute
        assert obj.existing == "wrapper_existing"  # From wrapper
        assert obj._wrapped_obj.existing == "exists"  # From wrapped

        # Test accessing a dynamically created attribute
        assert obj.nonexistent == "dynamic_nonexistent"

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects
        without raising exceptions during normal operations.
        """
        # Create a wrapper with None as the wrapped object
        obj = self.TestClass(None, None)

        # Verify wrapper's own attributes are accessible
        assert obj.two == "wrapper"
        assert obj.four == "wrapper"

        # Verify accessing wrapped attributes raises AttributeError, not TypeError
        with pytest.raises(AttributeError):
            _ = obj.one

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper,
        and that attribute access works correctly through multiple levels of wrapping.
        """
        # Create a wrapper
        inner = self.TestClass(self.ExampleOne(), self.ExampleTwo())

        # Create a wrapper that wraps the first wrapper
        outer = NestedDynamicWrapper(inner)

        # Verify that attribute access works through multiple levels of wrapping
        assert outer.one == "one"
        assert outer.three == "two"

        # Verify that accessing the inner wrapper's wrapped objects works
        assert outer._first.one == "one"

        # Verify that accessing the outer wrapper's own attributes works
        assert outer.nested_attr == "nested"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
