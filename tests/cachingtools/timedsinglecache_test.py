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
# Standard Libraries #
import time

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.timedsinglecache import TimedSingleCache


# Definitions #
# Classes #
class TestTimedSingleCache:
    """Test the TimedSingleCache class."""

    def test_single_cache_behavior(self):
        """Tests that TimedSingleCache only holds one item."""
        count = [0]
        def func(x):
            count[0] += 1
            return x * 10

        cache = TimedSingleCache(func=func)

        assert cache(1) == 10
        assert count[0] == 1

        # Second call same arg -> HIT
        assert cache(1) == 10
        assert count[0] == 1

        # Call with different arg -> REPLACES
        assert cache(2) == 20
        assert count[0] == 2

        # Call with first arg again -> MISS (because it was replaced)
        assert cache(1) == 10
        assert count[0] == 3

    def test_expiration(self):
        """Tests expiration of TimedSingleCache."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = TimedSingleCache(func=func, lifetime=0.1)
        assert cache(1) == 1
        assert count[0] == 1

        time.sleep(0.15)
        assert cache(1) == 1
        assert count[0] == 2

    def test_clear_cache(self):
        """Tests clear_cache method."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = TimedSingleCache(func=func)
        assert cache(1) == 1
        assert count[0] == 1

        cache.clear_cache()
        assert cache(1) == 1
        assert count[0] == 2

    def test_disable_caching(self):
        """Tests that disabling caching works."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = TimedSingleCache(func=func)
        assert cache(1) == 1
        assert count[0] == 1

        cache.disable_caching()
        assert cache(1) == 1
        assert count[0] == 2
        assert cache(1) == 1
        assert count[0] == 3


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
