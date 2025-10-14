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
        _is_cache: Determines if the caching functions of this object will cache.
        _caches: All the caches within this object.
    """

    # Class Attributes #
    _caches_: ClassVar[set[str]] = set()

    # Class Methods #
    # Construction/Destruction
    @classmethod
    def _init_class_(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> None:
        super().__init__(name, bases, namespace)
        cls._caches_ = cls._caches_.copy()

        for name, cls_attribute in namespace.items():
            if isinstance(cls_attribute, BaseTimedCache):
                cls._caches_.add(name)

    # Attributes #
    _is_cache: bool = True
    _caches: set[str]

    # Properties #
    @property
    def is_cache(self) -> bool:
        """Determines if the caching functions are enabled and puts them in the correct state when set."""
        return self._is_cache

    @is_cache.setter
    def is_cache(self, value: bool) -> None:
        if value is not self._is_cache:
            if value:
                self.enable_caching()
            else:
                self.disable_caching()

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the caching object.

        This constructor prepares the instance-level cache registry from the class-level
        definition and then delegates to the parent initializer. It accepts arbitrary
        positional and keyword arguments to support flexible subclass initializers.

        Args:
            *args: Positional arguments forwarded to the parent initializer.
            **kwargs: Keyword arguments forwarded to the parent initializer.
        """
        # Attributes #
        self._caches = self._caches_.copy()

        # Parent Initialization #
        super().__init__(*args, **kwargs)

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Gets the object's state for pickling.

        Deletes all cache methods for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        for name in self.get_caches():
            if name in state:
                del state[name]
        return state

    # Instance Methods #
    # Caches Operators
    def get_caches(self) -> set[str]:
        """Get all the caches in this object.

        Returns:
            All the cache objects within this object.
        """
        for name in dir(self):
            attribute = getattr(type(self), name, None)
            if isinstance(attribute, BaseTimedCache) or (
                attribute is None and isinstance(getattr(self, name), BaseTimedCache)
            ):
                self._caches.add(name)

        return self._caches

    def enable_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Enables all caches to cache.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Enable caches in the set.
        for name in caches:
            getattr(self, name).resume_caching()

        self._is_cache = True

    def disable_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Disables all caches to cache.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Disable caches in the set.
        for name in caches:
            getattr(self, name).stop_caching()

        self._is_cache = False

    def timeless_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Sets all caches to have no expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Disable expiration all caches in set.
        for name in caches:
            getattr(self, name).is_timed = False

    def timed_caching(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Sets all caches to have an expiration time.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Enable expiration for all caches in the set.
        for name in caches:
            getattr(self, name).is_timed = True

    def set_lifetimes(
        self,
        lifetime: int | float | None,
        exclude: set[str] | None = None,
        get_caches: bool = False,
    ) -> None:
        """Sets all caches to have an specific lifetime.

        Args:
            lifetime: The lifetime for all the caches to have.
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Set all the lifetimes
        for name in caches:
            getattr(self, name).lifetime = lifetime

    def clear_caches(self, exclude: set[str] | None = None, get_caches: bool = False) -> None:
        """Clears all caches in this object.

        Args:
            exclude: The names of the caches to exclude from caching.
            get_caches: Determines if get_caches will run before setting the caches.
        """
        # Get caches if needed.
        if get_caches:
            self.get_caches()

        # Exclude caches if needed.
        if exclude is not None:
            caches = self._caches.difference(exclude)
        else:
            caches = self._caches

        # Clear caches in the set.
        for name in caches:
            getattr(self, name).clear_cache()
