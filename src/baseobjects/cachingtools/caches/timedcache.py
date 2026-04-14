"""timedcache.py
A cache that periodically resets and include its instantiation decorator function.

This module provides the TimedCache class and related components for implementing a time-based cache with multiple
items. It includes TimedCache and TimedCacheMethod classes that wrap functions and methods to provide caching
functionality with automatic expiration after a specified lifetime. The cache can also be limited by size, with a
configurable replacement policy.
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
from dataclasses import dataclass
from time import perf_counter
from typing import Any

# Local Packages #
from ...bases import SEARCHSENTINEL
from ...collections import CircularDoublyLinkedContainer
from ...typing import AnyCallable
from .basetimedcache import BaseTimedCache, CacheInfo


# Definitions #
# Classes #
@dataclass(slots=True)
class TimedCacheInfo(CacheInfo):
    """Information about a timed cache.

    Attributes:
        maxsize: The maximum number of items the cache can hold.
    """

    # Attributes #
    cache_method: str = "unlimited_cache"
    maxsize: int | None = None


class TimedCache(BaseTimedCache):
    """A periodically clearing multiple item cache wrapper object for a function.

    This cache implementation stores multiple results based on the function's arguments. It supports
    optional maximum size limits and time-based expiration (TTL). When the cache is limited and reaches its
    maximum size, it can be configured with different replacement policies, though the default `TimedCache`
    does not automatically evict old items unless a specific policy (like LRU) is used or it is manually cleared.

    Attributes:
        cache_info_type: The type of cache information to use for this cache.
    """

    # Attributes #
    cache_info_type: type[TimedCacheInfo] = TimedCacheInfo

    # Properties #
    @property
    def maxsize(self) -> int | None:
        """The cache's max size and when updated it changes the cache to its optimal handle function."""
        return self.cache_info.maxsize

    @maxsize.setter
    def maxsize(self, value: int | None) -> None:
        self.set_maxsize(value)

    @property
    def priority_queue_type(self) -> type[CircularDoublyLinkedContainer]:
        """The priority queue type used for cache item management."""
        return self.cache_info.priority_queue_type

    @priority_queue_type.setter
    def priority_queue_type(self, value: type[CircularDoublyLinkedContainer]) -> None:
        self.cache_info.priority_queue_type = value

    @property
    def priority(self) -> Any:
        """The priority queue instance used for cache item management."""
        return self.cache_info.priority

    @priority.setter
    def priority(self, value: Any) -> None:
        self.cache_info.priority = value

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method which handles the caching logic and invokes the wrapped function.

        This method first checks if caching is enabled and if the cache has expired. It then attempts
        to retrieve a result from the cache using a key generated from the arguments. If the result
        is not in the cache, it calls the wrapped function and stores the result if appropriate.

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
                self.clear_cache(instance, cache_info=cache_info)

            # Fast path for key creation
            if not cache_info.typed and not kwargs:
                if len(args) == 1:
                    key = args[0]
                    if type(key) not in {int, str}:
                        key = args
                else:
                    key = args
            else:
                key = self.create_key(args, kwargs, cache_info.typed)

            result = cache_info.cache_container.get(key, SEARCHSENTINEL)
            if result is not SEARCHSENTINEL:
                return result

            if instance is not None:
                try:
                    result = self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
                except AttributeError:
                    result = self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]
            else:
                result = self.__wrapped__(*args, **kwargs)

            if cache_info.cache_method == "unlimited_cache":
                cache_info.cache_container[key] = result
            elif cache_info.maxsize is not None and len(cache_info.cache_container) < cache_info.maxsize:
                cache_info.cache_container[key] = result
            return result

        if instance is not None:
            try:
                return self.__wrapped__.__get__(instance, self.__owner__)(*args, **kwargs)  # type: ignore[misc]
            except AttributeError:
                return self.__wrapped__(instance, *args, **kwargs)  # type: ignore[misc]

        return self.__wrapped__(*args, **kwargs)

    def __init__(
        self,
        func: AnyCallable | None = None,
        maxsize: int | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            func: The function to wrap. If None, a function should be provided later via construct.
            maxsize: The maximum number of cached results to retain. If None, the cache is unlimited.
            typed: If True, cache keys are sensitive to the types of arguments.
            lifetime: The number of seconds before the cache automatically clears. If None, no timed clearing occurs.
            call_method: The default call method name to use for invoking the wrapped function.
            instanced: If True, the cache is stored per-instance when bound as a method.
            *args: Additional positional arguments forwarded to the parent initializer/constructor.
            init: If True, call construct to finish initialization.
            **kwargs: Additional keyword arguments forwarded to the parent initializer/constructor.
        """
        # Parent Initialization #
        super().__init__(func=func, init=False, *args, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                func=func,
                maxsize=maxsize,
                typed=typed,
                lifetime=lifetime,
                call_method=call_method,
                instanced=instanced,
                *args,
                **kwargs,
            )

    # Container Methods
    def __len__(self) -> int:
        """The method that gets this object's length.

        Returns:
            int: The number of items currently in the cache.
        """
        return self.get_length()

    # Instance Methods #
    # Constructors
    def construct(  # type: ignore[override]
        self,
        func: AnyCallable | None = None,
        maxsize: int | None = None,
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
            maxsize: The max size of the cache.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if maxsize is not None:
            self.maxsize = maxsize

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
    def unlimited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caches results without any limit on the number of items.

        Args:
            *args: Positional arguments for the wrapped function.
            cache_info: The cache information to use. If None, it will be retrieved.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        result = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if result is not SEARCHSENTINEL:
            return result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = result
            return result

    def limited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caches results but stops caching new items when the maximum size is reached.

        Args:
            *args: Positional arguments for the wrapped function.
            cache_info: The cache information to use. If None, it will be retrieved.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        result = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if result is not SEARCHSENTINEL:
            return result
        else:
            result = self.call_wrapped(*args, **kwargs)
            if cache_info.maxsize is not None and len(cache_info.cache_container) < cache_info.maxsize:
                cache_info.cache_container[key] = result
            return result

    # Cache Control
    def clear_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clears the cache and updates the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to clear.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        cache_info.cache_container.clear()
        super().clear_cache(*args, cache_info=cache_info, **kwargs)

    def set_maxsize(self, value: int | None) -> None:
        """Changes the cache's max size to a new value and updates the cache to its optimal handle function.

        Args:
            value: The new max size of the cache.
        """
        if value is None:
            self.cache_method = "unlimited_cache"
        elif value == 0:
            self.cache_method = "no_cache"
        else:
            self.cache_method = "limited_cache"

        self.cache_info.maxsize = value

    def poll(self, *args: Any, **kwargs: Any) -> bool:
        """Checks if there is room in the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.

        Returns:
            bool: True if the cache has space for more items; otherwise, False.
        """
        cache_info = self.get_cache_info(*args)
        return cache_info.maxsize is not None and len(cache_info.cache_container) < cache_info.maxsize

    def get_length(self, *args: Any) -> int:
        """Gets the length of the cache.

        Args:
            *args: Arguments that contain the instance if bound.

        Returns:
            int: The number of items currently in the cache.
        """
        cache_info = self.get_cache_info(*args)
        return len(cache_info.cache_container)


# Aliases #
timed_cache = TimedCache
