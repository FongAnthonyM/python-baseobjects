""" basetimedcache.py
An abstract class for creating timed cahce
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__

# Imports #
# Standard Libraries #
import abc
from collections.abc import Callable, Hashable, Iterable, Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any

# Third-Party Packages #

# Local Packages #
from ...typing import AnyCallable, GetObjectMethod
from ...bases import BaseObject, BaseMethod
from ...bases.singlekwargdispatch import singlekwargdispatchmethod


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

    __slots__ = "hashvalue"

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

    __slots__ = ["key", "result", "priority_link"]

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
        # Parent Attributes #
        super().__init__(*args, **kwargs)

        # Attributes #
        self.priority_link = priority_link

        self.key = key
        self.result = result


class BaseTimedCache(BaseMethod):
    """A base cache wrapper object for a function which resets its cache periodically.

    Class Attributes:
        sentinel: An object used to determine if a value was unsuccessfully found.
        cache_item_type = The class that will create the cache items.

    Attributes:
        __func__: The original function to wrap.
        __self__: The object to bind this object to.
        _is_collective: Determines if the cache is collective for all method bindings or for each instance.
        _instances: Copies of this object for specific owner instances.

        _maxsize: The max size of the lru_cache.
        typed: Determines if the function's arguments are type sensitive for caching.
        is_timed: Determines if the cache will be reset periodically.
        lifetime: The period between cache resets in seconds.
        expiration: The next time the cache will be rest.

        cache: Contains the results of the wrapped function.
        _defualt_caching_method: The default caching function to use.
        _caching_method: The designated function to handle caching.
        _previous_caching_method: The previous caching method used.

        _call_method: The function to call when this object is called.

    Args:
        func: The function to wrap.
        typed: Determines if the function's arguments are type sensitive for caching.
        lifetime: The period between cache resets in seconds.
        call_method: The default call method to use.
        collective: Determines if the cache is collective for all method bindings or for each instance.
        init: Determines if this object will construct.
    """
    __slots__ = BaseMethod.__slots__ | {
        "_is_collective",
        "typed",
        "is_timed",
        "lifetime",
        "expiration",
        "cache",
        "_default_caching_method",
        "_caching_method",
        "_previous_caching_method",
    }
    cache_item_type = CacheItem

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        typed: bool = False,
        lifetime: int | float | None = None,
        call_method: AnyCallable | str = "caching_call",
        collective: bool = True,
        init: bool = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Overriden Attributes #
        self._call_method: AnyCallable = self.caching_call.__func__

        # New Attributes #
        self._is_collective: bool = True

        self.typed: bool = False
        self.is_timed: bool = True
        self.lifetime: int | float | None = None
        self.expiration: int | float | None = 0

        self.cache: Any = None
        self._default_caching_method: AnyCallable = self.no_cache.__func__
        self._caching_method: AnyCallable = self.no_cache.__func__
        self._previous_caching_method: AnyCallable = self.no_cache.__func__

        # Object Construction #
        if init:
            self.construct(
                func=func,
                lifetime=lifetime,
                typed=typed,
                call_method=call_method,
                collective=collective,
            )

    @property
    def is_collective(self) -> bool:
        """Determines if the cache is collective for all method bindings or for each instance.

        When set, the __get__ method will be changed to match the chosen style.
        """
        return self._is_collective

    @is_collective.setter
    def is_collective(self, value: bool) -> None:
        if value is True:
            self._get_method_ = self.get_self_bind
        else:
            self._get_method_ = self.get_copy_bind
        self._is_collective = value

    @property
    def caching_method(self) -> AnyCallable:
        """The method that will be used for caching.

        When set, any function can be set or the name of a method within this object can be given to select it.
        """
        return self._caching_method.__get__(self, self.__class__)

    @caching_method.setter
    def caching_method(self, value: AnyCallable | str) -> None:
        self.set_caching_method(value)

    # Instance Methods #
    # Constructors
    def construct(
        self,
        func: AnyCallable | None = None,
        typed: bool = False,
        lifetime: int | float | None = None,
        call_method: AnyCallable | str = "caching_call",
        collective: bool = True,
    ) -> None:
        """The constructor for this object.

        Args:
            func:  The function to wrap.
            typed: Determines if the function's arguments are type sensitive for caching.
            lifetime: The period between cache resets in seconds.
            call_method: The default call method to use.
            collective: Determines if the cache is collective for all method bindings or for each instance.
        """
        if lifetime is not None:
            self.lifetime = lifetime

        if typed is not None:
            self.typed = typed

        if call_method is not None:
            self.set_call_method(call_method)

        if collective is not None:
            self.is_collective = collective

        super().construct(func=func, call_method=call_method)

    def copy(self) -> "BaseTimedCache":
        """The copy method for this object

        Returns:
            A copy of this object.
        """
        new = super().copy()

        if hasattr(self, self._default_caching_method.__name__):
            new._default_caching_method = getattr(new, self._default_caching_method.__name__)

        if hasattr(self, self._caching_method.__name__):
            new._caching_method = getattr(new, self._caching_method.__name__)

        if hasattr(self, self._previous_caching_method.__name__):
            new._previous_caching_method = getattr(new, self._previous_caching_method.__name__)

        return new

    # Binding
    def get_copy_bind(
        self,
        instance: Any = None,
        owner: type[Any] | None = None,
        new_binding: GetObjectMethod | str = "get_self",
        set_attr: bool = True,
    ) -> "BaseMethod":
        """The __get__ method where it binds a copy of this object to the other object. Changed default parameters.

        Args:
            instance: The other object requesting this object.
            owner: The class of the other object requesting this object.
            new_binding: The binding method the copied object will use.
            set_attr: Determines if the new object will be set as an attribute in the object.

        Returns:
            Either bound self or a new BaseMethod bound to the instance.
        """
        return super().get_copy_bind(instance, owner=owner, new_binding=new_binding, set_attr=set_attr)

    # Object Calling
    def caching_call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the caching function and clears the cache at certain time.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        if self.clear_condition():
            self.clear_cache()

        return self.caching_method(*args, **kwargs)

    def clearing_call(self, *args: Any, **kwargs: Any) -> Any:
        """Clears the cache then calls the caching function.

        Args:
            *args: Arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result or the caching_method.
        """
        self.clear_cache()

        return self.caching_method(*args, **kwargs)

    def clear_condition(self, *args: Any, **kwargs: Any) -> bool:
        """The condition used to determine if the cache should be cleared.

        Args:
            *args: Arguments that could be used to determine if the cache should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the cache should be cleared.

        Returns:
            Determines if the cache should be cleared.
        """
        return self.is_timed and self.lifetime is not None and perf_counter() >= self.expiration

    # Binding
    def bind_to_new(
        self,
        instance: Any,
        owner: type[Any] | None = None,
        name: str | None = None,
        set_attr: bool = True,
    ) -> "BaseTimedCache":
        """Creates a new instance of this object and binds it to another object.

        Args:
            instance: The object ot bing this object to.
            owner: The class of the other object requesting this object.
            name: The name of the attribute this object will bind to in the other object.
            set_attr: Determines if this object will be set as an attribute in the object.

        Returns:
            The new bound deepcopy of this object.
        """
        if hasattr(self, self._call_method.__name__):
            call_method = self._call_method.__name__
        else:
            call_method = self._call_method

        new_obj = type(self)(
            func=self.__func__,
            typed=self.typed,
            lifetime=self.lifetime,
            call_method=call_method,
            collective=self._is_collective,
        )
        new_obj.bind(instance=instance, owner=owner, name=name, set_attr=set_attr)
        return new_obj

    # Caching
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

        The key is constructed in a way that is flat as possible rather than
        as a nested structure that would take more memory.

        If there is only a single argument and its data type is known to cache
        its hash value, then that argument is returned without a wrapper.  This
        saves space and improves lookup speed.

        """
        # All of code below relies on kwds preserving the order input by the user.
        # Formerly, we sorted() the kwds before looping.  The new way is *much*
        # faster; however, it means that f(x=1, y=2) will now be treated as a
        # distinct call from f(y=2, x=1) which will be cached separately.
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

    def set_caching_method(self, method: AnyCallable | str) -> None:
        """Sets the caching method to another function or a method within this object can be given to select it.

        Args:
            method: The function or name to set the caching method to.
        """
        if isinstance(method, str):
            self._caching_method = getattr(self, method).__func__
        else:
            self._caching_method = method

    def no_cache(self, *args: Any, **kwargs: Any) -> Any:
        """A direct call to wrapped function with no caching.

        Args:
            *args: Arguments of the wrapped function.
            **kwargs: Keyword Arguments of the wrapped function.

        Returns:
            The result of the wrapped function.
        """
        return self.__func__(*args, **kwargs)

    # Cache Control
    @abc.abstractmethod
    def clear_cache(self) -> None:
        """Clear the cache and update the expiration of the cache."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    def stop_caching(self) -> None:
        """Stops using the cache, storing the method used."""
        self._previous_caching_method = self._caching_method
        self._caching_method = self.__func__
        self.clear_cache()

    def resume_caching(self) -> None:
        """Resumes caching by setting the call method to the previous call method"""
        self._caching_method = self._previous_caching_method

    @contextmanager
    def pause_caching(self) -> Callable[..., Iterator[None]]:
        self.stop_caching()
        yield None
        self.resume_caching()
