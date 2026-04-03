"""methodregistry_test.py
Tests for the MethodRegistry class in the baseobjects package.

This module provides tests for the MethodRegistry class, which is a dictionary-like object that stores functions and
methods. It provides methods for binding the registry to an instance.
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

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions import MethodRegistry
from baseobjects.functions.methodregistry import BaseMethodRegistry, BoundMethodRegistry
from baseobjects.testsuite.functions import (
    BaseMethodRegistryTestSuite,
    BoundMethodRegistryTestSuite,
    MethodRegistryTestSuite,
)


# Tests #
class TestBaseMethodRegistry(BaseMethodRegistryTestSuite):
    """Test the BaseMethodRegistry class."""

    # Attributes #
    UnitTestClass: type[BaseMethodRegistry] = BaseMethodRegistry


class TestBoundMethodRegistry(BoundMethodRegistryTestSuite):
    """Test the BoundMethodRegistry class."""

    # Attributes #
    UnitTestClass: type[BoundMethodRegistry] = BoundMethodRegistry
    BaseRegistryClass: type[BaseMethodRegistry] = BaseMethodRegistry


class TestMethodRegistry(MethodRegistryTestSuite):
    """Test the MethodRegistry class."""

    # Attributes #
    UnitTestClass: type[MethodRegistry] = MethodRegistry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
