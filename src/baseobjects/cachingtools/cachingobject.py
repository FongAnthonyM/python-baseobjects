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

# Downloaded Libraries #

# Local Libraries #
from ..baseobject import BaseObject
from .timedsinglecache import TimedSingleCache
from  .timedkeylesscache import TimedKeylessCache
from .timedcache import TimedCache
from .basetimedcache import BaseTimedCache


# Definitions #
# Classes #
class CachingObjectMethod(BaseTimedCache):
    """A timed cache wrapper for a method which includes extra control from the object."""

    # Instance Methods #
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
            self.clear_cache()

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

        self.clear_cache()

        if obj.is_cache:
            return self.caching_method(obj, *args, **kwargs)
        else:
            return self.__func__(obj, *args, **kwargs)


class TimedSingleCacheMethod(TimedSingleCache, CachingObjectMethod):
    """A mixin class that implements both TimedSingleCache and CachingObjectMethod"""
    pass


class TimedKeylessCacheMethod(TimedKeylessCache, CachingObjectMethod):
    """A mixin class that implements both TimedKeylessCache and CachingObjectMethod"""
    pass


class TimedCacheMethod(TimedCache, CachingObjectMethod):
    """A mixin class that implements both TimedCache and CachingObjectMethod"""
    pass


class CachingObject(BaseObject):
    """An abstract class which is has functionality for methods that are caching.

    Attributes:
        is_cache: Determines if the caching methods of this object will cache.
        _caches: All the caches within this object.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, init=True):
        # Attributes #
        self.is_cache = True

        self._caches = {}

        # Object Construction #
        if init:
            self.construct()

    # Instance Methods #
    # Constructors/Destructors #
    def construct(self, *args, **kwargs):
        """Constructs this object."""
        self.get_caches()

    # Caches
    def get_caches(self):
        """Get all the caches in this object.

        Returns:
            All the cache objects within this object.
        """
        for name in dir(self):
            attribute = getattr(type(self), name, None)
            if isinstance(attribute, BaseTimedCache) or attribute is None:
                self._caches[name] = getattr(self, name)

        return self._caches

    def clear_caches(self, get_caches=False):
        """Clears all caches in this object.

        Args:
            get_caches: Determine if get_caches will be ran before clearing the caches.
        """
        if not self._caches or get_caches:
            self.get_caches()

        for cache in self._caches.values():
            cache.clear_cache()


# Functions #
def timed_single_cache_method(typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed single cache method factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed single cache method factory.
    """

    def timed_cache_method_factory(func):
        """A factory for wrapping a method with a TimedSingleCacheMethod object.

        Args:
            func: The function to wrap with a TimedSingleCacheMethod.

        Returns:
            The TimeSingleCacheMethod object which wraps the given function.
        """
        return TimedSingleCacheMethod(func, typed=typed, lifetime=lifetime,
                                      call_method=call_method, collective=collective)

    return timed_cache_method_factory


def timed_keyless_cache_method(typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed keyless cache method factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed keyless cache method factory.
    """

    def timed_cache_method_factory(func):
        """A factory for wrapping a method with a TimedKeylessCacheMethod object.

        Args:
            func: The function to wrap with a TimedKeylessCacheMethod.

        Returns:
            The TimeKeylessCacheMethod object which wraps the given function.
        """
        return TimedKeylessCacheMethod(func, typed=typed, lifetime=lifetime,
                                       call_method=call_method, collective=collective)

    return timed_cache_method_factory


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
