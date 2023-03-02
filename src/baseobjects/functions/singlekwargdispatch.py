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
from ..typing import AnyCallable
from .dynamiccallable import DynamicMethod
from .basedecorator import BaseDecorator
from .callablemultiplexer import MethodMultiplexer


# Definitions #
# Classes #
class singlekwargdispatchmethod(DynamicMethod):
    """A wrapper for a bound singlekwargsipatch."""
    default_call_method: str = "search_call"

    # Calling
    def search_call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function's search methods and returns the result.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__func__.dispatcher.dispatch(self.__func__.parse(*args, **kwargs))(self.__self__, *args, **kwargs)


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
        func: The func to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """
    method_type: type[DynamicMethod] = singlekwargdispatchmethod

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        kwarg: AnyCallable | str | None = None,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self.dispatcher: singledispatch | None = None
        self.parse: MethodMultiplexer = MethodMultiplexer(instance=self, select="parse_first")
        self._kwarg: str | None = None

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Creation #
        if init:
            if isinstance(kwarg, str):
                self.construct(kwarg=kwarg, func=func)
            else:
                self.construct(func=kwarg)

    @property
    def kwarg(self) -> str | None:
        """The name of the kwarg to get the class for the dispatching."""
        return self._kwarg

    @kwarg.setter
    def kwarg(self, value: str | None) -> None:
        self.set_kwarg(kwarg=value)

    # Instance Methods #
    # Constructors
    def construct(self, kwarg: str | None = None, func: AnyCallable | None = None, *args:Any, **kwargs: Any) -> None:
        """Constructs this object based on the input.

        Args:
            kwarg: The name of kwarg to dispatch with.
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if kwarg is not None:
            self.kwarg = kwarg

        if func is not None:
            self.dispatcher = singledispatch(func)

        super().construct(self, *args, **kwargs)

        if self.dispatcher is not None:
            self.call_method = "search_call"

    # Setters
    def set_kwarg(self, kwarg: str | None) -> None:
        """Sets the name of the kwarg for dispatching and changes the arg parsing to check for the kwarg.

        Args:
            kwarg: The name of the kwarg or None for checking the first kwarg.
        """
        if kwarg is None:
            self.parse.select("parse_first")
        else:
            self.parse.select("parse_kwarg")
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
        return args[0].__class__ if args else kwargs.get(self._kwarg, None).__class__

    # Method Searching
    def search_call(self, *args: Any, **kwargs: Any) -> Any:
        """Parses input to decide which method to use in the registry.

        Args:
            *args: The arguments to pass to the found method.
            **kwargs: The keyword arguments to pass to the found method.

        Returns:
            The return of the found method.
        """
        return self.dispatcher.dispatch(self.parse(*args, **kwargs))(*args, **kwargs)