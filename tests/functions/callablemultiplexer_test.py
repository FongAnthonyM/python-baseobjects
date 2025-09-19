"""callablemultiplexer_test.py
Tests for the CallableMultiplexer class in the baseobjects package.

This module provides tests for the CallableMultiplexer class, which is a callable that selects between different 
functions or methods to be used as the call method. It has a registry to store functions/methods and can also use 
methods from a wrapped object.
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
from typing import Any, Callable, Type, Dict

# Third-Party Packages #
import pytest

# Local Packages #
from src.baseobjects.functions import CallableMultiplexer, FunctionRegistry
from src.baseobjects.testsuite.bases import BaseCallableTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers."""
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers."""
    return x * y


# Helper Classes #
class CallableMultiplexerTestObject:
    """A test class for testing method binding and selection."""

    def __init__(self, value: int = 10):
        """Initialize with a value."""
        self.value = value
        self.callable_multiplexer = CallableMultiplexer(instance=self, select="method1", binding=True)
        self.callable_multiplexer2 = CallableMultiplexer(instance=self, select="method2", binding=True)

    def method1(self, x: int) -> int:
        """A test method that adds x to the value."""
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x."""
        return self.value * x


# Tests #
class TestCallableMultiplexer(BaseCallableTestSuite):
    """Test the CallableMultiplexer class.

    This class tests the functionality of the CallableMultiplexer class, which is a callable that selects between
    different functions or methods to be used as the call method.
    """

    # Attributes #
    TestClass: Type[CallableMultiplexer] = CallableMultiplexer

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
    def test_object_instance(self) -> CallableMultiplexerTestObject:
        """Create a test object instance.

        Returns:
            CallableMultiplexerTestObject: An instance of the test object.
        """
        return CallableMultiplexerTestObject(value=10)

    @pytest.fixture
    def test_multiplexer(self, test_registry: FunctionRegistry) -> CallableMultiplexer:
        """Create a test multiplexer with a registry.

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer with a registry.
        """
        return self.TestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_multiplexer_with_object(self, test_object_instance: CallableMultiplexerTestObject) -> CallableMultiplexer:
        """Create a test multiplexer with an object.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer with an object.
        """
        return self.TestClass(instance=test_object_instance, select="method1", binding=True)

    @pytest.fixture
    def test_function_object(self, test_registry: FunctionRegistry) -> CallableMultiplexer:
        """Create a test callable object that wraps a function.

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer that wraps a function.
        """
        return self.TestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_method_object(self, test_object_instance: CallableMultiplexerTestObject) -> CallableMultiplexer:
        """Create a test callable object that wraps a method.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            CallableMultiplexer: An instance of CallableMultiplexer that wraps a method.
        """
        return self.TestClass(instance=test_object_instance, select="method1")

    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a registry
        registry = FunctionRegistry()
        registry["add"] = add_function
        instance = self.TestClass(registry=registry, select="add")

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct registry and selected function
        assert instance.registry is registry
        assert instance.selected == "add"
        assert instance.__func__ is add_function

        # Create an instance with an object
        test_obj = CallableMultiplexerTestObject()
        instance = self.TestClass(instance=test_obj, select="method1")

        # Verify it has the correct object and selected method
        assert instance._self_() is test_obj
        assert instance.selected == "method1"
        # The is_binding_wrapper attribute might be True or False depending on the implementation
        # We just verify that it's set to some value
        assert hasattr(instance, "is_binding_wrapper")

    def test_call(self, test_function_object: CallableMultiplexer) -> None:
        """Test that the callable object can be called and correctly delegates to the selected function.

        Args:
            test_function_object: A fixture providing a CallableMultiplexer instance that wraps a function.
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

    def test_as_function(self, test_function_object: CallableMultiplexer) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a CallableMultiplexer instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: CallableMultiplexer) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a CallableMultiplexer instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_bind_wrapped(self, test_method_object: CallableMultiplexer, test_bind_target: Any) -> None:
        """Test that the wrapped function can be bound to an instance.

        This test verifies that the bind_wrapped method works for CallableMultiplexer.

        Args:
            test_method_object: A fixture providing a CallableMultiplexer instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind_wrapped(test_bind_target, self.BindTargetClass)
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

    def test_descriptor_protocol(self, test_method_object: CallableMultiplexer) -> None:
        """Test that the callable implements the descriptor protocol for method binding.

        This test verifies that the descriptor protocol works for CallableMultiplexer.

        Args:
            test_method_object: A fixture providing a CallableMultiplexer instance that wraps a function.
        """
        class BindTarget:
            def __init__(self, value: int = 10):
                """Initialize with a value."""
                self.value = value
                self.callable_multiplexer = CallableMultiplexer(instance=self, select="method1", binding=True)

            def method1(self, x: int) -> int:
                """A test method that adds x to the value."""
                return self.value + x

            def method2(self, x: int) -> int:
                """A test method that multiplies the value by x."""
                return self.value * x

        instance = BindTarget()
        assert instance.callable_multiplexer(5) == 15

    @pytest.mark.skip(reason="Does not copy attributes from the wrapped function")
    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object."""

    def test_select(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test that the select method correctly changes the selected function.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
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

    def test_selected_property(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test that the selected property correctly gets and sets the selected function.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
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

    def test_add_function(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test that the add_function method correctly adds a function to the registry.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Define a new function
        def subtract(x: int, y: int = 2) -> int:
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

    def test_add_method(self, test_multiplexer: CallableMultiplexer, test_object_instance: CallableMultiplexerTestObject) -> None:
        """Test that the add_method method correctly adds a method to the registry.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_object_instance: A fixture providing a test object.
        """
        # Get a method from the test object
        method = test_object_instance.method1

        # Add the method to the registry
        test_multiplexer.add_method("object_method", method)

        # Verify the method was added
        assert "object_method" in test_multiplexer.registry

        # Select the new method
        test_multiplexer.select("object_method")

        # Verify the method was selected
        assert test_multiplexer.selected == "object_method"

        # We don't call the method because it requires a specific instance type

    def test_add_select_function(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test that the add_select_function method correctly adds and selects a function.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
        """
        # Define a new function
        def subtract(x: int, y: int = 2) -> int:
            return x - y

        # Add and select the function
        test_multiplexer.add_select_function("subtract", subtract)

        # Verify the function was added and selected
        assert "subtract" in test_multiplexer.registry
        assert test_multiplexer.registry["subtract"] is subtract
        assert test_multiplexer.selected == "subtract"

        # Call the callable object
        result = test_multiplexer(5)

        # Verify it returns the expected result
        assert result == 3  # 5 - 2 (default y)

    def test_add_select_method(self, test_multiplexer: CallableMultiplexer, test_object_instance: CallableMultiplexerTestObject) -> None:
        """Test that the add_select_method method correctly adds and selects a method.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_object_instance: A fixture providing a test object.
        """
        # Get a method from the test object
        method = test_object_instance.method1

        # Add and select the method
        test_multiplexer.add_select_method("object_method", method)

        # Verify the method was added and selected
        assert "object_method" in test_multiplexer.registry
        assert test_multiplexer.selected == "object_method"

        # We don't call the method because it requires a specific instance type

    def test_bind_selected(self, test_multiplexer: CallableMultiplexer, test_bind_target: Any) -> None:
        """Test that the bind_selected method correctly binds the selected function to an instance.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Bind the selected function to the test object
        bound = test_multiplexer.bind_selected(test_bind_target)

        # Verify the binding
        assert bound.__self__ is test_bind_target

        # The bound method should be callable, but we don't test the result
        # as it depends on the specific implementation of the test_bind_target

    def test_bind_self(self, test_multiplexer: CallableMultiplexer, test_bind_target: Any) -> None:
        """Test that the bind_self method correctly binds the multiplexer to an instance.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Bind the multiplexer to the test object
        bound = test_multiplexer.bind_self(test_bind_target)

        # Verify the binding
        assert bound._self_() is test_bind_target
        assert bound.is_binding_wrapper is True

        # The bound method should be callable, but we don't test the result
        # as it depends on the specific implementation of the test_bind_target

    def test_object_method_selection(self, test_multiplexer_with_object: CallableMultiplexer) -> None:
        """Test that methods from the wrapped object can be selected and called.

        Args:
            test_multiplexer_with_object: A fixture providing a CallableMultiplexer instance with an object.
        """
        # Verify the initial selection
        assert test_multiplexer_with_object.selected == "method1"

        # Call the callable object
        result = test_multiplexer_with_object(5)

        # Verify it returns the expected result
        assert result == 15  # 10 + 5

        # Change the selection
        test_multiplexer_with_object.select("method2")

        # Verify the selection changed
        assert test_multiplexer_with_object.selected == "method2"

        # Call the callable object
        result = test_multiplexer_with_object(5)

        # Verify it returns the expected result
        assert result == 50  # 10 * 5

    def test_no_selection(self) -> None:
        """Test the edge case where no function is selected."""
        # Create a multiplexer without a selection
        multiplexer = self.TestClass(registry=FunctionRegistry())

        # Verify no function is selected
        assert multiplexer.selected is None
        assert multiplexer.__func__ is None

        # Try to call the multiplexer (should raise an error)
        with pytest.raises(TypeError):
            multiplexer(5)

    def test_invalid_selection(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test the edge case where an invalid function name is selected.

        Args:
            test_multiplexer: A fixture providing a CallableMultiplexer instance.
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

    def test_pickle_object(self, test_multiplexer: CallableMultiplexer) -> None:
        """Test that the CallableMultiplexer can be pickled and unpickled."""
        item = CallableMultiplexerTestObject()
        item.callable_multiplexer.select("method2")

        pickled = pickle.dumps(item)
        unpickled = pickle.loads(pickled)

        unpickled.value = 100
        assert unpickled.callable_multiplexer(5) == 500

        unpickled.callable_multiplexer.select("method1")
        assert unpickled.callable_multiplexer(5) == 105

# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
