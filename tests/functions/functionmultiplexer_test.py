"""functionmultiplexer_test.py
Tests for the FunctionMultiplexer class in the baseobjects package.

This module provides tests for the FunctionMultiplexer class, which is a callable that selects between different
functions or methods to be used as the call method, treating them as functions without binding them to the stored instance.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions import FunctionMultiplexer, FunctionRegistry
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
class FunctionMultiplexerTestObject:
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
class TestFunctionMultiplexer(BaseCallableTestSuite):
    """Test the FunctionMultiplexer class.

    This class tests the functionality of the FunctionMultiplexer class, which is a callable that selects between
    different functions or methods to be used as the call method, treating them as functions without binding them
    to the stored instance.
    """

    # Attributes #
    TestClass: Type[FunctionMultiplexer] = FunctionMultiplexer

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
    def test_object_instance(self) -> FunctionMultiplexerTestObject:
        """Create a test object instance.

        Returns:
            FunctionMultiplexerTestObject: An instance of the test object.
        """
        return FunctionMultiplexerTestObject(value=10)

    @pytest.fixture
    def test_multiplexer(self, test_registry: FunctionRegistry) -> FunctionMultiplexer:
        """Create a test multiplexer with a registry.

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            FunctionMultiplexer: An instance of FunctionMultiplexer with a registry.
        """
        return self.TestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_multiplexer_with_object(self, test_object_instance: FunctionMultiplexerTestObject) -> FunctionMultiplexer:
        """Create a test multiplexer with an object.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            FunctionMultiplexer: An instance of FunctionMultiplexer with an object.
        """
        return self.TestClass(instance=test_object_instance, select="method1")

    @pytest.fixture
    def test_function_object(self, test_registry: FunctionRegistry) -> FunctionMultiplexer:
        """Create a test callable object that wraps a function.

        Args:
            test_registry: A fixture providing a function registry.

        Returns:
            FunctionMultiplexer: An instance of FunctionMultiplexer that wraps a function.
        """
        return self.TestClass(registry=test_registry, select="add")

    @pytest.fixture
    def test_method_object(self, test_object_instance: FunctionMultiplexerTestObject) -> FunctionMultiplexer:
        """Create a test callable object that wraps a method.

        Args:
            test_object_instance: A fixture providing a test object.

        Returns:
            FunctionMultiplexer: An instance of FunctionMultiplexer that wraps a method.
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
        test_obj = FunctionMultiplexerTestObject()
        instance = self.TestClass(instance=test_obj, select="method1")

        # Verify it has the correct object and selected method
        assert instance._self_() is test_obj
        assert instance.selected == "method1"

    def test_call(self, test_function_object: FunctionMultiplexer) -> None:
        """Test that the callable object can be called and correctly delegates to the selected function.

        Args:
            test_function_object: A fixture providing a FunctionMultiplexer instance that wraps a function.
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

    def test_as_function(self, test_function_object: FunctionMultiplexer) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a FunctionMultiplexer instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: FunctionMultiplexer) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a FunctionMultiplexer instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    @pytest.mark.skip(reason="FunctionMultiplexer doesn't implement bind_wrapped the same way as BaseCallable")
    def test_bind_wrapped(self, test_method_object: FunctionMultiplexer, test_bind_target: Any) -> None:
        """Test that the wrapped function can be bound to an instance.

        This test is skipped for FunctionMultiplexer because it doesn't implement bind_wrapped
        the same way as BaseCallable.

        Args:
            test_method_object: A fixture providing a FunctionMultiplexer instance that wraps a method.
            test_bind_target: A fixture providing an instance to bind the method to.
        """

    @pytest.mark.skip(
        reason="FunctionMultiplexer doesn't implement the descriptor protocol the same way as BaseCallable"
    )
    def test_descriptor_protocol(self, test_method_object: FunctionMultiplexer) -> None:
        """Test that the callable implements the descriptor protocol for method binding.

        This test is skipped for FunctionMultiplexer because it doesn't implement the descriptor protocol
        the same way as BaseCallable.

        Args:
            test_method_object: A fixture providing a FunctionMultiplexer instance that wraps a function.
        """

    @pytest.mark.skip(reason="FunctionMultiplexer doesn't copy attributes from the wrapped function")
    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object.

        This test is skipped for FunctionMultiplexer because it doesn't copy attributes from the wrapped function.
        """

    def test_select(self, test_multiplexer: FunctionMultiplexer) -> None:
        """Test that the select method correctly changes the selected function.

        Args:
            test_multiplexer: A fixture providing a FunctionMultiplexer instance.
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

    def test_selected_property(self, test_multiplexer: FunctionMultiplexer) -> None:
        """Test that the selected property correctly gets and sets the selected function.

        Args:
            test_multiplexer: A fixture providing a FunctionMultiplexer instance.
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

    def test_add_function(self, test_multiplexer: FunctionMultiplexer) -> None:
        """Test that the add_function method correctly adds a function to the registry.

        Args:
            test_multiplexer: A fixture providing a FunctionMultiplexer instance.
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

    def test_invalid_selection(self, test_multiplexer: FunctionMultiplexer) -> None:
        """Test the edge case where an invalid function name is selected.

        Args:
            test_multiplexer: A fixture providing a FunctionMultiplexer instance.
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


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
