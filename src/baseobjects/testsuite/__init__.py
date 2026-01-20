"""__init__.py
Test suites for the baseobjects package.

Contains test suites for the baseobjects package. It provides a structured testing framework to ensure the functionality
and reliability of the baseobjects components and is a basis for creating tests for hierarchies of components.
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
from .cachingtools import *
from .classregistration import *
from .functions import *
from .objects import *
from .versioning import VersionTestSuite
from .wrappers import *

__all__ = [
    "BaseCallableTestSuite",
    "BaseClassRegistryTestSuite",
    "BaseClassTestSuite",
    "BaseFunctionTestSuite",
    "BaseMethodTestSuite",
    "BaseObjectTestSuite",
    "BasePerformanceTestSuite",
    "BaseRegisteredClassTestSuite",
    "BaseTestSuite",
    "ConcreteBindTarget",
    "DispatchableClassTestSuite",
    "NamespaceRegisteredClassTestSuite",
    "StatsMicro",
    "VersionTestSuite",
    "concrete_coroutine",
    "concrete_coroutine_method",
    "concrete_function",
    "concrete_method",
]
