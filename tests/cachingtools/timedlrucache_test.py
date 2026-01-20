#!/usr/bin/env python
"""timedlrucache_test.py
Test for the TimedLRUCache class.
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
from baseobjects.cachingtools.caches.timedlrucache import TimedLRUCache
from baseobjects.testsuite.cachingtools.timedlrucachetestsuite import TimedLRUCacheTestSuite


# Definitions #
# Classes #
class TestTimedLRUCache(TimedLRUCacheTestSuite):
    """Test the TimedLRUCache class.

    This class tests the functionality of the TimedLRUCache class, utilizing the TimedLRUCacheTestSuite.
    """

    # Attributes #
    UnitTestClass = TimedLRUCache

    # Instance Methods #
    def test_pause_timer(self) -> None:
        """Tests pausing the timer."""


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
