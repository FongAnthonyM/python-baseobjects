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
from time import perf_counter
from typing import Any

# Local Packages #
from .timedsinglecache import TimedSingleCache, TimedSingleCacheInfo


# Definitions #
# Classes #
class TimedKeylessCache(TimedSingleCache):
    """A periodically clearing cache wrapper object for a function that only has one result.

    This cache implementation stores only a single result regardless of the input arguments.
    It is useful for functions whose results change only over time and are independent of
    the arguments provided.
    """

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method which handles the caching logic and invokes the wrapped function.

        This method first checks if caching is enabled and if the cache has expired. It stores
        a single result and ignores all arguments when checking if the result is already cached.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function, either from the cache or a fresh call.
        """
        instance = None
        if (reference := self._self_) is not None:
            instance = reference()

        if instance is not None:
            cache_info = self.get_instance_cache_info(instance) if self.instanced_cache else self.cache_info
        else:
            cache_info = self.cache_info

        if cache_info.is_caching:
            if cache_info.is_timed and cache_info.lifetime is not None and perf_counter() >= cache_info.expiration:
                cache_info.cache_container = None
                cache_info.args_key = None
                if cache_info.lifetime is not None:
                    cache_info.expiration = perf_counter() + cache_info.lifetime

            if not cache_info.args_key:
                cache_info.args_key = True
                if instance is not None:
                    try:
                        cache_info.cache_container = self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
                    except AttributeError:
                        cache_info.cache_container = self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]
                else:
                    cache_info.cache_container = self.__wrapped__(*args, **kwargs)

            return cache_info.cache_container

        if instance is not None:
            try:
                return self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
            except AttributeError:
                return self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]

        return self.__wrapped__(*args, **kwargs)

    # Cache Control
    def clear_cache(self, *args: Any, cache_info: TimedSingleCacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clears the cache and updates the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to clear.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        cache_info.cache_container = None
        cache_info.args_key = None
        super().clear_cache(*args, cache_info=cache_info, **kwargs)
timed_keyless_cache = TimedKeylessCache
