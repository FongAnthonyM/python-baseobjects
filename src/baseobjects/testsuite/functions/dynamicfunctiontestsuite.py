"""dynamicfunctiontestsuite.py
Base class for test suites which test DynamicFunction and its subclasses.

This module provides a base test suite for testing the DynamicFunction class and its subclasses. It defines
abstract methods for testing the core functionality of dynamic function objects, including multiplexed binding
and callback functionality, as well as function-specific behavior.
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
from typing import Any, Type

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions.dynamiccallable import DynamicFunction
from ..bases.basefunctionobjecttestsuite import BaseFunctionObjectTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Classes #
class DynamicFunctionTestSuite(DynamicCallableTestSuite, BaseFunctionObjectTestSuite):
    """Base class for test suites which test DynamicFunction and its subclasses.

    This class provides common functionality for test suites that test dynamic function objects, including fixtures and
    test methods for verifying the behavior of DynamicFunction objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be DynamicFunction or a subclass.
    """

    # Attributes #
    TestClass: Type[DynamicFunction]

    # Instance Methods #
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
    def test_call(self, test_function_object: DynamicFunction) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: DynamicFunction) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_attribute_copying(self) -> None:
        """Test that attributes from the wrapped function are correctly copied to the callable object."""

    @abstractmethod
    def test_bind_builtin(self, test_method_object: DynamicFunction) -> None:
        """Test that the callable object can be bound to an instance using the builtin method.

        Args:
            test_method_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_bind_wrapped(self, test_method_object: DynamicFunction) -> None:
        """Test that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: DynamicFunction) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_coroutine(self, test_coroutine_object: DynamicFunction) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicFunction instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: DynamicFunction) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a DynamicFunction instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_bind_method_property(self, test_method_object: DynamicFunction) -> None:
        """Test that the bind_method property correctly gets and sets the binding method.

        Args:
            test_method_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_call_method_property(self, test_function_object: DynamicFunction) -> None:
        """Test that the call_method property correctly gets and sets the call method.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_bind_multiplexer(self, test_method_object: DynamicFunction) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method.

        Args:
            test_method_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_call_multiplexer(self, test_function_object: DynamicFunction) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method.

        Args:
            test_function_object: A fixture providing a DynamicFunction instance that wraps a function.
        """

    @abstractmethod
    def test_bind(self, test_object: DynamicFunction, test_instance: Any) -> None:
        """Test that the function can be bound to an instance to create a method.

        Args:
            test_object: A fixture providing a DynamicFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_bind_to_attribute(self, test_object: DynamicFunction, test_instance: Any) -> None:
        """Test that the function can be bound to an instance and set as an attribute.

        Args:
            test_object: A fixture providing a DynamicFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_descriptor_protocol(self, test_object: DynamicFunction, test_instance: Any) -> None:
        """Test that the function implements the descriptor protocol for method binding.

        Args:
            test_object: A fixture providing a DynamicFunction instance.
            test_instance: A fixture providing an instance to bind the function to.
        """

    @abstractmethod
    def test_custom_method_type(self, test_instance: Any) -> None:
        """Test that the function can use a custom method type for binding.

        Args:
            test_instance: A fixture providing an instance to bind the function to.
        """