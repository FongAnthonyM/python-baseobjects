"""dynamicdecorator_test.py
Tests for the DynamicDecorator class in the baseobjects package.

This module provides tests for the DynamicDecorator class, which is an abstract decorator class that has multiplexed
binding and callback functionality. It tests the core functionality of DynamicDecorator, including instance creation,
decorator usage, binding, and multiplexed callback.
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
import asyncio
import pickle
from typing import Any, ClassVar, cast

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions import DynamicDecorator
from baseobjects.testsuite.functions import DynamicDecoratorTestSuite


# Definitions #
# Helper Functions #
def add_function(x: int, y: int = 2) -> int:
    """A test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    return x + y


async def add_coroutine(x: int, y: int = 2) -> int:
    """An async test function that adds two numbers.

    Returns:
        The sum of x and y.
    """
    await asyncio.sleep(0.01)  # Small delay to simulate async operation
    return x + y


def multiply_function(x: int, y: int = 3) -> int:
    """A test function that multiplies two numbers.

    Returns:
        The product of x and y.
    """
    return x * y


# Helper Classes #
class UnitTestClass:
    """A test class for testing decorator binding."""

    def __init__(self, value: int = 10) -> None:
        """Initialize with a value."""
        self.value = value

    def method1(self, x: int) -> int:
        """A test method that adds x to the value.

        Returns:
            The sum of value and x.
        """
        return self.value + x

    def method2(self, x: int) -> int:
        """A test method that multiplies the value by x.

        Returns:
            The product of value and x.
        """
        return self.value * x


# Tests #
class TestDynamicDecorator(DynamicDecoratorTestSuite):
    """Test the DynamicDecorator class.

    This class tests the functionality of the DynamicDecorator class, which is an abstract decorator class that has
    multiplexed binding and callback functionality.
    """

    # Attributes #
    UnitTestClass: type[DynamicDecorator] = DynamicDecorator

    # Instance Methods #
    def create_test_method_object(self) -> DynamicDecorator:
        """Create a test method object for testing.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a function.
        """
        return self.UnitTestClass(add_function)

    def test_bind_method_property(self) -> None:
        """Test that the bind_method property correctly gets and sets the binding method."""
        test_function_object = self.create_test_method_object()

        # Verify the initial bind_method
        assert test_function_object.bind_method == "bind_builtin"

        # Set the bind_method property to bind_wrapped
        test_function_object.bind_method = "bind_wrapped"

        # Verify the property was set correctly
        assert test_function_object.bind_method == "bind_wrapped"
        assert test_function_object.bind_multiplexer.selected == "bind_wrapped"

        # Set it back to the default
        test_function_object.bind_method = "bind_builtin"

        # Verify it was set back correctly
        assert test_function_object.bind_method == "bind_builtin"
        assert test_function_object.bind_multiplexer.selected == "bind_builtin"

    # Fixtures
    @pytest.fixture
    def test_function_object(self) -> DynamicDecorator:
        """Create a test function object that wraps a function.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a function.
        """
        return self.UnitTestClass(add_function)

    @pytest.fixture
    def test_coroutine_object(self) -> DynamicDecorator:
        """Create a test function object that wraps a coroutine function.

        Returns:
            DynamicDecorator: An instance of DynamicDecorator that wraps a coroutine function.
        """
        return self.UnitTestClass(add_coroutine)

    # Tests
    def test_init_false(self) -> None:
        """Test initialization with init=False."""
        obj = self.UnitTestClass(init=False, _return_partial=False)
        obj.construct()
        assert obj.__func__ is None

    def test_init_false_pickling(self) -> None:
        """Test pickling of an object initialized with init=False."""
        obj = self.UnitTestClass(init=False, _return_partial=False)
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.__wrapped__ is None

    @pytest.mark.parametrize(
        ("method_name", "expected"),
        [
            ("create_function_object", False),
            ("create_coroutine_object", True),
        ],
    )
    def test_is_coroutine(self, method_name: str, expected: bool) -> None:  # type: ignore[override]
        """Test the is_coroutine property."""
        obj = getattr(self, method_name)()
        assert obj.is_coroutine is expected

    def test_is_coroutine_marker_none(self) -> None:
        """Test marker is None check."""
        obj_none = self.UnitTestClass(_return_partial=False)
        assert obj_none._is_coroutine_marker is None

    @pytest.mark.parametrize("func", [add_function, add_coroutine])
    def test_instance_creation(self, func: Any) -> None:
        """Test that instances of the class can be created with different callables.

        Args:
            func: The function or coroutine to wrap.
        """
        # Create an instance
        instance = self.UnitTestClass(func)

        # Verify it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verify it has the correct function
        assert instance.__func__ is func

    @pytest.mark.parametrize("call_method", ["__call__", "call_wrapped", "as_function"])
    def test_call(self, test_function_object: DynamicDecorator, call_method: str) -> None:  # type: ignore[override]
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a DynamicDecorator instance that wraps a function.
            call_method: The name of the method to use for calling.
        """
        # Get the callable
        caller: Any
        if call_method == "__call__":
            caller = test_function_object
        elif call_method == "call_wrapped":
            caller = getattr(test_function_object, call_method)
        elif call_method == "as_function":
            caller = test_function_object.as_function()
            assert callable(caller)

        # Call the function
        result = caller(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        result = caller(3, 4)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    @pytest.mark.parametrize("call_method", ["__call__", "as_function"])
    def test_coroutine(self, test_coroutine_object: DynamicDecorator, call_method: str) -> None:  # type: ignore[override]
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a DynamicDecorator instance that wraps a coroutine function.
            call_method: The method to use for calling ('__call__' or 'as_function').
        """
        func: Any
        if call_method == "__call__":
            func = test_coroutine_object
        else:
            func = test_coroutine_object.as_function()
            assert callable(func)

        # Call the coroutine function and run it in an event loop
        coro = func(3)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

        # Call with different arguments
        coro = func(3, 4)
        result = asyncio.run(coro)

        # Verify it returns the expected result
        assert result == 7  # 3 + 4

    @pytest.mark.parametrize(
        ("kwargs", "expected_attrs"),
        [
            ({}, {}),
            (
                {"bind_method": "bind_wrapped", "call_method": "call_wrapped"},
                {"bind_method": "bind_wrapped", "call_method": "call_wrapped"},
            ),
        ],
    )
    def test_decorator_init_variants(self, kwargs: dict[str, Any], expected_attrs: dict[str, Any]) -> None:
        """Test initializing the decorator with various arguments (returning a partial)."""
        # Create a decorator (partial)
        decorator = self.UnitTestClass(**kwargs)

        # Verify it's a partial function
        # Standard Libraries #
        from functools import partial

        assert isinstance(decorator, partial)

        # Apply decorator
        @decorator
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        assert isinstance(test_func, self.UnitTestClass)
        for k, v in expected_attrs.items():
            assert getattr(test_func, k) == v

        result = test_func(3)
        assert result == 5  # 3 + 2 (default y)

    def test_bind_multiplexer(
        self,
        test_method_object: Any = None,
        test_bind_target: Any = None,
    ) -> None:
        """Test that the bind_multiplexer correctly delegates to the selected binding method."""
        # Create a test function object
        test_function_object = self.UnitTestClass(add_function)

        # Test with default bind_method
        assert test_function_object.bind_method == "bind_builtin"

        # Change the bind_method to bind_builtin
        test_function_object.bind_method = "bind_builtin"
        assert test_function_object.bind_method == "bind_builtin"

        # Add a custom bind method to the bind_multiplexer
        def custom_bind(self: Any, instance: Any, owner: Any) -> Any:
            # Just return the function itself
            return self.__func__

        test_function_object.bind_multiplexer.add_function("custom_bind", custom_bind)

        # Change the bind_method to custom_bind
        test_function_object.bind_method = "custom_bind"
        assert test_function_object.bind_method == "custom_bind"

        # Test with custom_bind
        bound_func = test_function_object.__get__(None, None)
        assert bound_func is add_function

    def test_call_multiplexer(self, test_function_object: Any = None) -> None:
        """Test that the call_multiplexer correctly delegates to the selected call method."""
        # Create a test function object
        test_function_object = self.UnitTestClass(add_function)

        # Test with default call_method
        assert test_function_object.call_method == "call_wrapped"

        # Add a custom call method to the call_multiplexer
        def custom_call(self: Any, *args: Any, **kwargs: Any) -> int:
            # Multiply the result by 2
            return cast(int, self.call_wrapped(*args, **kwargs) * 2)

        test_function_object.call_multiplexer.add_function("custom_call", custom_call)

        # Change the call_method to custom_call
        test_function_object.call_method = "custom_call"
        assert test_function_object.call_method == "custom_call"

        # Test with custom_call
        result = test_function_object(3)
        assert result == 10  # (3 + 2) * 2

    def test_change_function(self) -> None:  # type: ignore[override]
        """Test the edge case where the function is changed after creation."""
        # Create an instance with a function
        instance = self.UnitTestClass(add_function)

        # Verify it has the correct function
        assert instance.__func__ is add_function

        # Call the function
        result = instance(3)
        assert result == 5  # 3 + 2 (default y)

        # Change the function
        instance.__func__ = multiply_function

        # Verify it has the new function
        assert instance.__func__ is multiply_function

        # Call the new function
        result = instance(3)
        assert result == 9  # 3 * 3 (default y)

    def test_decorator_chaining(self) -> None:
        """Test that decorators can be chained."""
        # Define two decorators
        decorator1 = self.UnitTestClass()
        decorator2 = self.UnitTestClass()

        # Use the decorators to decorate a function
        @decorator1
        @decorator2
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        # Verify the decorated function is an instance of the decorator class
        assert isinstance(test_func, self.UnitTestClass)

        # Call the decorated function
        result = test_func(3)

        # Verify it returns the expected result
        assert result == 5  # 3 + 2 (default y)

    def test_no_function(self) -> None:
        """Tests the edge case where no function is provided."""
        # Standard Libraries #
        from functools import partial

        # Create an instance without a function
        instance = self.UnitTestClass()

        # Verify it's a partial
        assert isinstance(instance, partial)

    def test_decorator_usage(self) -> None:
        """Tests using the decorator in the standard Python way."""
        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def decorated_function(x: int, y: int = 2) -> int:
            return x + y

        assert isinstance(decorated_function, self.UnitTestClass)
        assert decorated_function(3) == 5

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests using the decorator with arguments."""
        # DynamicDecorator returns a partial when initialized with args but no function
        @self.UnitTestClass(call_method="call_wrapped")
        def decorated_function(x: int, y: int = 2) -> int:
            return x + y

        assert isinstance(decorated_function, self.UnitTestClass)
        assert decorated_function.call_method == "call_wrapped"
        assert decorated_function(3) == 5


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
