"""dynamicfunction_test.py
Tests for the DynamicFunction class in the baseobjects package.

This module provides tests for the DynamicFunction class, which is an abstract function class that has multiplexed 
binding and callback functionality. It tests the core functionality of DynamicFunction, including instance creation, 
function calling, binding, and multiplexed callback.
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
from src.baseobjects.functions import DynamicFunction
from src.baseobjects.testsuite.functions import DynamicFunctionTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers."""
    return x * y


async def async_add_function(x: int, y: int = 2) -> int:
    """An async test function that adds two numbers."""
    await asyncio.sleep(0.01)  # Small delay to simulate async operation
    return x + y


def instance_method(self, x: int, y: int = 2) -> tuple[int, Any]:
    """A test method that works with an instance as its first argument.

    Args:
        self: The instance this method is bound to
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        A tuple with the sum of x and y, and the instance
    """
    return x + y, self


# Helper Classes #
class DynamicFunctionTestObject:
    """A test class for testing method binding and selection."""

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
class TestDynamicFunction(DynamicFunctionTestSuite):
    """Test the DynamicFunction class.

    This class tests the functionality of the DynamicFunction class, which is an abstract function class that has 
    multiplexed binding and callback functionality.
    """

    # Attributes #
    TestClass: Type[DynamicFunction] = DynamicFunction

    # Instance Methods #
    def create_test_method_object(self) -> DynamicFunction:
        """Create a test method object for testing.

        Returns:
            DynamicFunction: An instance of DynamicFunction that wraps a method.
        """
        return self.create_method_object(instance_method)

    def test_bind_method_property(self) -> None:
        """Test that the bind_method property correctly gets and sets the binding method."""
        test_method_object = self.create_test_method_object()

        # Verify the initial bind_method
        assert test_method_object.bind_method == "bind_builtin"

        # Set the bind_method property to bind_wrapped (which exists in BaseCallable)
        test_method_object.bind_method = "bind_wrapped"

        # Verify the property was set correctly
        assert test_method_object.bind_method == "bind_wrapped"
        assert test_method_object.bind_multiplexer.selected == "bind_wrapped"

        # Set it back to the default
        test_method_object.bind_method = "bind_builtin"

        # Verify it was set back correctly
        assert test_method_object.bind_method == "bind_builtin"
        assert test_method_object.bind_multiplexer.selected == "bind_builtin"

    # Fixtures
    @pytest.fixture
    def test_object_instance(self) -> DynamicFunctionTestObject:
        """Create a test object instance.

        Returns:
            DynamicFunctionTestObject: An instance of the test object.
        """
        return DynamicFunctionTestObject(value=10)

    @pytest.fixture
    def test_function_object(self) -> DynamicFunction:
        """Create a test function object that wraps a function.

        Returns:
            DynamicFunction: An instance of DynamicFunction that wraps a function.
        """
        return self.TestClass(add_function)

    @pytest.fixture
    def test_coroutine_object(self) -> DynamicFunction:
        """Create a test function object that wraps a coroutine function.

        Returns:
            DynamicFunction: An instance of DynamicFunction that wraps a coroutine function.
        """
        return self.TestClass(async_add_function)

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

        # Create an instance with a method
        instance = self.TestClass(DynamicFunctionTestObject.method1)

        # Verify it has the correct method
        assert instance.__func__ is DynamicFunctionTestObject.method1

    def test_call(self, test_function_object: DynamicFunction) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function(self, test_function_object: DynamicFunction) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: DynamicFunction) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_coroutine(self, test_coroutine_object: DynamicFunction) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicFunction instance that wraps a coroutine function.
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

    def test_as_function_coroutine(self, test_coroutine_object: DynamicFunction) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a DynamicFunction instance that wraps a coroutine function.
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

    def test_bind_multiplexer(self) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method."""
        # Create a test function object with a method that works with an instance
        test_function_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicFunctionTestObject(value=10)

        # Test with default bind_method
        assert test_function_object.bind_method == "bind_builtin"
        bound_function = test_function_object.__get__(test_object_instance, type(test_object_instance))
        assert bound_function.__self__ is test_object_instance

        # Call the bound function
        result, instance = bound_function(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

        # Change the bind_method to bind_wrapped
        test_function_object.bind_method = "bind_wrapped"
        assert test_function_object.bind_method == "bind_wrapped"

        # Test with bind_wrapped
        bound_function = test_function_object.__get__(test_object_instance, type(test_object_instance))

        # Verify the binding
        assert bound_function.__func__ is test_function_object.__func__
        assert bound_function.__self__ is test_object_instance

        # Call the bound function
        result, instance = bound_function(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

    def test_call_multiplexer(self) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""
        # Create a test function object
        test_function_object = self.TestClass(add_function)

        # Test with default call_method
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

    def test_function_binding(self) -> None:
        """Test that the DynamicFunction can be bound to an instance."""
        # Create a test function object with a method that works with an instance
        test_function_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicFunctionTestObject(value=10)

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
        """Test that the DynamicFunction can be bound to an instance attribute."""
        # Create a test function object with a method that works with an instance
        test_function_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicFunctionTestObject(value=10)

        # Bind the function to an attribute of the instance
        test_function_object.bind_to_attribute(test_object_instance, name="custom_function")

        # Verify the binding
        assert hasattr(test_object_instance, "custom_function")
        assert callable(test_object_instance.custom_function)

        # Call the bound function
        result, instance = test_object_instance.custom_function(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

    def test_no_function(self) -> None:
        """Test the edge case where no function is provided."""
        # Create an instance without a function
        instance = self.TestClass()

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has no function
        assert instance.__func__ is None

        # Try to call the instance (should raise an error)
        with pytest.raises(TypeError):
            instance(3)

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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
