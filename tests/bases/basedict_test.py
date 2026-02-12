"""basedict_test.py
Tests for the BaseDict class in the baseobjects package.

This module contains tests for the BaseDict class, which is an abstract base class that inherits from both BaseObject
and UserDict. It combines the dictionary-like behavior of UserDict with the enhanced functionality of BaseObject,
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
from baseobjects.bases.collections import BaseDict
from baseobjects.testsuite.bases import BaseDictTestSuite


# Classes #
class TestBaseDict(BaseDictTestSuite):
    """Test the BaseDict class.

    This class tests the functionality of the BaseDict class, which is a mixin of UserDict and BaseObject.
    It creates a test subclass of BaseDict to test with.
    """

    # Class Definitions #
    class BaseTestDict(BaseDict):
        """A subclass of BaseDict for testing purposes."""

        __test__ = False

    # Attributes #
    UnitTestClass: type[BaseTestDict] = BaseTestDict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
