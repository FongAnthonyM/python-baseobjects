"""basefunctiontestsuite.py
Base class for test suites which test BaseFunction and its subclasses.

This module provides a base test suite for testing the BaseFunction class and its subclasses. It defines abstract
methods for testing the core functionality of function objects, including binding to instances, binding to attributes,
descriptor protocol, and custom method types. It inherits from BaseCallableTestSuite to include tests for the callable
behavior of functions.
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
from types import MethodType
from typing import Any

# Local Packages #
from ...bases import BaseFunction
from .basecallabletestsuite import BaseCallableTestSuite


# Definitions #
# Classes #
class BaseFunctionTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test BaseFunction and its subclasses.

    This class provides common functionality for test suites that test function objects, including fixtures and
    test methods for verifying the behavior of BaseFunction objects. Subclasses should implement the abstract methods
    and set the TestClass attribute.

    Attributes:
        TestClass: The class that the test suite is testing, which should be BaseFunction or a subclass.
    """

    # Attributes #
    TestClass: type[BaseFunction]

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
    def test_call_wrapped(self, test_function_object: BaseFunction) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """

    def test_bind(self, test_method_object: BaseFunction, test_bind_target: Any) -> None:
        """Test that the function can be bound to an instance to create a method.

        This test only varifies that a bound method is returned. This method may be overwritten to include validation
        that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind(test_bind_target, self.BindTargetClass)
        assert isinstance(bound_method, test_method_object.method_type)
        assert bound_method.__self__ is test_bind_target

    def test_bind_to_attribute(self, test_method_object: BaseFunction) -> None:
        """Test that the function can be bound to an instance and set as an attribute.

        This test only varifies that a bound method is returned and bound to the target instance's attribute. This
        method may be overwritten to include validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        new_bind_target = self.create_bind_target()
        bound_method = test_method_object.bind_to_attribute(new_bind_target, self.BindTargetClass)
        assert isinstance(bound_method, test_method_object.method_type)
        assert bound_method.__self__ is new_bind_target
        assert hasattr(new_bind_target, test_method_object.__wrapped__.__name__)

        bound_method_named = test_method_object.bind_to_attribute(
            new_bind_target,
            self.BindTargetClass,
            name="named_method",
        )
        assert isinstance(bound_method_named, test_method_object.method_type)
        assert bound_method_named.__self__ is new_bind_target
        assert hasattr(new_bind_target, "named_method")

    def test_descriptor_protocol(self, test_method_object: BaseFunction) -> None:
        """Test that the function implements the descriptor protocol for method binding.

        This test only varifies that the descriptor returns a bound method. This method may be overwritten to include
        validation that the method functions as intended.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """

        class BindTarget:
            new_method = test_method_object

        instance = BindTarget()
        assert isinstance(instance.new_method, MethodType)
        assert instance.new_method.__self__ is instance
