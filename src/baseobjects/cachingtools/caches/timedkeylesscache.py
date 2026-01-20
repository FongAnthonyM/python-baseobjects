"""timedkeylesscache.py
A timed cache which holds only a single item and does not create a key from arguments.

This module provides the TimedKeylessCache class and related components for implementing a simplified time-based
cache that stores only a single result regardless of the input arguments. Unlike other caches, it doesn't use the
function arguments to create cache keys, making it suitable for functions where the result is expected to be the
same regardless of input, but may change over time.
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
from .timedsinglecache import TimedSingleCache, TimedSingleCacheCallable, TimedSingleCacheMethod


# Definitions #
# Classes #
class TimedKeylessCacheCallable(TimedSingleCacheCallable):
    """A periodically clearing cache wrapper object for a function that only has one result.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    args_key: bool | None = None

    # Instance Methods #
    # Caching
    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that holds a single result.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if not self.args_key:
            self.cache_container = self.__wrapped__(*args, **kwargs)  # type:ignore[misc]
            self.args_key = True

        return self.cache_container


class TimedKeylessCacheMethod(TimedKeylessCacheCallable, TimedSingleCacheMethod):
    """A method class for TimedKeylessCache."""


class TimedKeylessCache(TimedKeylessCacheCallable, TimedSingleCache):
    """A function class for TimedKeylessCache."""

    # Attributes #
    method_type: type[TimedSingleCacheMethod] = TimedKeylessCacheMethod


# Aliases #
timed_keyless_cache = TimedKeylessCache
