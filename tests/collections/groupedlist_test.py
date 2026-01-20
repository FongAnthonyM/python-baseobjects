"""groupedlist_test.py
Tests for the GroupedList class in the baseobjects package.

This module provides tests for the GroupedList class, which is a list that contains any item, but nested GroupLists'
contents are treated as if they are elements of this list.
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
from baseobjects.collections import GroupedList
from baseobjects.testsuite.collections import GroupedListTestSuite


# Definitions #
# Tests #
class TestGroupedList(GroupedListTestSuite):
    """Test the GroupedList class.

    This class tests the functionality of the GroupedList class, which is a list that contains any item, but nested
    GroupLists' contents are treated as if they are elements of this list.
    """

    # Attributes #
    UnitTestClass: ClassVar[type[GroupedList]] = GroupedList


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
