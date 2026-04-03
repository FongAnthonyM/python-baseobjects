"""functionregistry_test.py
Tests for the FunctionRegistry class in the baseobjects package.

This module provides tests for the FunctionRegistry class, which is a dictionary-like object that stores functions and
methods. It provides methods for registering functions and updating from objects.
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
# from typing import

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.functions import FunctionRegistry
from baseobjects.testsuite.functions import FunctionRegistryTestSuite


# Tests #
class TestFunctionRegistry(FunctionRegistryTestSuite):
    """Test the FunctionRegistry class.

    This class tests the functionality of the FunctionRegistry class.
    """

    # Attributes #
    UnitTestClass: type[FunctionRegistry] = FunctionRegistry

    def test_init_false(self) -> None:
        """Test initialization with init=False."""
        registry = self.UnitTestClass(init=False)
        assert not registry

    def test_init_with_objects(self) -> None:
        """Test initialization with objects iterable."""

        class A:
            def foo(self) -> None:
                pass

        class B:
            def bar(self) -> None:
                pass

        registry = self.UnitTestClass(objects=[A(), B()])
        assert "foo" in registry
        assert "bar" in registry


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
