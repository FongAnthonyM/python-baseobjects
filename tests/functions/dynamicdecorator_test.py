"""dynamicdecorator_test.py
Tests for the DynamicDecorator class in the baseobjects package.

This module provides tests for the DynamicDecorator class, which is an abstract decorator class that has multiplexed 
binding and callback functionality. It tests the core functionality of DynamicDecorator, including instance creation, 
decorator usage, binding, and multiplexed callback.
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
from typing import Any, Type, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import DynamicDecorator
from src.baseobjects.testsuite.functions import DynamicDecoratorTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


async def add_coroutine(x: int, y: int = 2) -> int:
    """An async test function that adds two numbers."""
    await asyncio.sleep(0.01)  # Small delay to simulate async operation
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers."""
    return x * y


# Helper Classes #
class TestClass:
    """A test class for testing decorator binding."""

    def __init__(self, value: int = 10):
        """Initialize with a value."""
        self.value = value

    def method1(self, x: int) -> int:
        """A test method that adds x to the value."""
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x."""
        return self.value * x


# Tests #
class TestDynamicDecorator(DynamicDecoratorTestSuite):
    """Test the DynamicDecorator class.

    This class tests the functionality of the DynamicDecorator class, which is an abstract decorator class that has 
    multiplexed binding and callback functionality.
    """

    # Attributes #
    TestClass: Type[DynamicDecorator] = DynamicDecorator

    # Instance Methods #
    def create_test_method_object(self) -> DynamicDecorator:
        """Create a test method object for testing.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a function.
        """
        return self.TestClass(add_function)

    def test_bind_method_property(self) -> None:
        """Test that the bind_method property correctly gets and sets the binding method."""
        test_function_object = self.create_test_method_object()

        # Verify the initial bind_method
        assert test_function_object.bind_method == "bind_builtin"

        # Set the bind_method property to bind_wrapped
        test_function_object.bind_method = "bind_wrapped"

        # Verify the property was set correctly
        assert test_function_object.bind_method == "bind_wrapped"
        assert test_function_object.bind_multiplexer.selected == "bind_wrapped"

        # Set it back to the default
        test_function_object.bind_method = "bind_builtin"

        # Verify it was set back correctly
        assert test_function_object.bind_method == "bind_builtin"
        assert test_function_object.bind_multiplexer.selected == "bind_builtin"

    # Fixtures
    @pytest.fixture
    def test_function_object(self) -> DynamicDecorator:
        """Create a test function object that wraps a function.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a function.
        """
        return self.TestClass(add_function)

    @pytest.fixture
    def test_coroutine_object(self) -> DynamicDecorator:
        """Create a test function object that wraps a coroutine function.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a coroutine function.
        """
        return self.TestClass(add_coroutine)

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a function
        instance = self.TestClass(add_function)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct function
        assert instance.__func__ is add_function

        # Create an instance with a coroutine
        instance = self.TestClass(add_coroutine)

        # Verify it has the correct function
        assert instance.__func__ is add_coroutine

    def test_call(self, test_function_object: DynamicDecorator) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicDecorator instance that wraps a function.
        """
        # Call the function
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function(self, test_function_object: DynamicDecorator) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicDecorator instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        result = func(3)
        assert result == 5  # 3 + 2 (default y)

        result = func(3, 4)
        assert result == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: DynamicDecorator) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicDecorator instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_coroutine(self, test_coroutine_object: DynamicDecorator) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicDecorator instance that wraps a coroutine function.
        """
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

    def test_as_function_coroutine(self, test_coroutine_object: DynamicDecorator) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a DynamicDecorator instance that wraps a coroutine function.
        """
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

    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """
        # Define a decorator
        decorator = self.TestClass()

        # Use the decorator to decorate a function
        @decorator
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.TestClass)

        # Call the decorated function
        result = test_func(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Test using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.

        Args:
            *args: Positional arguments to pass to the decorator.
            **kwargs: Keyword arguments to pass to the decorator.
        """
        # Define a decorator with arguments
        decorator = self.TestClass(bind_method="bind_wrapped", call_method="call_wrapped")

        # Use the decorator to decorate a function
        @decorator
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.TestClass)

        # Verify the decorator has the correct bind_method and call_method
        assert test_func.bind_method == "bind_wrapped"
        assert test_func.call_method == "call_wrapped"

        # Call the decorated function
        result = test_func(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_bind_multiplexer(self) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method."""
        # Create a test function object
        test_function_object = self.TestClass(add_function)

        # Test with default bind_method
        assert test_function_object.bind_method == "bind_builtin"

        # Change the bind_method to bind_builtin
        test_function_object.bind_method = "bind_builtin"
        assert test_function_object.bind_method == "bind_builtin"

        # Add a custom bind method to the bind_multiplexer
        def custom_bind(self, instance, owner):
            # Just return the function itself
            return self.__func__

        test_function_object.bind_multiplexer.add_function("custom_bind", custom_bind)

        # Change the bind_method to custom_bind
        test_function_object.bind_method = "custom_bind"
        assert test_function_object.bind_method == "custom_bind"

        # Test with custom_bind
        bound_func = test_function_object.__get__(None, None)
        assert bound_func is add_function

    def test_call_multiplexer(self) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""
        # Create a test function object
        test_function_object = self.TestClass(add_function)

        # Test with default call_method
        assert test_function_object.call_method == "call_wrapped"

        # Add a custom call method to the call_multiplexer
        def custom_call(self, *args, **kwargs):
            # Multiply the result by 2
            result = self.call_wrapped(*args, **kwargs)
            return result * 2

        test_function_object.call_multiplexer.add_function("custom_call", custom_call)

        # Change the call_method to custom_call
        test_function_object.call_method = "custom_call"
        assert test_function_object.call_method == "custom_call"

        # Test with custom_call
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2

    def test_no_function(self) -> None:
        """Test the edge case where no function is provided."""
        # Create an instance without a function
        partial_decorator = self.TestClass()

        # Verify it's a partial function
        from functools import partial
        assert isinstance(partial_decorator, partial)

        # Create a function to decorate
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Apply the partial decorator to the function
        decorated_func = partial_decorator(test_func)

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(decorated_func, self.TestClass)

        # Verify it has the correct function
        assert decorated_func.__func__ is test_func

        # Call the decorated function
        result = decorated_func(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_change_function(self) -> None:
        """Test the edge case where the function is changed after creation."""
        # Create an instance with a function
        instance = self.TestClass(add_function)

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

    def test_decorator_chaining(self) -> None:
        """Test that decorators can be chained."""
        # Define two decorators
        decorator1 = self.TestClass()
        decorator2 = self.TestClass()

        # Use the decorators to decorate a function
        @decorator1
        @decorator2
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.TestClass)

        # Call the decorated function
        result = test_func(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
