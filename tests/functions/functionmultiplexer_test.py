"""functionmultiplexer_test.py
Tests for the FunctionMultiplexer class in the baseobjects package.

This module provides tests for the FunctionMultiplexer class, which is a callable that selects between different
functions or methods to be used as the call method. It does NOT bind methods to the multiplexer instance.
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
from baseobjects.functions import FunctionMultiplexer
from baseobjects.testsuite.functions import FunctionMultiplexerTestSuite


# Tests #
class TestFunctionMultiplexer(FunctionMultiplexerTestSuite):
    """Test the FunctionMultiplexer class.

    This class tests the functionality of the FunctionMultiplexer class.
    """

    # Attributes #
    UnitTestClass: type[FunctionMultiplexer] = FunctionMultiplexer


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
