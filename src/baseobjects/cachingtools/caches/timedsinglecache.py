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
from dataclasses import dataclass
from time import perf_counter
from typing import Any

# Local Packages #
from ...typing import AnyCallable
from .basetimedcache import BaseTimedCache, CacheInfo


# Definitions #
# Classes #
@dataclass(slots=True)
class TimedSingleCacheInfo(CacheInfo):
    """Information about a timed single cache.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    args_key: Hashable | None = None


class TimedSingleCache(BaseTimedCache):
    """A periodically clearing single item cache wrapper for a function.

    This cache implementation stores only the most recent result. If the function is called
    with different arguments, the previous result is replaced. This is highly memory-efficient
    for scenarios where only the last result is relevant.

    Attributes:
        args_key: The generated argument key of the current cached result.
    """

    # Attributes #
    cache_info_type: type[TimedSingleCacheInfo] = TimedSingleCacheInfo

    # Properties #
    @property
    def args_key(self) -> Hashable | None:
        """The generated argument key of the current cached result."""
        return self.cache_info.args_key

    @args_key.setter
    def args_key(self, value: Hashable | None) -> None:
        self.cache_info.args_key = value

    # Magic Methods
    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method which handles the caching logic and invokes the wrapped function.

        This method first checks if caching is enabled and if the cache has expired. It then generates
        a key from the arguments and compares it with the stored key. If they differ, the wrapped
        function is called and its result replaces the previous one.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function, either from the cache or a fresh call.
        """
        instance = None
        if (reference := self._self_) is not None:
            instance = reference()

        if instance is not None:
            cache_info = self.get_instance_cache_info(instance) if self.instanced_cache else self.cache_info
        else:
            cache_info = self.cache_info

        if cache_info.is_caching:
            if cache_info.is_timed and cache_info.lifetime is not None and perf_counter() >= cache_info.expiration:
                cache_info.cache_container = None
                cache_info.args_key = None
                if cache_info.lifetime is not None:
                    cache_info.expiration = perf_counter() + cache_info.lifetime

            key = self.create_key(args, kwargs, cache_info.typed)
            if key != cache_info.args_key:
                cache_info.args_key = key
                if instance is not None:
                    try:
                        cache_info.cache_container = self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
                    except AttributeError:
                        cache_info.cache_container = self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]
                else:
                    cache_info.cache_container = self.__wrapped__(*args, **kwargs)

            return cache_info.cache_container

        if instance is not None:
            try:
                return self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
            except AttributeError:
                return self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]

        return self.__wrapped__(*args, **kwargs)

    # Cache Control
    def clear_cache(self, *args: Any, cache_info: TimedSingleCacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clears the cache and updates the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to clear.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        cache_info.cache_container = None
        cache_info.args_key = None
        super().clear_cache(*args, cache_info=cache_info, **kwargs)

    # Caching Methods
    def init_cache_info(self, cache_info: TimedSingleCacheInfo) -> None:  # type: ignore[override]
        """Initializes the cache information.

        Args:
            cache_info: The cache information to initialize.
        """
        cache_info.cache_container = None
        cache_info.args_key = None


# Aliases #
timed_single_cache = TimedSingleCache
