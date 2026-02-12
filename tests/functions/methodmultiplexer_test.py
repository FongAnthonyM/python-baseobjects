"""methodmultiplexer_test.py
Tests for the MethodMultiplexer class in the baseobjects package.

This module provides tests for the MethodMultiplexer class, which is a callable that selects between different functions
or methods to be used as the call method. It binds methods to the multiplexer instance.
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
from baseobjects.functions import MethodMultiplexer
from baseobjects.testsuite.functions import MethodMultiplexerTestSuite


# Tests #
class TestMethodMultiplexer(MethodMultiplexerTestSuite):
    """Test the MethodMultiplexer class.

    This class tests the functionality of the MethodMultiplexer class.
    """

    # Attributes #
    UnitTestClass: type[MethodMultiplexer] = MethodMultiplexer


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
