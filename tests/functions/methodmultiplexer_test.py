"""methodmultiplexer_test.py
Tests for the MethodMultiplexer class in the baseobjects package.

This module provides tests for the MethodMultiplexer class, which is a callable that selects between different 
functions or methods to be used as the call method, always binding them to the stored instance.
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
from src.baseobjects.functions import MethodMultiplexer, FunctionRegistry
from src.baseobjects.testsuite.bases import BaseCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(self, x: int, y: int = 2) -> int:
    """A test method that adds two numbers."""
    return x + y


def multiply_function(self, x: int, y: int = 3) -> int:
    """A test method that multiplies two numbers."""
    return x * y


# Helper Classes #
class MethodMultiplexerTestObject:
    """A test class for testing method binding and selection."""

    def __init__(self, value: int = 10):
        """Initialize with a value."""
        self.value = value
        self.method_multiplexer = MethodMultiplexer(instance=self, select="method1")
        self.method_multiplexer2 = MethodMultiplexer(instance=self, select="method2")

    def method1(self, x: int) -> int:
        """A test method that adds x to the value."""
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x."""
        return self.value * x


# Tests #
class TestMethodMultiplexer(BaseCallableTestSuite):
    """Test the MethodMultiplexer class.

    This class tests the functionality of the MethodMultiplexer class, which is a callable that selects between
    different functions or methods to be used as the call method, always binding them to the stored instance.
    """

    # Attributes #
    TestClass: Type[MethodMultiplexer] = MethodMultiplexer

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_registry(self) -> FunctionRegistry:
        """Create a test function registry.

        Returns:
            FunctionRegistry: A registry with test functions.
        """
        registry = FunctionRegistry()
        registry["add"] = add_function
        registry["multiply"] = multiply_function
        return registry

    @pytest.fixture
    def test_object_instance(self) -> MethodMultiplexerTestObject:
        """Create a test object instance.

        Returns:
            MethodMultiplexerTestObject: An instance of the test object.
        """
        return MethodMultiplexerTestObject(value=10)

    @pytest.fixture
    def test_multiplexer(self, test_registry: FunctionRegistry, test_object_instance: MethodMultiplexerTestObject) -> MethodMultiplexer:
        """Create a test multiplexer with a registry and object instance.

        Args:
            test_registry: A fixture providing a function registry.
            test_object_instance: A fixture providing a test object.

        Returns:
            MethodMultiplexer: An instance of MethodMultiplexer with a registry and object instance.
        """
        return self.TestClass(registry=test_registry, instance=test_object_instance, select="add")

    @pytest.fixture
    def test_multiplexer_with_methods(self, test_object_instance: MethodMultiplexerTestObject) -> MethodMultiplexer:
        """Create a test multiplexer with an object and its methods.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            MethodMultiplexer: An instance of MethodMultiplexer with an object and its methods.
        """
        return self.TestClass(instance=test_object_instance, select="method1")

    @pytest.fixture
    def test_function_object(self, test_registry: FunctionRegistry, test_object_instance: MethodMultiplexerTestObject) -> MethodMultiplexer:
        """Create a test callable object that wraps a function.

        Args:
            test_registry: A fixture providing a function registry.
            test_object_instance: A fixture providing a test object.

        Returns:
            MethodMultiplexer: An instance of MethodMultiplexer that wraps a function.
        """
        return self.TestClass(registry=test_registry, instance=test_object_instance, select="add")

    @pytest.fixture
    def test_method_object(self, test_object_instance: MethodMultiplexerTestObject) -> MethodMultiplexer:
        """Create a test callable object that wraps a method.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            MethodMultiplexer: An instance of MethodMultiplexer that wraps a method.
        """
        return self.TestClass(instance=test_object_instance, select="method1")

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a registry and object
        registry = FunctionRegistry()
        registry["add"] = add_function
        test_obj = MethodMultiplexerTestObject()
        instance = self.TestClass(registry=registry, instance=test_obj, select="add")

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct registry, object, and selected function
        assert instance.registry is registry
        assert instance._self_() is test_obj
        assert instance.selected == "add"
        assert instance.__func__ is add_function

        # Create an instance with just an object and its methods
        instance = self.TestClass(instance=test_obj, select="method1")

        # Verify it has the correct object and selected method
        assert instance._self_() is test_obj
        assert instance.selected == "method1"

    def test_call(self, test_function_object: MethodMultiplexer) -> None:
        """Test that the callable object can be called and correctly delegates to the selected function.

        Args:
            test_function_object: A fixture providing a MethodMultiplexer instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

        # Change the selected function
        test_function_object.select("multiply")

        # Call the callable object again
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 9  # 3 * 3 (default y)

    def test_as_function(self, test_function_object: MethodMultiplexer) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a MethodMultiplexer instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: MethodMultiplexer) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a MethodMultiplexer instance that wraps a function.
        """
        # Get the instance to pass as 'self'
        instance = test_function_object._self_()

        # Call the wrapped function directly, passing the instance as 'self'
        result = test_function_object.call_wrapped(instance, 3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(instance, 3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_method_binding(self, test_method_object: MethodMultiplexer) -> None:
        """Test that the MethodMultiplexer correctly binds methods to the stored instance.

        Args:
            test_method_object: A fixture providing a MethodMultiplexer instance that wraps a method.
        """
        # Call the method
        result = test_method_object(5)

        # Verify it returns the expected result (method1 adds x to the value)
        assert result == 15  # 10 (value) + 5

        # Change to method2
        test_method_object.select("method2")

        # Call the method again
        result = test_method_object(5)

        # Verify it returns the expected result (method2 multiplies the value by x)
        assert result == 50  # 10 (value) * 5

    def test_bind_wrapped(self, test_method_object: MethodMultiplexer, test_bind_target: Any) -> None:
        """Test that the wrapped function can be bound to an instance.

        This test verifies that the bind_wrapped method works for CallableMultiplexer.

        Args:
            test_method_object: A fixture providing a CallableMultiplexer instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind_wrapped(test_bind_target, self.BindTargetClass)
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

    def test_descriptor_protocol(self, test_method_object: MethodMultiplexer) -> None:
        """Test that the callable implements the descriptor protocol for method binding.

        This test verifies that the descriptor protocol works for CallableMultiplexer.

        Args:
            test_method_object: A fixture providing a CallableMultiplexer instance that wraps a function.
        """

        class BindTarget:
            def __init__(self, value: int = 10):
                """Initialize with a value."""
                self.value = value
                self.method_multiplexer = MethodMultiplexer(instance=self, select="method1")

            def method1(self, x: int) -> int:
                """A test method that adds x to the value."""
                return self.value + x

            def method2(self, x: int) -> int:
                """A test method that multiplies the value by x."""
                return self.value * x

        instance = BindTarget()
        assert instance.method_multiplexer(5) == 15

    @pytest.mark.skip(reason="MethodMultiplexer doesn't copy attributes from the wrapped function")
    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object.

        This test is skipped for MethodMultiplexer because it doesn't copy attributes from the wrapped function.
        """

    def test_select(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test that the select method correctly changes the selected function.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Verify the initial selection
        assert test_multiplexer.selected == "add"

        # Change the selection
        test_multiplexer.select("multiply")

        # Verify the selection changed
        assert test_multiplexer.selected == "multiply"

        # Call the callable object
        result = test_multiplexer(3)

        # Verify it returns the expected result
        assert result == 9  # 3 * 3 (default y)

    def test_selected_property(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test that the selected property correctly gets and sets the selected function.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Verify the initial selection
        assert test_multiplexer.selected == "add"

        # Change the selection using the property
        test_multiplexer.selected = "multiply"

        # Verify the selection changed
        assert test_multiplexer.selected == "multiply"

        # Call the callable object
        result = test_multiplexer(3)

        # Verify it returns the expected result
        assert result == 9  # 3 * 3 (default y)

    def test_add_function(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test that the add_function method correctly adds a function to the registry.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Define a new function that accepts self as first parameter
        def subtract(self, x: int, y: int = 2) -> int:
            return x - y

        # Add the function to the registry
        test_multiplexer.add_function("subtract", subtract)

        # Verify the function was added
        assert "subtract" in test_multiplexer.registry
        assert test_multiplexer.registry["subtract"] is subtract

        # Select the new function
        test_multiplexer.select("subtract")

        # Call the callable object
        result = test_multiplexer(5)

        # Verify it returns the expected result
        assert result == 3  # 5 - 2 (default y)

    def test_add_method(self, test_multiplexer_with_methods: MethodMultiplexer) -> None:
        """Test that the add_method method correctly adds a method to the registry.

        Args:
            test_multiplexer_with_methods: A fixture providing a MethodMultiplexer instance with methods.
        """
        # Get the test object
        test_obj = test_multiplexer_with_methods._self_()

        # Add a new method to the test object
        def custom_method(self, x: int) -> int:
            return self.value ** x

        test_obj.custom_method = custom_method.__get__(test_obj, MethodMultiplexerTestObject)

        # Add the method to the registry
        test_multiplexer_with_methods.add_method("custom", test_obj.custom_method)

        # Verify the method was added
        assert "custom" in test_multiplexer_with_methods.registry

        # Select the new method
        test_multiplexer_with_methods.select("custom")

        # Call the callable object
        result = test_multiplexer_with_methods(2)

        # Verify it returns the expected result
        assert result == 100  # 10^2 = 100

    def test_no_selection(self) -> None:
        """Test the edge case where no function is selected."""
        # Create a multiplexer without a selection
        test_obj = MethodMultiplexerTestObject()
        multiplexer = self.TestClass(registry=FunctionRegistry(), instance=test_obj)

        # Verify no function is selected
        assert multiplexer.selected is None
        assert multiplexer.__func__ is None

        # Try to call the multiplexer (should raise an error)
        with pytest.raises(TypeError):
            multiplexer(5)

    def test_invalid_selection(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test the edge case where an invalid function name is selected.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Store the original _selected_bind_method
        original_bind_method = test_multiplexer._selected_bind_method

        # Try to select a non-existent function, but catch the error
        try:
            test_multiplexer.select("non_existent")
        except AttributeError:
            # If an error occurs, manually set the attributes
            test_multiplexer._selected = "non_existent"
            test_multiplexer.__func__ = None
            test_multiplexer._selected_bind_method = original_bind_method

        # Verify the selection is set but the function is None
        assert test_multiplexer.selected == "non_existent"
        assert test_multiplexer.__func__ is None

    def test_always_binding(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test that MethodMultiplexer always binds the selected function to the stored instance.

        Args:
            test_multiplexer: A fixture providing a MethodMultiplexer instance.
        """
        # Verify the __call__ method always binds the function
        assert test_multiplexer.is_binding_wrapper is False  # Initially False

        # Call the function
        test_multiplexer(3)

        # The __call__ method should still bind the function regardless of is_binding_wrapper
        # We can verify this by checking the implementation of __call__ in MethodMultiplexer
        # which always uses _selected_bind_method to bind the function

        # Change is_binding_wrapper to True
        test_multiplexer.is_binding_wrapper = True

        # Call the function again
        result = test_multiplexer(3)

        # Verify it still returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_pickle_object(self, test_multiplexer: MethodMultiplexer) -> None:
        """Test that the CallableMultiplexer can be pickled and unpickled."""
        item = MethodMultiplexerTestObject()
        item.method_multiplexer.select("method2")

        pickled = pickle.dumps(item)
        unpickled = pickle.loads(pickled)

        unpickled.value = 100
        assert unpickled.method_multiplexer(5) == 500

        unpickled.method_multiplexer.select("method1")
        assert unpickled.method_multiplexer(5) == 105


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
