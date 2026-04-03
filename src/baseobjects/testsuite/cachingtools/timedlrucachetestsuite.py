"""timedlrucachetestsuite.py
Test suite for the TimedLRUCache class.
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
from typing import Any

# Local Packages #
from ...cachingtools.caches.timedlrucache import TimedLRUCache
from .cachingtoolstestsuite import TimedCacheTestSuite


# Definitions #
# Classes #
class TimedLRUCacheTestSuite(TimedCacheTestSuite):
    """Base test suite for TimedLRUCache classes.

    This class provides common test functionality for LRU timed cache classes.
    """

    # Attributes #
    UnitTestClass: type[TimedLRUCache] = TimedLRUCache

    # Tests #
    def test_lru_eviction(self, example_functions: tuple[Any, Any]) -> None:
        """Tests the LRU eviction policy."""
        test_function, get_call_count = example_functions
        cache = self.UnitTestClass(func=test_function, maxsize=2)

        # Fill cache
        # Adds 1
        assert cache(1) == 2
        assert get_call_count() == 1

        # Adds 2
        assert cache(2) == 4
        assert get_call_count() == 2
        assert len(cache) == 2

        # Access 1 to make it recently used (MRU)
        assert cache(1) == 2
        assert get_call_count() == 2  # Cached

        # Adds 3, should evict 2 (LRU)
        assert cache(3) == 6
        assert len(cache) == 2
        assert get_call_count() == 3

        # Checks that 1 is still cached
        assert cache(1) == 2
        assert get_call_count() == 3  # Did not increase

        # Checks that 2 is evicted (should re-calculate)
        assert cache(2) == 4
        assert get_call_count() == 4
