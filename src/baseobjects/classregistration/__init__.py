"""__init__.py
Base class for registering and dispatching classes.
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
