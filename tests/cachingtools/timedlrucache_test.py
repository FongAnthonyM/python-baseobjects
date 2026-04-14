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
# Standard Libraries #
import time

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.timedlrucache import TimedLRUCache


# Definitions #
# Classes #
class TestTimedLRUCache:
    """Test the TimedLRUCache class."""

    def test_lru_behavior(self):
        """Tests LRU eviction."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = TimedLRUCache(func=func, maxsize=2)

        assert cache(1) == 1
        assert cache(2) == 2
        assert count[0] == 2

        # Access 1 again to make it recently used
        assert cache(1) == 1
        assert count[0] == 2

        # Add 3, should evict 2 (since 1 was recently used)
        assert cache(3) == 3
        assert count[0] == 3

        # 1 should still be in cache
        assert cache(1) == 1
        assert count[0] == 3

        # 2 should be evicted
        assert cache(2) == 2
        assert count[0] == 4

    def test_expiration(self):
        """Tests expiration of TimedLRUCache."""
        count = [0]
        def func(x):
            count[0] += 1
            return x

        cache = TimedLRUCache(func=func, lifetime=0.1)
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

        cache = TimedLRUCache(func=func)
        assert cache(1) == 1
        assert count[0] == 1

        cache.clear_cache()
        assert cache(1) == 1
        assert count[0] == 2


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
