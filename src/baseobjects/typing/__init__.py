"""__init__.py
Types to be used for type hints.

This module serves as the entry point for the typing subpackage, which provides type hint definitions used
throughout the baseobjects package. It imports and re-exports all type definitions from the generic and callables
modules, making them available for import directly from the typing subpackage.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Local Packages #
from .callables import *
from .generic import *

__all__ = [
    "AnyCallable",
    "AnyCallableType",
    "CallMethod",
    "DeleteMethod",
    "DescriptorGetMethod",
    "GetterMethod",
    "KT_co",
    "KeyType",
    "PropertyCallbacks",
    "SetterMethod",
    "VT_co",
    "ValueType",
]
