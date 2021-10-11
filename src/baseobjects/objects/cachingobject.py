#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" cachingobject.py
An abstract class which creates properties for this class automatically.
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
from functools import lru_cache, update_wrapper
from time import perf_counter

# Downloaded Libraries #

# Local Libraries #
from ..baseobject import BaseObject


# Definitions #
# Classes #
class TimedLRUCache(BaseObject):
    """A least recently used cache wrapper object for a function which resets its cache periodically.

    Attributes:
        _maxsize: The max size of the lru_cache.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.
        func: The original function to wrap.
        caching_func: The caching version of the function.
        call: The function to call when this object is called.

    Args:
        func:  The function to wrap.
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.
        init: Determines if this object will construct.
    """

    # Magic Methods
    # Construction/Destruction
    def __init__(self, func, lifetime=None, maxsize=None, init=True):
        self._maxsize = None

        self.is_timed = True
        self.lifetime = None
        self.expiration = None

        self.func = None
        self.caching_func = None
        self.call = None

        if init:
            self.construct(func=func, lifetime=lifetime, maxsize=maxsize)

    # Callable
    def __call__(self, *args, **kwargs):
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.call(*args, **kwargs)

    # Instance Methods
    # Constructors
    def construct(self, func=None, lifetime=None, maxsize=None):
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            lifetime: The period between cache resets in seconds.
            maxsize: The max size of the lru_cache.
        """
        if maxsize is not None:
            self._maxsize = maxsize

        if lifetime is not None:
            self.lifetime = lifetime
        self.expiration = perf_counter()

        if func is not None:
            self.func = func
            self.caching_func = lru_cache(maxsize=maxsize)(func)
            update_wrapper(self, self.caching_func)

    # Object Calling
    def set_call(self, caching=True):
        """Set the call method of this object to either the caching wrapper or the original function.

        Args:
            caching: Determines if the caching wrapper will be used or the original function.
        """
        if caching:
            self.call = self.caching_call
        else:
            self.call = self.func

    def caching_call(self, *args, **kwargs):
        """Calls the caching function and clears the cache at certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_func.
        """
        if self.clear_condition():
            self.cache_clear()

        return self.caching_func(*args, **kwargs)

    # Caching
    def clear_condition(self, *args, **kwargs):
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return (not self.is_timed or self.lifetime is None) and perf_counter() >= self.expiration

    def cache_clear(self):
        """Clear the cache and update the expiration of the cache."""
        self.caching_func.cache_clear()
        self.expiration = perf_counter() + self.lifetime


class TimedCacheMethod(TimedLRUCache):
    """A timed least recently used cache wrapper for a method which includes extra control from the object."""

    # Instance Methods
    # Object Calling
    def caching_call(self, obj, *args, **kwargs):
        """Calls the caching function, clears the cache at certain time, and allows the owning object to override.

        Args:
            obj: The object the whose method is being wrapped.
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_func.
        """
        if self.clear_condition(obj) or not obj.is_cache:
            self.cache_clear()

        if obj.is_cache:
            return self.caching_func(obj, *args, **kwargs)
        else:
            return self.func(obj, *args, **kwargs)


class CachingObject(BaseObject):
    """An abstract class which is has functionality for methods that are caching.

    Attributes:
        is_cache: Determines if the caching methods of this object will cache.
    """

    # Magic Methods
    # Construction/Destruction
    def __init__(self):
        self.is_cache = True


# Functions #
def timed_lru_cache(lifetime=None, maxsize=None):
    """A factory to be used a decorator that sets the parameters of timed lru cache function factory.

    Args:
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.

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
        return TimedLRUCache(func, lifetime=lifetime, maxsize=maxsize)

    return timed_lru_cache_factory


def timed_cache_method(lifetime=None, maxsize=None):
    """A factory to be used a decorator that sets the parameters of timed lru cache method factory.

    Args:
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.

    Returns:
        The parameterized timed lru cache method factory.
    """
    def timed_cache_method_factory(method):
        """A factory for wrapping a method with a TimedCacheMethod object.

            Args:
                method: The method to wrap with a TimedCacheMethod.

            Returns:
                The TimeCacheMethod object which wraps the given method.
            """
        return TimedCacheMethod(method, lifetime=lifetime, maxsize=maxsize)

    return timed_cache_method_factory
