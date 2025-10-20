"""basefunction_test.py
Tests for the BaseFunction class in the baseobjects package.

This module provides tests for the BaseFunction class, which extends BaseCallable to create function-like callable
objects that can be converted to methods when bound to instances. It provides utilities for binding to instances and
attributes, making it ideal for creating decorators and function factories.
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
from types import MethodType
from typing import Any, Type

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.bases import BaseFunction, BaseMethod
from src.baseobjects.testsuite.bases import BaseFunctionTestSuite, ExampleBindTarget, example_function


# Classes #
class TestBaseFunction(BaseFunctionTestSuite):
    """Test the BaseFunction class.

    This class tests the functionality of the BaseFunction class, which extends BaseCallable to create
    function-like callable objects that can be converted to methods when bound to instances.
    """

    # Attributes #
    TestClass: type[BaseFunction] = BaseFunction

    # Instance Methods #
    # Tests
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Test that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Create an instance with a test function
        instance = self.TestClass(example_function)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.TestClass)

        # Verify it has the correct wrapped function
        assert instance.__func__ is example_function

        # Verify it has the correct method_type
        assert instance.method_type is BaseMethod

    def test_call(self, test_function_object: BaseFunction) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

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

    def test_as_function(self, test_function_object: BaseFunction) -> None:
        """Test that the callable object can be converted to a standard Python function.

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
        assert func.__name__ == test_function_object.__name__
        assert func.__doc__ == test_function_object.__doc__
        assert func.__wrapped__ is test_function_object

    def test_call_wrapped(self, test_function_object: BaseFunction) -> None:
        """Test that the wrapped function can be called directly.

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

    def test_bind(self, test_method_object: BaseFunction, test_bind_target: ExampleBindTarget) -> None:
        """Test that the function can be bound to an instance to create a method.

        This test verifies that a bound method is returned and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Call the parent test method
        super().test_bind(test_method_object, test_bind_target)

        # Get a bound method
        bound_method = test_method_object.bind(test_bind_target, self.BindTargetClass)

        # Verify it's a method of the correct type
        assert isinstance(bound_method, test_method_object.method_type)

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is test_bind_target

        # Verify it returns the expected result when called
        result = bound_method(3)
        assert result == (5, test_bind_target)  # (3 + 2, instance)

    def test_bind_to_attribute(self, test_method_object: BaseFunction) -> None:
        """Test that the function can be bound to an instance and set as an attribute.

        This test verifies that a bound method is returned and bound to the target instance's attribute,
        and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Call the parent test method
        super().test_bind_to_attribute(test_method_object)

        # Create a new bind target and bind the method to it
        new_bind_target = self.create_bind_target()
        bound_method = test_method_object.bind_to_attribute(new_bind_target, self.BindTargetClass)

        # Verify it's a method of the correct type
        assert isinstance(bound_method, test_method_object.method_type)

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is new_bind_target

        # Verify it's set as an attribute on the instance
        assert hasattr(new_bind_target, test_method_object.__wrapped__.__name__)

        # Verify it returns the expected result when called through the attribute
        method_name = test_method_object.__wrapped__.__name__
        result = getattr(new_bind_target, method_name)(3)
        assert result == (5, new_bind_target)  # (3 + 2, instance)

        # Test with a custom name
        new_bind_target2 = self.create_bind_target()
        test_method_object.bind_to_attribute(
            new_bind_target2,
            self.BindTargetClass,
            name="custom_method",
        )

        # Verify it's set as an attribute with the custom name
        assert hasattr(new_bind_target2, "custom_method")

        # Verify it returns the expected result when called through the attribute
        result = new_bind_target2.custom_method(3)
        assert result == (5, new_bind_target2)  # (3 + 2, instance)

    def test_descriptor_protocol(self, test_method_object: BaseFunction) -> None:
        """Test that the function implements the descriptor protocol for method binding.

        This test verifies that the descriptor returns a bound method and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """
        # Call the parent test method
        super().test_descriptor_protocol(test_method_object)

        # Create a class with the function as a descriptor
        class DescriptorTest:
            descriptor_method = test_method_object

        # Create an instance of the class
        instance = DescriptorTest()

        # Verify the descriptor returns a bound method
        assert isinstance(instance.descriptor_method, MethodType)

        # Verify it's bound to the correct instance
        assert instance.descriptor_method.__self__ is instance

        # Verify it returns the expected result when called
        result = instance.descriptor_method(3)
        assert result == (5, instance)  # (3 + 2, instance)

    def test_custom_method_type(self) -> None:
        """Test that the method_type attribute can be customized."""

        # Create a custom method type
        class CustomMethod(BaseMethod):
            """A custom method type for testing."""

        # Create a function with the custom method type
        function = self.TestClass(example_function)
        function.method_type = CustomMethod

        # Create a bind target
        bind_target = self.create_bind_target()

        # Bind the function to the target
        bound_method = function.bind(bind_target, self.BindTargetClass)

        # Verify it's an instance of the custom method type
        assert isinstance(bound_method, CustomMethod)

        # Verify it's bound to the correct instance
        assert bound_method.__self__ is bind_target


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
