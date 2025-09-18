"""basedecoratortestsuite.py
Base class for test suites which test BaseDecorator and its subclasses.

This module provides a base test suite for testing the BaseDecorator class and its subclasses. It defines
abstract methods for testing the core functionality of decorators, including instance creation,
decorator factory behavior, and decorator usage.
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
from abc import abstractmethod
from functools import partial
from typing import Any, Callable, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import BaseDecorator
from ..bases import BaseFunctionTestSuite


# Definitions #
# Helper Functions #
def example_function(x: int, y: int = 2) -> int:
    """A simple test function that adds two numbers.

    Args:
        x: First number to add
        y: Second number to add (default: 2)

    Returns:
        The sum of x and y
    """
    return x + y


# Classes #
class BaseDecoratorTestSuite(BaseFunctionTestSuite):
    """Base class for test suites which test BaseDecorator and its subclasses.

    This class provides common functionality for test suites that test decorator objects, including fixtures and
    test methods for verifying the behavior of BaseDecorator objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseDecorator or a subclass.
    """

    # Attributes #
    TestClass: Type[BaseDecorator]

    # Instance Methods #
    # Fixtures
    @pytest.fixture
    def test_decorator_class(self) -> Type[BaseDecorator]:
        """Get the decorator class being tested.

        Returns:
            The decorator class being tested.
        """
        return self.TestClass

    @pytest.fixture
    def test_function(self) -> Callable:
        """Get a simple test function to decorate.

        Returns:
            A simple function that can be decorated.
        """
        return example_function

    @pytest.fixture
    def test_decorator(self, test_function: Callable) -> BaseDecorator:
        """Create a test decorator instance that wraps a function.

        Args:
            test_function: A fixture providing a function to decorate.

        Returns:
            BaseDecorator: An instance of the test class that wraps a function.
        """
        return self.TestClass(test_function)

    @pytest.fixture
    def test_decorator_factory(self) -> partial:
        """Create a test decorator factory.

        Returns:
            A partial function that can be used to create decorator instances.
        """
        return self.TestClass()

    # Tests
    @abstractmethod
    def test_instance_creation(self, test_function: Callable) -> None:
        """Test that instances of the decorator class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            test_function: A fixture providing a function to decorate.
        """

    @abstractmethod
    def test_create_decorator(self, test_function: Callable) -> None:
        """Test the create_decorator static method.

        This test verifies that the create_decorator method correctly creates a decorator instance.

        Args:
            test_function: A fixture providing a function to decorate.
        """

    @abstractmethod
    def test_new_with_func(self, test_function: Callable) -> None:
        """Test the __new__ method when a function is provided.

        This test verifies that __new__ returns a decorator instance when a function is provided.

        Args:
            test_function: A fixture providing a function to decorate.
        """

    @abstractmethod
    def test_new_without_func(self) -> None:
        """Test the __new__ method when no function is provided.

        This test verifies that __new__ returns a partial function when no function is provided.
        """

    @abstractmethod
    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """

    def test_call(self, test_decorator: BaseDecorator) -> None:
        """Test that the decorator can be called and correctly delegates to the wrapped function.

        Args:
            test_decorator: A fixture providing a BaseDecorator instance that wraps a function.
        """
        # Call the decorator with arguments
        result = test_decorator(3, 4)
        
        # Verify the result
        assert result == 7

    def test_factory_creation(self, test_decorator_factory: partial, test_function: Callable) -> None:
        """Test that a decorator factory can be used to create decorator instances.

        Args:
            test_decorator_factory: A fixture providing a decorator factory.
            test_function: A fixture providing a function to decorate.
        """
        # Create a decorator using the factory
        decorator = test_decorator_factory(test_function)
        
        # Verify the decorator was created correctly
        assert isinstance(decorator, self.TestClass)
        assert decorator.__wrapped__ == test_function
        
        # Verify the decorator works correctly
        assert decorator(3, 4) == 7


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])