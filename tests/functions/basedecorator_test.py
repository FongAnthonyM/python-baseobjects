#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" basedecorator_test.py
Tests for the basedecorator.py module in the baseobjects package.
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
from src.baseobjects.functions.basedecorator import BaseDecorator
from tests.bases.base_test import ClassTest


# Definitions #
class TestBaseDecorator(ClassTest):
    """Test the BaseDecorator class.

    This class tests the functionality of the BaseDecorator class, which implements the basic structure for creating
    decorators.
    """
    # Classes #
    class ConcreteDecorator(BaseDecorator):
        """A concrete implementation of BaseDecorator for testing purposes."""

        def __init__(self, func: Callable | None = None, prefix: str = "Decorated: ", *args: Any,
                     **kwargs: Any) -> None:
            self.prefix = prefix
            super().__init__(func=func, *args, **kwargs)

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            """Add a prefix to the result of the wrapped function."""
            result = self.__wrapped__(*args, **kwargs)
            if isinstance(result, str):
                return f"{self.prefix}{result}"
            return result

    # Class Attributes #
    class_: Type[BaseDecorator] = BaseDecorator

    # Instance Methods #
    # Tests
    def test_create_decorator(self) -> None:
        """Test the create_decorator static method.

        This test verifies that the create_decorator method correctly creates a decorator instance.
        """
        # Define a simple function to decorate
        def test_func() -> str:
            return "test"

        # Create a decorator using the static method
        decorator = BaseDecorator.create_decorator(self.ConcreteDecorator, test_func, (), {"prefix": "Test: "})
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.ConcreteDecorator)
        assert decorator.__wrapped__ == test_func
        assert decorator.prefix == "Test: "
        
        # Verify the decorator works correctly
        assert decorator() == "Test: test"

    def test_new_with_func(self) -> None:
        """Test the __new__ method when a function is provided.

        This test verifies that __new__ returns a decorator instance when a function is provided.
        """
        # Define a simple function to decorate
        def test_func() -> str:
            return "test"

        # Create a decorator with a function
        decorator = self.ConcreteDecorator(test_func)
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.ConcreteDecorator)
        assert decorator.__wrapped__ == test_func
        
        # Verify the decorator works correctly
        assert decorator() == "Decorated: test"

    def test_new_without_func(self) -> None:
        """Test the __new__ method when no function is provided.

        This test verifies that __new__ returns a partial function when no function is provided.
        """
        # Create a decorator without a function
        decorator_factory = self.ConcreteDecorator(prefix="Factory: ")
        
        # Verify the decorator factory is a partial function
        assert callable(decorator_factory)
        
        # Define a simple function to decorate
        def test_func() -> str:
            return "test"
        
        # Use the factory to create a decorator
        decorator = decorator_factory(test_func)
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.ConcreteDecorator)
        assert decorator.__wrapped__ == test_func
        assert decorator.prefix == "Factory: "
        
        # Verify the decorator works correctly
        assert decorator() == "Factory: test"

    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """
        # Create a variable for the decorator class (it is more readable than using self.ConcreteDecorator)
        concrete_decorator = self.ConcreteDecorator

        # Use the decorator directly
        @concrete_decorator
        def direct_func() -> str:
            return "direct"
        
        # Verify the decorator works correctly
        assert direct_func() == "Decorated: direct"
        
        # Use the decorator with arguments
        @concrete_decorator(prefix="Custom: ")
        def custom_func() -> str:
            return "custom"
        
        # Verify the decorator with arguments works correctly
        assert custom_func() == "Custom: custom"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])