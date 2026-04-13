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
        priority_queue_type: The type of priority queue to hold cache item priorities.
        priority: The priority queue used for cache item management.
    """

    # Attributes #
    cache_method: str = "unlimited_cache"
    maxsize: int | None = None
    priority_queue_type: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer
    priority: Any = None


class TimedCache(BaseTimedCache):
    """A periodically clearing multiple item cache wrapper object for a function.

    Class Attributes:
        priority_queue_type: The type of priority queue to hold cache item priorities.

    Args:
        func: The function to wrap.
        maxsize: The max size of the cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        instanced: Determines if the cache exists in the main function or in the method instances.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
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

    # Magic Methods #
    # Construction/Destruction
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
        super().__init__(*args, init=False, **kwargs)  # type: ignore[misc]

        # Object Construction #
        if init:
            self.construct(  # type: ignore[misc]
                *args,
                func=func,
                maxsize=maxsize,
                typed=typed,
                lifetime=lifetime,
                call_method=call_method,
                instanced=instanced,
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
    def init_cache_info(self, cache_info: TimedCacheInfo) -> None:  # type: ignore[override]
        """Initializes the cache information.

        Args:
            cache_info: The cache information to initialize.
        """
        super().init_cache_info(cache_info)
        cache_info.priority = cache_info.priority_queue_type()

    def unlimited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        cache_item = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_info.cache_container[key] = self.cache_item_type(key=key, result=result)
            return result

    def limited_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> Any:
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information to use for caching.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        key = self.create_key(args, kwargs, cache_info.typed)
        cache_item = cache_info.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            if cache_info.maxsize is not None and len(cache_info.cache_container) < cache_info.maxsize:
                cache_info.cache_container[key] = self.cache_item_type(result=result)
            return result

    # Cache Control
    def clear_cache(self, *args: Any, cache_info: TimedCacheInfo | None = None, **kwargs: Any) -> None:  # type: ignore[override]
        """Clear the cache and update the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to clear.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            cache_info = self.get_cache_info(*args)  # type: ignore[assignment]

        cache_info.cache_container.clear()
        cache_info.priority.clear()
        super().clear_cache(*args, cache_info=cache_info, **kwargs)

    def set_maxsize(self, value: int | None) -> None:
        """Change the cache's max size to a new value and updates the cache to its optimal handle function.

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
