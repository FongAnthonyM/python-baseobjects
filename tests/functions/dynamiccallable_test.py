"""dynamiccallable_test.py
Tests for the DynamicCallable class in the baseobjects package.

This module provides tests for the DynamicCallable class, which is an abstract callable class that has multiplexed
binding and callback functionality. It tests the core functionality of DynamicCallable, including instance creation,
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
from typing import Any, Callable, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions import DynamicCallable, DynamicFunction, DynamicMethod
from src.baseobjects.testsuite.functions import DynamicCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers."""
    return x * y


# Helper Classes #
class DynamicCallableTestObject:
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
class TestDynamicCallable(DynamicCallableTestSuite):
    """Test the DynamicCallable class.

    This class tests the functionality of the DynamicCallable class, which is an abstract callable class that has
    multiplexed binding and callback functionality.
    """

    # Attributes #
    TestClass: Type[DynamicCallable] = DynamicCallable

    # Instance Methods #
    def create_test_method_object(self) -> DynamicCallable:
        """Create a test method object for testing.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a method.
        """
        return self.create_method_object()

    # @pytest.mark.skip(reason="DynamicCallable doesn't support pickling of methods")
    def test_pickling(self, test_object: DynamicCallable) -> None:
        """Test pickling and unpickling of the callable object.

        This test is skipped for DynamicCallable because it doesn't support pickling of methods.

        Args:
            test_object: A fixture providing a DynamicCallable instance.
        """
        super().test_pickling(test_object)

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
    def test_object_instance(self) -> DynamicCallableTestObject:
        """Create a test object instance.

        Returns:
            DynamicCallableTestObject: An instance of the test object.
        """
        return DynamicCallableTestObject(value=10)

    @pytest.fixture
    def test_function_object(self) -> DynamicCallable:
        """Create a test callable object that wraps a function.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a function.
        """
        return self.create_function_object(add_function)

    @pytest.fixture
    def test_method_object(self) -> DynamicCallable:
        """Create a test callable object that wraps a method.

        Returns:
            DynamicCallable: An instance of DynamicCallable that wraps a method.
        """
        return self.create_method_object()

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
        instance = self.TestClass(DynamicCallableTestObject.method1)

        # Verify it has the correct method
        assert instance.__func__ is DynamicCallableTestObject.method1

    def test_call(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_as_function(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: DynamicCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_dynamic_method(self, test_bind_target: Any) -> None:
        """Test the DynamicMethod subclass.

        Args:
            test_bind_target: A fixture providing an instance to bind the method to.
        """

        # Create a method that can work with the test_bind_target
        def compatible_method(self, x: int) -> int:
            """A test method that works with any object as self."""
            return x + 5  # Just return x + 5, ignoring self

        # Create a DynamicMethod instance
        dynamic_method = DynamicMethod(compatible_method)

        # Verify it's an instance of the correct class
        assert isinstance(dynamic_method, DynamicMethod)

        # Verify the default bind_method is bind_self
        assert dynamic_method.bind_method == "bind_self"
        assert dynamic_method.default_bind_method == "bind_self"

        # Bind the method to an instance
        bound_method = dynamic_method.__get__(test_bind_target, type(test_bind_target))

        # Verify the binding
        assert bound_method._self_() is test_bind_target

        # Call the bound method
        result = bound_method(3)

        # Verify it returns the expected result
        assert result == 8  # 3 + 5

    def test_dynamic_function(self) -> None:
        """Test the DynamicFunction subclass."""
        # Create a DynamicFunction instance
        dynamic_function = DynamicFunction(add_function)

        # Verify it's an instance of the correct class
        assert isinstance(dynamic_function, DynamicFunction)

        # Call the function
        result = dynamic_function(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_bind_method_change(self, test_method_object: DynamicCallable, test_bind_target: Any) -> None:
        """Test that changing the bind_method affects how the object is bound.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a method.
            test_bind_target: A fixture providing an instance to bind the method to.
        """

        # Add a custom bind method to the bind_multiplexer
        def bind_custom(self, instance, owner=None):
            # Create a function that returns a fixed value
            def fixed_value(*args, **kwargs):
                return 42

            return fixed_value

        test_method_object.bind_multiplexer.add_function("bind_custom", bind_custom)

        # Change the bind_method to bind_custom
        test_method_object.bind_method = "bind_custom"
        assert test_method_object.bind_method == "bind_custom"

        # Test with bind_custom
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Verify it returns the fixed value
        assert bound_method() == 42

    def test_call_method_change(self, test_function_object: DynamicCallable) -> None:
        """Test that changing the call_method affects how the object is called.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

        # Add multiple call methods to the call_multiplexer
        def call_double(self, *args, **kwargs):
            return self.call_wrapped(*args, **kwargs) * 2

        def call_triple(self, *args, **kwargs):
            return self.call_wrapped(*args, **kwargs) * 3

        test_function_object.call_multiplexer.add_function("call_double", call_double)
        test_function_object.call_multiplexer.add_function("call_triple", call_triple)

        # Test with call_double
        test_function_object.call_method = "call_double"
        assert test_function_object.call_method == "call_double"
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2

        # Test with call_triple
        test_function_object.call_method = "call_triple"
        assert test_function_object.call_method == "call_triple"
        result = test_function_object(3)
        assert result == 15  # (3 + 2) * 3

        # Test switching back to call_wrapped
        test_function_object.call_method = "call_wrapped"
        assert test_function_object.call_method == "call_wrapped"
        result = test_function_object(3)
        assert result == 5  # 3 + 2

    def test_construct_with_bind_method(self) -> None:
        """Test that the bind_method can be set during construction."""
        # Create an instance with a specific bind_method
        instance = self.TestClass(add_function, bind_method="bind_wrapped")

        # Verify the bind_method was set correctly
        assert instance.bind_method == "bind_wrapped"

    def test_construct_with_call_method(self) -> None:
        """Test that the call_method can be set during construction."""
        # Create an instance with a specific call_method
        instance = self.TestClass(add_function, call_method="call_wrapped")

        # Verify the call_method was set correctly
        assert instance.call_method == "call_wrapped"

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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
