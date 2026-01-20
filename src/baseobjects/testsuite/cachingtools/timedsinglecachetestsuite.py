"""timedsinglecachetestsuite.py
Test suite for the TimedSingleCache class.
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
from typing import Any, ClassVar

# Local Packages #
from ...cachingtools.caches.timedsinglecache import TimedSingleCache
from .cachingtoolstestsuite import TimedCacheTestSuite


# Definitions #
# Classes #
class TimedSingleCacheTestSuite(TimedCacheTestSuite):
    """Base test suite for TimedSingleCache classes.

    This class provides common test functionality for single item timed cache classes.
    """

    UnitTestClass: ClassVar[type[TimedSingleCache]] = TimedSingleCache

    # Tests #
    def test_single_item_replacement(self, example_functions: tuple[Any, Any]) -> None:
        """Tests that the cache holds only a single item and replaces it on new args."""
        test_function, get_call_count = example_functions
        cache = self.UnitTestClass(func=test_function)

        # First call
        assert cache(1) == 2
        assert get_call_count() == 1

        # Second call, same args -> cached
        assert cache(1) == 2
        assert get_call_count() == 1

        # Third call, different args -> replaces cache
        assert cache(2) == 4
        assert get_call_count() == 2

        # Fourth call, first args -> re-executed (because it was replaced)
        assert cache(1) == 2
        assert get_call_count() == 3

    def test_refresh_expiration(self, example_functions: tuple[Any, Any]) -> None:
        """Tests the refresh_expiration method."""
        test_function, get_call_count = example_functions
        lifetime = 0.1
        cache = self.UnitTestClass(func=test_function, lifetime=lifetime)

        assert cache(1) == 2

        # Wait almost lifetime
        time.sleep(lifetime * 0.6)

        # Refresh expiration
        cache.refresh_expiration()

        # Wait another chunk (total > original lifetime)
        time.sleep(lifetime * 0.6)

        # Should still be cached because we refreshed
        assert cache(1) == 2
        assert get_call_count() == 1

        # Wait until full expiration
        time.sleep(lifetime)

        # Should be expired now
        assert cache(1) == 2
        assert get_call_count() == 2
