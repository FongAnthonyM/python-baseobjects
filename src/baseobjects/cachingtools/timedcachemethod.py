#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedcachemethod.py
A cache for methods that periodically resets and include its instantiation decorator function.
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
class TimedCacheMethod(TimedCache):
    """A timed cache wrapper for a method which includes extra control from the object."""

    # Instance Methods
    # Object Calling
    def caching_call(self, *args, **kwargs):
        """Calls the caching function, clears the cache at certain time, and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        if self.clear_condition() or not obj.is_cache:
            self.cache_clear()

        if obj.is_cache:
            return self.caching_method(obj, *args, **kwargs)
        else:
            return self.__func__(obj, *args, **kwargs)

    def clearing_call(self, *args, **kwargs):
        """Clears the cache then calls the caching function and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        self.cache_clear()

        if obj.is_cache:
            return self.caching_method(obj, *args, **kwargs)
        else:
            return self.__func__(obj, *args, **kwargs)


# Functions #
def timed_cache_method(maxsize=None, typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed cache method factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed cache method factory.
    """

    def timed_cache_method_factory(func):
        """A factory for wrapping a method with a TimedCacheMethod object.

        Args:
            func: The function to wrap with a TimedCacheMethod.

        Returns:
            The TimeCacheMethod object which wraps the given function.
        """
        return TimedCacheMethod(func, maxsize=maxsize, typed=typed, lifetime=lifetime,
                                call_method=call_method, collective=collective)

    return timed_cache_method_factory
