"""dynamicdecorator.py
An abstract class which implements a dynamic decorator with multiplexed callback.
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
from typing import Any

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
    BaseDecorator.
    """
