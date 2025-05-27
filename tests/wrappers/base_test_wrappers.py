#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" base_test_wrappers.py
Base test class for wrapper classes in the baseobjects package.
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
from typing import Any, Optional, Type

# Third-Party Packages #
import pytest

# Local Packages #
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class BaseWrapperTest(ClassTest):
    """Base test class for wrapper classes.

    This class provides common test functionality for wrapper classes that wrap other objects and provide access to
    their attributes and methods.
    """

    # Class Definitions #
    class ExampleOne:
        """An example class for testing wrappers.

        This class has attributes and methods that can be wrapped by wrapper classes.
        """
        def __init__(self) -> None:
            """Initialize with attributes."""
            self.one = "one"
            self.two = "one"
            self.common = "example_one"

        def __eq__(self, other: Any) -> bool:
            """Always return True for equality comparison."""
            return True

        def method(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "one"

        def __str__(self) -> str:
            """Return a string representation of this class."""
            return "ExampleOne"

    class ExampleTwo:
        """Another example class for testing wrappers.

        This class has different attributes and methods than ExampleOne.
        """
        def __init__(self) -> None:
            """Initialize with attributes."""
            self.one = "two"
            self.three = "two"
            self.common = "example_two"

        def function(self) -> str:
            """Return a string identifying this class.

            Returns:
                A string identifying this class.
            """
            return "two"

        def __str__(self) -> str:
            """Return a string representation of this class."""
            return "ExampleTwo"

    class ExampleWithGetAttr:
        """An example class with a __getattr__ method.

        This class is used to test how wrappers handle objects with __getattr__.
        """
        def __init__(self) -> None:
            """Initialize with attributes."""
            self.existing = "exists"

        def __getattr__(self, name: str) -> str:
            """Return a dynamic attribute."""
            return f"dynamic_{name}"

    class NormalWrapper:
        """A simple wrapper class for comparison.

        This class manually implements wrapping functionality.
        """
        def __init__(self, first: Any) -> None:
            """Initialize with a wrapped object.

            Args:
                first: The object to wrap.
            """
            self._first = first
            self.four = "wrapper"

        @property
        def one(self) -> str:
            """Get the 'one' attribute from the wrapped object.

            Returns:
                The 'one' attribute from the wrapped object.
            """
            return self._first.one

    # Attributes #
    class_: Optional[Type[Any]] = None

    # Instance Methods #
    # Fixtures
    def new_object(self) -> Any:
        """Create a new test object.

        This method should be overridden by subclasses to create a specific test object.

        Returns:
            A new test object.
        """
        pass

    def pickle_object(self) -> None:
        """Test pickling and unpickling of a test object.

        This method creates a test object, pickles it, unpickles it, and verifies that the unpickled object has the same
        attributes as the original.
        """
        obj = self.new_object()
        pickle_jar = pickle.dumps(obj)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(obj))

    @pytest.fixture(params=[new_object])
    def test_object(self, request: Any) -> Any:
        """Fixture that returns a test object.

        Args:
            request: The pytest request object.

        Returns:
            A test object created by the method specified in the request parameters.
        """
        return request.param(self)

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the wrapper class can be created.

        This method should be overridden by subclasses to test instance creation for specific wrapper classes.
        """
        pass

    def test_pickling(self, test_object: Any) -> None:
        """Test pickling and unpickling of a wrapper object.

        This test verifies that wrapper objects can be pickled and unpickled correctly.

        Args:
            test_object: The test object to pickle and unpickle.
        """
        pickle_jar = pickle.dumps(test_object)
        new_obj = pickle.loads(pickle_jar)
        assert set(dir(new_obj)) == set(dir(test_object))

    def test_copy(self, test_object: Any) -> None:
        """Test copying a wrapper object.

        This test verifies that wrapper objects can be copied correctly, and that the copy shares the same wrapped
        objects.

        Args:
            test_object: The test object to copy.
        """
        new = test_object.copy()
        assert id(new._first) == id(test_object._first)

    def test_deepcopy(self, test_object: Any) -> None:
        """Test deep copying a wrapper object.

        This test verifies that wrapper objects can be deep copied correctly, and that the deep copy has different
        wrapped objects.

        Args:
            test_object: The test object to deep copy.
        """
        new = test_object.deepcopy()
        assert id(new._first) != id(test_object._first)

    def test_wrapper_overrides(self, test_object: Any) -> None:
        """Test that wrapper attributes and methods override wrapped objects.

        This test verifies that attributes and methods defined in the wrapper take precedence over those in wrapped
        objects.

        Args:
            test_object: The test object to check.
        """
        assert test_object.two == "wrapper"
        assert test_object.four == "wrapper"
        assert test_object.wrap() == "wrapper"

    def test_example_one_overrides(self, test_object: Any) -> None:
        """Test that attributes and methods from ExampleOne are accessible.

        This test verifies that attributes and methods from the first wrapped object are accessible through the wrapper.

        Args:
            test_object: The test object to check.
        """
        assert test_object.one == "one"
        assert test_object.method() == "one"

    def test_example_two_overrides(self, test_object: Any) -> None:
        """Test that attributes and methods from ExampleTwo are accessible.

        This test verifies that attributes and methods from the second wrapped object are accessible through the
        wrapper.

        Args:
            test_object: The test object to check.
        """
        assert test_object.three == "two"
        assert test_object.function() == "two"

    def test_setting_wrapped(self, test_object: Any) -> None:
        """Test setting attributes on wrapped objects.

        This test verifies that setting attributes through the wrapper correctly updates the wrapped objects.

        Args:
            test_object: The test object to check.
        """
        test_object.one = "set"
        assert test_object._first.one == "set"

    def test_deleting_wrapped(self, test_object: Any) -> None:
        """Test deleting attributes on wrapped objects.

        This test verifies that deleting attributes through the wrapper correctly removes them from the wrapped objects.

        Args:
            test_object: The test object to check.
        """
        del test_object.one
        assert "one" not in dir(test_object._first)

    @pytest.mark.xfail
    def test_magic_inheritance(self, test_object: Any) -> None:
        """Test that magic methods are inherited from wrapped objects. (They are not currently)

        This test verifies that magic methods from wrapped objects are accessible through the wrapper. The equality
        magic method is being tested here. This test is expected to fail.

        Args:
            test_object: The test object to check.
        """
        assert test_object == 1

    def test_conflicting_attributes(self, test_object: Any) -> None:
        """Test how the wrapper handles attributes with the same name in multiple wrapped objects.

        This test verifies that when multiple wrapped objects have attributes with the same name, the attribute from the
        first wrapped object in the resolution order is used.

        Args:
            test_object: The test object to check.
        """
        assert test_object.common == "example_one"

    def test_none_wrapped_object(self) -> None:
        """Test how the wrapper handles None values for wrapped objects.

        This test verifies that the wrapper can handle None values for wrapped objects without raising exceptions during
        normal operations.
        """
        # This test needs to be implemented by subclasses
        raise NotImplementedError

    def test_nested_wrappers(self) -> None:
        """Test how the wrapper handles nested wrappers.

        This test verifies that wrappers can be nested, with one wrapper wrapping another wrapper, and that attribute
        access works correctly through multiple levels of wrapping.
        """
        # This test needs to be implemented by subclasses
        raise NotImplementedError
