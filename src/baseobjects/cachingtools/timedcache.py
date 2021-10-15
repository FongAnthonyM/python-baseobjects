#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedcache.py
A cache that periodically resets and include its instantiation decorator function.
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
from functools import update_wrapper
from time import perf_counter

# Downloaded Libraries #

# Local Libraries #
from ..baseobject import BaseObject
from ..objects import CirularDoublyLinkedContainer


# Definitions #
# Classes #
class _HashedSeq(list):
    """This class guarantees that hash() will be called no more than once per element.
    """
    __slots__ = "hashvalue"

    def __init__(self, tuple_, hash_=hash):
        self[:] = tuple_
        self.hashvalue = hash_(tuple_)

    def __hash__(self):
        return self.hashvalue


class CacheItem(BaseObject):
    """An item within a cache which contains the result and a link to priority.
    """
    __slots__ = ["key", "result", "priority_link"]

    # Magic Methods
    # Construction/Destruction
    def __init__(self, key=None, result=None, priority_link=None):
        self.priority_link = priority_link

        self.key = key
        self.result = result


class TimedCache(BaseObject):
    """A cache wrapper object for a function which resets its cache periodically.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.

        _maxsize: The max size of the lru_cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        priority: A container that keeps track of cache deletion priority.
        cache: Contains the results of the wrapped function.
        caching_method: The designated function to handle caching.

        _call_method: The function to call when this object is called.

    Args:
        func:  The function to wrap.
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """
    sentinel = object()
    cache_item_type = CacheItem

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, func=None, maxsize=None, typed=False, lifetime=None,
                 call_method="cache_call", collective=True,  init=True):
        self.__func__ = None
        self.__self__ = None
        self._is_collective = True
        self.__get_method = self.get_self
        self._instances = {}

        self._maxsize = None
        self.typed = False
        self.is_timed = True
        self.lifetime = None
        self.expiration = None

        self.priority = CirularDoublyLinkedContainer()
        self.cache = {}
        self._caching_method = self.unlimited_cache

        self._call_method = None

        if init:
            self.construct(func=func, lifetime=lifetime, maxsize=maxsize, typed=typed,
                           call_method=call_method, collective=collective)

    @property
    def is_collective(self):
        return self._is_collective

    @is_collective.setter
    def is_collective(self, value):
        if value is True:
            self.__get_method = self.get_self
        else:
            self.__get_method = self.get_subinstance
        self._is_collective = value

    @property
    def _get_method(self):
        return self.__get_method

    @_get_method.setter
    def _get_method(self, value):
        self.set_get_method(value)

    @property
    def maxsize(self):
        """The cache's max size and when updated it changes the cache to its optimal handle function."""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value):
        self.set_maxsize(value)

    @property
    def caching_method(self):
        return self._caching_method

    @caching_method.setter
    def caching_method(self, value):
        self.set_caching_method(value)

    @property
    def call_method(self):
        return self._call_method

    @call_method.setter
    def call_method(self, value):
        self.set_call_method(value)

    # Descriptors
    def __get__(self, instance, owner=None):
        return self._get_method(instance, owner=owner)

    # Callable
    def __call__(self, *args, **kwargs):
        """The call magic method for this object.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The results of the wrapped function.
        """
        return self.call_method(*args, **kwargs)

    # Container Methods
    def __len__(self):
        return self.get_length()

    # Instance Methods #
    # Constructors
    def construct(self, func=None, maxsize=None, typed=None, lifetime=None,  call_method=None, collective=None):
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            maxsize: The max size of the cache.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            collective: Determines if the cache is collective for all method bindings or for each instance.
        """
        if maxsize is not None:
            self.maxsize = maxsize

        if lifetime is not None:
            self.lifetime = lifetime
        self.expiration = perf_counter()

        if typed is not None:
            self.typed = typed

        if call_method is not None:
            self.set_call_method(call_method)

        if collective is not None:
            self.is_collective = collective

        if func is not None:
            self.__func__ = func
            update_wrapper(self, self.__func__)

    # Descriptor
    def set_get_method(self, method):
        if isinstance(method, str):
            method = getattr(self, method)

        self.__get_method = method

    def get_self(self, instance, owner=None):
        if instance is not None:
            self.bind(instance)
        return self

    def get_subinstance(self, instance, owner=None):
        if instance is None:
            return self
        else:
            bound = self._instances.get(instance, self.sentinel)
            if bound is self.sentinel:
                self._instances[instance] = bound = self.bind_to_new(instance=instance)
            return bound

    # Object Calling
    def set_call_method(self, method):
        """Set the call method of this object to either the caching wrapper or the original function.

        Args:
            method: The name of the method to call when this object is called.
        """
        if method is None:
            method = self.__func__
        elif isinstance(method, str):
            method = getattr(self, method)

        self._call_method = method

    def caching_call(self, *args, **kwargs):
        """Calls the caching function and clears the cache at certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        if self.clear_condition():
            self.cache_clear()

        return self.caching_method(*args, **kwargs)

    def clearing_call(self, *args, **kwargs):
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        self.cache_clear()

        return self.caching_method(*args, **kwargs)

    def clear_condition(self, *args, **kwargs):
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

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

    def bind_to_new(self, instance, name=None):
        """Creates a deepcopy of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            name: The name of the attribute this object will bind to in the other object.

        Returns:
            The new bound deepcopy of this object.
        """
        if self._call_method.__name__ in dir(self):
            call_method = self._call_method.__name__
        else:
            call_method = self._call_method

        new_obj = type(self)(func=self.__func__, maxsize=self.maxsize, typed=self.typed, lifetime=self.lifetime,
                             call_method=call_method, collective=self._is_collective)
        new_obj.bind(instance, name=name)
        return new_obj

    # Caching
    def create_key(self, args, kwds, typed, kwd_mark=(object(),), fasttypes={int, str},
                   tuple_=tuple, type_=type, len_=len):
        """Make a cache key from optionally typed positional and keyword arguments.

        The key is constructed in a way that is flat as possible rather than
        as a nested structure that would take more memory.

        If there is only a single argument and its data type is known to cache
        its hash value, then that argument is returned without a wrapper.  This
        saves space and improves lookup speed.

        """
        # All of code below relies on kwds preserving the order input by the user.
        # Formerly, we sorted() the kwds before looping.  The new way is *much*
        # faster; however, it means that f(x=1, y=2) will now be treated as a
        # distinct call from f(y=2, x=1) which will be cached separately.
        key = args
        if kwds:
            key += kwd_mark
            for item in kwds.items():
                key += item
        if typed:
            key += tuple_(type_(v) for v in args)
            if kwds:
                key += tuple_(type_(v) for v in kwds.values())
        elif len_(key) == 1 and type_(key[0]) in fasttypes:
            return key[0]
        return _HashedSeq(key)

    def set_maxsize(self, value):
        """Change the cache's max size to a new value and updates the cache to its optimal handle function.

        Args:
            value: The new max size of the cache.
        """
        if value is None:
            self.caching_method = self.unlimited_cache
        elif value == 0:
            self.caching_method = self.no_cache
        else:
            self.caching_method = self.limited_cache

        self._maxsize = value

    def poll(self):
        return self.cache.__len__() <= self._maxsize

    def get_length(self):
        return self.cache.__len__()

    def no_cache(self, *args, **kwargs):
        """A direct call to wrapped function with no caching.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__func__(*args, **kwargs)

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
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            self.cache[key] = self.cache_item_type(key=key, result=result)
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
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)
            if self.cache.__len__() <= self._maxsize:
                self.cache[key] = self.cache_item_type(result=result)
            return result

    def set_caching_method(self, method):
        if isinstance(method, str):
            method = getattr(self, method)

        self._caching_method = method

    def cache_clear(self):
        """Clear the cache and update the expiration of the cache."""
        self.cache.clear()
        self.priority.clear()
        self.expiration = perf_counter() + self.lifetime


# Functions #
def timed_cache(maxsize=None, typed=False, lifetime=None, call_method="cache_call", collective=True):
    """A factory to be used a decorator that sets the parameters of timed cache function factory.

    Args:
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed cache function factory.
    """

    def timed_cache_factory(func):
        """A factory for wrapping a function with a TimedCache object.

        Args:
            func: The function to wrap with a TimedCache.

        Returns:
            The TimeCache object which wraps the given function.
        """
        return TimedCache(func, maxsize=maxsize, typed=typed, lifetime=lifetime,
                          call_method=call_method, collective=collective)

    return timed_cache_factory
