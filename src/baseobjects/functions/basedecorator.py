"""basedecorator.py
An abstract class which implements the basic structure for creating decorators.

This module provides the BaseDecorator class, which extends BaseFunction to create decorator-like callable objects. It
enables the creation of both simple decorators and decorators that accept arguments, handling both regular functions and
coroutine functions.
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
from collections.abc import Callable
from functools import partial
from typing import Any

# Local Packages #
from ..typing import DescriptorGetMethod
from ..bases import BaseMethod


# Definitions #
# Classes #
class BaseDecorator(BaseMethod):
    """An abstract class which implements the basic structure for creating decorators.

    BaseDecorator provides a foundation for creating Python decorators with extended functionality. It can be used
    directly as a decorator or subclassed to create custom decorators. The class handles both regular functions and
    coroutine functions, and supports decorators with or without arguments.
    """

    # Static Methods #
    @staticmethod
    def create_decorator(
        cls: type[BaseDecorator],
        func: Any,
        args: tuple[Any, ...],
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

    # Construction/Destruction
    def __new__(  # type: ignore[misc]
        cls,
        *args: Any,
        func: Any | None = None,
        _return_partial: bool = True,
        **kwargs: Any,
    ) -> BaseDecorator | Callable[..., BaseDecorator]:
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
        if (
            func is None
            and (not args or not (callable(args[0]) or isinstance(args[0], (classmethod, staticmethod))))
            and _return_partial
        ):
            return partial(cls.create_decorator, cls, args=args, kwargs=kwargs)
        else:
            return super().__new__(cls)

    # Pickling
    def __getnewargs_ex__(self) -> tuple[tuple[Any, ...], dict[str, Any]]:
        """Provides the arguments needed to recreate this object during unpickling.

        Returns:
            The arguments needed to recreate this object during unpickling.
        """
        return (), {"_return_partial": False}

    # Method Overrides #
    # Special method overriding which leads to less overhead.
    __get__: DescriptorGetMethod = BaseMethod.bind_builtin
