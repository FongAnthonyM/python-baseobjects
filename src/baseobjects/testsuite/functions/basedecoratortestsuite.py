"""basedecoratortestsuite.py
Base class for test suites which test BaseDecorator and its subclasses.

This module provides a base test suite for testing the BaseDecorator class and its subclasses. It defines abstract
methods for testing the core functionality of decorators, including instance creation, decorator factory behavior, and
decorator usage.
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
from functools import partial
from typing import Any

# Third-Party Packages #
import pytest

# Local Packages #
from ...functions import BaseDecorator
from ..bases import BaseFunctionTestSuite, concrete_function


# Definitions #
# Classes #
class BaseDecoratorTestSuite(BaseFunctionTestSuite):
    """Base class for test suites which test BaseDecorator and its subclasses.

    This class provides common functionality for test suites that test decorator objects, including fixtures and
    test methods for verifying the behavior of BaseDecorator objects. Subclasses should implement the abstract methods
    and set the UnitTestClass attribute.

    Attributes:
        UnitTestClass: The class that the test suite is testing, which should be BaseDecorator or a subclass.
    """

    UnitTestClass: type[BaseDecorator]

    # Tests #
    # Magic Methods #
    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_call(self, test_function_object: BaseDecorator, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object can be called and correctly delegates to the wrapped function."""
        assert test_function_object(*args) == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_call_wrapped(self, test_function_object: BaseDecorator, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the wrapped function can be called directly."""
        assert test_function_object.call_wrapped(*args) == expected

    # Instantiation #
    def test_instance_creation(self, *args: Any, **kwargs: Any) -> None:
        """Tests that instances of the class can be created.

        Args:
            *args: Positional arguments list to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Creates an instance with a test function
        instance = self.UnitTestClass(concrete_function)

        # Verifies it's an instance of the correct class
        assert isinstance(instance, self.UnitTestClass)

        # Verifies it has the correct wrapped function
        assert instance.__func__ is concrete_function

    # Pickling #
    def test_init_false_pickling(self) -> None:
        """Tests pickling of an object initialized with init=False."""
        # Standard Libraries #
        import pickle

        obj = self.UnitTestClass(init=False, _return_partial=False)
        dump = pickle.dumps(obj)
        loaded = pickle.loads(dump)
        assert loaded.__wrapped__ is None

    # Functionality #
    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_as_function(self, test_function_object: BaseDecorator, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object can be converted to a standard Python function."""
        func = test_function_object.as_function()
        assert callable(func)
        assert func(*args) == expected

        assert func.__name__ == test_function_object.__name__  # type: ignore[attr-defined]
        assert func.__doc__ == test_function_object.__doc__
        assert func.__wrapped__ is test_function_object  # type: ignore[attr-defined]

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_coroutine(self, test_coroutine_object: BaseDecorator, args: tuple[Any, ...], expected: Any) -> None:
        """Tests that the callable object correctly handles coroutine functions."""
        coro = test_coroutine_object(*args)
        assert asyncio.iscoroutine(coro)
        result = asyncio.run(coro)
        assert result == expected

    @pytest.mark.parametrize(
        ("args", "expected"),
        [
            ((3,), 5),
            ((3, 4), 7),
        ],
    )
    def test_as_function_coroutine(
        self,
        test_coroutine_object: BaseDecorator,
        args: tuple[Any, ...],
        expected: Any,
    ) -> None:
        """Tests that the callable object wrapping a coroutine can be converted to a coroutine function."""
        func = test_coroutine_object.as_function()
        assert callable(func)

        coro = func(*args)
        result = asyncio.run(coro)
        assert result == expected

    def test_create_decorator_method(self) -> None:
        """Tests the create_decorator static method.

        This test verifies that the create_decorator method correctly creates a decorator instance.
        """
        decorator = self.UnitTestClass.create_decorator(self.UnitTestClass, concrete_function, (), {})
        assert isinstance(decorator, self.UnitTestClass)

    def test_new_without_func(self, *args: Any, **kwargs: Any) -> None:
        """Tests the __new__ method when no function is provided.

        This test only verifies that __new__ returns a partial function when no function is provided. This method may be
        overridden to validation that the decorator functions as intended.

        Args:
            *args: Positional arguments to pass to the class constructor.
            **kwargs: Keyword arguments to pass to the class constructor.
        """
        # Test Uninitialized
        partial_func = self.UnitTestClass(*args, **kwargs)
        assert isinstance(partial_func, partial)

        # Test Initialization
        decorated_func = partial_func(concrete_function)
        assert isinstance(decorated_func, self.UnitTestClass)

    def test_new_with_func(self, *args: Any, **kwargs: Any) -> None:
        """Tests the __new__ method when a function is provided.

        This test only verifies that __new__ returns a decorator instance when a function is provided. This method may
        be overridden to validation that the decorator functions as intended.

        Args:
            *args: Positional arguments to pass to the decorator constructor.
            **kwargs: Keyword arguments to pass to the decorator constructor.
        """
        # Test Initialization
        decorated_func = self.UnitTestClass(concrete_function, *args, **kwargs)
        assert isinstance(decorated_func, self.UnitTestClass)

    def test_decorator_usage(self) -> None:
        """Tests using the decorator in the standard Python way.

        This test verifies that the decorator can be used in the standard Python way.
        """

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        assert isinstance(test_func, self.UnitTestClass)
        assert test_func(3) == 5

    def test_decorator_with_args(self, *args: Any, **kwargs: Any) -> None:
        """Tests using the decorator with arguments.

        This test verifies that the decorator can be used with arguments.

        Args:
            *args: Positional arguments to pass to the decorator.
            **kwargs: Keyword arguments to pass to the decorator.
        """

        @self.UnitTestClass(*args, **kwargs)
        def test_func(x: int, y: int = 2) -> int:
            return x + y

        assert isinstance(test_func, self.UnitTestClass)
        assert test_func(3) == 5

    def test_coroutine_decorator(self) -> None:
        """Tests that the decorator correctly handles coroutine functions."""

        @self.UnitTestClass  # type: ignore[untyped-decorator]
        async def test_coro(x: int, y: int = 2) -> int:
            await asyncio.sleep(0)
            return x + y

        assert isinstance(test_coro, self.UnitTestClass)
        coro = test_coro(3)
        assert asyncio.run(coro) == 5

    def test_init_false(self) -> None:
        """Tests initialization with init=False."""
        obj = self.UnitTestClass(init=False, _return_partial=False)
        obj.construct()
        assert obj.__func__ is None


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
