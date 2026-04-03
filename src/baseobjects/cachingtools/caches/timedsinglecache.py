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
from .basetimedcache import BaseTimedCache, BaseTimedCacheCallable, BaseTimedCacheMethod


# Definitions #
# Classes #
class TimedSingleCacheCallable(BaseTimedCacheCallable):
    """A periodically clearing single item cache wrapper for a function.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    _cache_method: str = "caching"
    _instanced_cache: bool = False
    args_key: Hashable | None = None

    # Instance Methods #
    # Constructors
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

        super().construct(
            func=func,
            typed=typed,
            lifetime=lifetime,
            call_method=call_method,
            instanced=instanced,
            *args,
            **kwargs,
        )

    # Caching Methods
    def caching(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that holds a single result.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        if key != self.args_key:
            self.cache_container = self.call_wrapped(*args, **kwargs)
            self.args_key = key

        return self.cache_container

    # Cache Control
    def refresh_expiration(self) -> None:
        """Refreshes the expiration to be a lifetime later than now."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def clear_cache(self) -> None:
        """Clears the cache and update the expiration of the cache."""
        self.cache_container = None
        self.args_key = None
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime


class TimedSingleCacheMethod(BaseTimedCacheMethod, TimedSingleCacheCallable):
    """A method class for TimedSingleCache."""

    def construct(self, func: Any | None = None, *args: Any, **kwargs: Any) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        self.args_key = None
        super().construct(func, *args, **kwargs)


class TimedSingleCache(TimedSingleCacheCallable, BaseTimedCache):
    """A function class for TimedSingleCache."""

    # Attributes #
    method_type: type[BaseTimedCacheMethod] = TimedSingleCacheMethod


# Aliases #
timed_single_cache = TimedSingleCache
