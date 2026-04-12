"""singlekwargdispatchtestsuite.py
Base test suite for singlekwargdispatch and its subclasses.

This module contains the base test suite for singlekwargdispatch and its subclasses.
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
import pickle
from typing import Any, Literal

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import singlekwargdispatch
from .basedecoratortestsuite import BaseDecoratorTestSuite


# Classes #
class SingleKwargDispatchTestSuite(BaseDecoratorTestSuite):
    """Base test suite for singlekwargdispatch.

    This class provides common test functionality for singlekwargdispatch.
    """

    UnitTestClass: type[singlekwargdispatch] = singlekwargdispatch

    # Tests #
    # Magic Methods #
    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((1,), 3),
            ((1, 3), 4),
        ],
    )
    def test_call(self, test_function_object: Any, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object can be called and correctly delegates to the wrapped function."""
        # example_function(x, y=2) -> x + y
        assert test_function_object(*args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((1,), 3),
            ((1, 3), 4),
        ],
    )
    def test_call_wrapped(self, test_function_object: Any, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the wrapped function can be called directly."""
        assert test_function_object.call_wrapped(*args) == expected

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created."""
        instance = self.create_function_object()
        assert isinstance(instance, self.UnitTestClass)

    # Pickling #
    def test_init_false_pickling(self) -> None:
        """Tests pickling of an object initialized with init=False."""
        obj = self.UnitTestClass(init=False, _return_partial=False)
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.__wrapped__ is None

    # Functionality #
    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((1,), 3),
            ((1, 3), 4),
        ],
    )
    def test_as_function(self, test_function_object: Any, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object can be converted to a standard Python function."""
        func = test_function_object.as_function()
        assert callable(func)
        assert func(*args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((1,), 3),
            ((1, 3), 4),
        ],
    )
    def test_coroutine(self, test_coroutine_object: Any, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object correctly handles coroutine functions."""
        # example_coroutine(x, y=2) -> x + y (async)
        # Standard Libraries #
        import asyncio

        loop = asyncio.new_event_loop()
        try:
            assert loop.run_until_complete(test_coroutine_object(*args)) == expected
        finally:
            loop.close()

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((1,), 3),
            ((1, 3), 4),
        ],
    )
    def test_as_function_coroutine(self, test_coroutine_object: Any, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object wrapping a coroutine can be converted to a coroutine function."""
        # Standard Libraries #
        import asyncio
        import inspect

        func = test_coroutine_object.as_function()
        assert inspect.iscoroutinefunction(func)
        loop = asyncio.new_event_loop()
        try:
            assert loop.run_until_complete(func(*args)) == expected
        finally:
            loop.close()

    def test_decorator_usage(self) -> None:
        """Tests using the decorator in the standard Python way."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(x: int) -> int:
            return x + 1

        assert isinstance(test_func, self.UnitTestClass)
        assert test_func(1) == 2

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests using the decorator with arguments."""

        # singlekwargdispatch accepts arguments like kwarg="name"
        @self.UnitTestClass(kwarg="x")
        def test_func(x: int = 0) -> int:
            return x + 1

        assert isinstance(test_func, self.UnitTestClass)
        assert test_func(x=1) == 2

    def test_new_with_bound_method(self) -> None:
        """Tests creating a BaseCallable from a bound method."""

        class MyClass:
            def method(self, arg: Any) -> Any:
                return f"bound: {arg}"

        inst = MyClass()
        bound = inst.method
        obj = self.UnitTestClass(bound)
        assert obj("test") == "bound: test"

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False, _return_partial=False)
        obj.construct()
        assert isinstance(obj, self.UnitTestClass)

    def test_is_coroutine(self) -> None:
        """Tests the is_coroutine property."""
        # Test with standard function
        obj = self.create_function_object()
        assert not obj.is_coroutine

        # Test with coroutine function
        coro_obj = self.create_coroutine_object()
        assert coro_obj.is_coroutine

        # Test marker is None check
        obj_none = self.UnitTestClass(_return_partial=False)
        assert obj_none._is_coroutine_marker is None

    def test_dispatch_no_args_error(self) -> None:
        """Tests that calling a dispatched function with no arguments raises TypeError."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> None:
            pass

        with pytest.raises(TypeError, match="No args or kwargs given to dispatch"):
            test_func()

    @pytest.mark.parametrize(
        ("registrar", "match"),
        [
            (lambda f: f.register(123), "Invalid first argument"),
            (lambda f: f.register("not a type", lambda x: x), "Invalid first argument to"),
        ],
    )
    def test_register_invalid_usage(self, registrar: Any, match: str) -> None:
        """Tests invalid usage of register method."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> None:
            pass

        with pytest.raises(TypeError, match=match):
            registrar(test_func)

    @pytest.mark.parametrize(
        ("annotation", "match"),
        [
            (None, "Invalid first argument"),
            (123, "Invalid annotation"),
            (int | Literal[1], "not all arguments are classes"),
        ],
    )
    def test_register_annotation_errors(self, annotation: Any, match: str) -> None:
        """Tests registering functions with invalid or missing annotations."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> None:
            pass

        def _(arg: Any) -> None:
            pass

        if annotation is not None:
            _.__annotations__["arg"] = annotation

        with pytest.raises(TypeError, match=match):
            test_func.register(_)

    def test_classmethod_dispatch(self) -> None:
        """Tests dispatching on a class method."""

        class MyClass:
            @self.UnitTestClass  # type: ignore[untyped-decorator]
            @classmethod
            def dispatch(cls, arg: Any) -> str:
                return "base"

            @dispatch.register(int)
            @classmethod
            def _(cls, arg: int) -> str:
                return "int"

        assert MyClass.dispatch("s") == "base"
        assert MyClass.dispatch(1) == "int"

    def test_function_kwarg_dispatch(self) -> None:
        """Tests kwarg dispatch on a standalone function."""

        @self.UnitTestClass(kwarg="x")
        def test_func(x: Any = 0) -> str:
            return f"base: {x}"

        @test_func.register(str)  # type: ignore[untyped-decorator]
        def _(x: str) -> str:
            return f"str: {x}"

        assert test_func(x="a") == "str: a"
        assert test_func("a") == "str: a"
        assert test_func() == "base: 0"

    def test_register_decorator_no_args(self) -> None:
        """Tests using @register without arguments."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> str:
            return "base"

        @test_func.register
        def _(arg: int) -> str:
            return "int"

        assert test_func(1) == "int"

    def test_register_union(self) -> None:
        """Tests registering a Union of types."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> str:
            return "base"

        @test_func.register(int | float)
        def _(arg: Any) -> str:
            return "number"

        assert test_func(1) == "number"
        assert test_func(1.0) == "number"
        assert test_func("s") == "base"

    def test_dispatch_cache_invalidation(self) -> None:
        """Tests that the dispatch cache is invalidated when cache token changes."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(arg: Any) -> str:
            return "base"

        test_func(1)
        assert int in test_func.dispatch_cache

        # Manually change token to simulate invalidation
        test_func.cache_token = "OLD_TOKEN"  # noqa: S105

        # Trigger dispatch again
        test_func(1)
