"""__init__.py
Provides test suite classes for class registration.

This module serves as an initialization file for the testsuite.classregistration package, which provides test suite
classes for testing class registration functionality. It imports and exposes classes like BaseClassRegistryTestSuite,
BaseRegisteredClassTestSuite, and others, making them available for direct import from the
testsuite.classregistration package. These test suites ensure the proper functioning of class registration and
dispatching mechanisms in the baseobjects package.
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
from .baseclassregistrytestsuite import BaseClassRegistryTestSuite
from .baseregisteredclasstestsuite import BaseRegisteredClassTestSuite
from .dispatchableclasstestsuite import DispatchableClassTestSuite
from .namespaceregisteredclasstestsuite import NamespaceRegisteredClassTestSuite
