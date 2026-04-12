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
from typing import Any

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.bases import BaseFunction, BaseMethod
from baseobjects.testsuite.bases import BaseFunctionTestSuite, concrete_function


# Classes #
class TestBaseFunction(BaseFunctionTestSuite):
    """Test the BaseFunction class.

    This class tests the functionality of the BaseFunction class, which extends BaseCallable to create function-like
    callable objects that can be converted to methods when bound to instances.
    """

    # Attributes #
    UnitTestClass: type[BaseFunction] = BaseFunction

    # Instance Methods #
    # Tests
    def test_descriptor_protocol(self, test_method_object: Any) -> None:
        """Test that the function implements the descriptor protocol for method binding.

        This test verifies that the descriptor returns a bound method and that it functions correctly.

        Args:
            test_method_object: A fixture providing a BaseFunction instance that wraps a function.
        """

        class BindTarget:
            new_method = test_method_object

        instance = BindTarget()
        assert isinstance(instance.new_method, (MethodType, BaseMethod))
        assert instance.new_method.__self__ is instance

        # Verify it returns the expected result when called
        result = instance.new_method(3)
        assert result == (5, instance)  # (3 + 2, instance)

    def test_custom_method_type(self) -> None:
        """Test that the bind_method_type attribute can be customized."""

        # Create a custom method type
        class CustomMethod(BaseMethod):
            """A custom method type for testing."""

        # Create a function with the custom method type
        function = self.UnitTestClass(concrete_function)
        function.bind_method_type = CustomMethod

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
