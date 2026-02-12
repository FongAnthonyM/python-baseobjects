"""orderabledict_test.py
Tests for the OrderableDict class in the baseobjects package.

This module provides tests for the OrderableDict class, which extends BaseDict to implement a dictionary that maintains
an explicit ordering of its keys. Unlike OrderedDict from the standard library, OrderableDict allows for direct
manipulation of the key order through various methods.
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
from baseobjects.collections import OrderableDict
from baseobjects.testsuite.collections import OrderableDictTestSuite


# Definitions #
# Tests #
class TestOrderableDict(OrderableDictTestSuite):
    """Tests the OrderableDict class.

    This class tests the functionality of the OrderableDict class, which extends BaseDict to implement a dictionary
    that maintains an explicit ordering of its keys and allows for direct manipulation of the key order.
    """

    # Attributes #
    UnitTestClass: type[OrderableDict] = OrderableDict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
