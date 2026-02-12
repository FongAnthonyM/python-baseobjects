"""dynamicfunctiontestsuite.py
Base class for test suites which test DynamicFunction and its subclasses.

This module provides a base test suite for testing the DynamicFunction class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic function objects, including multiplexed binding and callback
functionality, as well as function-specific behavior.
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

# Local Packages #
from ...functions.dynamiccallable import DynamicFunction
from ..bases.basefunctiontestsuite import BaseFunctionTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers.

    Returns:
        The product of x and y.
    """
    return x * y


async def async_add_function(x: int, y: int = 2) -> int:
    """An async test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    await asyncio.sleep(0.01)
    return x + y


def instance_method(self: Any, x: int, y: int = 2) -> tuple[int, Any]:
    """A test method that works with an instance as its first argument.

    Returns:
        A tuple containing the sum and the instance.
    """
    return x + y, self


# Classes #
class DynamicFunctionTestSuite(DynamicCallableTestSuite, BaseFunctionTestSuite):
    """Base class for test suites which test DynamicFunction and its subclasses.

    This class provides common functionality for test suites that test dynamic function objects, including fixtures and
    test methods for verifying the behavior of DynamicFunction objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be DynamicFunction or a subclass.
    """

    UnitTestClass: type[DynamicFunction]

    # Tests #
    def test_coroutine(self, test_function_object: DynamicFunction) -> None:
        """Tests that the callable object correctly handles coroutine functions."""
        test_coroutine_object = self.create_coroutine_object(async_add_function)

        # Call the coroutine function and run it in an event loop
        coro = test_coroutine_object(3)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        coro = test_coroutine_object(3, 4)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function_coroutine(self) -> None:
        """Tests that the callable object wrapping a coroutine can be converted to a coroutine function."""
        test_coroutine_object = self.create_coroutine_object(async_add_function)

        # Convert to a standard Python function
        func = test_coroutine_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Call the function and run it in an event loop
        coro = func(3)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        coro = func(3, 4)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_function_binding(self, test_function_object: DynamicFunction) -> None:
        """Tests that the DynamicFunction can be bound to an instance."""
        # Create a test function object with a method that works with an instance
        test_function_object = self.create_method_object(instance_method)  # type: ignore[assignment]
        test_object_instance = self.create_bind_target()

        # Bind the function to the instance
        bound_function = test_function_object.bind(test_object_instance)

        # Verify the binding
        assert bound_function.__self__ is test_object_instance

        # Call the bound function
        result, instance = bound_function(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

    def test_function_binding_to_attribute(self) -> None:
        """Tests that the DynamicFunction can be bound to an instance attribute."""
        # Create a test function object with a method that works with an instance
        test_function_object = self.create_method_object(instance_method)
        test_object_instance = self.create_bind_target()

        # Bind the function to an attribute of the instance
        test_function_object.bind_to_attribute(test_object_instance, name="custom_function")  # type: ignore[attr-defined]

        # Verify the binding
        assert hasattr(test_object_instance, "custom_function")
        assert callable(test_object_instance.custom_function)

        # Call the bound function
        result, instance = test_object_instance.custom_function(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

    def test_change_function(self, test_function_object: DynamicFunction) -> None:
        """Tests the edge case where the function is changed after creation."""
        # Create an instance with a function
        instance = self.create_function_object(add_function)

        # Verify it has the correct function
        assert instance.__func__ is add_function

        # Call the function
        result = instance(3)
        assert result == 5  # 3 + 2 (default y)

        # Change the function
        instance.__func__ = multiply_function

        # Verify it has the new function
        assert instance.__func__ is multiply_function

        # Call the new function
        result = instance(3)
        assert result == 9  # 3 * 3 (default y)
