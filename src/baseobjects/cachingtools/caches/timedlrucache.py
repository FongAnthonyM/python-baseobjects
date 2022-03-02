""" timedlrucache.py
A lru cache that periodically resets and include its instantiation decorator function.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from collections.abc import Callable
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...types_ import AnyCallable
from .timedcache import TimedCache


# Definitions #
# Classes #
class TimedLRUCache(TimedCache):
    """A periodically clearing Least Recently Used (LRU) cache wrapper object for a function.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.
        cache_item_type = The class that will create the cache items.
        priority_queue_type = The type of priority queue to hold cache item priorities.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.
        _instances: Copies of this object for specific owner instances.

        _maxsize: The max size of the lru_cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        priority: A container that keeps track of cache deletion priority.
        cache: Contains the results of the wrapped function.
        _defualt_caching_method: The default caching function to use.
        _caching_method: The designated function to handle caching.

        _call_method: The function to call when this object is called.

        _maxsize: The number of results the cache will hold before replacing results.

        priority: The object that will control the replacement of cached results.

    Args:
        func: The function to wrap.
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """

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
        cache_item = self.cache.get(key, self.sentinel)

        if cache_item is not self.sentinel:
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            self.cache[key] = item = self.cache_item_type(key=key, result=result)
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
        cache_item = self.cache.get(key, self.sentinel)

        if cache_item is not self.sentinel:
            self.priority.move_node_start(cache_item.priority_link)
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            if self.cache.__len__() <= self._maxsize:
                self.cache[key] = item = self.cache_item_type(key=key, result=result)
                priority_link = self.priority.insert(item, 0)
                item.priority_link = priority_link
            else:
                priority_link = self.priority.last_node
                old_key = priority_link.key

                item = self.cache_item_type(key=key, result=result, priority_link=priority_link)
                priority_link.data = item

                del cache_item[old_key]
                self.cache[key] = item

                self.priority.shift_right()

            return result


# Functions #
def timed_lru_cache(
    maxsize: int | None = None,
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: AnyCallable | str = "caching_call",
    collective: bool = True,
) -> Callable[[AnyCallable], TimedLRUCache]:
    """A factory to be used a decorator that sets the parameters of timed lru cache function factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed lru cache function factory.
    """

    def timed_lru_cache_factory(func: AnyCallable) -> TimedLRUCache:
        """A factory for wrapping a function with a TimedLRUCache object.

        Args:
            func: The function to wrap with a TimedLRUCache.

        Returns:
            The TimeLRUCache object which wraps the given function.
        """
        return TimedLRUCache(
            func,
            maxsize=maxsize,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            collective=collective,
        )

    return timed_lru_cache_factory
