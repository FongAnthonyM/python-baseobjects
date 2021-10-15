#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedlrucache.py
A lru cache that periodically resets and include its instantiation decorator function.
"""
# Package Header #
from ..__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Default Libraries #

# Downloaded Libraries #

# Local Libraries #
from .timedcache import TimedCache


# Definitions #
# Classes #
class TimedLRUCache(TimedCache):
    """A least recently used cache wrapper object for a function which resets its cache periodically.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _maxsize: The max size of the lru_cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        priority: A container that keeps track of cache deletion priority.
        cache: Contains the results of the wrapped function.
        caching_method: The designated function to handle caching.

        call_type: The default call method to use.
        call: The function to call when this object is called.

    Args:
        func: The function to wrap.
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.
        call_type: The default call method to use.
        typed: Determines if the function's arguments are type sensitive for caching.
        init: Determines if this object will construct.
    """

    # Instance Methods
    # LRU Caching
    def unlimited_cache(self, *args, **kwargs):
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

    def limited_cache(self, *args, **kwargs):
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
def timed_lru_cache(maxsize=None, typed=False, lifetime=None, call_method="cache_call", collective=True):
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

    def timed_lru_cache_factory(func):
        """A factory for wrapping a function with a TimedLRUCache object.

        Args:
            func: The function to wrap with a TimedLRUCache.

        Returns:
            The TimeLRUCache object which wraps the given function.
        """
        return TimedLRUCache(func, maxsize=maxsize, typed=typed, lifetime=lifetime,
                             call_method=call_method, collective=collective)

    return timed_lru_cache_factory

