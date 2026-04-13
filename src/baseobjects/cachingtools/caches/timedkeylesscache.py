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
from .timedsinglecache import TimedSingleCache, TimedSingleCacheInfo


# Definitions #
# Classes #
class TimedKeylessCache(TimedSingleCache):
    """A periodically clearing cache wrapper object for a function that only has one result."""

    # Instance Methods #
    # Constructors
    def construct(
        self,
        func: Any | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        super().construct(  # type: ignore[misc]
            *args,
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            instanced=instanced,
            **kwargs,
        )

    # Caching
    def caching(self, *args: Any, cache_info: TimedSingleCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caching that holds a single result.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        if not cache_info.args_key:
            cache_info.cache_container = self.call_wrapped(*args, **kwargs)
            cache_info.args_key = True

        return cache_info.cache_container


# Aliases #
timed_keyless_cache = TimedKeylessCache
