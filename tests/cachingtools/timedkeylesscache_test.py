#!/usr/bin/env python
"""timedkeylesscache_test.py
Test for the TimedKeylessCache class.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2021, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.timedkeylesscache import TimedKeylessCache
from baseobjects.testsuite.cachingtools.timedkeylesscachetestsuite import TimedKeylessCacheTestSuite


# Definitions #
# Classes #
class TestTimedKeylessCache(TimedKeylessCacheTestSuite):
    """Test the TimedKeylessCache class.

    This class tests the functionality of the TimedKeylessCache class, utilizing the TimedKeylessCacheTestSuite.
    """

    # Attributes #
    UnitTestClass = TimedKeylessCache

    # Instance Methods #
    def test_pause_timer(self) -> None:
        """Tests pausing the timer."""


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
