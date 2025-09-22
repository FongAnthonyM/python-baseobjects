"""dynamiccallabletestsuite.py
Base class for test suites which test DynamicCallable and its subclasses.

This module provides a base test suite for testing the DynamicCallable class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic callable objects, including multiplexed binding and callback
functionality.
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
from abc import abstractmethod
from typing import Any, Type

# Third-Party Packages #

# Local Packages #
from ...functions.dynamiccallable import DynamicCallable
from ..bases.basecallabletestsuite import BaseCallableTestSuite


# Definitions #
# Classes #
class DynamicCallableTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test DynamicCallable and its subclasses.

    This class provides common functionality for test suites that test dynamic callable objects, including fixtures and
    test methods for verifying the behavior of DynamicCallable objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be DynamicCallable or a subclass.
    """

    # Attributes #
    TestClass: Type[DynamicCallable]

    # Instance Methods #
    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    @abstractmethod
    def test_call(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: DynamicCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    def test_bind_method_property(self) -> None:
        """Test that the bind_method property correctly gets and sets the binding method."""
        method_object = self.create_method_object()

        # Set the bind_method property
        method_object.bind_method = "bind_wrapped"

        # Verify the property was set correctly
        assert method_object.bind_method == "bind_wrapped"
        assert method_object.bind_multiplexer.selected == "bind_wrapped"

        # Set it back to the default
        method_object.bind_method = "bind_builtin"

        # Verify it was set back correctly
        assert method_object.bind_method == "bind_builtin"
        assert method_object.bind_multiplexer.selected == "bind_builtin"

    def test_call_method_property(self) -> None:
        """Test that the call_method property correctly gets and sets the call method."""
        method_object = self.create_method_object()

        # Set the call_method property
        method_object.call_method = "call_wrapped"

        # Verify the property was set correctly
        assert method_object.call_method == "call_wrapped"
        assert method_object.call_multiplexer.selected == "call_wrapped"

        # Set it back to the default
        method_object.call_method = "call_wrapped"

        # Verify it was set correctly
        assert method_object.call_method == "call_wrapped"
        assert method_object.call_multiplexer.selected == "call_wrapped"

    def test_bind_multiplexer(self, test_method_object: DynamicCallable, test_bind_target: Any) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method.

        This test verifies that the bind_multiplexer correctly delegates to the selected binding method. This method may
        be overwritten to include validation beyond checking that the function is correct.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a method.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Test with default bind_method (bind_builtin)
        assert test_method_object.bind_method == "bind_builtin"
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))
        assert bound_method.__self__ is test_bind_target

        # Change the bind_method to bind_wrapped
        test_method_object.bind_method = "bind_wrapped"
        assert test_method_object.bind_method == "bind_wrapped"

        # Test with bind_wrapped
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

    def test_call_multiplexer(self, test_function_object: DynamicCallable) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method.

        This test verifies that the call_multiplexer correctly delegates to the selected call method. This method may be
        overwritten to include validation beyond checking that the function is correct.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """
        # Test with default call_method (call_wrapped)
        assert test_function_object.call_method == "call_wrapped"
        result = test_function_object(3)
        assert result == 5  # 3 + 2 (default y)

        # Add a custom call method to the call_multiplexer
        def custom_call(self, *args, **kwargs):
            # Multiply the result by 2
            return self.call_wrapped(*args, **kwargs) * 2

        test_function_object.call_multiplexer.add_function("custom_call", custom_call)

        # Change the call_method to custom_call
        test_function_object.call_method = "custom_call"
        assert test_function_object.call_method == "custom_call"

        # Test with custom_call
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2
