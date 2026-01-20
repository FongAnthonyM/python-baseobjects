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
from contextlib import contextmanager
from time import perf_counter
from typing import Any

# Local Packages #
from ...bases import BaseObject
from ...functions import DynamicCallable, DynamicDecorator, DynamicMethod, MethodMultiplexer
from ...typing import AnyCallable

# Definitions #
# Constants #
_KWD_MARK = object()  # Sentinel for create_key kwd_mark to avoid B008 (no calls in defaults)


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


class CacheItem(BaseObject):
    """An item within a cache which contains the result and a link to priority.

    Attributes:
        priority_link: The object that represents this item's priority.
        key: The key to this item in the cache.
        result: The cached value.
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
        """Initializes this object with the given arguments.

        Args:
            key: The key to this item in the cache.
            result: The value to store in the cache.
            priority_link: The object that represents this item's priority.
            *args: Additional positional arguments forwarded to BaseObject.
            **kwargs: Additional keyword arguments forwarded to BaseObject.
        """
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
        expiration: The next time the cache will be reset.


        cache_container: Contains the results of the wrapped function.
        _cache_method: The name of the caching method.
        _previous_cache_method: The previous caching method used.
        cache: The multiplexer which controls the caching method being used.
    """

    # Attributes #
    _cast_excluded: set[str] = DynamicCallable._cast_excluded | {"cache"}
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

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

        Returns:
            The state of the object.
        """
        state = super().__getstate__()
        # Normalize to a dict for augmentation
        if state is None:
            d: dict[str, Any] = {}
            slots: dict[str, Any] | None = None
        elif isinstance(state, tuple):
            d = {} if state[0] is None else state[0].copy()
            slots = state[1]
        else:
            d = state.copy()
            slots = None
        # Save and drop cache multiplexer
        try:
            d["_saved_cache_method"] = None if self.cache is None else self.cache.selected
        except AttributeError:
            d["_saved_cache_method"] = None
        d.pop("cache", None)
        if slots is None:
            return d
        return (d, slots)

    def __setstate__(self, state: Any) -> None:
        """Reconstruct cache multiplexer from stored configuration after unpickling.

        Args:
            state: The state to restore.
        """
        saved_cache = None
        if isinstance(state, dict):
            saved_cache = state.pop("_saved_cache_method", None)
        elif isinstance(state, tuple):
            if state[0] is not None:
                saved_cache = state[0].pop("_saved_cache_method", None)
        super().__setstate__(state)
        # Recreate cache multiplexer and reselect method
        self.cache = MethodMultiplexer(instance=self, select=self._cache_method)
        if saved_cache is not None:
            self.cache.select(saved_cache)
            self._cache_method = saved_cache

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
        self._previous_cache_method: str = self._cache_method
        self.cache: MethodMultiplexer = MethodMultiplexer(instance=self, select=self._cache_method)

        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(
                func,
                typed,
                lifetime,
                call_method,
                instanced,
                *args,
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

    # Caching Methods
    def no_cache(self, *args: Any, **kwargs: Any) -> Any:
        """No caching is done, the function is evaluated.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__wrapped__(*args, **kwargs)  # type:ignore[misc]

    # Cache Control
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

    def clear_condition(self, *args: Any, **kwargs: Any) -> bool:
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            Determines if the cache should be cleared.
        """
        return (
            self.is_timed
            and self.lifetime is not None
            and self.expiration is not None
            and perf_counter() >= self.expiration
        )

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
        """Resumes caching by setting the call method to the previous call method."""
        self.cache_method = self._previous_cache_method

    @contextmanager
    def pause_caching(self) -> Iterator[None]:
        """Temporarily pause caching within the context manager.

        Yields:
            None: Yields None while caching is paused within the context.
        """
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


def _rebind_method(owner: type[Any], name: str, instance: Any) -> Any:
    """Rebinds a method to an instance.

    Args:
        owner: The class that owns the method.
        name: The name of the method.
        instance: The instance to bind the method to.

    Returns:
        The bound method.
    """
    descriptor = getattr(owner, name)
    return descriptor.__get__(instance, owner)


class BaseTimedCacheMethod(BaseTimedCacheCallable, DynamicMethod):  # type: ignore[misc]
    """An abstract method class for timed caches."""

    # Pickling
    def __reduce__(self) -> str | tuple[Any, ...]:
        """Support for pickling.

        Returns:
            The state of the object.
        """
        if (
            self.__self__ is not None
            and self.__owner__ is not None
            and self.__wrapped__ is not None
            and hasattr(self.__wrapped__, "__name__")
        ):
            state = self.__getstate__()
            if isinstance(state, dict):
                state = state.copy()
                state.pop("__wrapped__", None)
            elif isinstance(state, tuple):
                d = state[0]
                if d is not None:
                    d = d.copy()
                    d.pop("__wrapped__", None)
                    state = (d, state[1])

            return (_rebind_method, (self.__owner__, self.__wrapped__.__name__, self.__self__), state)
        return super().__reduce__()

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


class BaseTimedCache(BaseTimedCacheCallable, DynamicDecorator):
    """An abstract function class for timed caches."""

    # Attributes #
    method_type: type[BaseTimedCacheMethod]

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
        """Creates a method of this function which is bound to another object and sets the method as an attribute.

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
            name = self.__wrapped__.__name__  # type:ignore[union-attr]

        method = self.bind(instance, owner)
        setattr(instance, name, method)

        return method

    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime
