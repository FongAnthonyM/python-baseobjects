""" functiondescriptor.py
A class that wraps a function so look like a data descriptor. Allows for the contained function to bereplaced making the
callback dynamic.
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
from collections.abc import Callable
from types import MethodType
from typing import Any
import weakref

# Third-Party Packages #

# Local Packages #
from ..typing import AnyCallable
from .baseobject import BaseObject


# Definitions #
# Classes #
class FunctionDescriptor(BaseObject):
    """A class that wraps a function so look like a data descriptor.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.

    Attributes:
        __func__: The function to wrap.

    Args:
        func: The function to wrap.
    """
    __slots__ = {"__func__"}

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func: AnyCallable | None = None) -> None:
        # Special Attributes #
        self.__func__: AnyCallable | None = func

    # Descriptors
    def __get__(self, instance: Any, owner: type[Any] | None = None) -> MethodType:
        """When this object is requested by another object as an attribute.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.

        Returns:
            The bound BaseMethod which can either self or a new BaseMethod.
        """
        return self.__func__.__get__(instance, owner)

    def __set__(self, instance, value) -> None:
        """When this object is requested by another object as an attribute.

            Args:
                instance: The other object requesting this object.
                value: A new function to wrap.
        """
        self.__func__ = value

    def __del__(self) -> None:
        """When the function would be deleted, set it to None."""
        self.__func__ = None

    # Callable
    def __call__(self, *args, **kwargs) -> Any:
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.__func__(*args, **kwargs)
