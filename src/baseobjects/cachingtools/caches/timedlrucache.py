"""timedlrucache.py
A Least Recently Used (LRU) cache that periodically resets.

This module provides the TimedLRUCache class and related components for implementing a time-based Least Recently Used
(LRU) cache. It extends the basic timed cache functionality with an LRU eviction policy, which removes the least
recently accessed items when the cache reaches its maximum size. This combines the benefits of time-based expiration
with efficient memory usage through the LRU algorithm.
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
from collections import OrderedDict
from time import perf_counter
from typing import Any

# Local Packages #
from ...bases import SEARCHSENTINEL
from .timedcache import TimedCache, TimedCacheInfo


# Definitions #
# Classes #
class TimedLRUCache(TimedCache):
    """A periodically clearing Least Recently Used (LRU) cache wrapper object for a function.

    This cache implementation stores multiple results based on the function's arguments. It uses
    a Least Recently Used (LRU) eviction policy to manage the cache size, ensuring that the most
    frequently accessed items are retained when the cache reaches its maximum size.
    """

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method which handles the caching logic and invokes the wrapped function.

        This method first checks if caching is enabled and if the cache has expired. It then attempts
        to retrieve a result from the cache using a key generated from the arguments. If the result
        is found, it is moved to the end of the cache (marking it as most recently used). If not
        found, it calls the wrapped function, stores the result, and performs LRU eviction if needed.

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
                self.clear_cache(instance, cache_info=cache_info)

            # Fast path for key creation
            if not cache_info.typed and not kwargs:
                if len(args) == 1:
                    key = args[0]
                    if type(key) not in {int, str}:
                        key = args
                else:
                    key = args
            else:
                key = self.create_key(args, kwargs, cache_info.typed)

            result = cache_info.cache_container.get(key, SEARCHSENTINEL)
            if result is not SEARCHSENTINEL:
                cache_info.cache_container.move_to_end(key)
                return result

            if instance is not None:
                try:
                    result = self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
                except AttributeError:
                    result = self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]
            else:
                result = self.__wrapped__(*args, **kwargs)

            cache_info.cache_container[key] = result
            if cache_info.maxsize is not None and len(cache_info.cache_container) > cache_info.maxsize:
                cache_info.cache_container.popitem(last=False)
            return result

        if instance is not None:
            try:
                return self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
            except AttributeError:
                return self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]

        return self.__wrapped__(*args, **kwargs)

    # Instance Methods #
    # Constructors
    def init_cache_info(self, cache_info: TimedCacheInfo) -> None:
        """Initializes the cache information.

        Args:
            cache_info: The cache information to initialize.
        """
        super().init_cache_info(cache_info)
        cache_info.cache_container = OrderedDict()

    # LRU Caching
    def unlimited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caches results without any limit on the number of items, maintaining LRU order.

        Args:
            *args: Positional arguments for the wrapped function.
            cache_info: The cache information to use. If None, it will be retrieved.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        result = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if result is not SEARCHSENTINEL:
            cache_info.cache_container.move_to_end(key)
            return result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = result
            return result

    def limited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caches results and performs LRU eviction when the maximum size is reached.

        Args:
            *args: Positional arguments for the wrapped function.
            cache_info: The cache information to use. If None, it will be retrieved.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        result = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if result is not SEARCHSENTINEL:
            cache_info.cache_container.move_to_end(key)
            return result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = result
            if cache_info.maxsize is not None and len(cache_info.cache_container) > cache_info.maxsize:
                cache_info.cache_container.popitem(last=False)
            return result


# Aliases #
timed_lru_cache = TimedLRUCache
