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
        lifetime: The period between cache resets in seconds.
        priority: The priority queue used for cache item management.
    """

    # Attributes #
    cache_method: str = "unlimited_cache"
    maxsize: int | None = None
    priority_queue_type: type[CircularDoublyLinkedContainer] | None = None
    priority: Any = None


class TimedCache(BaseTimedCache):
    """A periodically clearing multiple item cache wrapper object for a function.

    Class Attributes:
        priority_queue_type: The type of priority queue to hold cache item priorities.

    Attributes:
        _maxsize: The number of results the cache will hold before replacing results.

        priority: The object that will control the replacement of cached results.

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

        # Overriden Attributes #
        self.cache_info.priority = self.cache_info.priority_queue_type()
        self.cache_info.cache_container = {}

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
    def get_priority(self, *args: Any, **kwargs: Any) -> Any:
        """Gets the priority queue for the method.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.

        Returns:
            The priority queue.
        """
        if not self.instanced_cache or not args:
            return self.priority

        instance = args[0]
        priority_name = getattr(self.__wrapped__, "__name__", "") + "_priority"

        try:
            caches = instance.__cache__
        except AttributeError:
            caches = {}
            instance.__cache__ = caches

        if (priority := caches.get(priority_name, None)) is None:
            caches[priority_name] = priority = self.priority_queue_type()

        return priority

    def unlimited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_container = self.get_cache_container(*args, **kwargs)
        cache_item = cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            cache_container[key] = self.cache_item_type(key=key, result=result)
            return result

    def limited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching that does not cache new results when cache is full.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_container = self.get_cache_container(*args, **kwargs)
        cache_item = cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.call_wrapped(*args, **kwargs)
            if self._maxsize is not None and cache_container.__len__() < self._maxsize:
                cache_container[key] = self.cache_item_type(result=result)
            return result

    # Cache Control
    def clear_cache(self, *args: Any, **kwargs: Any) -> None:
        """Clear the cache and update the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        cache_container = self.get_cache_container(*args, **kwargs)
        cache_container.clear()
        priority = self.get_priority(*args, **kwargs)
        priority.clear()
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

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

        self._maxsize = value

    def poll(self, *args: Any, **kwargs: Any) -> bool:
        """Checks if there is room in the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.

        Returns:
            bool: True if the cache has space for more items; otherwise, False.
        """
        return self._maxsize is not None and len(self.get_cache_container(*args, **kwargs)) < self._maxsize

    def get_length(self, *args: Any, **kwargs: Any) -> int:
        """Gets the length of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.

        Returns:
            int: The number of items currently in the cache.
        """
        return len(self.get_cache_container(*args, **kwargs))


# Aliases #
timed_cache = TimedCache
