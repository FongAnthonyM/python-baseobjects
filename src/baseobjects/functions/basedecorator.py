"""basedecorator.py
An abstract class which implements the basic structure for creating decorators.
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
    """An abstract class which implements the basic structure for creating decorators."""

    # Static Methods #
    @staticmethod
    def create_decorator(cls: BaseDecorator, func: AnyCallable, args: tuple, kwargs: dict[str, Any]) -> BaseDecorator:
        """A static method for creating a decorator."""
        return cls(func, *args, **kwargs)

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, *args: Any, func: AnyCallable | None = None, **kwargs: Any) -> BaseDecorator | partial :
        """Dispatches either the decorator instnace or creates a factory for creating instances.

        Args:
            func: The function or method to wrap.
            *args: Positional arguments for building an instance.
            **kwargs: Keyword arguments for building an instance.
        """
        if func is None and (not args or not callable(args[0])):
            return partial(cls.create_decorator, cls, args=args, kwargs=kwargs)
        else:
            return super().__new__(cls)
