"""timedcache.py
A cache that periodically resets and include its instantiation decorator function.

This module provides the TimedCache class and related components for implementing a time-based cache with multiple
items. It includes TimedCacheCallable and TimedCacheMethod classes that wrap functions and methods to provide caching
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
from time import perf_counter
from typing import Any

# Local Packages #
from ...bases import SEARCHSENTINEL
from ...collections import CircularDoublyLinkedContainer
from ...typing import AnyCallable
from .basetimedcache import BaseTimedCache, BaseTimedCacheCallable, BaseTimedCacheMethod


# Definitions #
# Classes #
class TimedCacheCallable(BaseTimedCacheCallable):
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
    _cache_method: str = "unlimited_cache"
    _maxsize: int | None = None
    priority_queue_type: type[CircularDoublyLinkedContainer] = CircularDoublyLinkedContainer
    priority: Any

    # Properties #
    @property
    def maxsize(self) -> int | None:
        """The cache's max size and when updated it changes the cache to its optimal handle function."""
        return self._maxsize

    @maxsize.setter
    def maxsize(self, value: int | None) -> None:
        self.set_maxsize(value)

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
        # Attributes #
        self.priority: Any = self.priority_queue_type()

        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Overriden Attributes #
        self.cache_container: dict[Any, Any] = {}

        # Object Construction #
        if init:
            self.construct(
                func,
                maxsize,
                typed,
                lifetime,
                call_method,
                instanced,
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
            **kwargs,
        )

    # Caching Methods
    def unlimited_cache(self, *args: Any, **kwargs: Any) -> Any:
        """Caching with no limit on items in the cache.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        key = self.create_key(args, kwargs, self.typed)
        cache_item = self.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)  # type:ignore[misc]
            self.cache_container[key] = self.cache_item_type(key=key, result=result)
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
        cache_item = self.cache_container.get(key, SEARCHSENTINEL)

        if cache_item is not SEARCHSENTINEL:
            return cache_item.result
        else:
            result = self.__func__(*args, **kwargs)  # type:ignore[misc]
            if self._maxsize is not None and self.cache_container.__len__() < self._maxsize:
                self.cache_container[key] = self.cache_item_type(result=result)
            return result

    # Cache Control
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        self.cache_container.clear()
        self.priority.clear()
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

    def poll(self) -> bool:
        """Checks if there is room in the cache.

        Returns:
            bool: True if the cache has space for more items; otherwise, False.
        """
        return self._maxsize is not None and len(self.cache_container) < self._maxsize

    def get_length(self) -> int:
        """Gets the length of the cache.

        Returns:
            int: The number of items currently in the cache.
        """
        return len(self.cache_container)


class TimedCacheMethod(TimedCacheCallable, BaseTimedCacheMethod):  # type: ignore[misc]
    """A method class for TimedCache."""


class TimedCache(TimedCacheCallable, BaseTimedCache):
    """A function class for TimedCache."""

    # Attributes #
    method_type: type[TimedCacheMethod] = TimedCacheMethod

    # Instance Methods #
    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> TimedCacheMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self.method_type(
            func=self.__func__,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            instanced=self.instanced_cache,
            maxsize=self.maxsize,
        )

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> TimedCacheMethod | TimedCache:
        """Creates a method of this function which is bound to another object and sets the method as an attribute.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set the method to. Default is the function name.

        Returns:
            The bound method of this function.
        """
        if name is None:
            name = self.__func__.__name__  # type:ignore[union-attr]

        if instance is None:
            return self

        method = self.method_type(
            func=self.__func__,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            instanced=self.instanced_cache,
            maxsize=self.maxsize,
        )
        setattr(instance, name, method)

        return method


# Aliases #
timed_cache = TimedCache
