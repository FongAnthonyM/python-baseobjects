"""baselist_test.py
Tests for the BaseList class in the baseobjects package.

This module contains tests for the BaseList class, which is an abstract base class that inherits from both BaseObject
and UserList. It combines the list-like behavior of UserList with the enhanced functionality of BaseObject,
such as proper copying and deep copying support.
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
from baseobjects.bases.collections import BaseList
from baseobjects.testsuite.bases import BaseListTestSuite


# Classes #
class BaseTestList(BaseList):
    """A subclass of BaseList for testing purposes."""

    __test__ = False


# Tests #
class TestBaseList(BaseListTestSuite):
    """Test the BaseList class.

    This class tests the functionality of the BaseList class, which is a mixin of UserList and BaseObject. It creates a
    test subclass of BaseList to test with.
    """

    # Attributes #
    UnitTestClass: type[BaseTestList] = BaseTestList


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
