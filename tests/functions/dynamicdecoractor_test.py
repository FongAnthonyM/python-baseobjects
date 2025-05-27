#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" dynamicdecoractor_test.py
Tests for the dynamicdecoractor.py module in the baseobjects package.
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

# Local Packages #
from src.baseobjects.functions.dynamicdecoractor import DynamicDecorator
from tests.bases.base_test import ClassTest


# Definitions #
# Classes #
class TestDynamicDecorator(ClassTest):
    """Test the DynamicDecorator class.

    This class tests the functionality of the DynamicDecorator class, which combines the functionality of BaseDecorator
    and DynamicFunction.
    """
    # Classes #
    class ConcreteDynamicDecorator(DynamicDecorator):
        """A concrete implementation of DynamicDecorator for testing purposes."""

        def __init__(self, func: Callable | None = None, prefix: str = "Decorated: ", *args: Any,
                     **kwargs: Any) -> None:
            self.prefix = prefix
            super().__init__(func=func, *args, **kwargs)

        def custom_bind(self, instance: Any = None, owner: Type[Any] | None = None) -> Any:
            """A custom bind method for testing."""
            # Just return a tuple of the arguments
            return (instance, owner, self.prefix)

        def custom_call(self, *args: Any, **kwargs: Any) -> Any:
            """A custom call method for testing."""
            # Add a prefix to the result
            result = self.__wrapped__(*args, **kwargs)
            if isinstance(result, str):
                return f"{self.prefix}{result}"
            return result

    # Class Attributes #
    class_: Type[DynamicDecorator] = DynamicDecorator

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_func(self) -> Callable:
        """Create a test function for use in tests.

        Returns:
            A simple test function that returns a string.
        """
        def func() -> str:
            return "test"
        return func

    @pytest.fixture
    def dynamic_decorator(self, test_func: Callable) -> ConcreteDynamicDecorator:
        """Create a ConcreteDynamicDecorator instance for testing.

        Args:
            test_func: A fixture providing a test function.

        Returns:
            A ConcreteDynamicDecorator instance wrapping the test function.
        """
        return self.ConcreteDynamicDecorator(test_func)

    # Tests
    def test_init(self, test_func: Callable) -> None:
        """Test the initialization of DynamicDecorator.

        This test verifies that DynamicDecorator can be initialized with a function.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a dynamic decorator with a function
        dynamic_decorator = self.ConcreteDynamicDecorator(test_func)
        
        # Verify the dynamic decorator was created correctly
        assert dynamic_decorator.__wrapped__ == test_func
        assert dynamic_decorator.prefix == "Decorated: "
        assert dynamic_decorator.bind_method == "bind_builtin"
        assert dynamic_decorator.call_method == "call_wrapped"

    def test_new_with_func(self, test_func: Callable) -> None:
        """Test the __new__ method when a function is provided.

        This test verifies that __new__ returns a decorator instance when a function is provided.

        Args:
            test_func: A fixture providing a test function.
        """
        # Create a decorator with a function
        decorator = self.ConcreteDynamicDecorator(test_func)
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.ConcreteDynamicDecorator)
        assert decorator.__wrapped__ == test_func
        
        # Verify the decorator works correctly
        assert decorator() == "test"

    def test_new_without_func(self) -> None:
        """Test the __new__ method when no function is provided.

        This test verifies that __new__ returns a partial function when no function is provided.
        """
        # Create a decorator without a function
        decorator_factory = self.ConcreteDynamicDecorator(prefix="Factory: ")
        
        # Verify the decorator factory is a partial function
        assert callable(decorator_factory)
        
        # Define a simple function to decorate
        def test_func() -> str:
            return "test"
        
        # Use the factory to create a decorator
        decorator = decorator_factory(test_func)
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.ConcreteDynamicDecorator)
        assert decorator.__wrapped__ == test_func
        assert decorator.prefix == "Factory: "
        
        # Verify the decorator works correctly
        assert decorator() == "test"

    def test_bind_method_property(self, dynamic_decorator: ConcreteDynamicDecorator) -> None:
        """Test the bind_method property.

        This test verifies that the bind_method property correctly gets and sets the bind method.

        Args:
            dynamic_decorator: A fixture providing a ConcreteDynamicDecorator instance.
        """
        # Verify the default bind method
        assert dynamic_decorator.bind_method == "bind_builtin"
        
        # Set a custom bind method
        dynamic_decorator.bind_method = "custom_bind"
        
        # Verify the bind method was set correctly
        assert dynamic_decorator.bind_method == "custom_bind"
        assert dynamic_decorator.default_bind_method == "custom_bind"

    def test_call_method_property(self, dynamic_decorator: ConcreteDynamicDecorator) -> None:
        """Test the call_method property.

        This test verifies that the call_method property correctly gets and sets the call method.

        Args:
            dynamic_decorator: A fixture providing a ConcreteDynamicDecorator instance.
        """
        # Verify the default call method
        assert dynamic_decorator.call_method == "call_wrapped"
        
        # Set a custom call method
        dynamic_decorator.call_method = "custom_call"
        
        # Verify the call method was set correctly
        assert dynamic_decorator.call_method == "custom_call"
        assert dynamic_decorator.default_call_method == "custom_call"

    def test_get(self, dynamic_decorator: ConcreteDynamicDecorator) -> None:
        """Test the __get__ method.

        This test verifies that the __get__ method correctly delegates to the bind multiplexer.

        Args:
            dynamic_decorator: A fixture providing a ConcreteDynamicDecorator instance.
        """
        # Set a custom bind method
        dynamic_decorator.bind_method = "custom_bind"
        
        # Create a test instance and class
        class TestClass:
            pass
        
        test_instance = TestClass()
        
        # Call __get__ through descriptor protocol
        result = dynamic_decorator.__get__(test_instance, TestClass)
        
        # Verify the result
        assert result == (test_instance, TestClass, "Decorated: ")

    def test_call(self, dynamic_decorator: ConcreteDynamicDecorator) -> None:
        """Test the __call__ method.

        This test verifies that the __call__ method correctly delegates to the call multiplexer.

        Args:
            dynamic_decorator: A fixture providing a ConcreteDynamicDecorator instance.
        """
        # Verify the default call behavior
        assert dynamic_decorator() == "test"
        
        # Set a custom call method
        dynamic_decorator.call_method = "custom_call"
        
        # Verify the custom call behavior
        assert dynamic_decorator() == "Decorated: test"

    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """
        # Create a variable for the decorator class (it is more readable than using self.ConcreteDynamicDecorator)
        dynamic_decorator = self.ConcreteDynamicDecorator

        # Use the decorator directly
        @dynamic_decorator
        def direct_func() -> str:
            return "direct"
        
        # Verify the decorator works correctly
        assert direct_func() == "direct"
        
        # Use the decorator with arguments
        @dynamic_decorator(prefix="Custom: ")
        def custom_func() -> str:
            return "custom"
        
        # Verify the decorator with arguments works correctly
        assert custom_func() == "custom"

    def test_dynamic_decorator_usage(self) -> None:
        """Test using the decorator with dynamic binding and calling.

        This test verifies that the decorator can dynamically switch between different
        binding and calling methods.
        """
        # Create a variable for the decorator class (it is more readable than using self.ConcreteDynamicDecorator)
        dynamic_decorator = self.ConcreteDynamicDecorator

        # Use the decorator with arguments
        @dynamic_decorator(prefix="Dynamic: ")
        def dynamic_func() -> str:
            return "dynamic"
        
        # Verify the default behavior
        assert dynamic_func() == "dynamic"
        
        # Change the call method
        dynamic_func.call_method = "custom_call"
        
        # Verify the custom call behavior
        assert dynamic_func() == "Dynamic: dynamic"
        
        # Change back to the default call method
        dynamic_func.call_method = "call_wrapped"
        
        # Verify the default behavior is restored
        assert dynamic_func() == "dynamic"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])