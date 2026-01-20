"""dynamiccallabletestsuite.py
Base class for test suites which test DynamicCallable and its subclasses.

This module provides a base test suite for testing the DynamicCallable class and its subclasses. It defines abstract
methods for testing the core functionality of dynamic callable objects, including multiplexed binding and callback
functionality.
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
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions.dynamiccallable import DynamicCallable
from ..bases.basecallabletestsuite import BaseCallableTestSuite


# Definitions #
# Classes #
class DynamicCallableTestSuite(BaseCallableTestSuite):
    """Base class for test suites which test DynamicCallable and its subclasses.

    This class provides common functionality for test suites that test dynamic callable objects, including fixtures and
    test methods for verifying the behavior of DynamicCallable objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be DynamicCallable or a subclass.
    """

    UnitTestClass: ClassVar[type[DynamicCallable]]

    # Tests #
    # Magic Methods #
    def test_call_method_property(self) -> None:
        """Tests that the call_method property correctly gets and sets the call method."""
        method_object = self.create_method_object()

        # Set the call_method property
        method_object.call_method = "call_wrapped"  # type: ignore[attr-defined]

        # Verify the property was set correctly
        assert method_object.call_method == "call_wrapped"  # type: ignore[attr-defined]
        assert method_object.call_multiplexer.selected == "call_wrapped"  # type: ignore[attr-defined]

        # Set it back to the default
        method_object.call_method = "call_wrapped"  # type: ignore[attr-defined]

        # Verify it was set correctly
        assert method_object.call_method == "call_wrapped"  # type: ignore[attr-defined]
        assert method_object.call_multiplexer.selected == "call_wrapped"  # type: ignore[attr-defined]

    def test_call_multiplexer(self, test_function_object: DynamicCallable) -> None:
        """Tests that the call_multiplexer correctly delegates to the selected call method.

        This test verifies that the call_multiplexer correctly delegates to the selected call method. This method may be
        overwritten to include validation beyond checking that the function is correct.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """
        # Test with default call_method (call_wrapped)
        assert test_function_object.call_method == "call_wrapped"
        result = test_function_object(3)
        assert result == 5  # 3 + 2 (default y)

        # Add a custom call method to the call_multiplexer
        def custom_call(self: Any, *args: Any, **kwargs: Any) -> Any:
            # Multiply the result by 2
            return self.call_wrapped(*args, **kwargs) * 2

        test_function_object.call_multiplexer.add_function("custom_call", custom_call)

        # Change the call_method to custom_call
        test_function_object.call_method = "custom_call"
        assert test_function_object.call_method == "custom_call"

        # Test with custom_call
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2

    def test_call_method_change(self, test_function_object: DynamicCallable) -> None:
        """Tests that changing the call_method affects how the object is called.

        Args:
            test_function_object: A fixture providing a DynamicCallable instance that wraps a function.
        """

        # Add multiple call methods to the call_multiplexer
        def call_double(self: Any, *args: Any, **kwargs: Any) -> int:
            return cast(int, self.call_wrapped(*args, **kwargs) * 2)

        def call_triple(self: Any, *args: Any, **kwargs: Any) -> int:
            return cast(int, self.call_wrapped(*args, **kwargs) * 3)

        test_function_object.call_multiplexer.add_function("call_double", call_double)
        test_function_object.call_multiplexer.add_function("call_triple", call_triple)

        # Test with call_double
        test_function_object.call_method = "call_double"
        assert test_function_object.call_method == "call_double"
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2

        # Test with call_triple
        test_function_object.call_method = "call_triple"
        assert test_function_object.call_method == "call_triple"
        result = test_function_object(3)
        assert result == 15  # (3 + 2) * 3

        # Test switching back to call_wrapped
        test_function_object.call_method = "call_wrapped"
        assert test_function_object.call_method == "call_wrapped"
        result = test_function_object(3)
        assert result == 5  # 3 + 2

    # Functionality #
    def test_bind_method_property(self) -> None:
        """Tests that the bind_method property correctly gets and sets the binding method."""
        method_object = self.create_method_object()

        # Set the bind_method property
        method_object.bind_method = "bind_wrapped"  # type: ignore[attr-defined]

        # Verify the property was set correctly
        assert method_object.bind_method == "bind_wrapped"  # type: ignore[attr-defined]
        assert method_object.bind_multiplexer.selected == "bind_wrapped"  # type: ignore[attr-defined]

        # Set it back to the default
        method_object.bind_method = "bind_builtin"  # type: ignore[attr-defined]

        # Verify it was set back correctly
        assert method_object.bind_method == "bind_builtin"  # type: ignore[attr-defined]
        assert method_object.bind_multiplexer.selected == "bind_builtin"  # type: ignore[attr-defined]

    def test_bind_multiplexer(self, test_method_object: DynamicCallable, test_bind_target: Any) -> None:
        """Tests that the bind_multiplexer correctly delegates to the selected binding method.

        This test verifies that the bind_multiplexer correctly delegates to the selected binding method. This method may
        be overwritten to include validation beyond checking that the function is correct.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a method.
            test_bind_target: A fixture providing an instance to bind the method to.
        """
        # Test with default bind_method (bind_builtin)
        assert test_method_object.bind_method == "bind_builtin"
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))
        assert bound_method.__self__ is test_bind_target

        # Change the bind_method to bind_wrapped
        test_method_object.bind_method = "bind_wrapped"
        assert test_method_object.bind_method == "bind_wrapped"

        # Test with bind_wrapped
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))
        assert bound_method.__func__ is test_method_object.__func__
        assert bound_method.__self__ is test_bind_target

    def test_bind_method_change(self, test_method_object: DynamicCallable, test_bind_target: Any) -> None:
        """Tests that changing the bind_method affects how the object is bound.

        Args:
            test_method_object: A fixture providing a DynamicCallable instance that wraps a method.
            test_bind_target: A fixture providing an instance to bind the method to.
        """

        # Add a custom bind method to the bind_multiplexer
        def bind_custom(self: Any, instance: Any, owner: Any = None) -> Any:
            # Create a function that returns a fixed value
            def fixed_value(*args: Any, **kwargs: Any) -> int:
                return 42

            return fixed_value

        test_method_object.bind_multiplexer.add_function("bind_custom", bind_custom)

        # Change the bind_method to bind_custom
        test_method_object.bind_method = "bind_custom"
        assert test_method_object.bind_method == "bind_custom"

        # Test with bind_custom
        bound_method = test_method_object.__get__(test_bind_target, type(test_bind_target))

        # Verify it returns the fixed value
        assert bound_method() == 42

    def test_construct_with_bind_method(self) -> None:
        """Tests that the bind_method can be set during construction."""

        # Create an instance with a specific bind_method
        def temp_func() -> None:
            pass

        instance = self.UnitTestClass(temp_func, bind_method="bind_wrapped")

        # Verify the bind_method was set correctly
        assert instance.bind_method == "bind_wrapped"

    def test_construct_with_call_method(self) -> None:
        """Tests that the call_method can be set during construction."""

        # Create an instance with a specific call_method
        def temp_func() -> None:
            pass

        instance = self.UnitTestClass(temp_func, call_method="call_wrapped")

        # Verify the call_method was set correctly
        assert instance.call_method == "call_wrapped"

    def test_no_function(self) -> None:
        """Tests the edge case where no function is provided."""
        # Create an instance without a function
        instance = self.UnitTestClass()

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has no function
        assert instance.__func__ is None

        # Try to call the instance (should raise an error)
        with pytest.raises(TypeError):
            instance(3)
