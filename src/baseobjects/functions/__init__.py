"""__init__.py
functions provides classes for functions and methods.
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
from .singlekwargdispatch import singlekwargdispatch
from .functionregistry import FunctionRegistry
from .methodregistry import MethodRegistry
from .callablemultiplexer import CallableMultiplexer, MethodMultiplexer
from .dynamiccallable import DynamicCallable, DynamicMethod, DynamicFunction
from .dynamicdecoractor import DynamicDecorator
