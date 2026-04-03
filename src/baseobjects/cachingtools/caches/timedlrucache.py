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
from .timedcache import TimedCache, TimedCacheCallable, TimedCacheMethod


# Definitions #
# Classes #
class TimedLRUCacheCallable(TimedCacheCallable):
    """A periodically clearing Least Recently Used (LRU) cache wrapper object for a function."""

    # Instance Methods #
    # LRU Caching
    def unlimited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)

        if (cache_item := self.cache_container.get(key, SEARCHSENTINEL)) is not SEARCHSENTINEL:
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            self.cache_container[key] = item = self.cache_item_type(key=key, result=result)
            priority_link = self.priority.insert(item, 0)
            item.priority_link = priority_link
            return result

    def limited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)

        if (cache_item := self.cache_container.get(key, SEARCHSENTINEL)) is not SEARCHSENTINEL:
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            self.cache_container[key] = item = self.cache_item_type(key=key, result=result)
            if self._maxsize is not None and len(self.cache_container) <= self._maxsize:
                item.priority_link = self.priority.insert(item, 0)
            else:
                priority_link = self.priority.last_node
                old_key = priority_link.data.key

                priority_link.data = item
                item.priority_link = priority_link

                del self.cache_container[old_key]

                self.priority.shift_right()

            return result


class TimedLRUCacheMethod(TimedCacheMethod, TimedLRUCacheCallable):
    """A method class for TimedLRUCache."""

    def construct(self, func: Any | None = None, *args: Any, **kwargs: Any) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        super().construct(func, *args, **kwargs)


class TimedLRUCache(TimedLRUCacheCallable, TimedCache):
    """A function class for TimedLRUCache."""

    # Attributes #
    method_type: type[TimedLRUCacheMethod] = TimedLRUCacheMethod


# Aliases #
timed_lru_cache = TimedLRUCache
