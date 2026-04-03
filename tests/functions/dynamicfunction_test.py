"""dynamicfunction_test.py
Tests for the DynamicFunction class in the baseobjects package.

This module provides tests for the DynamicFunction class, which is an abstract function class that has multiplexed
binding and callback functionality. It tests the core functionality of DynamicFunction, including instance creation,
function calling, binding, and multiplexed callback.
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
from baseobjects.functions import DynamicFunction
from baseobjects.testsuite.functions import DynamicFunctionTestSuite


# Tests #
class TestDynamicFunction(DynamicFunctionTestSuite):
    """Test the DynamicFunction class.

    This class tests the functionality of the DynamicFunction class, which is an abstract function class that has
    multiplexed binding and callback functionality.
    """

    # Attributes #
    UnitTestClass: type[DynamicFunction] = DynamicFunction


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
