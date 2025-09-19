"""basedecoratortestsuite.py
Base class for test suites which test BaseDecorator and its subclasses.

This module provides a base test suite for testing the BaseDecorator class and its subclasses. It defines abstract
methods for testing the core functionality of decorators, including instance creation, decorator factory behavior, and
decorator usage.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import BaseDecorator
from ..bases import BaseFunctionTestSuite, example_function


# Definitions #
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
    # Tests
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    @abstractmethod
    def test_call(self, test_function_object: BaseDecorator) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: BaseDecorator) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: BaseDecorator) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseDecorator instance that wraps a function.
        """
        
    @abstractmethod
    def test_coroutine(self, test_coroutine_object: BaseDecorator) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a BaseDecorator instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: BaseDecorator) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a BaseDecorator instance that wraps a coroutine function.
        """

    def test_create_decorator_method(self) -> None:
        """Test the create_decorator static method.

        This test verifies that the create_decorator method correctly creates a decorator instance.
        """
        decorator = self.TestClass.create_decorator(self.TestClass, example_function, (), {})
        assert isinstance(decorator, self.TestClass)

    def test_new_without_func(self, *args: Any, **kwargs: Any) -> None:
        """Test the __new__ method when no function is provided.

        This test only verifies that __new__ returns a partial function when no function is provided. This method may be
        overridden to validation that the decorator functions as intended.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Test Uninitialized
        partial_func = self.TestClass(*args, **kwargs)
        assert isinstance(partial_func, partial)

        # Test Initialization
        decorated_func = partial_func(example_function)
        assert isinstance(decorated_func, self.TestClass)

    def test_new_with_func(self, *args: Any, **kwargs: Any) -> None:
        """Test the __new__ method when a function is provided.

        This test only verifies that __new__ returns a decorator instance when a function is provided. This method may
        be overridden to validation that the decorator functions as intended.

        Args:
            test_function: A fixture providing a function to decorate.
        """
        # Test Initialization
        decorated_func = self.TestClass(example_function, *args, **kwargs)
        assert isinstance(decorated_func, self.TestClass)

    @abstractmethod
    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """

    @abstractmethod
    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Test using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.

        Args:
            *args: Positional arguments to pass to the decorator.
            **kwargs: Keyword arguments to pass to the decorator.
        """



# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])