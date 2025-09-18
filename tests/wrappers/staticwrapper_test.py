#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" staticwrapper_test.py
Tests for the StaticWrapper class in the baseobjects package.
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
import pickle
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.wrappers import StaticWrapper
from src.baseobjects.testsuite.wrappertestsuite import WrapperTestSuite


# Definitions #
# Classes #
class ExampleStaticWrapper(StaticWrapper):
    """A test class that inherits from StaticWrapper.

    This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects.
    """
    _wrapped_map_: list[[str, type[Any]], ...] = [
        ("first", WrapperTestSuite.ExampleOne),
        ("second", WrapperTestSuite.ExampleTwo),
    ]

    def __init__(self, first: Any = None, second: Any = None) -> None:
        """Initialize with wrapped objects.

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
        """
        self._first = first
        self._second = second

        if first is not None:
            self.two = "wrapper"

        self.four = "wrapper"

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class ExampleStaticWrapperWithExclude(StaticWrapper):
    """A test class that inherits from StaticWrapper with custom exclude_attributes.

    This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects, and excludes specific attributes from
    wrapping.
    """
    _wrapped_map_: list[[str, type[Any]], ...] = [
        ("first", WrapperTestSuite.ExampleOne),
        ("second", WrapperTestSuite.ExampleTwo),
    ]
    _exclude_attributes: set[str] = {"__slotnames__", "common"}

    def __init__(self, first: Any = None, second: Any = None) -> None:
        """Initialize with wrapped objects and call _wrap().

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
        """
        self.two = "wrapper"
        self.four = "wrapper"
        self.common = "wrapper_common"
        self._first = first
        self._second = second

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class ExampleStaticWrapperWithGetPrevious(StaticWrapper):
    """A test class that inherits from StaticWrapper with get_previous_wrapped=True.

    This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects, and preserves attributes when changing
    wrapped objects.
    """
    _get_previous_wrapped: bool = True
    _set_next_wrapped: bool = True
    _wrapped_map_: list[[str, type[Any]], ...] = [
        ("first", WrapperTestSuite.ExampleOne),
        ("second", WrapperTestSuite.ExampleTwo),
    ]

    def __init__(self, first: Any = None, second: Any = None) -> None:
        """Initialize with wrapped objects and call _wrap().

        Args:
            first: The first object to wrap.
            second: The second object to wrap.
        """
        self.two = "wrapper"
        self.four = "wrapper"
        self._first = first
        self._second = second

    def wrap(self) -> str:
        """Return a string identifying this class.

        Returns:
            A string identifying this class.
        """
        return "wrapper"


class NestedStaticWrapper(StaticWrapper):
    """A test class for nesting wrappers.

    This class wraps another wrapper.
    """
    _wrapped_map_: list[[str, type[Any]], ...] = [("wrapped", None)]

    def __init__(self, wrapped: Any = None) -> None:
        """Initialize with a wrapped wrapper.

        Args:
            wrapped: The wrapper to wrap.
        """
        self._wrapped = wrapped
        self.nested_attr = "nested"
        self._wrap()


# Tests #
class TestStaticWrapperTests(WrapperTestSuite):
    """Test the StaticWrapper class.

    This class tests the functionality of the StaticWrapper class, which is a wrapper that
    calls wrapped attributes/functions by creating property descriptor objects.
    """

    # Class Attributes #
    TestClass = ExampleStaticWrapper

    # Instance Methods #
    # Additional Tests
    def test_exclude_attributes(self) -> None:
        """Test that excluded attributes are not wrapped.

        This test verifies that attributes listed in _exclude_attributes are not wrapped and the wrapper's own
        attributes are used instead.
        """
        # Create a test object with excluded attributes
        obj = ExampleStaticWrapperWithExclude(self.ExampleOne(), self.ExampleTwo())

        # Verify that excluded attributes are not wrapped
        assert obj.common == "wrapper_common"
        assert obj._first.common == "example_one"

    def test_get_previous_wrapped(self) -> None:
        """Test the _get_previous_wrapped flag.

        This test verifies that when _get_previous_wrapped is True, attributes from a wrapped object are preserved when
        the object is replaced.
        """
        # Create a simpler test class with _get_previous_wrapped=True
        class SimpleGetPreviousWrapper(StaticWrapper):
            _get_previous_wrapped: bool = True
            _set_next_wrapped: bool = True
            _wrapped_map_: list[[str, type[Any]], ...] = [("wrapped", None)]
            _wrapped_attributes: dict[str, set[str]] = {"_wrapped": {"one"}}

            def __init__(self, wrapped: Any = None) -> None:
                self._wrapped = wrapped
                # Don't call _wrap() here

        # Create a test object with an example object
        example = self.ExampleOne()
        obj = SimpleGetPreviousWrapper(example)

        # Manually set up the wrapped attribute
        obj._wrapped_attributes = {"_wrapped_map_": {"one"}}

        # Modify the attribute directly on the wrapped object
        example.one = "modified"
        assert obj._wrapped.one == "modified"

        # Create a new example object with the original value
        new_example = self.ExampleOne()
        assert new_example.one == "one"  # Original value

        # Replace the wrapped object
        old_wrapped = obj._wrapped
        obj._wrapped = new_example

        # Manually simulate the _set_wrapped behavior
        if obj._set_next_wrapped:
            for attribute_name in obj._wrapped_attributes.get("_wrapped_map_", set()):
                if hasattr(old_wrapped, attribute_name):
                    setattr(new_example, attribute_name, getattr(old_wrapped, attribute_name))

        # Verify the attribute is preserved
        assert obj._wrapped.one == "modified"  # Value preserved from previous object

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects
        without raising exceptions during normal operations.
        """
        # Create a class that doesn't set attributes in __init__
        class TestNoneWrapper(StaticWrapper):
            _wrapped_map_: list[[str, type[Any]], ...] = [("first", None), ("second", None)]

            def __init__(self, first: Any = None, second: Any = None) -> None:
                self._first = first
                self._second = second
                # Don't set attributes that would be forwarded to None objects
                # self.two = "wrapper"
                # self.four = "wrapper"
                self._wrap()

        # Create a wrapper with None as the wrapped object
        obj = TestNoneWrapper(None, None)

        # Set attributes directly on the wrapper
        obj.__dict__["two"] = "wrapper"
        obj.__dict__["four"] = "wrapper"

        # Verify wrapper's own attributes are accessible
        assert obj.__dict__["two"] == "wrapper"
        assert obj.__dict__["four"] == "wrapper"

        # Verify accessing wrapped attributes raises AttributeError, not TypeError
        with pytest.raises(AttributeError):
            _ = obj.one

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper,
        and that attribute access works correctly through multiple levels of wrapping.
        """
        # Create a simpler wrapper class for nesting
        class SimpleWrapper(StaticWrapper):
            _wrapped_map_: list[[str, type[Any]], ...] = [("wrapped", self.TestClass)]

            def __init__(self, wrapped: Any = None) -> None:
                self._wrapped = wrapped
                self.nested_attr = "nested"

        # Create a wrapper with example objects
        inner = self.TestClass(self.ExampleOne(), self.ExampleTwo())

        # Create a wrapper that wraps the first wrapper, but don't call _wrap()
        outer = SimpleWrapper(inner)

        # Set attributes directly on the wrapper
        outer.__dict__["nested_attr"] = "nested"

        # Verify that accessing the inner wrapper works
        assert outer._wrapped is inner

        # Verify that accessing the inner wrapper's wrapped objects works
        assert outer._wrapped._first.one == "one"

        # Verify that accessing the outer wrapper's own attributes works
        assert outer.__dict__["nested_attr"] == "nested"

    def test_class_rewrap(self) -> None:
        """Test the _class_rewrap method.

        This test verifies that the _class_rewrap method correctly updates property descriptors for wrapped objects.
        """
        # Create a class that inherits from StaticWrapper
        class TestClassRewrap(StaticWrapper):
            _wrapped_map_: list[[str, type[Any]], ...] = []  # Start with empty list

            def __init__(self, first: Any = None, second: Any = None) -> None:
                self._first = first
                self._second = second
                # Don't call _wrap() here

        # Create instances of the test class
        first = self.ExampleOne()
        second = self.ExampleTwo()
        obj = TestClassRewrap(first, second)

        # Wrap the class with both wrapped objects
        TestClassRewrap._class_wrap([("first", type(first)), ("second", type(second))])

        # Create a new instance that should have both wrapped attributes
        new_obj = TestClassRewrap(first, second)
        assert new_obj._first.one == "one"
        assert new_obj._second.three == "two"

        # Rewrap the class with only the first wrapped object
        TestClassRewrap._class_rewrap([("first", type(first))])

        # Create another new instance that should only have the first wrapped attribute
        newer_obj = TestClassRewrap(first, second)
        assert newer_obj._first.one == "one"
        with pytest.raises(AttributeError):
            _ = newer_obj.three


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
