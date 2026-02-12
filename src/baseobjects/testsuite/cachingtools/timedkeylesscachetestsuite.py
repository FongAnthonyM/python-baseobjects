"""timedkeylesscachetestsuite.py
Test suite for the TimedKeylessCache class.
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
from ...cachingtools.caches.timedkeylesscache import TimedKeylessCache
from .cachingtoolstestsuite import TimedCacheTestSuite


# Definitions #
# Classes #
class TimedKeylessCacheTestSuite(TimedCacheTestSuite):
    """Base test suite for TimedKeylessCache classes.

    This class provides common test functionality for keyless timed cache classes.
    """

    # Attributes #
    UnitTestClass: type[TimedKeylessCache] = TimedKeylessCache

    # Tests #
    def test_caching(self, *args: Any, **kwargs: Any) -> None:
        """Tests the caching behavior of the cache class (keyless)."""
        caching_func, _, get_call_count = self.create_test_caching_function(*args, **kwargs)
        result1 = caching_func(2)
        assert result1 == 4
        assert get_call_count() == 1

        # Call with different arg, returns cached result
        result2 = caching_func(3)
        assert result2 == 4  # Keyless
        assert get_call_count() == 1

    def test_keyless_caching(self, *args: Any, **kwargs: Any) -> None:
        """Tests that the cache ignores arguments (keyless behavior)."""
        # This test is now redundant with test_caching override but keeping for clarity
        self.test_caching(*args, **kwargs)
