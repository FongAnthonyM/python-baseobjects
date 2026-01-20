"""__init__.py
bases.collection provides base classes for collection-type objects.

This package contains abstract base classes that combine the functionality of Python's standard collection classes (like
UserDict and UserList) with the BaseObject class. These hybrid classes serve as foundations for creating custom
collection types that have both the standard collection behavior and the enhanced functionality provided by BaseObject,
such as proper copying and deep copying support.

The classes in this package are designed to be subclassed rather than used directly, providing a consistent interface
and behavior for all collection objects in the baseobjects framework.
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
from .basedict import BaseDict
from .baselist import BaseList

__all__ = ["BaseDict", "BaseList"]
