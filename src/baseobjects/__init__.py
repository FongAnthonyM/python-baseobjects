"""__init__.py
baseobjects provides several base classes and tools.

This package contains a collection of base classes and utility tools for Python development. It includes abstract base
classes, metaclasses, composition tools, and various utility functions that can be used as building blocks for more
complex applications.
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
from .bases import *
from .composition import *
from .functions import *

__all__ = [
    "DEFAULTSENTINEL",
    "SEARCHSENTINEL",
    "BaseCallable",
    "BaseComponent",
    "BaseComposite",
    "BaseDecorator",
    "BaseDict",
    "BaseDispatchingComposite",
    "BaseFunction",
    "BaseList",
    "BaseMeta",
    "BaseMethod",
    "BaseObject",
    "BaseReducible",
    "CallableMultiplexer",
    "DispatchableComposite",
    "DynamicCallable",
    "DynamicDecorator",
    "DynamicFunction",
    "DynamicMethod",
    "FunctionMultiplexer",
    "FunctionRegistry",
    "MethodMultiplexer",
    "MethodRegistry",
    "SentinelObject",
    "singlekwargdispatch",
]
