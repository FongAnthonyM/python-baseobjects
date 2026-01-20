#!/usr/bin/env python
"""timedsinglecache_test.py
Test for the TimedSingleCache class.
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
from baseobjects.cachingtools.caches.timedsinglecache import TimedSingleCache
from baseobjects.testsuite.cachingtools.timedsinglecachetestsuite import TimedSingleCacheTestSuite


# Definitions #
# Classes #
class TestTimedSingleCache(TimedSingleCacheTestSuite):
    """Test the TimedSingleCache class.

    This class tests the functionality of the TimedSingleCache class, utilizing the TimedSingleCacheTestSuite.
    """

    # Attributes #
    UnitTestClass = TimedSingleCache

    # Instance Methods #
    def test_pause_timer(self) -> None:
        """Tests pausing the timer."""

    def test_refresh_expiration_no_lifetime(self) -> None:
        """Tests refresh_expiration with no lifetime."""
        cache = self.UnitTestClass(lambda: None, lifetime=None)
        cache.refresh_expiration()
        assert cache.expiration == 0


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
