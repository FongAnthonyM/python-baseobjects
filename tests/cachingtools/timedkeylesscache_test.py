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
# Standard Libraries #
import time

# Third-Party Packages #
import pytest

# Source Packages #
from baseobjects.cachingtools.caches.timedkeylesscache import TimedKeylessCache


# Definitions #
# Classes #
class TestTimedKeylessCache:
    """Test the TimedKeylessCache class."""

    def test_keyless_cache_behavior(self):
        """Tests that TimedKeylessCache ignores arguments."""
        count = [0]
        def func(*args, **kwargs):
            count[0] += 1
            return count[0]

        cache = TimedKeylessCache(func=func)

        assert cache() == 1
        assert count[0] == 1

        # Second call -> HIT
        assert cache() == 1
        assert count[0] == 1

        # Call with arguments -> STILL HIT (it's keyless)
        assert cache(1, 2, a=3) == 1
        assert count[0] == 1

    def test_expiration(self):
        """Tests expiration of TimedKeylessCache."""
        count = [0]
        def func():
            count[0] += 1
            return count[0]

        cache = TimedKeylessCache(func=func, lifetime=0.1)
        assert cache() == 1
        assert count[0] == 1

        time.sleep(0.15)
        assert cache() == 2
        assert count[0] == 2

    def test_clear_cache(self):
        """Tests clear_cache method."""
        count = [0]
        def func():
            count[0] += 1
            return count[0]

        cache = TimedKeylessCache(func=func)
        assert cache() == 1
        assert count[0] == 1

        cache.clear_cache()
        assert cache() == 2
        assert count[0] == 2


# Main #
if __name__ == "__main__":
    pytest.main(["-v", "-s"])
