"""dynamicmethod_test.py
Tests for the DynamicMethod class in the baseobjects package.

This module provides tests for the DynamicMethod class, which is an abstract method class that has multiplexed
binding and callback functionality. It tests the core functionality of DynamicMethod, including instance creation,
method calling, binding, and multiplexed callback.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import DynamicMethod
from src.baseobjects.testsuite.functions import DynamicMethodTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


async def add_method_coroutine(self, x: int, y: int = 2) -> int:
    """An async test function that adds two numbers."""
    await asyncio.sleep(0.01)  # Small delay to simulate async operation
    return x + y, self


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


def multiply_method(self, x: int, y: int = 3) -> tuple[int, Any]:
    """A test method that multiplies two numbers.

    Args:
        self: The instance this method is bound to
        x: First number to multiply
        y: Second number to multiply (default: 3)

    Returns:
        A tuple with the product of x and y, and the instance
    """
    return x * y, self


# Helper Classes #
class DynamicMethodTestObject:
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
class TestDynamicMethod(DynamicMethodTestSuite):
    """Test the DynamicMethod class.

    This class tests the functionality of the DynamicMethod class, which is an abstract method class that has
    multiplexed binding and callback functionality.
    """

    # Attributes #
    TestClass: Type[DynamicMethod] = DynamicMethod

    # Instance Methods #
    def create_test_method_object(self) -> DynamicMethod:
        """Create a test method object for testing.

        Returns:
            DynamicMethod: An instance of DynamicMethod that wraps a method.
        """
        return self.create_method_object(instance_method)

    def test_bind_method_property(self) -> None:
        """Test that the bind_method property correctly gets and sets the binding method."""
        test_method_object = self.create_test_method_object()

        # Verify the initial bind_method
        assert test_method_object.bind_method == "bind_self"

        # Set the bind_method property to bind_wrapped (which exists in BaseCallable)
        test_method_object.bind_method = "bind_wrapped"

        # Verify the property was set correctly
        assert test_method_object.bind_method == "bind_wrapped"
        assert test_method_object.bind_multiplexer.selected == "bind_wrapped"

        # Set it back to the default
        test_method_object.bind_method = "bind_self"

        # Verify it was set back correctly
        assert test_method_object.bind_method == "bind_self"
        assert test_method_object.bind_multiplexer.selected == "bind_self"

    # Fixtures
    @pytest.fixture
    def test_object_instance(self) -> DynamicMethodTestObject:
        """Create a test object instance.

        Returns:
            DynamicMethodTestObject: An instance of the test object.
        """
        return DynamicMethodTestObject(value=10)

    @pytest.fixture
    def test_method_object(self) -> DynamicMethod:
        """Create a test method object that wraps a method.

        Returns:
            DynamicMethod: An instance of DynamicMethod that wraps a method.
        """
        return self.TestClass(instance_method)

    @pytest.fixture
    def test_coroutine_object(self) -> DynamicMethod:
        """Create a test method object that wraps a coroutine function.

        Returns:
            DynamicMethod: An instance of DynamicMethod that wraps a coroutine function.
        """
        return self.TestClass(add_method_coroutine)

    @pytest.fixture
    def bound_method_object(
        self, test_method_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> DynamicMethod:
        """Create a bound method object.

        Returns:
            DynamicMethod: A bound method object.
        """
        return test_method_object.__get__(test_object_instance, type(test_object_instance))

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a function
        instance = self.TestClass(instance_method)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct function
        assert instance.__func__ is instance_method

        # Create an instance with a method
        instance = self.TestClass(DynamicMethodTestObject.method1)

        # Verify it has the correct method
        assert instance.__func__ is DynamicMethodTestObject.method1

    def test_call(self, test_method_object: DynamicMethod, test_object_instance: DynamicMethodTestObject) -> None:
        """Test that the method object can be called and correctly delegates to the wrapped function.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Bind the method to an instance
        bound_method = test_method_object.__get__(test_object_instance, type(test_object_instance))

        # Call the bound method
        result, instance = bound_method(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Call with different arguments
        result, instance = bound_method(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_as_function(
        self, test_method_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> None:
        """Test that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Bind the method to an instance
        bound_method = test_method_object.__get__(test_object_instance, type(test_object_instance))

        # Convert to a standard Python function
        func = bound_method.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        result, instance = func(3)
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        result, instance = func(3, 4)
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_call_wrapped(
        self, test_method_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Call the wrapped function directly
        result, instance = test_method_object.call_wrapped(test_object_instance, 3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Call with different arguments
        result, instance = test_method_object.call_wrapped(test_object_instance, 3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_call_binding(
        self, test_method_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> None:
        """Test that the bound method correctly passes the instance as the first argument when called.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Bind the method to an instance
        bound_method = test_method_object.bind_self(test_object_instance, type(test_object_instance))

        # Call the wrapped function directly
        result, instance = bound_method.call_binding(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Call with different arguments
        result, instance = bound_method.call_binding(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_bind_multiplexer(self) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method."""
        # Create a test method object with a method that works with an instance
        test_method_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicMethodTestObject(value=10)

        # Test with default bind_method
        assert test_method_object.bind_method == "bind_self"
        bound_method = test_method_object.__get__(test_object_instance, type(test_object_instance))

        # Verify the binding
        assert bound_method.__self__ is test_object_instance

        # Call the bound method
        result, instance = bound_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

        # Change the bind_method to bind_wrapped
        test_method_object.bind_method = "bind_wrapped"
        assert test_method_object.bind_method == "bind_wrapped"

        # Test with bind_wrapped
        bound_method = test_method_object.__get__(test_object_instance, type(test_object_instance))

        # Verify the binding
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_object_instance

        # Call the bound method
        result, instance = bound_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance

    def test_call_multiplexer(self) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""
        # Create a test method object
        test_method_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicMethodTestObject(value=10)

        # Bind the method to the instance
        bound_method = test_method_object.__get__(test_object_instance, type(test_object_instance))

        # Test with default call_method
        assert bound_method.call_method == "call_wrapped"
        result, instance = bound_method(3)
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Add a custom call method to the call_multiplexer
        def custom_call(self, *args, **kwargs):
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
        assert instance is test_object_instance

    def test_coroutine(
        self, test_coroutine_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> None:
        """Test that the method object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicMethod instance that wraps a coroutine function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Bind the method to an instance
        bound_method = test_coroutine_object.__get__(test_object_instance, type(test_object_instance))

        # Call the coroutine function and run it in an event loop
        coro = bound_method(3)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Call with different arguments
        coro = bound_method(3, 4)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_as_function_coroutine(
        self, test_coroutine_object: DynamicMethod, test_object_instance: DynamicMethodTestObject
    ) -> None:
        """Test that the method object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a DynamicMethod instance that wraps a coroutine function.
            test_object_instance: A fixture providing a test object instance.
        """
        # Bind the method to an instance
        bound_method = test_coroutine_object.__get__(test_object_instance, type(test_object_instance))

        # Convert to a standard Python function
        func = bound_method.as_function()

        # Verify it's a function
        assert callable(func)

        # Call the function and run it in an event loop
        coro = func(3)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)
        assert instance is test_object_instance

        # Call with different arguments
        coro = func(3, 4)
        result, instance = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4
        assert instance is test_object_instance

    def test_no_function(self) -> None:
        """Test the edge case where no function is provided."""
        # Create an instance without a function
        instance = self.TestClass()

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has no function
        assert instance.__func__ is None

        # Create a test object instance to bind to
        test_object_instance = DynamicMethodTestObject(value=10)

        # Bind the method to the instance
        bound_method = instance.__get__(test_object_instance, type(test_object_instance))

        # Try to call the instance (should raise an error)
        with pytest.raises(TypeError):
            bound_method(3)

    def test_change_function(self) -> None:
        """Test the edge case where the function is changed after creation."""
        # Create an instance with a function
        instance = self.TestClass(instance_method)

        # Verify it has the correct function
        assert instance.__func__ is instance_method

        # Create a test object instance to bind to
        test_object_instance = DynamicMethodTestObject(value=10)

        # Bind the method to the instance
        bound_method = instance.__get__(test_object_instance, type(test_object_instance))

        # Call the function
        result, instance_returned = bound_method(3)
        assert result == 5  # 3 + 2 (default y)
        assert instance_returned is test_object_instance

        # Change the function
        bound_method.__func__ = multiply_method

        # Verify it has the new function
        assert bound_method.__func__ is multiply_method

        # Call the new function
        result, instance_returned = bound_method(3)
        assert result == 9  # 3 * 3 (default y)
        assert instance_returned is test_object_instance

    def test_method_binding_to_attribute(self) -> None:
        """Test that the DynamicMethod can be bound to an instance attribute."""
        # Create a test method object with a method that works with an instance
        test_method_object = self.TestClass(instance_method)

        # Create a test object instance to bind to
        test_object_instance = DynamicMethodTestObject(value=10)

        # Bind the method to an attribute of the instance
        test_method_object.bind_to_attribute(test_object_instance, name="custom_method")

        # Verify the binding
        assert hasattr(test_object_instance, "custom_method")
        assert callable(test_object_instance.custom_method)

        # Call the bound method
        result, instance = test_object_instance.custom_method(5)

        # Verify it returns the expected result
        assert result == 7  # 5 + 2 (default y)
        assert instance is test_object_instance


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
