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
from collections import OrderedDict
from collections.abc import Hashable, Iterable, Iterator
from copy import copy
from types import MethodType
from contextlib import contextmanager
from dataclasses import dataclass
from time import perf_counter
from typing import Any


# Local Packages #
from ...bases import SentinelObject
from ...functions import BaseDecorator
from ...typing import AnyCallable, DescriptorGetMethod


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
        is_caching: Determines if the cache is currently active.
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
    is_caching: bool = True
    typed: bool = False
    is_timed: bool = True
    lifetime: int | float | None = None
    expiration: int | float | None = 0
    cache_method: str = "no_cache"
    cache_item_type: Any = None
    cache_container: Any = None


class BaseTimedCache(BaseDecorator):
    """A base cache wrapper object for a function which resets its cache periodically.

    Attributes:
        instanced_cache: Determines if the cache exists in the main function or in the method instances.

        cache_info_type: The type of cache information to use.
        cache_info: The cache information.
    """

    # Attributes #
    instanced_cache: bool = False

    cache_info_type: type[CacheInfo] = CacheInfo

    cache_info: CacheInfo

    # Properties #
    @property
    def __func__(self) -> AnyCallable | None:
        """The function which this callable wraps."""
        return self.__wrapped__

    @__func__.setter
    def __func__(self, value: AnyCallable | None) -> None:
        """Sets the function which this callable wraps and clears the cache."""
        self.__wrapped__ = value
        self.clear_cache()

    @__func__.deleter
    def __func__(self) -> None:
        """Deletes the wrapped function and clears the cache."""
        self.__wrapped__ = None
        self.clear_cache()

    @property
    def cache_method(self) -> str:
        """The name of the method used when caching."""
        return self.cache_info.cache_method

    @cache_method.setter
    def cache_method(self, value: str) -> None:
        self.cache_info.cache_method = value

    @property
    def is_active(self) -> bool:
        """Determines if the cache is currently active (not in 'no_cache' mode)."""
        return self.get_cache_info().cache_method != "no_cache"

    @property
    def is_caching(self) -> bool:
        """Determines if the cache is currently enabled."""
        if (reference := self._self_) is not None and (instance := reference()) is not None:
            return self.get_is_caching(instance)
        return self.cache_info.is_caching

    @is_caching.setter
    def is_caching(self, value: bool) -> None:
        cache_info = self.get_cache_info()
        cache_info.is_caching = value

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
        self.init_cache_info(self.cache_info)
        self._bound_cache_info: CacheInfo | None = None

        # Parent Initialization #
        super().__init__(func=func, init=False, *args, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                func=func,
                typed=typed,
                lifetime=lifetime,
                call_method=call_method,
                instanced=instanced,
                *args,
                **kwargs,
            )

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]]:
        """Gets the state of this object for pickling.

        Returns:
            The state of this object.
        """
        state = super().__getstate__()
        if state is None:
            d_state: dict[str, Any] = {}
            slots: dict[str, Any] | None = None
        elif isinstance(state, tuple):
            d_state = {} if state[0] is None else state[0].copy()
            slots = state[1]
        else:
            d_state = state.copy()
            slots = None

        if slots is None:
            return d_state
        return (d_state, slots)

    def __setstate__(self, state: Any) -> None:
        """Sets the state of this object.

        Args:
            state: The state to set.
        """
        super().__setstate__(state)
        if not hasattr(self, "cache_info"):
            self.cache_info = self.cache_info_type()
            self.init_cache_info(self.cache_info)

    # Binding
    __get__: DescriptorGetMethod = BaseDecorator.bind_self

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """The call magic method which calls the caching method.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        instance = None
        if (reference := self._self_) is not None:
            instance = reference()

        if instance is not None:
            cache_info = self.get_instance_cache_info(instance) if self.instanced_cache else self.cache_info
        else:
            cache_info = self.cache_info

        if cache_info.is_caching:
            return getattr(self, cache_info.cache_method)(instance, *args, cache_info=cache_info, **kwargs)

        return self.no_cache(instance, *args, cache_info=cache_info, **kwargs)

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
        """Makes a cache key from optionally typed positional and keyword arguments.

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
        if not typed and not kwds:
            if len_(args) == 1:
                key = args[0]
                if type_(key) in {int, str}:
                    return key
            return args

        if kwd_mark is None:
            kwd_mark = (_KWD_MARK,)

        key = args
        if kwds:
            key += kwd_mark + tuple_(kwds.items())

        if typed:
            key += tuple_(type_(v) for v in args)
            if kwds:
                key += tuple_(type_(v) for v in kwds.values())

        return key

    # Caching Methods
    def init_cache_info(self, cache_info: CacheInfo) -> None:
        """Initializes the cache information.

        Args:
            cache_info: The cache information to initialize.
        """
        cache_info.cache_item_type = CacheItem
        cache_info.cache_container = {}

    def no_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> Any:
        """Performs no caching and evaluates the function.

        Args:
            *args: Arguments of the wrapped function.
            cache_info: The cache information (ignored).
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        instance = args[0]
        if instance is not None:
            try:
                return self.__wrapped__.__get__(instance, self.__owner__)(*args[1:], **kwargs)  # type: ignore[misc]
            except AttributeError:
                return self.__wrapped__(instance, *args[1:], **kwargs)  # type: ignore[misc]

        return self.__wrapped__(*args[1:], **kwargs)

    # Cache Control
    def get_cache_info(self, instance: Any = None) -> CacheInfo:
        """Gets the cache information for the method.

        Args:
            instance: The instance to get the cache information from.

        Returns:
            The cache information object.
        """
        if self.instanced_cache:
            if instance is None and (reference := self._self_) is not None:
                instance = reference()

            if instance is not None:
                return self.get_instance_cache_info(instance)
        return self.cache_info

    def get_instance_cache_info(self, instance: Any) -> CacheInfo:
        """Gets the cache information for the method from the instance.

        Args:
            instance: The instance to get the cache information from.

        Returns:
            The cache information object.
        """
        try:
            caches = instance.__cache__
        except AttributeError:
            caches = instance.__cache__ = {}

        try:
            method_name = self.__wrapped__.__name__
        except AttributeError:
            method_name = ""

        if (cache_info := caches.get(method_name, None)) is None:
            caches[method_name] = cache_info = copy(self.cache_info)
            self.init_cache_info(cache_info)

        return cache_info

    def get_is_caching(self, instance: Any = None, cache_info: CacheInfo | None = None) -> bool:
        """Determines if caching is enabled for this object.

        Args:
            instance: The instance to check caching for. If None, the cache info will be retrieved from the cache.
            cache_info: The cache info to check. If None, the cache info will be retrieved.

        Returns:
            If caching is enabled for this object.
        """
        if cache_info is None:
            cache_info = self.get_cache_info()

        if instance is not None and not getattr(instance, "_is_caching", True):
            return False

        return cache_info.is_caching

    @abc.abstractmethod
    def clear_cache(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:
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

        if cache_info.lifetime is not None:
            cache_info.expiration = perf_counter() + cache_info.lifetime

    def enable_caching(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:
        """Enables caching for this object.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to enable.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        cache_info.is_caching = True

    def disable_caching(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:
        """Disables caching for this object.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to disable.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        cache_info.is_caching = False

    @contextmanager
    def pause_caching(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> Iterator[None]:
        """Temporarily pauses caching within the context manager.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to pause.
            **kwargs: Keyword arguments.

        Yields:
            None: Yields None while caching is paused within the context.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        original_is_caching = cache_info.is_caching
        cache_info.is_caching = False
        yield None
        cache_info.is_caching = original_is_caching

    def refresh_expiration(self, *args: Any, cache_info: CacheInfo | None = None, **kwargs: Any) -> None:
        """Refreshes the expiration of the cache.

        Args:
            *args: Arguments that contain the instance if bound.
            cache_info: The cache information to refresh.
            **kwargs: Keyword arguments.
        """
        if cache_info is None:
            instance = None
            if (reference := self._self_) is not None:
                instance = reference()

            cache_info = self.get_cache_info(instance)

        if cache_info.lifetime is not None:
            cache_info.expiration = perf_counter() + cache_info.lifetime

    def call_clearing(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        cache_info = self.get_cache_info()
        self.clear_cache(*args, cache_info=cache_info, **kwargs)
        return getattr(self, cache_info.cache_method)(*args, cache_info=cache_info, **kwargs)
