#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" caches.py
Cache classes and their instantiation decorator functions.
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
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _maxsize: The max size of the lru_cache.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.
        call_type: The default call method to use.
        caching_func: The caching version of the function.
        call: The function to call when this object is called.

    Args:
        func: The function to wrap.
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.
        call_type: The default call method to use.
        init: Determines if this object will construct.
    """

    # Magic Methods
    # Construction/Destruction
    def __init__(self, func, lifetime=None, maxsize=None, call_type=None, init=True):
        self.__func__ = None
        self.__self__ = None
        self._maxsize = None

        self.is_timed = True
        self.lifetime = None
        self.expiration = None
        self.call_type = "caching_call"

        self.caching_func = None
        self.call = None

        if init:
            self.construct(func=func, lifetime=lifetime, maxsize=maxsize, call_type=call_type)

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
    def construct(self, func=None, lifetime=None, maxsize=None, call_type=None):
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            lifetime: The period between cache resets in seconds.
            maxsize: The max size of the lru_cache.
            call_type: The default call method to use.
        """
        if maxsize is not None:
            self._maxsize = maxsize

        if lifetime is not None:
            self.lifetime = lifetime
        self.expiration = perf_counter()

        if call_type is not None:
            self.call_type = call_type

        self.set_call(call_type=self.call_type)

        if func is not None:
            self.__func__ = func
            self.caching_func = lru_cache(maxsize=maxsize)(func)
            update_wrapper(self, self.__func__)

    # Object Calling
    def set_call(self, call_type):
        """Set the call method of this object to either the caching wrapper or the original function.

        Args:
            call_type: The name of the method to call when this object is called.
        """
        call_type = call_type.lower()
        if call_type == "caching_call":
            self.call = self.caching_call
        elif call_type == "clearing_call":
            self.call = self.clearing_call
        else:
            self.cache_clear()
            self.call = self.__func__

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

    def clearing_call(self, *args, **kwargs):
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_func.
        """
        self.cache_clear()

        return self.caching_func(*args, **kwargs)

    # Binding
    def bind(self, instance, name=None):
        """Binds this object to another object to give this object method functionality.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.
        """
        self.__self__ = instance
        if name is not None:
            setattr(instance, name, self)

    def bind_to_deepcopy(self, instance, name=None, memo={}):
        """Creates a deepcopy of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            The new bound deepcopy of this object.
        """
        new_obj = self.deepcopy(memo=memo)
        new_obj.bind(instance, name=name)
        return new_obj

    # Caching
    def clear_condition(self, *args, **kwargs):
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

    def cache_clear(self):
        """Clear the cache and update the expiration of the cache."""
        self.caching_func.cache_clear()
        self.expiration = perf_counter() + self.lifetime

    # Copying
    def deepcopy(self, memo={}):
        """Creates a deep copy of this object.

        Args:
            memo (dict): A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        new_obj = super().deepcopy(memo=memo)
        TimedLRUCache.construct(new_obj, func=new_obj.__func__)

        return new_obj


class TimedCacheMethod(TimedLRUCache):
    """A timed least recently used cache wrapper for a method which includes extra control from the object."""

    # Instance Methods
    # Object Calling
    def caching_call(self, *args, **kwargs):
        """Calls the caching function, clears the cache at certain time, and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_func.
        """
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        if self.clear_condition() or not obj.is_cache:
            self.cache_clear()

        if obj.is_cache:
            return self.caching_func(obj, *args, **kwargs)
        else:
            return self.__func__(obj, *args, **kwargs)

    def clearing_call(self, *args, **kwargs):
        """Clears the cache then calls the caching function and allows the owning object to override.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_func.
        """
        if self.__self__ is not None:
            obj = self.__self__
        else:
            obj = args[0]

        self.cache_clear()

        if obj.is_cache:
            return self.caching_func(obj, *args, **kwargs)
        else:
            return self.__func__(obj, *args, **kwargs)


# Functions #
def timed_lru_cache(lifetime=None, maxsize=None, call_type=None):
    """A factory to be used a decorator that sets the parameters of timed lru cache function factory.

    Args:
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.
        call_type: The default call method to use.

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
        return TimedLRUCache(func, lifetime=lifetime, maxsize=maxsize, call_type=call_type)

    return timed_lru_cache_factory


def timed_cache_method(lifetime=None, maxsize=None, call_type=None):
    """A factory to be used a decorator that sets the parameters of timed lru cache method factory.

    Args:
        lifetime: The period between cache resets in seconds.
        maxsize: The max size of the lru_cache.
        call_type: The default call method to use.

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
        return TimedCacheMethod(method, lifetime=lifetime, maxsize=maxsize, call_type=call_type)

    return timed_cache_method_factory
