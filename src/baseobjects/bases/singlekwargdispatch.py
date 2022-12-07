""" singlekwargdispatch.py
Extends singledispatch to allow kwargs to be used for dispatching.

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
from functools import singledispatch, singledispatchmethod
from types import NoneType
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable, AnyCallableType
from .basedecorator import BaseDecorator


# Definitions #
# Classes #
class singlekwargdispatch(BaseDecorator, singledispatchmethod):
    """Extends singledispatch to allow kwargs to be used for dispatching.

    The normal single dispatching requires at least one arg for dispatching. This object retains this functionality, but
    allows the first kwarg to be used for dispatching if no args are provided. Furthermore, a kwarg name can be
    specified to have the dispatcher use that kwarg instead of the first kwarg.

    Attributes:
        dispatcher: The single dispatcher to use for this object.
        func: The original method to wrap for single dispatching.
        parse: The method for parsing the args for the class to use for dispatching.
        _kwarg: The name of the kwarg to use of parsing the args for the class to use for dispatching.

    Args:
        kwarg: Either the name of kwarg to dispatch with or the method to wrap.
        method: The method to wrap.
    """
    __slots__ = BaseDecorator.__slots__ | {"dispatcher", "func", "_parse", "_kwarg"}

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, kwarg: AnyCallable | str, method: AnyCallable | None = None) -> None:
        # Parent Attributes #
        BaseDecorator.__init__(self, init=False)

        # Override Attributes #
        self._default_call_method = self.method_search.__func__

        # New Attributes #
        self.dispatcher: singledispatch | None = None
        self.func: AnyCallable | None = None
        self._parse: AnyCallableType = self.parse_first.__func__
        self._kwarg: str | None = None

        # Object Creation #
        if isinstance(kwarg, str):
            self.construct(kwarg=kwarg, func=method)
        else:
            self.construct(func=kwarg)

    @property
    def kwarg(self) -> str | None:
        """The name of the kwarg to get the class for the dispatching."""
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    @property
    def parse(self) -> AnyCallableType:
        """A descriptor to create the bound parse method."""
        return self._parse.__get__(self, self.__class__)

    @parse.setter
    def parse(self, value: AnyCallableType) -> None:
        self._parse = value

    # Instance Methods #
    # Constructors
    def construct(self, kwarg: str | None = None, func: AnyCallable | None = None, **kwargs: Any) -> None:
        """Constructs this object based on the input.

        Args:
            kwarg: The name of kwarg to dispatch with.
            func: The method to wrap.
            **kwargs: The other keyword arguments to construct a BaseMethod.
        """
        if kwarg is not None:
            self.kwarg = kwarg

        if func is not None:
            self.dispatcher = singledispatch(func)

        BaseDecorator.construct(self, func=func, **kwargs)

    # Setters
    def set_kwarg(self, kwarg: str | None) -> None:
        """Sets the name of the kwarg for dispatching and changes the arg parsing to check for the kwarg.

        Args:
            kwarg: The name of the kwarg or None for checking the first kwarg.
        """
        if kwarg is None:
            self._parse = self.parse_first.__func__
        else:
            self._parse = self.parse_kwarg.__func__
        self._kwarg = kwarg

    # Parameter Parsers
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
            try:
                return next(iter(kwargs.values())).__class__
            except StopIteration:
                return NoneType

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
            return kwargs.get(self._kwarg, None).__class__

    # Method Searching
    def method_search(self, *args: Any, **kwargs: Any) -> Any:
        """Parses input to decide which method to use in the registry.

        Args:
            *args: The arguments to pass to the found method.
            **kwargs: The keyword arguments to pass to the found method.

        Returns:
            The return of the found method.
        """
        return self.dispatcher.dispatch(self.parse(*args, **kwargs))(*args, **kwargs)


class singlekwargdispatchmethod(singlekwargdispatch):
    """The method version of singlekwargdispatch."""

    # Method Searching
    def method_search(self, *args: Any, **kwargs: Any) -> Any:
        """Parses input to decide which method to use in the registry.

        Args:
            *args: The arguments to pass to the found method.
            **kwargs: The keyword arguments to pass to the found method.

        Returns:
            The return of the found method.
        """
        method = self.dispatcher.dispatch(self.parse(*args, **kwargs))
        return method.__get__(self.__self__, self.__owner__)(*args, **kwargs)
