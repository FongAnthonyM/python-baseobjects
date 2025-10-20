"""singlekwargdispatch_test.py
Tests for the singlekwargdispatch decorator in the baseobjects package.

This module provides tests for the singlekwargdispatch decorator, which extends singledispatch
to allow keyword arguments to be used for dispatching.
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
import copy
import pickle
from functools import partial
from typing import Any, Type, Union
from collections.abc import Callable

# Third-Party Packages #
import pytest

# Source Packages #
from src.baseobjects.functions import BaseDecorator, singlekwargdispatch
from src.baseobjects.testsuite import BaseDecoratorTestSuite, example_coroutine, example_function


# Definitions #
# Functions #
@singlekwargdispatch
def dispatching_function(x: int | str, y: int = 2) -> Any:
    return f"Default: {x}, {y}"


@dispatching_function.register
def _(x: int, y: int = 2) -> Any:
    return f"Integer: {x}, {y}"


@dispatching_function.register(str)
def _(x: str, y: int = 2) -> Any:
    return f"String: {x}, {y}"


@singlekwargdispatch(kwarg="x")
def dispatch_kwarg_function(x: int | str | None = None, y: int = 2) -> Any:
    return f"Default: {x}, {y}"


@dispatch_kwarg_function.register
def _(x: int = 0, y: int = 2) -> Any:
    return f"Integer: {x}, {y}"


@dispatch_kwarg_function.register(str)
def _(x: str = "", y: int = 2) -> Any:
    return f"String: {x}, {y}"


@singlekwargdispatch
async def dispatch_coroutine(x: int | str, y: int = 2) -> Any:
    return f"Default: {x}, {y}"


@dispatch_coroutine.register
async def _(x: int, y: int = 2) -> Any:
    await asyncio.sleep(0.001)  # Simulate some async work
    return f"Integer: {x}, {y}"


@dispatch_coroutine.register(str)
async def _(x: str, y: int = 2) -> Any:
    await asyncio.sleep(0.001)  # Simulate some async work
    return f"String: {x}, {y}"


# Classes #
class DispatchTestClass:
    """A class with methods for testing singlekwargdispatch."""

    @singlekwargdispatch
    def dispatch_arg(self, arg: int | str, **kwargs) -> str:
        """Default implementation."""
        return f"Default: {arg}"

    @dispatch_arg.register
    def _(self, arg: int, **kwargs) -> str:
        """Process an integer."""
        return f"Integer: {arg}"

    @dispatch_arg.register(str)
    def _(self, arg: str, **kwargs) -> str:
        """Process a string."""
        return f"String: {arg}"

    @singlekwargdispatch(kwarg="kwarg")
    def dispatch_kwarg(self, arg: Any = None, kwarg: int | str | None = None, **kwargs) -> str:
        """Default implementation with specific kwarg."""
        return f"Default: {kwarg}"

    @dispatch_kwarg.register
    def _(self, arg: Any = None, kwarg: int = 0, **kwargs) -> str:
        """Process an integer value."""
        return f"Integer: {kwarg}"

    @dispatch_kwarg.register(str)
    def _(self, arg: Any = None, kwarg: str = "", **kwargs) -> str:
        """Process a string value."""
        return f"String: {kwarg}"

    @singlekwargdispatch
    async def dispatch_coroutine(self, arg: int | str, **kwargs) -> str:
        """Default implementation for coroutine."""
        return f"Default: {arg}"

    @dispatch_coroutine.register
    async def _(self, arg: int, **kwargs) -> str:
        """Process an integer in coroutine."""
        await asyncio.sleep(0.001)  # Simulate some async work
        return f"Integer: {arg}"

    @dispatch_coroutine.register(str)
    async def _(self, arg: str, **kwargs) -> str:
        """Process a string in coroutine."""
        await asyncio.sleep(0.001)  # Simulate some async work
        return f"String: {arg}"


# Tests #
class TestSingleKwargDispatch(BaseDecoratorTestSuite):
    """Test the singlekwargdispatch decorator.

    This class tests the functionality of the singlekwargdispatch decorator, which extends singledispatch
    to allow keyword arguments to be used for dispatching.

    Attributes:
        TestClass: The class that the test suite is testing, which is singlekwargdispatch.
    """

    # Attributes #
    DispatchTestClass = DispatchTestClass

    @property
    def TestClass(self):
        """Get the decorator class being tested.

        Returns:
            The decorator class being tested.
        """
        return singlekwargdispatch

    # Instance Methods #
    def create_function_object(self, *args: Any, **kwargs: Any) -> singlekwargdispatch:
        """Create a test function decorated with singlekwargdispatch.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            A function decorated with singlekwargdispatch.
        """
        return dispatching_function

    def create_coroutine_object(self, *args: Any, **kwargs: Any) -> singlekwargdispatch:
        """Create a test coroutine decorated with singlekwargdispatch.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.

        Returns:
            A coroutine decorated with singlekwargdispatch.
        """
        return dispatch_coroutine

    # Fixtures
    @pytest.fixture
    def test_dispatch_object(self) -> DispatchTestClass:
        """Create a test object with dispatched methods.

        Returns:
            An instance of DispatchTestClass.
        """
        return self.DispatchTestClass()

    @pytest.fixture
    def test_kwarg_decorated_function(self) -> Callable:
        """Create a test function decorated with singlekwargdispatch with kwarg parameter.

        Returns:
            A function decorated with singlekwargdispatch with kwarg parameter.
        """
        return dispatch_kwarg_function

    # Tests
    def test_instance_creation(self) -> None:
        """Test that instances of the decorator class can be created."""
        # Create with no parameters
        decorator1 = singlekwargdispatch()
        assert decorator1 is not None
        assert isinstance(decorator1, partial)

        # Create with function parameter
        def test_func(x: Any) -> Any:
            return x

        decorator2 = singlekwargdispatch(test_func)
        assert decorator2 is not None
        assert isinstance(decorator2, singlekwargdispatch)
        assert decorator2.__wrapped__ == test_func

        # Create with kwarg parameter
        decorator3 = singlekwargdispatch(kwarg="x")
        assert decorator3 is not None
        assert isinstance(decorator3, partial)

        # Create with both function and kwarg parameters
        decorator4 = singlekwargdispatch(test_func, kwarg="x")
        assert decorator4 is not None
        assert isinstance(decorator4, singlekwargdispatch)
        assert decorator4.__wrapped__ == test_func
        assert decorator4.kwarg == "x"

    @pytest.mark.skip(
        reason="Python pickling struggles with the masked referencing of decorators. The dill package might work.",
    )
    def test_pickling(self, test_object: singlekwargdispatch) -> None:
        """Test pickling and unpickling of a singlekwargdispatch object.

        Args:
            test_object: A fixture providing a singlekwargdispatch instance.
        """

    def test_call(self, test_function_object: singlekwargdispatch) -> None:
        """Test that the callable object can be called and correctly delegates to the wrapped function.

        Args:
            test_function_object: A fixture providing a singlekwargdispatch instance that wraps a function.
        """
        # Test with integer
        result = test_function_object(5)
        assert result == "Integer: 5, 2"

        # Test with string
        result = test_function_object("test")
        assert result == "String: test, 2"

        # Test with float (default case)
        result = test_function_object(5.5)
        assert result == "Default: 5.5, 2"

    def test_as_function(self, test_function_object: singlekwargdispatch) -> None:
        """Test that the callable object can be converted to a standard Python function.

        Args:
            test_function_object: A fixture providing a singlekwargdispatch instance that wraps a function.
        """
        # Get the function
        func = test_function_object.as_function()

        # Test that it's callable
        assert callable(func)

        # Test that it works correctly
        assert func(5) == "Integer: 5, 2"
        assert func("test") == "String: test, 2"
        assert func(5.5) == "Default: 5.5, 2"

    def test_call_wrapped(self, test_function_object: singlekwargdispatch) -> None:
        """Test that the wrapped function can be called directly.

        Args:
            test_function_object: A fixture providing a singlekwargdispatch instance that wraps a function.
        """
        # Call the wrapped function directly
        result = test_function_object.call_wrapped(5)
        assert result == "Default: 5, 2"

        result = test_function_object.call_wrapped("test")
        assert result == "Default: test, 2"

    def test_coroutine(self, test_coroutine_object: singlekwargdispatch) -> None:
        """Test that the callable object correctly handles coroutine functions.

        Args:
            test_coroutine_object: A fixture providing a singlekwargdispatch instance that wraps a coroutine function.
        """
        # Test with integer
        result = asyncio.run(test_coroutine_object(5))
        assert result == "Integer: 5, 2"

        # Test with string
        result = asyncio.run(test_coroutine_object("test"))
        assert result == "String: test, 2"

        # Test with float (default case)
        result = asyncio.run(test_coroutine_object(5.5))
        assert result == "Default: 5.5, 2"

    def test_as_function_coroutine(self, test_coroutine_object: singlekwargdispatch) -> None:
        """Test that the callable object wrapping a coroutine can be converted to a coroutine function.

        Args:
            test_coroutine_object: A fixture providing a singlekwargdispatch instance that wraps a coroutine function.
        """
        # Get the function
        func = test_coroutine_object.as_function()

        # Test that it's callable
        assert callable(func)

        # Test that it works correctly
        assert asyncio.run(func(5)) == "Integer: 5, 2"
        assert asyncio.run(func("test")) == "String: test, 2"
        assert asyncio.run(func(5.5)) == "Default: 5.5, 2"

    def test_decorator_usage(self) -> None:
        """Test using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """

        # Test basic usage
        @singlekwargdispatch
        def test_func(x: Any) -> Any:
            return f"Default: {x}"

        assert test_func is not None
        assert hasattr(test_func, "registry")

        # Test with kwarg parameter
        @singlekwargdispatch(kwarg="x")
        def test_func2(x: Any = None) -> Any:
            return f"Default: {x}"

        assert test_func2 is not None
        assert hasattr(test_func2, "registry")
        assert test_func2.kwarg == "x"

        # Test with register
        @singlekwargdispatch
        def multi_func(x: int | str) -> str:
            return f"Default: {x}"

        @multi_func.register
        def _(x: int) -> str:
            return f"Integer: {x}"

        @multi_func.register(str)
        def _(x: str) -> str:
            return f"String: {x}"

        assert multi_func(5) == "Integer: 5"
        assert multi_func("test") == "String: test"
        assert multi_func(5.5) == "Default: 5.5"

    def test_decorator_with_args(self) -> None:
        """Test using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.
        """

        # Define a test function
        def test_function(x: Any) -> Any:
            return x

        # Test with kwarg parameter
        decorator = singlekwargdispatch(kwarg="x")
        assert decorator is not None
        assert isinstance(decorator, partial)

        # Apply the decorator to a function
        decorated_func = decorator(test_function)
        assert decorated_func is not None
        assert isinstance(decorated_func, singlekwargdispatch)
        assert decorated_func.kwarg == "x"

        # Test with both function and kwarg parameters
        decorator = singlekwargdispatch(test_function, kwarg="x")
        assert decorator is not None
        assert isinstance(decorator, singlekwargdispatch)
        assert decorator.kwarg == "x"

    def test_kwarg_property(self) -> None:
        """Test the kwarg property.

        This test verifies that the kwarg property correctly gets and sets the kwarg name.
        """

        # Define a test function with a parameter that matches the kwarg
        def test_function(test_param: Any = None) -> Any:
            return test_param

        # Create a decorator with the kwarg parameter
        decorator = singlekwargdispatch(test_function, kwarg="test_param")
        assert decorator.kwarg == "test_param"

        # Change the kwarg
        decorator.kwarg = "new_param"
        assert decorator.kwarg == "new_param"

        # Set to None
        decorator.kwarg = None
        assert decorator.kwarg is None

    def test_set_kwarg_method(self) -> None:
        """Test the set_kwarg method.

        This test verifies that the set_kwarg method correctly sets the kwarg name.
        """

        # Create a decorator instance with a function to avoid getting a partial
        @singlekwargdispatch
        def func(x: Any) -> Any:
            return x

        assert func.kwarg is None

        # Set kwarg
        func.set_kwarg("test_param")
        assert func.kwarg == "test_param"

        # Set to None
        func.set_kwarg(None)
        assert func.kwarg is None

    def test_parse_first_method(self) -> None:
        """Test the parse_first method.

        This test verifies that the parse_first method correctly parses args and kwargs to determine the dispatch type.
        """

        # Create a decorator instance with a function to avoid getting a partial
        @singlekwargdispatch
        def func(x: Any) -> Any:
            return x

        # Test with actual function calls
        assert func(5) == 5  # Should use the default implementation

        @func.register
        def _(x: int) -> Any:
            return f"Integer: {x}"

        assert func(5) == "Integer: 5"  # Should use the int implementation

        @func.register(str)
        def _(x: str) -> Any:
            return f"String: {x}"

        assert func("test") == "String: test"  # Should use the str implementation

        # Test with no args (should raise TypeError)
        with pytest.raises(TypeError):
            func()

    def test_parse_kwarg_method(self) -> None:
        """Test the parse_kwarg method.

        This test verifies that the parse_kwarg method correctly parses args and kwargs to determine the dispatch type.
        """

        # Create a decorator instance with a function and kwarg to avoid getting a partial
        @singlekwargdispatch(kwarg="x")
        def func(x: Any = None) -> Any:
            return f"Default: {x}"

        # Test with default implementation
        assert func() == "Default: None"

        # Register implementations for different types
        @func.register
        def _(x: int = 0) -> Any:
            return f"Integer: {x}"

        @func.register(str)
        def _(x: str = "") -> Any:
            return f"String: {x}"

        # Test with kwarg
        assert func(x=5) == "Integer: 5"
        assert func(x="test") == "String: test"

        # Test with positional arg
        assert func(5) == "Integer: 5"
        assert func("test") == "String: test"

        # Test with missing kwarg and arg (should use default)
        assert func() == "Default: None"

    def test_register_method(self) -> None:
        """Test the register method.

        This test verifies that the register method correctly registers functions for specific types.
        """

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Register with decorator
        @func.register
        def _(x: int) -> Any:
            return f"Integer: {x}"

        # Register with explicit type
        @func.register(str)
        def _(x: str) -> Any:
            return f"String: {x}"

        # Test dispatch
        assert func(5) == "Integer: 5"
        assert func("test") == "String: test"
        assert func(5.5) == "Default: 5.5"

        # Test registry
        assert int in func.registry
        assert str in func.registry

    def test_dispatch_method(self) -> None:
        """Test the dispatch method.

        This test verifies that the dispatch method correctly returns the function registered for a given class.
        """

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Store the default implementation
        default_impl = func.__wrapped__

        @func.register
        def int_func(x: int) -> Any:
            return f"Integer: {x}"

        @func.register(str)
        def str_func(x: str) -> Any:
            return f"String: {x}"

        # Test that the correct implementations are used
        assert func(5) == "Integer: 5"
        assert func("test") == "String: test"
        assert func(5.5) == "Default: 5.5"

        # Test that the registry contains the correct implementations
        assert int in func.registry
        assert str in func.registry
        assert func.registry[int] == int_func
        assert func.registry[str] == str_func
        assert func.registry[object] == default_impl

    def test_dispatch_call_method(self) -> None:
        """Test the dispatch_call method.

        This test verifies that the dispatch_call method correctly dispatches calls to the appropriate registered function.
        """
        decorator = singlekwargdispatch(example_function)

        @decorator.register
        def _(x: int, y: int = 2) -> Any:
            return f"Integer: {x}, {y}"

        @decorator.register(str)
        def _(x: str, y: int = 2) -> Any:
            return f"String: {x}, {y}"

        # Test dispatch_call
        assert decorator.dispatch_call(5) == "Integer: 5, 2"
        assert decorator.dispatch_call("test") == "String: test, 2"
        assert decorator.dispatch_call(5.5) == 7.5

    def test_method_arg_dispatch(self, test_dispatch_object: DispatchTestClass) -> None:
        """Test dispatching based on positional arguments.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of the first argument.

        Args:
            test_dispatch_object: A fixture providing a DispatchTestClass instance.
        """
        assert test_dispatch_object.dispatch_arg(1) == "Integer: 1"
        assert test_dispatch_object.dispatch_arg("test") == "String: test"
        assert test_dispatch_object.dispatch_arg(1.5) == "Default: 1.5"

    def test_method_kwarg_dispatch(self, test_dispatch_object: DispatchTestClass) -> None:
        """Test dispatching based on a specific keyword argument.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of a specific keyword
        argument when configured with the kwarg parameter.

        Args:
            test_dispatch_object: A fixture providing a DispatchTestClass instance.
        """
        assert test_dispatch_object.dispatch_kwarg(kwarg=1) == "Integer: 1"
        assert test_dispatch_object.dispatch_kwarg(kwarg="test") == "String: test"
        assert test_dispatch_object.dispatch_kwarg(kwarg=1.5) == "Default: 1.5"

        # Test with positional arg for kwarg
        assert test_dispatch_object.dispatch_kwarg("not", kwarg=1) == "Integer: 1"
        assert test_dispatch_object.dispatch_kwarg(-1, kwarg="test") == "String: test"

    def test_method_coroutine_dispatch(self, test_dispatch_object: DispatchTestClass) -> None:
        """Test dispatching with coroutine methods.

        This test verifies that singlekwargdispatch correctly works with coroutine methods.

        Args:
            test_dispatch_object: A fixture providing a DispatchTestClass instance.
        """
        assert asyncio.run(test_dispatch_object.dispatch_coroutine(1)) == "Integer: 1"
        assert asyncio.run(test_dispatch_object.dispatch_coroutine("test")) == "String: test"
        assert asyncio.run(test_dispatch_object.dispatch_coroutine(1.5)) == "Default: 1.5"

    def test_function_arg_dispatch(self, test_function_object: Callable) -> None:
        """Test dispatching based on positional arguments for functions.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of the first argument
        for standalone functions.

        Args:
            test_function_object: A fixture providing a decorated function.
        """
        assert test_function_object(1) == "Integer: 1, 2"
        assert test_function_object("test") == "String: test, 2"
        assert test_function_object(1.5) == "Default: 1.5, 2"

        # Test with custom y value
        assert test_function_object(1, 3) == "Integer: 1, 3"
        assert test_function_object("test", 3) == "String: test, 3"

    def test_function_kwarg_dispatch(self, test_kwarg_decorated_function: Callable) -> None:
        """Test dispatching based on a specific keyword argument for functions.

        This test verifies that singlekwargdispatch correctly dispatches based on the type of a specific keyword
        argument for standalone functions.

        Args:
            test_kwarg_decorated_function: A fixture providing a decorated function with kwarg parameter.
        """
        assert test_kwarg_decorated_function(x=1) == "Integer: 1, 2"
        assert test_kwarg_decorated_function(x="test") == "String: test, 2"
        assert test_kwarg_decorated_function(x=1.5) == "Default: 1.5, 2"

        # Test with custom y value
        assert test_kwarg_decorated_function(x=1, y=3) == "Integer: 1, 3"
        assert test_kwarg_decorated_function(x="test", y=3) == "String: test, 3"

    def test_pickling_objects(self, test_dispatch_object: DispatchTestClass) -> None:
        """Test pickling and unpickling of objects with singlekwargdispatch methods.

        This test verifies that objects with singlekwargdispatch methods can be pickled and unpickled correctly,
        preserving the dispatch functionality.

        Args:
            test_dispatch_object: A fixture providing a DispatchTestClass instance.
        """
        pickle_jar = pickle.dumps(test_dispatch_object)
        unpickled_obj = pickle.loads(pickle_jar)

        assert unpickled_obj is not test_dispatch_object
        assert set(dir(unpickled_obj)) == set(dir(test_dispatch_object))

        # Test dispatch functionality is preserved
        assert unpickled_obj.dispatch_arg(1) == "Integer: 1"
        assert unpickled_obj.dispatch_arg("test") == "String: test"
        assert unpickled_obj.dispatch_kwarg(kwarg=1) == "Integer: 1"
        assert unpickled_obj.dispatch_kwarg(kwarg="test") == "String: test"

    def test_copying_objects(self, test_dispatch_object: DispatchTestClass) -> None:
        """Test copying of objects with singlekwargdispatch methods.

        This test verifies that objects with singlekwargdispatch methods can be copied correctly,
        preserving the dispatch functionality.

        Args:
            test_dispatch_object: A fixture providing a DispatchTestClass instance.
        """
        # Test shallow copy
        shallow_copy = copy.copy(test_dispatch_object)
        assert shallow_copy is not test_dispatch_object

        # Test dispatch functionality is preserved
        assert shallow_copy.dispatch_arg(1) == "Integer: 1"
        assert shallow_copy.dispatch_arg("test") == "String: test"
        assert shallow_copy.dispatch_kwarg(kwarg=1) == "Integer: 1"
        assert shallow_copy.dispatch_kwarg(kwarg="test") == "String: test"

        # Test deep copy
        deep_copy = copy.deepcopy(test_dispatch_object)
        assert deep_copy is not test_dispatch_object

        # Test dispatch functionality is preserved
        assert deep_copy.dispatch_arg(1) == "Integer: 1"
        assert deep_copy.dispatch_arg("test") == "String: test"
        assert deep_copy.dispatch_kwarg(kwarg=1) == "Integer: 1"
        assert deep_copy.dispatch_kwarg(kwarg="test") == "String: test"

    def test_union_type_registration(self) -> None:
        """Test registration with Union types.

        This test verifies that the register method correctly handles Union types.
        """

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Register with Union type
        @func.register
        def _(x: int | str) -> Any:
            return f"Int or Str: {x}"

        # Test dispatch
        assert func(5) == "Int or Str: 5"
        assert func("test") == "Int or Str: test"
        assert func(5.5) == "Default: 5.5"

    def test_none_type_registration(self) -> None:
        """Test registration with None type.

        This test verifies that the register method correctly handles None type.
        """

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Register with None type
        @func.register
        def _(x: None) -> Any:
            return "None"

        # Test dispatch
        assert func(None) == "None"
        assert func(5) == "Default: 5"

    def test_invalid_annotation(self) -> None:
        """Test registration with invalid annotation.

        This test verifies that the register method correctly handles invalid annotations.
        """

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Try to register with non-class annotation
        with pytest.raises(TypeError):
            # Create a non-class object to use as an annotation
            not_a_class = "not a class"
            func.register(not_a_class, lambda x: "Invalid")

    def test_cache_token_update(self) -> None:
        """Test that the cache token is updated when registering abstract classes.

        This test verifies that the cache token is updated when registering classes with __abstractmethods__.
        """
        # Standard Libraries #
        from abc import ABC, abstractmethod

        class AbstractTest(ABC):
            @abstractmethod
            def test(self) -> None:
                pass

        class ConcreteTest(AbstractTest):
            def test(self) -> None:
                pass

        @singlekwargdispatch
        def func(x: Any) -> Any:
            return f"Default: {x}"

        # Register with abstract class
        @func.register
        def _(x: AbstractTest) -> Any:
            return "Abstract"

        # Test that cache token is updated
        assert func.cache_token is not None

        # Test dispatch
        assert func(ConcreteTest()) == "Abstract"


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
