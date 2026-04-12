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
from collections.abc import Hashable, Iterable, Iterator
from copy import copy
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Any

# Local Packages #
from ...bases import SentinelObject
from ...functions import DynamicCallable, DynamicDecorator, MethodMultiplexer
from ...typing import AnyCallable


# Definitions #
# Constants #
_KWD_MARK = SentinelObject("_KWD_MARK")  # Sentinel for create_key kwd_mark to avoid B008 (no calls in defaults)


# Classes #
class _HashedSeq:
    """A hash value based on an iterable.

    Attributes:
        value: The sequence value.
        hashvalue: The hash value to store.
    """

    # slots #
    __slots__: str | Iterable[str] = ("hashvalue", "value")

    # Attributes #
    value: tuple[Any, ...]
    hashvalue: int

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, tuple_: tuple[Any, ...], hash_: AnyCallable = hash) -> None:
        """Initializes this object with the given arguments.

        Args:
            tuple_: The iterable to create a hash value from.
            hash_: The function that will create hash value.
        """
        # Attributes #
        self.value = tuple_
        self.hashvalue = hash_(tuple_)

    # Representation
    def __hash__(self) -> int:
        """Gets the hash value of this object.

        Returns:
            int: The cached hash value for this sequence.
        """
        return self.hashvalue

    def __eq__(self, other: Any) -> bool:
        """Checks if this object is equal to another object.

        Args:
            other: The object to compare to.

        Returns:
            True if the objects are equal, False otherwise.
        """
        if isinstance(other, _HashedSeq):
            return self.hashvalue == other.hashvalue and self.value == other.value
        return bool(self.value == other)


@dataclass(slots=True)
class CacheItem:
    """An item within a cache which contains the result and a link to priority.

    Attributes:
        priority_link: The object that represents this item's priority.
        key: The key to this item in the cache.
        result: The cached value.
    """

    # Attributes #
    priority_link: Hashable | None = None
    key: Hashable | None = None
    result: Any = None


@dataclass(slots=True)
class CacheInfo:
    """Information about a cache.

    Attributes:
        is_cache: Determines if the cache is currently active.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be reset.
        previous_cache_method: The name of the previous caching method.
        cache_method: The name of the caching method.
        cache_item_type: The type of item to use in the cache.
        cache_container: Contains the results of the wrapped function.
    """

    # Attributes #
    is_cache: bool = True
    typed: bool = False
    is_timed: bool = True
    lifetime: int | float | None = None
    expiration: int | float | None = 0
    previous_cache_method: str = "no_cache"
    cache_method: str = "no_cache"
    cache_item_type: Any = None
    cache_container: Any = None


class BaseTimedCache(DynamicDecorator):
    """A base cache wrapper object for a function which resets its cache periodically.

    Attributes:
        _cast_excluded: The attributes that will not be casted.
        default_call_method: The default call method to use.
        instanced_cache: Determines if the cache exists in the main function or in the method instances.

        cache_info_type: The type of cache information to use.
        cache_info: The cache information.
    """

    # Attributes #
    _cast_excluded: set[str] = DynamicCallable._cast_excluded | {"cache"}
    default_call_method: str = "call_caching"
    instanced_cache: bool = False

    cache_info_type: type[CacheInfo] = CacheInfo

    cache_info: CacheInfo

    # Properties #
    @property
    def cache_method(self) -> str:
        """The name of the method used when caching."""
        return self.cache_info.cache_method

    @cache_method.setter
    def cache_method(self, value: str) -> None:
        self.cache_info.cache_method = value

    @property
    def typed(self) -> bool:
        """Determines if the function's arguments are type sensitive for caching."""
        return self.cache_info.typed

    @typed.setter
    def typed(self, value: bool) -> None:
        self.cache_info.typed = value

    @property
    def is_timed(self) -> bool:
        """Determines if the cache will be reset periodically."""
        return self.cache_info.is_timed

    @is_timed.setter
    def is_timed(self, value: bool) -> None:
        self.cache_info.is_timed = value

    @property
    def lifetime(self) -> int | float | None:
        """The period between cache resets in seconds."""
        return self.cache_info.lifetime

    @lifetime.setter
    def lifetime(self, value: int | float | None) -> None:
        self.cache_info.lifetime = value

    @property
    def expiration(self) -> int | float | None:
        """The next time the cache will be reset."""
        return self.cache_info.expiration

    @expiration.setter
    def expiration(self, value: int | float | None) -> None:
        self.cache_info.expiration = value

    @property
    def cache_item_type(self) -> Any:
        """The type of item to use in the cache."""
        return self.cache_info.cache_item_type

    @cache_item_type.setter
    def cache_item_type(self, value: Any) -> None:
        self.cache_info.cache_item_type = value

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
        """Initializes this object with the given arguments.

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
        self.cache_info = self.cache_info_type()
        self.cache_info.cache_container = {}

        # Parent Initialization #
        super().__init__(*args, func=func, init=False, **kwargs)  # type: ignore[misc]

        # Object Construction #
        if init:
            self.construct(  # type: ignore[misc]
                *args,
                func=func,
                typed=typed,
                lifetime=lifetime,
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
        if lifetime is not None:
            self.lifetime = lifetime

        if typed is not None:
            self.typed = typed

        if call_method is not None:
            self.call_method = call_method

        if instanced is not None:
            self.instanced_cache = instanced

        super().construct(func, *args, **kwargs)

    # Key Creation
    def create_key(
        self,
        args: tuple[Any, ...],
        kwds: dict[str, Any],
        typed: bool,
        kwd_mark: tuple[Any, ...] | None = None,
        fasttypes: set[type] | None = None,
        tuple_: AnyCallable = tuple,
        type_: AnyCallable = type,
        len_: AnyCallable = len,
    ) -> _HashedSeq | Hashable:
        """Make a cache key from optionally typed positional and keyword arguments.

        The key is constructed in a way that is flat as possible rather than as a nested structure that would take
        more memory. If there is only a single argument and its data type is known to cache its hash value, then that
        argument is returned without a wrapper. This saves space and improves lookup speed.

        Args:
            args: The positional arguments to create the key from.
            kwds: The keyword arguments to create the key from.
            typed: Determines if the function's arguments are type sensitive for caching.
            kwd_mark: The sentinel to use for separating positional and keyword arguments.
            fasttypes: The types that are known to be fast to hash.
            tuple_: The tuple class to use.
            type_: The type class to use.
            len_: The len function to use.

        Returns:
            _HashedSeq | Hashable: A hashed sequence representing the key for lookups. When a single fast-typed
            argument is provided, the raw argument (e.g., an int or str) is returned directly for efficiency.
        """
        if kwd_mark is None:
            kwd_mark = (_KWD_MARK,)
        if fasttypes is None:
            fasttypes = {int, str}
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
            return key[0]  # type: ignore[no-any-return]
        return key

    # Caching Methods
    def cache(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> Any:
        """Caches the result of the wrapped function."""
        return getattr(self, cache_info.cache_method)(*args, **kwargs)

    def no_cache(self, *args: Any, **kwargs: Any) -> Any:
        """No caching is done, the function is evaluated.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.call_wrapped(*args, **kwargs)

    # Cache Control
    def get_cache_info(self, *args: Any) -> Any:
        """Gets the cache information for the method.

        Args:
            *args: Arguments that contain the instance if bound.

        Returns:
            The cache container.
        """
        if not self.instanced_cache or not args:
            return self.cache_info

        instance = args[0]
        method_name = getattr(self.__wrapped__, "__name__", "")

        try:
            caches = instance.__cache__
        except AttributeError:
            caches = {}
            instance.__cache__ = caches

        if (cache_info := caches.get(method_name, None)) is None:
            caches[method_name] = cache_info = copy(self.cache_info)

        return cache_info

    def clear_condition(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> bool:
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            Determines if the cache should be cleared.
        """
        return (
            cache_info.is_timed
            and cache_info.lifetime is not None
            and cache_info.expiration is not None
            and perf_counter() >= cache_info.expiration
        )

    @abc.abstractmethod
    def clear_cache(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> None:
        """Clear the cache and update the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        if cache_info.lifetime is not None:
            cache_info.expiration = perf_counter() + cache_info.lifetime
        if (clear_cache := getattr(self.__wrapped__, "clear_cache", None)) is not None:
            clear_cache(cache_info)

    def enable_caching(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> None:
        """Enables caching for this object.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        cache_info.is_cache = True
        if (enable_caching := getattr(self.__wrapped__, "enable_caching", None)) is not None:
            enable_caching(cache_info)

    def disable_caching(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> None:
        """Disables caching for this object.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        cache_info.is_cache = False
        if (disable_caching := getattr(self.__wrapped__, "disable_caching", None)) is not None:
            disable_caching(cache_info)

    def stop_caching(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> None:
        """Stops using the cache, storing the method used.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        if cache_info.cache_method != "no_cache":
            cache_info.previous_cache_method = cache_info.cache_method
        cache_info.cache_method = "no_cache"
        if (stop_caching := getattr(self.__wrapped__, "stop_caching", None)) is not None:
            stop_caching(cache_info)

    def resume_caching(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> None:
        """Resumes caching by setting the call method to the previous call method.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.
        """
        cache_info.cache_method = cache_info.previous_cache_method
        if (resume_caching := getattr(self.__wrapped__, "resume_caching", None)) is not None:
            resume_caching(cache_info)

    @contextmanager
    def pause_caching(self, cache_info: CacheInfo, *args: Any, **kwargs: Any) -> Iterator[None]:
        """Temporarily pause caching within the context manager.

        Args:
            *args: Arguments that contain the instance if bound.
            **kwargs: Keyword arguments.

        Yields:
            None: Yields None while caching is paused within the context.
        """
        self.stop_caching(cache_info, *args, **kwargs)
        yield None
        self.resume_caching(cache_info, *args, **kwargs)

    # Calling
    def call_caching(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the caching function and clears the cache at a certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        cache_info = self.get_cache_info(*args)
        if not cache_info.is_cache:
            return self.call_wrapped(*args, **kwargs)

        if self.clear_condition(cache_info, *args, **kwargs):
            self.clear_cache(cache_info, *args, **kwargs)

        return self.cache(cache_info, *args, **kwargs)

    def call_clearing(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the cache.
        """
        cache_info = self.get_cache_info(*args)
        self.clear_cache(cache_info, *args, **kwargs)
        return self.cache(cache_info, *args, **kwargs)
