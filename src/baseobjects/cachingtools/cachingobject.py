"""cachingobject.py
An abstract class which creates properties for this class automatically.

This module provides the CachingObject class, which is an abstract base class that implements caching functionality
for methods and properties. It allows for enabling, disabling, and managing caches within objects, as well as
setting cache lifetimes and clearing caches.
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
from typing import Any, ClassVar

# Local Packages #
from ..bases import BaseReducible
from ..metaclasses import InitMeta
from .caches import BaseTimedCache


# Definitions #
# Classes #
class CachingObject(BaseReducible, metaclass=InitMeta):
    """An abstract class which has functionality for functions that are caching.

    Attributes:
        _is_caching: Determines if the caching functions of this object will cache.
        _caches: All the caches within this object.
    """

    # Class Attributes #
    _caches_: ClassVar[dict[str, BaseTimedCache]] = {}

    # Class Methods #
    @staticmethod
    def _is_caching_instance(attribute: Any) -> bool:
        """Determines if the given attribute is a cache instance or contains one.

        Args:
            attribute: The attribute to check.

        Returns:
            True if it is or contains a cache instance, False otherwise.
        """
        return isinstance(attribute, BaseTimedCache)

    # Construction/Destruction
    @classmethod
    def _init_class_(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        """Initializes the class when it is created.

        Args:
            name: The name of the class.
            bases: The base classes of the class.
            namespace: The namespace of the class.
        """
        # Class Construction #
        cls._caches_ = cls._caches_.copy()

        # Update the class-level caches from the current namespace
        for name, cls_attribute in namespace.items():
            if cls._is_caching_instance(cls_attribute):
                cls._caches_[name] = cls_attribute
            elif name in cls._caches_:
                # If a subclass overrides a cache with a non-cache, remove it
                del cls._caches_[name]

    # Attributes #
    __cache__: dict[str, Any]
    _is_caching: bool = True
    _caches: dict[str, BaseTimedCache]

    # Properties #
    @property
    def any_caching(self) -> bool:
        """Returns if any cache has its caching enabled."""
        return self.get_any_caching()

    @property
    def all_caching(self) -> bool:
        """Returns if all caches have their caching enabled."""
        return self.get_all_caching()

    @property
    def any_caches_active(self) -> bool:
        """Returns if any caches are currently active."""
        return self.get_any_caches_active()

    @property
    def all_caches_active(self) -> bool:
        """Returns if all caches are currently active."""
        return self.get_all_caches_active()

    @property
    def any_caches_timed(self) -> bool:
        """Returns if any cache has timing enabled."""
        return self.get_any_caches_timed()

    @property
    def all_caches_timed(self) -> bool:
        """Returns if all caches have timing enabled."""
        return self.get_all_caches_timed()

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes this object with the given arguments.

        This constructor prepares the instance-level cache registry from the class-level
        definition and then delegates to the parent initializer. It accepts arbitrary
        positional and keyword arguments to support flexible subclass initializers.

        Args:
            *args: Positional arguments forwarded to the parent initializer.
            **kwargs: Keyword arguments forwarded to the parent initializer.
        """
        # Attributes #
        self.__cache__ = {}
        self._caches = self._caches_.copy()

        # Parent Initialization #
        super().__init__(*args, **kwargs)

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

        Deletes all cache methods for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        match state:
            case dict():
                keys = [k for k, v in state.items() if isinstance(v, BaseTimedCache)]
                for k in keys:
                    del state[k]
                state.pop("__cache__", None)
                state.pop("_caches", None)
            case tuple() if state[0] is not None:
                keys = [k for k, v in state[0].items() if isinstance(v, BaseTimedCache)]
                for k in keys:
                    del state[0][k]
                state[0].pop("__cache__", None)
                state[0].pop("_caches", None)
        return state

    def __setstate__(self, state: Any) -> None:
        """Sets the state of this object.

        Args:
            state: The state to set.
        """
        super().__setstate__(state)
        self._caches = self._caches_.copy()
        self.__cache__ = {}

    # Instance Methods #
    # Inspection
    def get_caches(self) -> dict[str, BaseTimedCache]:
        """Gets all the caches in this object.

        Returns:
            All the cache objects within this object.
        """
        self._caches.clear()

        # Iterate over MRO in reverse to allow overriding by subclasses
        slot_names = set()
        for cls in reversed(self.__class__.mro()):
            if (cls_dict := getattr(cls, "__dict__", None)) is not None:
                for name, attribute in cls_dict.items():
                    if self._is_caching_instance(attribute):
                        self._caches[name] = getattr(self, name)
                    elif name in self._caches:
                        # If a subclass overrides a cache with a non-cache, remove it
                        del self._caches[name]

            if isinstance((slots := getattr(cls, "__slots__", ())), str):
                slot_names.add(slots)
            else:
                slot_names.update(slots)

        # Check instance-level caches in slots
        for name in slot_names:
            if name != "__dict__" and name != "__weakref__":
                if (attribute := getattr(self, name, None)) is not None:
                    if self._is_caching_instance(attribute):
                        self._caches[name] = attribute
                    elif name in self._caches:
                        # Instance-level override of a class-level cache
                        del self._caches[name]

        # Check instance-level caches in __dict__
        if (instance_dict := getattr(self, "__dict__", None)) is not None:
            for name, attribute in instance_dict.items():
                if self._is_caching_instance(attribute):
                    self._caches[name] = attribute
                elif name in self._caches:
                    # Instance-level override of a class-level cache
                    del self._caches[name]

        return self._caches

    # State
    def get_any_caching(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if any cache has its caching enabled.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If any cache has its caching enabled.
        """
        if not self._is_caching:
            return False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    g_info(self).is_caching
                ):
                    return True
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and g_info(self).is_caching:
                    return True

        return False

    def get_all_caching(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if all caches have their caching enabled.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If all caches have their caching enabled.
        """
        if not self._is_caching:
            return False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    not g_info(self).is_caching
                ):
                    return False
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and not g_info(self).is_caching:
                    return False

        return True

    def get_any_caches_active(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if any caches are currently active (not in 'no_cache' mode).

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If any caches are currently active.
        """
        if not self._is_caching:
            return False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    g_info(self).cache_method != "no_cache"
                ):
                    return True
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and g_info(self).cache_method != "no_cache":
                    return True

        return False

    def get_all_caches_active(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if all caches are currently active (not in 'no_cache' mode).

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If all caches are currently active.
        """
        if not self._is_caching:
            return False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    g_info(self).cache_method == "no_cache"
                ):
                    return False
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and g_info(self).cache_method == "no_cache":
                    return False

        return True

    def get_any_caches_timed(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if any cache has timing enabled.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If any cache has timing enabled.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    g_info(self).is_timed
                ):
                    return True
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and g_info(self).is_timed:
                    return True

        return False

    def get_all_caches_timed(self, exclude: set[str] | None = None, caches: bool = False) -> bool:
        """Checks if all caches have timing enabled.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.

        Returns:
            If all caches have timing enabled.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if (
                    name not in exclude and
                    (g_info := getattr(cache, "get_cache_info", None)) is not None and
                    not g_info(self).is_timed
                ):
                    return False
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None and not g_info(self).is_timed:
                    return False

        return True

    # Caches Operators
    def enable_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Enables all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if not exclude:
            self._is_caching = True

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (method := getattr(cache, "enable_caching", None)) is not None:
                    method(self)
        else:
            for cache in self._caches.values():
                if (method := getattr(cache, "enable_caching", None)) is not None:
                    method(self)

    def disable_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Disables all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if not exclude:
            self._is_caching = False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (method := getattr(cache, "disable_caching", None)) is not None:
                    method(self)
        else:
            for cache in self._caches.values():
                if (method := getattr(cache, "disable_caching", None)) is not None:
                    method(self)

    def stop_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Stops all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if not exclude:
            self._is_caching = False

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (method := getattr(cache, "stop_caching", None)) is not None:
                    method(self)
        else:
            for cache in self._caches.values():
                if (method := getattr(cache, "stop_caching", None)) is not None:
                    method(self)

    def resume_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Resumes all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if not exclude:
            self._is_caching = True

        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (method := getattr(cache, "resume_caching", None)) is not None:
                    method(self)
        else:
            for cache in self._caches.values():
                if (method := getattr(cache, "resume_caching", None)) is not None:
                    method(self)

    def timeless_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Sets all caches to have no expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (g_info := getattr(cache, "get_cache_info", None)) is not None:
                    g_info(self).is_timed = False
        else:
            for cache in self._caches.values():
                if (g_info := getattr(cache, "get_cache_info", None)) is not None:
                    g_info(self).is_timed = False

    def timed_caching(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Sets all caches to have an expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (get_cache_info := getattr(cache, "get_cache_info", None)) is not None:
                    get_cache_info(self).is_timed = True
        else:
            for cache in self._caches.values():
                if (get_cache_info := getattr(cache, "get_cache_info", None)) is not None:
                    get_cache_info(self).is_timed = True

    def set_lifetimes(
        self,
        lifetime: int | float | None,
        exclude: set[str] | None = None,
        caches: bool = False,
    ) -> None:
        """Sets all caches to have a specific lifetime.

        Args:
            lifetime: The lifetime for all the caches to have.
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (get_cache_info := getattr(cache, "get_cache_info", None)) is not None:
                    get_cache_info(self).lifetime = lifetime
        else:
            for cache in self._caches.values():
                if (get_cache_info := getattr(cache, "get_cache_info", None)) is not None:
                    get_cache_info(self).lifetime = lifetime

    def clear_caches(self, exclude: set[str] | None = None, caches: bool = False) -> None:
        """Clears all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            caches: Determines if get_caches will run before setting the caches.
        """
        if caches:
            self.get_caches()

        if exclude:
            for name, cache in self._caches.items():
                if name not in exclude and (method := getattr(cache, "clear_cache", None)) is not None:
                    method(self)
        else:
            for cache in self._caches.values():
                if (method := getattr(cache, "clear_cache", None)) is not None:
                    method(self)
