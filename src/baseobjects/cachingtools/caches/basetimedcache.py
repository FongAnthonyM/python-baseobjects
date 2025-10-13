"""basetimedcache.py
An abstract class for creating timed cache.

This module provides the BaseTimedCache class and related components for implementing time-based caching functionality.
It includes classes for cache items, cache callable wrappers, and the main abstract base class that defines the
interface and common behavior for all timed cache implementations. The caches automatically invalidate entries after
a specified lifetime has elapsed.
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
import abc
from collections.abc import Hashable, Iterable
from contextlib import contextmanager
from time import perf_counter
from typing import Any, ContextManager

# Local Packages #
from ...bases import BaseObject
from ...functions import DynamicCallable, DynamicDecorator, DynamicMethod, MethodMultiplexer
from ...typing import AnyCallable


# Definitions #
# Classes #
class _HashedSeq(list):
    """A hash value based on an iterable.

    Attributes:
        hashvalue: The hash value to store.

    Args:
        tuple_: The iterable to create a hash value from.
        hash_: The function that will create hash value.
    """

    __slots__: str | Iterable[str] = "hashvalue"

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, tuple_: Iterable, hash_: AnyCallable = hash) -> None:
        # Attributes #
        self[:] = tuple_
        self.hashvalue = hash_(tuple_)

    # Representation
    def __hash__(self) -> int:
        """Get the hash value of this object."""
        return self.hashvalue


class CacheItem(BaseObject):
    """An item within a cache which contains the result and a link to priority.

    Attributes:
        priority_link: The object that represents this item's priority.
        key: The key to this item in the cache.
        result: The cached value.

    Args:
        key: The key to this item in the cache.
        result: The value to store in the cache.
        priority_link: The object that represents this item's priority.
    """

    # Attributes #
    priority_link: Hashable | None
    key: Hashable | None
    result: Any | None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        key: Hashable | None = None,
        result: Any | None = None,
        priority_link: Any | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # Parent Initialization #
        super().__init__(*args, **kwargs)

        # Attributes #
        self.priority_link = priority_link

        self.key = key
        self.result = result


class BaseTimedCacheCallable(DynamicCallable):
    """A base cache wrapper object for a function which resets its cache periodically.

    Attributes:
        _instanced_cache: Determines if the cache exists in the main function or in the method instances.

        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        cache_item_type = The class that will create the cache items.
        cache_container: Contains the results of the wrapped function.
        _cache_method: The name of the caching method.
        _previous_cache_method: The previous caching method used.
        cache: The multiplexer which controls the caching method being use.

    Args:
        func: The function to wrap.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        instanced: Determines if the cache exists in the main function or in the method instances.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _cast_excluded: set = DynamicCallable._cast_excluded | {"cache"}
    default_call_method: str = "call_caching"

    _instanced_cache: bool = False

    typed: bool = False
    is_timed: bool = True
    lifetime: int | float | None = None
    expiration: int | float | None = 0

    cache_item_type: Any = CacheItem
    cache_container: Any = None

    _cache_method: str = "no_cache"
    _previous_cache_method: str = "no_cache"
    cache: MethodMultiplexer

    # Properties #
    @property
    def instanced_cache(self) -> bool:
        """Determines if the cache exists in the main function or in the method instances."""
        return self._instanced_cache

    @instanced_cache.setter
    def instanced_cache(self, value: bool) -> None:
        self._instanced_cache = value

    @property
    def cache_method(self) -> str:
        """The name of the method used when caching."""
        return self._cache_method

    @cache_method.setter
    def cache_method(self, value: str) -> None:
        self.cache.select(value)
        self._cache_method = value

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        typed: bool | None = None,
        lifetime: int | float | None = None,
        call_method: str | None = None,
        instanced: bool | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Attributes #
        self._previous_cache_method: str = self._cache_method
        self.cache: MethodMultiplexer = MethodMultiplexer(instance=self, select=self._cache_method)

        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                func=func,
                lifetime=lifetime,
                typed=typed,
                call_method=call_method,
                instanced=instanced,
                **kwargs,
            )

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
        """The constructor for this object.

        Args:
            func: The function to wrap.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            instanced: Determines if the cache exists in the main function or in the method instances.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if lifetime is not None:
            self.lifetime = lifetime

        if typed is not None:
            self.typed = typed

        if call_method is not None:
            self.call_method = call_method

        if instanced is not None:
            self.instanced_cache = instanced

        super().construct(func=func, *args, **kwargs)

    # Caching Methods
    def no_cache(self, *args: Any, **kwargs: Any) -> Any:
        """No caching is done, the function is evaluated.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__wrapped__(*args, **kwargs)

    # Cache Control
    def create_key(
        self,
        args: tuple,
        kwds: dict,
        typed: bool,
        kwd_mark: tuple = (object(),),
        fasttypes: set = {int, str},
        tuple_: AnyCallable = tuple,
        type_: AnyCallable = type,
        len_: AnyCallable = len,
    ) -> _HashedSeq:
        """Make a cache key from optionally typed positional and keyword arguments.

        The key is constructed in a way that is flat as possible rather than as a nested structure that would take
        more memory. If there is only a single argument and its data type is known to cache its hash value, then that
        argument is returned without a wrapper. This saves space and improves lookup speed.
        """
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

    def clear_condition(self, *args: Any, **kwargs: Any) -> bool:
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def stop_caching(self) -> None:
        """Stops using the cache, storing the method used."""
        self._previous_cache_method = self.cache_method
        self.cache_method = "no_cache"
        self.clear_cache()

    def resume_caching(self) -> None:
        """Resumes caching by setting the call method to the previous call method"""
        self.cache_method = self._previous_cache_method

    @contextmanager
    def pause_caching(self) -> ContextManager[None]:
        self.stop_caching()
        yield None
        self.resume_caching()

    # Calling
    def call_caching(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the caching function and clears the cache at a certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        if self.clear_condition():
            self.clear_cache()

        return self.cache(*args, **kwargs)

    def call_clearing(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        self.clear_cache()

        return self.cache(*args, **kwargs)


class BaseTimedCacheMethod(BaseTimedCacheCallable, DynamicMethod):
    """An abstract method class for timed caches."""

    # Instance Methods #
    # Cache Control
    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    # Calling
    def call_caching(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the caching function and clears the cache at a certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        if self.clear_condition():
            self.clear_cache()

        return self.cache(self._self_(), *args, **kwargs)

    def call_clearing(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        self.clear_cache()

        return self.cache(self._self_(), *args, **kwargs)


class BaseTimedCache(BaseTimedCacheCallable, DynamicDecorator):
    """An abstract function class for timed caches."""

    # Attributes #
    method_type: type[DynamicMethod] = BaseTimedCacheMethod

    # Properties #
    @property
    def instanced_cache(self) -> bool:
        """Determines if the cache exists in the main function or in the method instances.

        When set, the __get__ method will be changed to match the chosen style.
        """
        return self._instanced_cache

    @instanced_cache.setter
    def instanced_cache(self, value: bool) -> None:
        if value:
            self.bind_multiplexer.select("bind_to_attribute")
        else:
            self.bind_multiplexer.select("bind_builtin")
        self._instanced_cache = value

    # Instance Methods #
    # Binding
    def bind(self, instance: Any = None, owner: type[Any] | None = None) -> BaseTimedCacheMethod:
        """Creates a method of this function which is bound to another object.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.

        Returns:
            The bound method of this function.
        """
        return self.method_type(
            func=self.__wrapped__,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            instanced=self.instanced_cache,
        )

    def bind_to_attribute(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        name: str | None = None,
    ) -> BaseTimedCacheCallable:
        """Creates a method of this function which is bound to another object and sets the method an attribute.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object being bound to.
            name: The name of the attribute to set the method to. Default is the function name.

        Returns:
            The bound method of this function.
        """
        if instance is None:
            return self

        if name is None:
            name = self.__wrapped__.__name__

        method = self.method_type(
            func=self.__wrapped__,
            instance=instance,
            owner=owner,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=self.call_method,
            instanced=self.instanced_cache,
        )
        setattr(instance, name, method)

        return method

    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime
