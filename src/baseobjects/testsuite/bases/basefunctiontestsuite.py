"""basefunctionobjecttestsuite.py
Base class for test suites which test BaseFunction and its subclasses.

This module provides a base test suite for testing the BaseFunction class and its subclasses. It defines
abstract methods for testing the core functionality of function objects, including binding to instances,
binding to attributes, descriptor protocol, and custom method types. It inherits from BaseCallableTestSuite
to include tests for the callable behavior of functions.
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
import copy
from typing import Any, Type, Callable

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseFunction, BaseMethod
from .basecallabletestsuite import BaseCallableTestSuite, example_method, example_function, example_coroutine


# Definitions #
# Classes #
class BaseFunctionObjectTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test BaseFunction and its subclasses.

    This class provides common functionality for test suites that test function objects, including fixtures and
    test methods for verifying the behavior of BaseFunction objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseFunction or a subclass.
    """

    # Attributes #
    TestClass: Type[BaseFunction]
    BindTargetClass: Type[Any]

    # Instance Methods #
    def create_bind_target(self, *args: Any, **kwargs) -> Any:
        """Create a test instance to bind methods to.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            The test instance.
        """
        return self.BindTargetClass(*args, **kwargs)

    # Fixtures
    @pytest.fixture
    def test_bind_target(self) -> Any:
        """Create a test instance to bind methods to.

        Returns:
            Any: An instance to bind methods to.
        """
        return self.create_bind_target()

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
    def test_call(self, test_function_object: BaseFunction) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: BaseFunction) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    @abstractmethod
    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object."""

    @abstractmethod
    def test_bind_builtin(self, test_method_object: BaseFunction) -> None:
        """Test that the callable object can be bound to an instance using the builtin method.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    @abstractmethod
    def test_bind_wrapped(self, test_method_object: BaseFunction) -> None:
        """Test that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: BaseFunction) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    @abstractmethod
    def test_coroutine(self, test_coroutine_object: BaseFunction) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a BaseFunction instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: BaseFunction) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a BaseFunction instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_bind(self, test_object: BaseFunction, test_instance: Any) -> None:
        """Test that the function can be bound to an instance to create a method.

        Args:
            test_object: A fixture providing a BaseFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_bind_to_attribute(self, test_object: BaseFunction, test_instance: Any) -> None:
        """Test that the function can be bound to an instance and set as an attribute.

        Args:
            test_object: A fixture providing a BaseFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_descriptor_protocol(self, test_object: BaseFunction, test_instance: Any) -> None:
        """Test that the function implements the descriptor protocol for method binding.

        Args:
            test_object: A fixture providing a BaseFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_custom_method_type(self, test_instance: Any) -> None:
        """Test that the function can use a custom method type for binding.

        Args:
            test_instance: A fixture providing an instance to bind the function to.
        """
