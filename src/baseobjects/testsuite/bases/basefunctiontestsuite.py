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
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...bases import BaseFunction
from .basecallabletestsuite import BaseCallableTestSuite, concrete_function


# Definitions #
# Classes #
class BaseFunctionTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test BaseFunction and its subclasses.

    This class provides common functionality for test suites that test function objects, including fixtures and
    test methods for verifying the behavior of BaseFunction objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseFunction or a subclass.
    """

    # Attributes #
    UnitTestClass: type[BaseFunction]

    # Tests #
    # Magic Methods #
    def test_call(self, test_function_object: BaseFunction) -> None:  # type: ignore[override]
        """Tests that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Call the callable object
        result = test_function_object(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    def test_call_wrapped(self, test_function_object: BaseFunction) -> None:  # type: ignore[override]
        """Tests that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = test_function_object.call_wrapped(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test function
        instance = self.UnitTestClass(concrete_function)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has the correct wrapped function
        assert instance.__func__ is concrete_function

    # Functionality #
    def test_as_function(self, test_function_object: BaseFunction) -> None:  # type: ignore[override]
        """Tests that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Convert to a standard Python function
        func = test_function_object.as_function()

        # Verify it's a function
        assert callable(func)

        # Verify it returns the expected result
        assert func(3) == 5  # 3 + 2 (default y)
        assert func(3, 4) == 7  # 3 + 4

        # Verify it has the correct attributes
        assert func.__name__ == test_function_object.__name__  # type: ignore[attr-defined]
        assert func.__doc__ == test_function_object.__doc__
        assert func.__wrapped__ is test_function_object  # type: ignore[attr-defined]

    def test_bind(self, test_method_object: BaseFunction, test_bind_target: Any) -> None:
        """Tests that the function can be bound to an instance to create a method.

        This test verifies that a bound method is returned and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseCallable instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        bound_method = test_method_object.bind(test_bind_target, self.BindTargetClass)
        assert isinstance(bound_method, test_method_object.method_type)
        assert bound_method.__self__ is test_bind_target

        # Verify it returns the expected result when called
        result = bound_method(3)
        assert result == (5, test_bind_target)  # (3 + 2, instance)

    @pytest.mark.parametrize("name", [None, "named_method"])
    def test_bind_to_attribute(self, test_method_object: BaseFunction, name: str | None) -> None:
        """Tests that the function can be bound to an instance and set as an attribute.

        This test verifies that a bound method is returned and bound to the target instance's attribute,
        and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
            name: The name of the attribute to set.
        """
        new_bind_target = self.create_bind_target()

        kwargs = {}
        if name is not None:
            kwargs["name"] = name
            expected_name = name
        else:
            expected_name = test_method_object.__wrapped__.__name__  # type:ignore[union-attr]

        bound_method = test_method_object.bind_to_attribute(new_bind_target, self.BindTargetClass, **kwargs)
        assert isinstance(bound_method, test_method_object.method_type)
        assert bound_method.__self__ is new_bind_target
        assert hasattr(new_bind_target, expected_name)

        # Verify it returns the expected result when called through the attribute
        result = getattr(new_bind_target, expected_name)(3)
        assert result == (5, new_bind_target)  # (3 + 2, instance)

    def test_bind_to_attribute_none_instance(self, test_method_object: BaseFunction) -> None:
        """Tests bind_to_attribute with None instance."""
        ret = test_method_object.bind_to_attribute(None)
        assert ret is test_method_object
