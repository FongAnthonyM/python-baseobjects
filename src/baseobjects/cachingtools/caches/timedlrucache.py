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
from typing import Any

# Local Packages #
from ...bases import SEARCHSENTINEL
from .timedcache import TimedCache, TimedCacheInfo


# Definitions #
# Classes #
class TimedLRUCache(TimedCache):
    """A periodically clearing Least Recently Used (LRU) cache wrapper object for a function."""

    # Instance Methods #
    # LRU Caching
    def unlimited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        cache_item = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            cache_info.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = item = self.cache_item_type(key=key, result=result)
            priority_link = cache_info.priority.insert(item, 0)
            item.priority_link = priority_link
            return result

    def limited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        cache_item = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            cache_info.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = item = self.cache_item_type(key=key, result=result)
            if cache_info.maxsize is not None and len(cache_info.cache_container) <= cache_info.maxsize:
                item.priority_link = cache_info.priority.insert(item, 0)
            else:
                priority_link = cache_info.priority.last_node
                old_key = priority_link.data.key

                priority_link.data = item
                item.priority_link = priority_link

                del cache_info.cache_container[old_key]

                cache_info.priority.shift_right()

            return result


# Aliases #
timed_lru_cache = TimedLRUCache
