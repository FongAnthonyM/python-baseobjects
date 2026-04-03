"""sentinelobject_test.py
Tests for the SentinelObject class in the baseobjects package.

This module provides tests for the SentinelObject class, which implements a singleton pattern through a registry
mechanism, ensuring that only one instance exists for each unique identifier.
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
from baseobjects.bases import SentinelObject
from baseobjects.testsuite.bases import SentinelObjectTestSuite


# Classes #
class TestSentinelObject(SentinelObjectTestSuite):
    """Test the SentinelObject class.

    This class tests the functionality of the SentinelObject class, which implements a singleton pattern through a
    registry mechanism, ensuring that only one instance exists for each unique identifier.
    """

    # Attributes #
    UnitTestClass: type[SentinelObject] = SentinelObject

    @pytest.mark.parametrize("sentinel_name", ["DEFAULTSENTINEL", "SEARCHSENTINEL"])
    def test_predefined_constants(self, sentinel_name: str) -> None:
        """Test the predefined sentinel constants.

        This test verifies that the predefined sentinel constants DEFAULTSENTINEL and SEARCHSENTINEL
        are instances of SentinelObject with the correct identities.

        Args:
            sentinel_name: The name of the sentinel constant to test.
        """
        # Source Packages #
        import baseobjects.bases.sentinelobject as sentinel_module

        # Get the sentinel object
        sentinel = getattr(sentinel_module, sentinel_name)

        # Validate
        assert isinstance(sentinel, self.UnitTestClass)
        assert sentinel.identity == sentinel_name
        assert sentinel is self.UnitTestClass(sentinel_name)


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
