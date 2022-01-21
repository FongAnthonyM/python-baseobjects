#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" timedkeylesscache.py
A timed cache that only hold a single item and does not create a key from arguments.
"""
# Package Header #
from ...__header__ import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #
from collections.abc import Callable
from time import perf_counter
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...types_ import AnyCallable
from .timedsinglecache import TimedSingleCache


# Definitions #
# Classes #
class TimedKeylessCache(TimedSingleCache):
    """A periodically clearing cache wrapper object for a function that only has one result.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.
        cache_item_type = The class that will create the cache items.
        priority_queue_type = The type of priority queue to hold cache item priorities.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.
        _instances: Copies of this object for specific owner instances.

        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        cache: Contains the results of the wrapped function.
        _defualt_caching_method: The default caching function to use.
        _caching_method: The designated function to handle caching.

        _call_method: The function to call when this object is called.

        args_key: The flag that notes the cache is occupied.

    Args:
        func: The function to wrap.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        typed: bool = False,
        lifetime: int | float | None = None,
        call_method: AnyCallable | str = "caching_call",
        collective: bool = True,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # New Attributes #
        self.args_key: bool | None = None

        # Object Construction #
        if init:
            self.construct(
                func=func,
                lifetime=lifetime,
                typed=typed,
                call_method=call_method,
                collective=collective,
            )

    # Instance Methods #
    # Caching
    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if not self.args_key:
            self.cache = self.__func__(*args, **kwargs)
            self.args_key = True

        return self.cache

    def cache_clear(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        self.cache = None
        self.args_key = False
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


# Functions #
def timed_keyless_cache(
    typed: bool = False,
    lifetime: int | float | None = None,
    call_method: AnyCallable | str = "caching_call",
    collective: bool = True,
) -> Callable[[AnyCallable], TimedKeylessCache]:
    """A factory to be used a decorator that sets the parameters of timed keyless cache function factory.

    Args:
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.

    Returns:
        The parameterized timed keyless cache function factory.
    """

    def timed_keyless_cache_factory(func: AnyCallable) -> TimedKeylessCache:
        """A factory for wrapping a function with a TimedKeylessCache object.

        Args:
            func: The function to wrap with a TimedKeylessCache.

        Returns:
            The TimeKeylessCache object which wraps the given function.
        """
        return TimedKeylessCache(
            func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            collective=collective,
        )

    return timed_keyless_cache_factory
