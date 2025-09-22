"""__init__.py
The bases package provides fundamental base classes for object-oriented programming in Python.

This module serves as an initialization file for the bases package, which contains fundamental base classes used
throughout the baseobjects library. It imports and exposes classes like BaseObject, BaseMeta, BaseCallable, and
SentinelObject, making them available for direct import from the bases package.

The bases package includes the following key components:

- BaseObject: An abstract base class that implements fundamental functionality for all objects, such as copying
  and deep copying. It serves as a foundation for other classes in the baseobjects package.

- BaseReducible: Extends BaseObject to add functionality for object reduction and pickling, properly handling
  both __dict__ and __slots__ attributes during serialization and deserialization.

- BaseMeta: An abstract metaclass that extends ABCMeta to provide proper support for copying and deep copying
  of metaclass instances (classes).

- BaseCallable: An abstract class that implements the basic structure for creating callable objects, with
  derivatives BaseMethod and BaseFunction for creating method-like and function-like objects.

- SentinelObject: A singleton class for creating unique sentinel values that can be used for special cases
  in function arguments, return values, or as markers in data structures.

These classes provide a solid foundation for building complex object hierarchies with consistent behavior
and functionality.
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
from .sentinelobject import SentinelObject, DEFAULTSENTINEL, SEARCHSENTINEL
from .baseobject import BaseObject
from .basereducible import BaseReducible
from .basemeta import BaseMeta
from .basecallable import BaseCallable, BaseMethod, BaseFunction
from .collections import *
