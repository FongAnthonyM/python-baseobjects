"""basedecorator.py
An abstract class which implements the basic structure for creating decorators.

This module provides the BaseDecorator class, which extends BaseFunction to create decorator-like callable objects. It
enables the creation of both simple decorators and decorators that accept arguments, handling both regular functions and
coroutine functions.
"""
# Futures Imports #
from __future__ import annotations

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
from functools import partial

# Third-Party Packages #

# Local Packages #
from ..bases import BaseFunction
from ..typing import AnyCallable
from .dynamiccallable import DynamicFunction


# Definitions #
# Classes #
class BaseDecorator(BaseFunction):
    """An abstract class which implements the basic structure for creating decorators.

    BaseDecorator provides a foundation for creating Python decorators with extended functionality. It can be used
    directly as a decorator or subclassed to create custom decorators. The class handles both regular functions and
    coroutine functions, and supports decorators with or without arguments.
    """

    # Static Methods #
    @staticmethod
    def create_decorator(
        cls: type[BaseDecorator],
        func: AnyCallable,
        args: tuple,
        kwargs: dict[str, Any],
    ) -> BaseDecorator:
        """A static method for creating a decorator instance.

        This method is used internally by the decorator factory mechanism to create decorator instances when the
        decorator is called with arguments. It's typically not called directly by users but is invoked through the
        partial function returned by __new__ when the decorator is used with arguments.

        Args:
            cls: The class to create an instance of (BaseDecorator or a subclass).
            func: The function or method to wrap with the decorator.
            args: Positional arguments that will be passed to the decorator.
            kwargs: Keyword arguments that will be passed to the decorator.

        Returns:
            An instance of the decorator class that wraps the specified function.
        """
        return cls(func, *args, **kwargs)

    # Magic Methods #
    # Construction/Destruction
    def __new__(
        cls,
        *args: Any,
        func: AnyCallable | None = None,
        _return_partial: bool = True,
        **kwargs: Any,
    ) -> BaseDecorator | partial:
        """Creates either a decorator instance or a factory for creating decorator instances.

        This method implements the dual-mode behavior of decorators:
        1. When called with a function (either as the first positional argument or as the `func` parameter), it creates
           and returns a decorator instance that wraps that function.
        2. When called without a function, it returns a partial function that will create a decorator instance when
           later called with a function.

        This enables both standard decorator usage (@decorator) and parameterized decorator usage
        (@decorator(arg1=value1)).

        Args:
            *args: Positional arguments. If the first argument is callable, it's treated as the function to wrap.
            func: The function or method to wrap. If provided, a decorator instance is created.
            _return_partial: If True and no function is provided, returns a partial function for later instantiation.
                             If False, always creates an instance (used internally for pickling).
            **kwargs: Keyword arguments for configuring the decorator.

        Returns:
            Either a BaseDecorator instance wrapping the provided function, or a partial functionthat will create such
            an instance when called with a function.
        """
        if func is None and (not args or not callable(args[0])) and _return_partial:
            return partial(cls.create_decorator, cls, args=args, kwargs=kwargs)
        else:
            return super().__new__(cls)

    # Reduction/Pickling
    def __reduce__(self) -> tuple[Any, tuple[Any], Any]:
        """Reduce the decorator to be picklable.

        This method enables decorator instances to be properly pickled and unpickled.

        The reduction strategy:
        1. Uses a partial function with __new__ to create a new instance without returning a partial
        2. Provides an empty tuple as the second element (no positional args for __new__)
        3. Includes the instance state from __getstate__ as the third element

        Returns:
            A tuple containing:
            - A partial function that will create a new instance
            - An empty tuple (no positional args for __new__)
            - The instance state from __getstate__
        """
        return partial(self.__new__, self.__class__, _return_partial=False), (), self.__getstate__()
