"""__init__.py
functions provides classes for functions and methods.

This module serves as an initialization file for the functions package, which provides various utility classes
for working with functions and methods. It imports and exposes classes like BaseDecorator, DynamicCallable, and
function registries, making them available for direct import from the functions package. These tools enable
advanced function manipulation, method dispatching, and callable object management.
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
from .basedecorator import BaseDecorator
from .callablemultiplexer import CallableMultiplexer, FunctionMultiplexer, MethodMultiplexer
from .dynamiccallable import DynamicCallable, DynamicFunction, DynamicMethod
from .dynamicdecoractor import DynamicDecorator
from .functionregistry import FunctionRegistry
from .methodregistry import MethodRegistry
from .singlekwargdispatch import singlekwargdispatch
