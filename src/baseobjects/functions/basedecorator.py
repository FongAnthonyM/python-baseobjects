""" basedecorator.py
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
    def construct_call(self, *args: Any, **kwargs: Any) -> "BaseDecorator":
        """A method for constructing this object via this object being called.

        Args:
            *args: The arguments from the call which can construct this object.
            **kwargs: The keyword arguments from the call which can construct this object.

        Returns:
            This object.
        """
        if args:
            self.construct(func=args[0])
        else:
            self.construct(**kwargs)
        return self
