"""dynamicmethodtestsuite.py
Base class for test suites which test DynamicMethod and its subclasses.

This module provides a base test suite for testing the DynamicMethod class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic method objects, including multiplexed binding and callback
functionality, as well as method-specific behavior.
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
import asyncio
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions.dynamiccallable import DynamicMethod
from ..bases.basemethodtestsuite import BaseMethodTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Helper Functions #
def instance_method(self: Any, x: int, y: int = 2) -> tuple[int, Any]:
    """A test method that works with an instance as its first argument.

    Returns:
        A tuple containing the sum and the instance.
    """
    return x + y, self


async def add_method_coroutine(self: Any, x: int, y: int = 2) -> tuple[int, Any]:
    """An async test function that adds two numbers.

    Returns:
        A tuple containing the sum and the instance.
    """
    await asyncio.sleep(0.01)
    return x + y, self


def multiply_method(self: Any, x: int, y: int = 3) -> tuple[int, Any]:
    """A test method that multiplies two numbers.

    Returns:
        A tuple containing the product and the instance.
    """
    return x * y, self


# Classes #
class DynamicMethodTestSuite(DynamicCallableTestSuite, BaseMethodTestSuite):
    """Base class for test suites which test DynamicMethod and its subclasses.

    This class provides common functionality for test suites that test dynamic method objects, including fixtures and
    test methods for verifying the behavior of DynamicMethod objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be DynamicMethod or a subclass.
    """

    UnitTestClass: type[DynamicMethod]

    # Tests #
    # Magic Methods #
    def test_call_binding(self, test_method_object: DynamicMethod, test_bind_target: Any) -> None:  # type: ignore[override]
        """Tests that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
            test_bind_target: A fixture providing a test object instance.
        """
        # Ensure we have a method that returns the instance (use instance_method)
        test_method_object = self.create_method_object(instance_method)  # type: ignore[assignment]

        # Bind the method to an instance
        bound_method = test_method_object.bind_self(test_bind_target, type(test_bind_target))

        # Call the wrapped function directly
        result, instance = bound_method.call_binding(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_bind_target

        # Call with different arguments
        result, instance = bound_method.call_binding(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_bind_target

    def test_call_multiplexer(self, test_function_object: Any) -> None:
        """Tests that the call_multiplexer correctly delegates to the selected call method."""
        # For DynamicMethod, test_function_object fixture might not be appropriate if it creates a function object
        # without self handling?
        # But we can create our own.
        test_method_object = self.create_method_object(instance_method)
        test_bind_target = self.create_bind_target()

        # Bind the method to the instance
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Test with default call_method
        assert bound_method.call_method == "call_wrapped"
        result, instance = bound_method(3)
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_bind_target

        # Add a custom call method to the call_multiplexer
        def custom_call(self: Any, *args: Any, **kwargs: Any) -> tuple[int, Any]:
            # Multiply the result by 2
            result, instance = self.call_wrapped(*args, **kwargs)
            return result * 2, instance

        bound_method.call_multiplexer.add_function("custom_call", custom_call)

        # Change the call_method to custom_call
        bound_method.call_method = "custom_call"
        assert bound_method.call_method == "custom_call"

        # Test with custom_call
        result, instance = bound_method(3)
        assert result == 10  # (3 + 2) * 2
        assert instance is test_bind_target

    def test_call_method_change(self, test_function_object: Any) -> None:
        """Tests that changing the call_method affects how the object is called.

        Args:
            test_function_object: Ignored in this override.
        """
        # Use a method that returns a number for easier math testing
        test_method_object = self.create_method_object(multiply_method)
        test_bind_target = self.create_bind_target()

        # Bind
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Add multiple call methods to the call_multiplexer
        # They receive (self, instance, *args, **kwargs) because DynamicMethod passes instance
        def call_double(self: Any, instance: Any, *args: Any, **kwargs: Any) -> tuple[int, Any]:
            result, inst = self.call_wrapped(instance, *args, **kwargs)
            return result * 2, inst

        def call_triple(self: Any, instance: Any, *args: Any, **kwargs: Any) -> tuple[int, Any]:
            result, inst = self.call_wrapped(instance, *args, **kwargs)
            return result * 3, inst

        test_method_object.call_multiplexer.add_function("call_double", call_double)  # type: ignore[attr-defined]
        test_method_object.call_multiplexer.add_function("call_triple", call_triple)  # type: ignore[attr-defined]

        # Test with call_double
        test_method_object.call_method = "call_double"  # type: ignore[attr-defined]
        assert test_method_object.call_method == "call_double"  # type: ignore[attr-defined]

        # Call bound method
        result, instance = bound_method(3)
        assert result == 18  # (3 * 3) * 2 = 18. Default y=3. multiply_method(x, y=3) -> 3*3=9. *2 -> 18.
        assert instance is test_bind_target

        # Test with call_triple
        test_method_object.call_method = "call_triple"  # type: ignore[attr-defined]
        assert test_method_object.call_method == "call_triple"  # type: ignore[attr-defined]
        result, instance = bound_method(3)
        assert result == 27  # 9 * 3 = 27
        assert instance is test_bind_target

        # Switch back
        test_method_object.call_method = "call_wrapped"  # type: ignore[attr-defined]
        result, instance = bound_method(3)
        assert result == 9
        assert instance is test_bind_target

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a function
        instance = self.UnitTestClass(instance_method)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has the correct function
        assert instance.__func__ is instance_method

    # Functionality #
    def test_bind_method_property(self) -> None:
        """Tests that the bind_method property correctly gets and sets the binding method."""
        test_method_object = self.create_method_object()

        # Verify the initial bind_method
        assert test_method_object.bind_method == "bind_self"  # type: ignore[attr-defined]

        # Set the bind_method property to bind_wrapped
        test_method_object.bind_method = "bind_wrapped"  # type: ignore[attr-defined]

        # Verify the property was set correctly
        assert test_method_object.bind_method == "bind_wrapped"  # type: ignore[attr-defined]
        assert test_method_object.bind_multiplexer.selected == "bind_wrapped"  # type: ignore[attr-defined]

        # Set it back to the default
        test_method_object.bind_method = "bind_self"  # type: ignore[attr-defined]

        # Verify it was set back correctly
        assert test_method_object.bind_method == "bind_self"  # type: ignore[attr-defined]
        assert test_method_object.bind_multiplexer.selected == "bind_self"  # type: ignore[attr-defined]

    def test_bind_multiplexer(self, test_method_object: DynamicMethod, test_bind_target: Any) -> None:  # type: ignore[override]
        """Tests that the bind_multiplexer correctly delegates to the selected binding method."""
        # Ensure we have a method that returns the instance
        test_method_object = self.create_method_object(instance_method)  # type: ignore[assignment]

        # Test with default bind_method
        assert test_method_object.bind_method == "bind_self"
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Verify the binding
        assert bound_method.__self__ is test_bind_target

        # Call the bound method
        result, instance = bound_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_bind_target

        # Change the bind_method to bind_wrapped
        test_method_object.bind_method = "bind_wrapped"
        assert test_method_object.bind_method == "bind_wrapped"

        # Test with bind_wrapped
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Verify the binding
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

        # Call the bound method
        result, instance = bound_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_bind_target

    def test_coroutine(self, test_bind_target: Any) -> None:
        """Tests that the method object correctly handles coroutine functions."""
        test_coroutine_object = self.create_method_object(add_method_coroutine)

        # Bind the method to an instance
        bound_method = test_coroutine_object.__get__(test_bind_target, type(test_bind_target))

        # Call the coroutine function and run it in an event loop
        coro = bound_method(3)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_bind_target

        # Call with different arguments
        coro = bound_method(3, 4)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_bind_target

    def test_as_function_coroutine(self, test_bind_target: Any) -> None:  # type: ignore[override]
        """Tests that the method object wrapping a coroutine can be converted to a coroutine function."""
        test_coroutine_object = self.create_method_object(add_method_coroutine)

        # Bind the method to an instance
        bound_method = test_coroutine_object.__get__(test_bind_target, type(test_bind_target))

        # Convert to a standard Python function
        func = bound_method.as_function()

        # Verify it's a function
        assert callable(func)

        # Call the function and run it in an event loop
        coro = func(3)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_bind_target

        # Call with different arguments
        coro = func(3, 4)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_bind_target

    def test_no_function(self) -> None:
        """Tests the edge case where no function is provided."""
        # Create an instance without a function
        instance = self.UnitTestClass()

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has no function
        assert instance.__func__ is None

        test_bind_target = self.create_bind_target()

        # Bind the method to the instance
        bound_method = instance.__get__(test_bind_target, type(test_bind_target))

        # Try to call the instance (should raise an error)
        with pytest.raises(TypeError):
            bound_method(3)

    def test_change_function(self, test_bind_target: Any) -> None:
        """Tests the edge case where the function is changed after creation."""
        # Create an instance with a function
        instance = self.UnitTestClass(instance_method)

        # Verify it has the correct function
        assert instance.__func__ is instance_method

        # Bind the method to the instance
        bound_method = instance.__get__(test_bind_target, type(test_bind_target))

        # Call the function
        result, instance_returned = bound_method(3)
        assert result == 5  # 3 + 2 (default y)
        assert instance_returned is test_bind_target

        # Change the function
        bound_method.__func__ = multiply_method

        # Verify it has the new function
        assert bound_method.__func__ is multiply_method

        # Call the new function
        result, instance_returned = bound_method(3)
        assert result == 9  # 3 * 3 (default y)
        assert instance_returned is test_bind_target

    def test_method_binding_to_attribute(self, test_bind_target: Any) -> None:
        """Tests that the DynamicMethod can be bound to an instance attribute."""
        # Create a test method object with a method that works with an instance
        test_method_object = self.UnitTestClass(instance_method)

        # Bind the method to an attribute of the instance
        test_method_object.bind_to_attribute(test_bind_target, name="custom_method")

        # Verify the binding
        assert hasattr(test_bind_target, "custom_method")
        assert callable(test_bind_target.custom_method)

        # Call the bound method
        result, instance = test_bind_target.custom_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_bind_target

    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method.

        DynamicMethod injects the instance (self) into the call, which conflicts with already bound methods
        that don't expect an extra argument. Therefore, this test is skipped/overridden for DynamicMethod.
        """
