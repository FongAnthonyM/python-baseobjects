"""timeddict_test.py
Tests for the TimedDict class in the baseobjects package.

This module provides tests for the TimedDict class, which extends BaseDict to implement a dictionary that clears its
contents after a specified time has elapsed.
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
from baseobjects.collections import TimedDict
from baseobjects.testsuite.collections import TimedDictTestSuite


# Definitions #
# Tests #
class TestTimedDict(TimedDictTestSuite):
    """Test the TimedDict class.

    This class tests the functionality of the TimedDict class, which extends BaseDict to implement a dictionary that
    clears its contents after a specified time has elapsed.
    """

    # Attributes #
    UnitTestClass: type[TimedDict] = TimedDict


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
