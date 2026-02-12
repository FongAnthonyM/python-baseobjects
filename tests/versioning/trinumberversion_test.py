#!/usr/bin/env python
"""trinumberversion_test.py
Test suite for the TriNumberVersion class.
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
from baseobjects.testsuite.versioning.trinumberversiontestsuite import TriNumberVersionTestSuite
from baseobjects.versioning.trinumberversion import TriNumberVersion


# Definitions #
# Classes #
class TestTriNumberVersion(TriNumberVersionTestSuite):
    """Test suite for the TriNumberVersion class.

    This class tests the functionality of the TriNumberVersion class, which is a concrete implementation of the Version
    abstract class that represents a version with three numbers (major.minor.patch).
    """

    # Class Attributes #
    UnitTestClass: type[TriNumberVersion] = TriNumberVersion


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
