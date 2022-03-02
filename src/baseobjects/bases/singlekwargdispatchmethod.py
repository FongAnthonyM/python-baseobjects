""" singlekwargdispatchmethod.py
Extends singledispaatchermethod to allow kwargs to be used for dispatching.

The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
specified to have the dispatcher use that kwarg instead of the first kwarg.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from functools import singledispatch, singledispatchmethod, update_wrapper
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..types_ import AnyCallable, AnyCallableType


# Definitions #
# Classes #
class singlekwargdispatchmethod(singledispatchmethod):
    """Extends singledispaatchermethod to allow kwargs to be used for dispatching.

    The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
    allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
    specified to have the dispatcher use that kwarg instead of the first kwarg.

    Attributes:
        dispatcher: The single dispatcher to use for this object.
        func: The method to wrap for single dispatching.
        parse: The method for parsing the args for the class to use for dispatching.
        _kwarg: The name of the kwarg to use of parsing the args for the class to use for dispatching.

    Args:
        kwarg: Either the name of kwarg to dispatch with or the method to wrap.
        method: The method to wrap.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, kwarg: AnyCallable | str, method: AnyCallable | None = None) -> None:
        # Attributes #
        self.dispatcher: singledispatch | None = None
        self.func: AnyCallable | None = None
        self.parse: AnyCallableType = self.parse_first
        self._kwarg: str | None = None

        # Object Creation #
        if isinstance(kwarg, str):
            self.construct(kwarg=kwarg, method=method)
        else:
            self.construct(method=kwarg)

    @property
    def kwarg(self) -> str | None:
        """The name of the kwarg to get the class for the dispatching."""
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    # Descriptors
    def __get__(self, obj: Any, cls: type[Any] | None = None) -> AnyCallable:
        """The method for when this object is requested by another object as an attribute.

        Args:
            obj: The other object requesting this object.
            cls: The class of the other object requesting this object.

        Returns:
            The method to be dispatched.
        """

        def _method(*args: Any, **kwargs: Any) -> Any:
            type_ = self.parse(*args, **kwargs)
            method = self.dispatcher.dispatch(type_)
            return method.__get__(obj, cls)(*args, **kwargs)

        _method.__isabstractmethod__ = self.__isabstractmethod__
        _method.register = self.register
        _method.set_kwarg = self.set_kwarg
        update_wrapper(_method, self.func)
        return _method

    # Callable
    def __call__(self, method: AnyCallable | None = None) -> "singlekwargdispatchmethod":
        """The call magic method for this object.

        Args:
            method: The method to make a single kwarg dispatch method for.

        Returns:
           This object.
        """
        self.construct(method=method)
        return self

    # Instance Methods #
    # Constructors
    def construct(self, kwarg: str | None = None, method: AnyCallable | None = None) -> None:
        """Constructs this object based on the input.

        Args:
            kwarg: The name of kwarg to dispatch with.
            method: The method to wrap.
        """
        if kwarg is not None:
            self.kwarg = kwarg

        if method is not None:
            if not callable(method) and not hasattr(method, "__get__"):
                raise TypeError(f"{method!r} is not callable or a descriptor")

            self.dispatcher = singledispatch(method)
            self.func = method

    def set_kwarg(self, kwarg: str | None) -> None:
        """Sets the name of the kwarg for dispatching and changes the arg parsing to check for the kwarg.

        Args:
            kwarg: The name of the kwarg or None for checking the first kwarg.
        """
        if kwarg is None:
            self.parse = self.parse_first
        else:
            self.parse = self.parse_kwarg
        self._kwarg = kwarg

    def parse_first(self, *args: Any, **kwargs: Any) -> type[Any]:
        """Parses input for the first arg or the first kwarg's class to be used for dispatching.

        Args:
            *args: The args given to the method.
            **kwargs: The kwargs given to the method.

        Returns:
            The class to be used for dispatching.
        """
        if args:
            return args[0].__class__
        else:
            return next(iter(kwargs.values())).__class__

    def parse_kwarg(self, *args: Any, **kwargs: Any) -> type[Any]:
        """Parses input for the first arg or a specific kwarg's class to be used for dispatching.

        Args:
            *args: The args given to the method.
            **kwargs: The kwargs given to the method.

        Returns:
            The class to be used for dispatching.
        """
        if args:
            return args[0].__class__
        else:
            return kwargs[self._kwarg].__class__
