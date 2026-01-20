"""singlekwargdispatch_test.py
Tests for the singlekwargdispatch class.
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
from unittest.mock import patch

# Third-Party Packages #
# Imports #
import pytest

# Source Packages #
from baseobjects.functions import singlekwargdispatch


# Classes #
class DispatchUnitTestClass:
    """A class for testing singlekwargdispatch."""
    def __init__(self) -> None:
        """Initializes the test class."""
        self.value = 0

    @singlekwargdispatch(kwarg="arg")
    def dispatch_method(self, arg: Any, **kwargs: Any) -> str:
        """The default dispatch method.

        Returns:
            str: The result.
        """
        return f"default: {arg}"

    @dispatch_method.register(int)  # type: ignore[untyped-decorator]
    def _(self, arg: int, **kwargs: Any) -> str:
        """Int dispatch.

        Returns:
            str: The result.
        """
        return f"int: {arg}"

    @dispatch_method.register(str)  # type: ignore[untyped-decorator]
    def _(self, arg: str, **kwargs: Any) -> str:
        """Str dispatch.

        Returns:
            str: The result.
        """
        return f"str: {arg}"

    @singlekwargdispatch
    def dispatch_no_kwarg(self, arg: Any, **kwargs: Any) -> str:
        """A dispatch method without a configured kwarg.

        Returns:
            str: The result.
        """
        return f"default: {arg}"

    @dispatch_no_kwarg.register(int)
    def _(self, arg: int, **kwargs: Any) -> str:
        """Int dispatch for no kwarg.

        Returns:
            str: The result.
        """
        return f"int: {arg}"


# Global function for pickling test
def _inner_pickle_func(arg: Any = None) -> str: return "default"


pickle_test_func = singlekwargdispatch(_inner_pickle_func, kwarg="arg")


@pickle_test_func.register(int)
def _(arg: int) -> str: return "int"


class TestSingleKwargDispatch:
    """Test the singlekwargdispatch class."""

    @pytest.fixture
    def test_obj(self) -> DispatchUnitTestClass:
        """Fixture for creating a DispatchUnitTestClass instance.

        Returns:
            DispatchUnitTestClass: The test object.
        """
        return DispatchUnitTestClass()

    def test_dispatch_by_arg(self, test_obj: DispatchUnitTestClass) -> None:
        """Tests dispatching by positional argument."""
        assert test_obj.dispatch_method(1) == "int: 1"
        assert test_obj.dispatch_method("a") == "str: a"
        assert test_obj.dispatch_method(1.0) == "default: 1.0"

    def test_dispatch_by_kwarg(self, test_obj: DispatchUnitTestClass) -> None:
        """Tests dispatching by keyword argument."""
        assert test_obj.dispatch_method(arg=1) == "int: 1"
        assert test_obj.dispatch_method(arg="a") == "str: a"
        # Mixed
        assert test_obj.dispatch_method(1, other="ignored") == "int: 1"

    def test_dispatch_no_kwarg_configured(self, test_obj: DispatchUnitTestClass) -> None:
        """Tests dispatching when no kwarg name is configured."""
        # When no kwarg name is configured, it falls back to first kwarg if no args provided
        assert test_obj.dispatch_no_kwarg(1) == "int: 1"
        assert test_obj.dispatch_no_kwarg(arg=1) == "int: 1"

    def test_register(self, test_obj: DispatchUnitTestClass) -> None:
        """Tests registering a new dispatch type."""
        @DispatchUnitTestClass.dispatch_method.register(float)  # type: ignore[untyped-decorator]
        def _(self: Any, arg: float, **kwargs: Any) -> str:
            return f"float: {arg}"

        assert test_obj.dispatch_method(1.0) == "float: 1.0"

    def test_properties(self) -> None:
        """Tests the properties of the singlekwargdispatch object."""
        d = singlekwargdispatch(lambda x: x)
        assert d.kwarg is None
        d.kwarg = "foo"
        assert d.kwarg == "foo"

    def test_dispatcher_property(self) -> None:
        """Tests the dispatcher property."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        assert func.dispatcher is not None
        assert callable(func.dispatcher)

    def test_standalone_function(self) -> None:
        """Tests usage as a standalone function decorator."""
        @singlekwargdispatch
        def func(arg: Any) -> str:
            return "default"

        @func.register(int)
        def _(arg: int) -> str:
            return "int"

        assert func(1) == "int"
        assert func("s") == "default"

    def test_register_type_hint(self) -> None:
        """Tests registering using type hints."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        @func.register
        def _(arg: int) -> str:
            return "int"

        assert func(1) == "int"

    def test_register_union(self) -> None:
        """Tests registering a Union type."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        @func.register(int | float)
        def _(arg: Any) -> str:
            return "number"

        assert func(1) == "number"
        assert func(1.0) == "number"
        assert func("s") == "default"

    def test_register_errors(self) -> None:
        """Tests error conditions during registration."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        # Test invalid type with method argument
        with pytest.raises(TypeError, match="Invalid first argument"):
            func.register("not a class", lambda x: x)  # type: ignore

        # Test invalid annotation (using an instance instead of class)
        # We use an object that is valid in python syntax but fails _is_valid_dispatch_type
        class NotAClass:
            pass

        obj = NotAClass()

        # We need to ensure get_type_hints returns 'obj'.
        # Since 'obj' is a local variable, string annotation might fail if not careful,
        # but passing the object directly as annotation works in recent python.

        with pytest.raises(TypeError, match="Invalid annotation"):
            @func.register
            def _(arg: obj) -> None: ...  # type: ignore

    def test_no_args_dispatch_kwarg(self) -> None:
        """Tests dispatching when no arguments are provided."""
        @singlekwargdispatch(kwarg="arg")
        def func(arg: Any = None) -> str: return "default"

        @func.register(type(None))  # type: ignore[untyped-decorator]
        def _(arg: Any = None) -> str: return "none"

        assert func() == "none"

    def test_parse_kwarg_fallback(self) -> None:
        """Tests fallback logic for parsing kwargs."""
        d = singlekwargdispatch(lambda *a, **k: "default")
        d.set_kwarg("myarg")

        # parse_kwarg logic: missing kwarg -> missing arg -> return _default_parse (NoneType)
        assert d() == "default"

        @d.register(type(None))
        def _(*a: Any, **k: Any) -> str: return "handled"

        assert d() == "handled"

    def test_classmethod_dispatch(self) -> None:
        """Tests dispatching on a class method."""
        class MyClass:
            @singlekwargdispatch
            @classmethod
            def method(cls, arg: Any) -> str:
                """Method docstring.

                Returns:
                    str: The result.
                """
                return f"default {cls.__name__}"

            @method.register(int)
            @classmethod
            def _(cls, arg: int) -> str:
                """Int method.

                Returns:
                    str: The result.
                """
                return f"int {cls.__name__}"

        assert MyClass.method("s") == "default MyClass"
        assert MyClass.method(1) == "int MyClass"

    def test_register_union_error(self) -> None:
        """Tests error when registering an invalid Union type."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        with pytest.raises(TypeError, match="not all arguments are classes"):
            @func.register
            def _(arg: int | list[int]) -> None: ...

    def test_pickling(self) -> None:
        """Tests pickling of component."""
        # Standard Libraries #
        import pickle

        # Use global pickle_test_func
        # Pickle and unpickle
        dump = pickle.dumps(pickle_test_func)
        loaded = pickle.loads(dump)

        assert loaded(1) == "int"
        assert loaded() == "default"
        # Check if dispatch_cache was restored/cleared (it's weakref dict so it might be empty)
        # Just check it exists
        assert hasattr(loaded, "dispatch_cache")

    def test_construct_without_func(self) -> None:
        """Tests construction without a wrapped function."""
        d = singlekwargdispatch(init=False, _return_partial=False)
        d.construct()  # func is None
        assert not hasattr(d, "func")

        # Construct with func
        d.construct(lambda x: x)
        assert d.func is not None

    def test_register_empty_annotations(self) -> None:
        """Tests error when registering a function with no annotations."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        def no_anno(arg):  # type: ignore[no-untyped-def]  # noqa: ANN001, ANN202
            pass

        with pytest.raises(TypeError, match="Invalid first argument"):
            func.register(no_anno)

    def test_abstract_method_dispatch(self) -> None:
        """Tests dispatching on abstract base classes."""
        # Standard Libraries #
        from abc import ABC, abstractmethod

        class Abstract(ABC):
            @abstractmethod
            def foo(self) -> str:
                """Abstract foo."""

        class Concrete(Abstract):
            def foo(self) -> str:
                """Concrete foo.

                Returns:
                    str: The result.
                """
                return "concrete"

        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        @func.register(Abstract)
        def _(arg: Any) -> str: return "abstract"

        # This should trigger cache_token logic if Abstract has __abstractmethods__
        assert func(Concrete()) == "abstract"

        # To trigger cache invalidation, define another subclass?
        class Concrete2(Abstract):
            def foo(self) -> str:
                """Concrete2 foo.

                Returns:
                    str: The result.
                """
                return "concrete2"

        # Call again to see if it works
        assert func(Concrete2()) == "abstract"

    def test_pickling_no_func(self) -> None:
        """Tests pickling without a wrapped function."""
        # Standard Libraries #
        import pickle
        d = singlekwargdispatch(init=False, _return_partial=False)
        dump = pickle.dumps(d)
        loaded = pickle.loads(dump)
        assert not hasattr(loaded, "func")

    def test_cache_invalidation(self) -> None:
        """Tests cache invalidation logic."""
        # Standard Libraries #
        from unittest.mock import patch

        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        # Manually set a cache token to simulate it being set
        token1 = object()
        func.cache_token = token1

        # Populate cache
        func.dispatch_cache[int] = lambda x: x
        assert int in func.dispatch_cache

        # Patch get_cache_token to return something else
        token2 = object()
        with patch("baseobjects.functions.singlekwargdispatch.get_cache_token", return_value=token2):
            # Dispatch something
            func.dispatch(str)

        # Cache should have been cleared (int removed)
        assert int not in func.dispatch_cache
        # And str added
        assert str in func.dispatch_cache
        assert func.cache_token is token2

    def test_missing_args_error(self) -> None:
        """Tests error when required arguments are missing."""
        @singlekwargdispatch
        def func(arg: Any) -> str: return "default"

        # Calling without args/kwargs should raise TypeError in parse_first
        with pytest.raises(TypeError, match="No args or kwargs"):
            func()

    def test_register_with_kwarg_annotation(self) -> None:
        """Tests registering with keyword argument annotation."""
        @singlekwargdispatch(kwarg="myarg")
        def func(myarg: Any = None) -> str: return "default"

        @func.register  # type: ignore[untyped-decorator]
        def _(myarg: int) -> str: return "int"

        assert func(myarg=1) == "int"

    def test_construct_classmethod_kwarg(self) -> None:
        """Tests construction with a classmethod and kwarg."""
        class TestClass:
            @singlekwargdispatch(kwarg="x")
            @classmethod
            def method(cls, x: int = 0) -> str:
                return "default"

        assert TestClass.method(x=1) == "default"

    def test_getstate_no_dict(self) -> None:
        """Test getstate when super().__getstate__ returns None or tuple without dict."""
        obj = singlekwargdispatch(lambda x: x)

        with patch("baseobjects.functions.basedecorator.BaseDecorator.__getstate__", return_value=None):
            state = obj.__getstate__()
            assert state is None

        with patch("baseobjects.functions.basedecorator.BaseDecorator.__getstate__", return_value=(None, {})):
            state = obj.__getstate__()
            assert state == (None, {})


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
