"""dynamicdecoractor.py
An abstract class which implements a dynamic decorator with multiplexed callback.
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
# Local Packages #
from .basedecorator import BaseDecorator
from .dynamiccallable import DynamicFunction


# Definitions #
# Classes #
class DynamicDecorator(BaseDecorator, DynamicFunction):
    """An abstract decorator class that has multiplexed binding and callback.

    This class combines the functionality of BaseDecorator for creating decorators and DynamicFunction for providing
    multiplexed callback capabilities. The BaseDecorator class operates slightly faster than this class, but this class
    allows for efficient switching between different binding and callback functions/methods. This can be useful for
    runtime multiplexing of binding and callback functions/methods.

    Also, if either binding or callback is desired to be static (multiplexing is not required), then override the
    __get__ or __call__ methods of this class. If both binding and callback are static then consider using
    BaseDecorator. Example:
    >>> # Method Overrides #
    >>> # Special method overriding which leads to less overhead.
    >>> __get__: GetObjectMethod = BaseDecorator.bind_builtin  # Assigns __get__ to a previously defined method.
    >>> __call__: AnyCallable = BaseDecorator.call_binding  # Assigns __call__ to a previously defined method.
    """
