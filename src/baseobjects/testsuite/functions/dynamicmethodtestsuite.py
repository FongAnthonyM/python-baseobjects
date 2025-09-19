"""dynamicmethodtestsuite.py
Base class for test suites which test DynamicMethod and its subclasses.

This module provides a base test suite for testing the DynamicMethod class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic method objects, including multiplexed binding and callback
functionality, as well as method-specific behavior.
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

# Local Packages #
from ...functions.dynamiccallable import DynamicMethod
from ..bases.basemethodtestsuite import BaseMethodTestSuite
from .dynamiccallabletestsuite import DynamicCallableTestSuite


# Definitions #
# Classes #
class DynamicMethodTestSuite(DynamicCallableTestSuite, BaseMethodTestSuite):
    """Base class for test suites which test DynamicMethod and its subclasses.

    This class provides common functionality for test suites that test dynamic method objects, including fixtures and
    test methods for verifying the behavior of DynamicMethod objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be DynamicMethod or a subclass.
    """

    # Attributes #
    TestClass: Type[DynamicMethod]

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
    def test_call(self, test_method_object: DynamicMethod) -> None:
        """Test that the method object can be called and correctly delegates to the wrapped function.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
        """

    @abstractmethod
    def test_as_function(self, test_method_object: DynamicMethod) -> None:
        """Test that the method object can be converted to a standard Python function.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
        """

    @abstractmethod
    def test_call_wrapped(self, test_method_object: DynamicMethod) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_method_object: A fixture providing a DynamicMethod instance that wraps a function.
        """
