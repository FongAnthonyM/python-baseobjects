"""basedecorator.py
An abstract class which implements the basic structure for creating decorators.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .dynamiccallable import DynamicFunction


# Definitions #
# Classes #
class BaseDecorator(DynamicFunction):
    """An abstract class which implements the basic structure for creating decorators."""

    default_call_method: str = "construct_call"

    # Instance Methods #
    # Calling
    def construct_call(self, func: AnyCallable | None = None, *args: Any, **kwargs: Any) -> "BaseDecorator":
        """A method for constructing this object via this object being called.

        Args:
            func: The function or method to wrap.
            *args: The arguments from the call which can construct this object.
            **kwargs: The keyword arguments from the call which can construct this object.

        Returns:
            This object.
        """
        self.construct(func=func, *args, **kwargs)
        instance = getattr(func, "__self__", None)
        return self if instance is None else self.__get__(instance, instance.__class__)
