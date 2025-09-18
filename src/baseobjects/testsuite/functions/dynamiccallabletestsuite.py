"""dynamiccallabletestsuite.py
Base class for test suites which test DynamicCallable and its subclasses.

This module provides a base test suite for testing the DynamicCallable class and its subclasses. It defines
abstract methods for testing the core functionality of dynamic callable objects, including multiplexed binding
and callback functionality.
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
from ...functions.dynamiccallable import DynamicCallable
from ..bases.basecallabletestsuite import BaseCallableTestSuite, example_function, example_method, example_coroutine


# Definitions #
# Classes #
class DynamicCallableTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test DynamicCallable and its subclasses.

    This class provides common functionality for test suites that test dynamic callable objects, including fixtures and
    test methods for verifying the behavior of DynamicCallable objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be DynamicCallable or a subclass.
    """

    # Attributes #
    TestClass: Type[DynamicCallable]

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
    def test_call(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_function_object: DynamicCallable) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_bind_builtin(self, test_method_object: DynamicCallable) -> None:
        """Test that the callable object can be bound to an instance using the builtin method.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_bind_wrapped(self, test_method_object: DynamicCallable) -> None:
        """Test that the wrapped function can be bound to an instance.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_function_object: DynamicCallable) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_coroutine(self, test_coroutine_object: DynamicCallable) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicCallable instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_as_function_coroutine(self, test_coroutine_object: DynamicCallable) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a DynamicCallable instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_bind_method_property(self, test_method_object: DynamicCallable) -> None:
        """Test that the bind_method property correctly gets and sets the binding method.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_method_property(self, test_function_object: DynamicCallable) -> None:
        """Test that the call_method property correctly gets and sets the call method.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_bind_multiplexer(self, test_method_object: DynamicCallable) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

    @abstractmethod
    def test_call_multiplexer(self, test_function_object: DynamicCallable) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """