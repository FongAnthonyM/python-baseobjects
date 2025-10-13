"""dynamicfunctiontestsuite.py
Base class for test suites which test DynamicFunction and its subclasses.

This module provides a base test suite for testing the DynamicFunction class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic function objects, including multiplexed binding and callback
functionality, as well as function-specific behavior.
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
from ..bases.basefunctiontestsuite import BaseFunctionTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Classes #
class DynamicFunctionTestSuite(DynamicCallableTestSuite, BaseFunctionTestSuite):
    """Base class for test suites which test DynamicFunction and its subclasses.

    This class provides common functionality for test suites that test dynamic function objects, including fixtures and
    test methods for verifying the behavior of DynamicFunction objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be DynamicFunction or a subclass.
    """

    # Attributes #
    TestClass: type[DynamicFunction]

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
