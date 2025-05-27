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
import pickle
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.wrappers import StaticWrapper
from tests.wrappers.base_test_wrappers import BaseWrapperTest


# Definitions #
# Classes #
class TestStaticWrapper(BaseWrapperTest):
    """Test the StaticWrapper class.

    This class tests the functionality of the StaticWrapper class, which is a wrapper that
    calls wrapped attributes/functions by creating property descriptor objects.
    """

    # Class Definitions #
    class StaticWrapperTestObject1(StaticWrapper):
        """A test class that inherits from StaticWrapper.

        This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects.
        """
        _wrapped_types: list[Any] = [BaseWrapperTest.ExampleOne(), BaseWrapperTest.ExampleTwo()]
        _wrap_attributes: list[str] = ["_first", "_second"]

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

    class StaticWrapperTestObject2(StaticWrapper):
        """Another test class that inherits from StaticWrapper.

        This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects, and calls _wrap() during
        initialization.
        """
        _set_next_wrapped: bool = True
        _wrap_attributes: list[str] = ["_first", "_second"]

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
            self._wrap()

        def wrap(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "wrapper"

    class StaticWrapperTestObject3(StaticWrapper):
        """A test class that inherits from StaticWrapper with custom exclude_attributes.

        This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects, and excludes specific attributes from
        wrapping.
        """
        _wrap_attributes: list[str] = ["_first", "_second"]
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
            self._wrap()

        def wrap(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "wrapper"

    class StaticWrapperTestObject4(StaticWrapper):
        """A test class that inherits from StaticWrapper with get_previous_wrapped=True.

        This class uses StaticWrapper to wrap ExampleOne and ExampleTwo objects, and preserves attributes when changing
        wrapped objects.
        """
        _get_previous_wrapped: bool = True
        _set_next_wrapped: bool = True
        _wrap_attributes: list[str] = ["_first", "_second"]

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
            self._wrap()

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
        _wrap_attributes: list[str] = ["_wrapped"]

        def __init__(self, wrapped: Any = None) -> None:
            """Initialize with a wrapped wrapper.

            Args:
                wrapped: The wrapper to wrap.
            """
            self._wrapped = wrapped
            self.nested_attr = "nested"
            self._wrap()

    # Attributes #
    class_: Type[StaticWrapper] = StaticWrapperTestObject1

    # Instance Methods #
    # Fixtures
    def new_object_1(self) -> StaticWrapperTestObject1:
        """Create a new StaticWrapperTestObject1 instance.

        Returns:
            A new StaticWrapperTestObject1 instance with ExampleOne and ExampleTwo objects.
        """
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject1(first, second)

    def new_object_2(self) -> StaticWrapperTestObject2:
        """Create a new StaticWrapperTestObject2 instance.

        Returns:
            A new StaticWrapperTestObject2 instance with ExampleOne and ExampleTwo objects.
        """
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject2(first, second)

    def new_object_3(self) -> StaticWrapperTestObject3:
        """Create a new StaticWrapperTestObject3 instance.

        Returns:
            A new StaticWrapperTestObject3 instance with ExampleOne and ExampleTwo objects.
        """
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject3(first, second)

    def new_object_4(self) -> StaticWrapperTestObject4:
        """Create a new StaticWrapperTestObject4 instance.

        Returns:
            A new StaticWrapperTestObject4 instance with ExampleOne and ExampleTwo objects.
        """
        first = self.ExampleOne()
        second = self.ExampleTwo()
        return self.StaticWrapperTestObject4(first, second)

    @pytest.fixture(params=[new_object_1, new_object_2, new_object_3, new_object_4])
    def test_object(self, request: Any) -> Any:
        """Fixture that returns a test object.

        Args:
            request: The pytest request object.

        Returns:
            A test object created by the method specified in the request parameters.
        """
        return request.param(self)

    # Additional Tests
    def test_exclude_attributes(self) -> None:
        """Test that excluded attributes are not wrapped.

        This test verifies that attributes listed in _exclude_attributes are not wrapped and the wrapper's own
        attributes are used instead.
        """
        obj = self.new_object_3()
        assert obj.common == "wrapper_common"
        assert obj._first.common == "example_one"

    def test_get_previous_wrapped(self) -> None:
        """Test the _get_previous_wrapped flag.

        This test verifies that when _get_previous_wrapped is True, attributes from a wrapped object are preserved when
        the object is replaced.
        """
        obj = self.new_object_4()

        # Modify an attribute in the wrapped object
        obj.one = "modified"
        assert obj._first.one == "modified"

        # Replace the wrapped object and verify the attribute is preserved
        new_first = self.ExampleOne()
        assert new_first.one == "one"  # Original value
        obj._first = new_first
        assert obj._first.one == "modified"  # Value preserved from previous object

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper, and that attribute
        access works correctly through multiple levels of wrapping.
        """
        inner = self.new_object_1()
        outer = self.NestedStaticWrapper(inner)

        # Test access to inner wrapper's attributes
        assert outer.one == "one"
        assert outer.three == "two"

        # Test access to inner wrapper's wrapped objects' attributes
        assert outer._wrapped._first.one == "one"

        # Test access to outer wrapper's own attributes
        assert outer.nested_attr == "nested"

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects without raising exceptions during
        normal operations.
        """
        obj = self.StaticWrapperTestObject2(None, None)

        # Verify wrapper's own attributes are accessible
        assert obj.two == "wrapper"
        assert obj.four == "wrapper"

        # Verify accessing wrapped attributes raises AttributeError, not TypeError
        with pytest.raises(AttributeError):
            _ = obj.one


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
