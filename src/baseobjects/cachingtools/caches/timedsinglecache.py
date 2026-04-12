"""timedsinglecache.py
A timed cache that holds only a single item.

This module provides the TimedSingleCache class and related components for implementing a time-based cache that
stores only a single result at a time. Unlike the standard timed cache, this implementation replaces the previous
cached result whenever a new function call with different arguments is made. This is useful for functions where
only the most recent result needs to be cached, saving memory while still providing caching benefits.
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
from collections.abc import Hashable
from time import perf_counter
from typing import Any

# Local Packages #
from ...typing import AnyCallable
from .basetimedcache import BaseTimedCache


# Definitions #
# Classes #
class TimedSingleCache(BaseTimedCache):
    """A periodically clearing single item cache wrapper for a function.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    _instanced_cache: bool = False
    args_key: Hashable | None = None

    # Instance Methods #
    # Constructors
    def __init__(self, *args: Any, init: bool = True, **kwargs: Any) -> None:
        """Initializes this object.

        Args:
            *args: Arguments for inheritance.
            init: Determines if this object will construct.
            **kwargs: Keyword arguments for inheritance.
        """
        super().__init__(*args, init=False, **kwargs)
        self.cache_method = "caching"
        if init:
            self.construct(*args, **kwargs)

    def construct(
        self,
        func: AnyCallable | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        self.args_key = None

        super().construct(  # type: ignore[misc]
            *args,
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            instanced=instanced,
            **kwargs,
        )

    # Caching Methods
    def get_args_key(self, *args: Any, **kwargs: Any) -> Any:
        """Gets the generated argument key of the current cached result.

        Args:
            *args: Arguments that could be used to determine the key.
            **kwargs: Keyword arguments that could be used to determine the key.

        Returns:
            The argument key of the cache.
        """
        if not self.instanced_cache or not args:
            return self.args_key

        instance = args[0]
        key_name = getattr(self.__wrapped__, "__name__", "") + "_args_key"

        try:
            caches = instance.__cache__
        except AttributeError:
            caches = {}
            instance.__cache__ = caches

        if (cache := caches.get(key_name, None)) is None:
            caches[key_name] = cache = {}

        return cache

    def set_args_key(self, value: Any, *args: Any, **kwargs: Any) -> None:
        """Sets the generated argument key of the current cached result.

        Args:
            value: The key to set.
            *args: Arguments that could be used to determine the key location.
            **kwargs: Keyword arguments that could be used to determine the key location.
        """
        if not self.instanced_cache or not args:
            self.args_key = value
            return

        instance = args[0]
        key_name = getattr(self.__wrapped__, "__name__", "") + "_args_key"

        try:
            cache = instance.__cache__
        except AttributeError:
            cache = {}
            instance.__cache__ = cache

        cache[key_name] = value

    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that holds a single result.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        args_key = self.get_args_key(*args, **kwargs)
        if key != args_key:
            self.set_cache_container(self.call_wrapped(*args, **kwargs), *args, **kwargs)
            self.set_args_key(key, *args, **kwargs)

        return self.get_cache_container(*args, **kwargs)

    # Cache Control
    def refresh_expiration(self) -> None:
        """Refreshes the expiration to be a lifetime later than now."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def clear_cache(self, *args: Any, **kwargs: Any) -> None:
        """Clears the cache and update the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        self.set_cache_container(None, *args, **kwargs)
        self.set_args_key(None, *args, **kwargs)
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


# Aliases #
timed_single_cache = TimedSingleCache
