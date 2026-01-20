"""dynamicdecoratortestsuite.py
Base class for test suites which test DynamicDecorator and its subclasses.

This module provides a base test suite for testing the DynamicDecorator class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic decorator objects, including multiplexed binding and callback
functionality, as well as decorator-specific behavior.
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
from typing import Any, ClassVar

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions.dynamicdecorator import DynamicDecorator
from .basedecoratortestsuite import BaseDecoratorTestSuite
from .dynamicfunctiontestsuite import DynamicFunctionTestSuite


# Definitions #
# Classes #
class DynamicDecoratorTestSuite(BaseDecoratorTestSuite, DynamicFunctionTestSuite):
    """Base class for test suites which test DynamicDecorator and its subclasses.

    This class provides common functionality for test suites that test dynamic decorator objects, including fixtures and
    test methods for verifying the behavior of DynamicDecorator objects. Subclasses should implement the abstract
    methods and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be DynamicDecorator or a subclass.
    """

    UnitTestClass: ClassVar[type[DynamicDecorator]]

    # Tests #
    # Magic Methods #
    @abstractmethod
    def test_call(self, test_function_object: DynamicDecorator) -> None:  # type: ignore[override]
        """Tests that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicDecorator instance that wraps a function.
        """

    # Instantiation #
    @abstractmethod
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        This is an abstract method that must be implemented by subclasses.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """

    # Functionality #
    @abstractmethod
    def test_coroutine(self, test_coroutine_object: DynamicDecorator) -> None:  # type: ignore[override]
        """Tests that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicDecorator instance that wraps a coroutine function.
        """

    @abstractmethod
    def test_decorator_usage(self) -> None:
        """Tests using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """

    @abstractmethod
    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.

        Args:
            *args: Positional arguments to pass to the decorator.
            **kwargs: Keyword arguments to pass to the decorator.
        """


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
