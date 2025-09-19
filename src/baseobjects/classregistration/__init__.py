"""__init__.py
Base class for registering and dispatching classes.

This module provides classes for registering and dispatching classes based on input types or other criteria. It includes
BaseClassRegistry for managing class registrations, BaseRegisteredClass for classes that can be registered, and
DispatchableClass for classes that can be dynamically selected based on input.
"""
# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports
# Local Packages #
from .baseclassregistry import BaseClassRegistry
from .baseregisteredclass import BaseRegisteredClass
from .namespaceclassregistry import NamespaceClassRegistry
from .namespaceregisteredclass import NamespaceRegisteredClass
from .dispatchableclass import DispatchableClass
