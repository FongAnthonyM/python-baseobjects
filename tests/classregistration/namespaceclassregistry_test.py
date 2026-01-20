#!/usr/bin/env python
"""namespaceclassregistry_test.py
Tests for the NamespaceClassRegistry class in the baseobjects package.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from typing import ClassVar

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.testsuite.classregistration import NamespaceClassRegistryTestSuite


# Definitions #
# Classes #
class TestNamespaceClassRegistry(NamespaceClassRegistryTestSuite):
    """Tests the NamespaceClassRegistry, which is a registry for classes in namespaces.

    Attributes:
        UnitTestClass: The class that the test suite is testing.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[NamespaceClassRegistry]] = NamespaceClassRegistry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
