"""callables.py
Type hints for callables.

This module provides type hint definitions for various callable objects used throughout the baseobjects package.
It includes type hints for general callables, object methods, and property-related methods (getters, setters, and
deleters). These type hints help with static type checking and improve code documentation.
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
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Types #
# Callables
AnyCallable = Callable[..., Any]
AnyCallableType = Callable[..., type[Any]]

# Objects
GetObjectMethod = Callable[[Any, Any, type[Any] | None, ...], "BaseMethod"]

# Getters, Setters, and Deletes
GetterMethod = Callable[[Any], Any]
SetterMethod = Callable[[Any, str], None]
DeleteMethod = Callable[[Any], None]
PropertyCallbacks = tuple[GetterMethod, SetterMethod, DeleteMethod]

# Available Types
__all__ = [
    "AnyCallable",
    "AnyCallableType",
    "GetObjectMethod",
    "GetterMethod",
    "SetterMethod",
    "DeleteMethod",
    "PropertyCallbacks",
]
