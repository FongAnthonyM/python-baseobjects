"""baseobject.py
BaseObject is an abstract class which implements fundamental functions that all objects should have.

This module provides the BaseObject class, which is an abstract base class that implements fundamental functionality
that should be available in all objects, such as copying and deep copying. It serves as a foundation for other classes
in the baseobjects package and provides a consistent interface for object manipulation.

The BaseObject class is designed to be a head class for object hierarchies, providing common functionality that
ensures consistent behavior across all derived classes. It implements Python's copy protocol through the __copy__
and __deepcopy__ methods, which are essential for creating both shallow and deep copies of objects. These methods
are implemented using Python's internal copy mechanisms to ensure proper copying behavior, including handling of
circular references and custom reduction methods.
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
from abc import ABC
from copy import (
    Error,
    _copy_dispatch,
    _copy_immutable,
    _deepcopy_atomic,
    _deepcopy_dispatch,
    _keep_alive,
    _reconstruct,
)
from copyreg import dispatch_table
from typing import Any


# Definitions #
# Classes #
class BaseObject(ABC):
    """An abstract class that implements fundamental functions that all objects should have.

    BaseObject serves as a foundation class for creating well-behaved Python objects. It provides implementations for
    essential object operations such as copying and deep copying. These implementations follow Python's standard
    protocols and handle edge cases appropriately.

    This class is designed to be subclassed rather than instantiated directly. Derived classes inherit the copy
    functionality and can override or extend it as needed. The class provides both magic methods
    (__copy__, __deepcopy__) and convenience methods (copy, deepcopy) for creating copies of objects.
    """

    # Magic Methods #
    # Construction/Destruction #
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize a new BaseObject instance.

        This is a minimal initialization method that accepts arbitrary positional and keyword arguments but does not
        perform any operations with them. This allows derived classes to have flexible initialization signatures without
        needing to explicitly handle parent class arguments.

        In most cases, derived classes should call super().__init__(*args, **kwargs) to ensure proper initialization of
        the inheritance chain, even though this base implementation is empty.

        Args:
            *args: Positional arguments, not used in this implementation but a placeholder for future expansion.
            **kwargs: Keyword arguments, not used in this implementation but a placeholder for future expansion.
        """

    def __copy__(self) -> Any:
        """Create a shallow copy of this object.

        This method implements Python's copy protocol for shallow copying. It is called by the copy.copy() function and
        follows Python's standard copy algorithm:

        1. First, it checks if a copy method is registered for this class in the copy dispatch table
        2. If the class is a subclass of type, it uses _copy_immutable
        3. Otherwise, it attempts to use a registered reductor function or the object's __reduce_ex__ or __reduce__
           methods
        4. Finally, it reconstructs the object from the reduction result

        This implementation ensures proper handling of custom copy behavior, immutable objects, and reduction methods.

        Returns:
            A shallow copy of this object, with the same type but independent state.
        """
        cls = type(self)

        copier = _copy_dispatch.get(cls)
        if copier:
            return copier(self)

        if issubclass(cls, type):
            # treat it as a regular class:
            return _copy_immutable(self)

        reductor = dispatch_table.get(cls)
        if reductor is not None:
            rv = reductor(self)
        else:
            reductor = getattr(self, "__reduce_ex__", None)
            if reductor is not None:
                rv = reductor(4)
            else:
                reductor = getattr(self, "__reduce__", None)
                if reductor:
                    rv = reductor()
                else:
                    raise Error("un(shallow)copyable object of type %s" % cls)

        if isinstance(rv, str):
            return self
        return _reconstruct(self, None, *rv)

    def __deepcopy__(self, memo: dict | None = None, _nil=[]) -> Any:
        """Create a deep copy of this object.

        This method implements Python's copy protocol for deep copying. It is called by the copy.deepcopy() function and
        follows Python's standard deep copy algorithm:

        1. If a memo dictionary is not provided, it creates one to track objects that have already been copied to
           prevent infinite recursion with circular references
        2. If this object has already been copied (present in the memo dictionary), it returns the existing copy
        3. It checks if a deepcopy method is registered for this class in the deepcopy dispatch table
        4. If the class is a subclass of type, it uses _deepcopy_atomic
        5. Otherwise, it attempts to use a registered reductor function or the object's __reduce_ex__ or __reduce__
           methods
        6. Finally, it reconstructs the object from the reduction result and stores it in the memo dictionary

        This implementation ensures proper handling of circular references, custom deepcopy behavior, immutable objects,
        and reduction methods.

        Args:
            memo: A dictionary that maps object IDs to their copies, used to handle circular references.
                If None, a new dictionary is created.
            _nil: An internal parameter used as a sentinel value for the memo dictionary lookup.
                This should not be specified by callers.

        Returns:
            A deep copy of this object, with the same type but completely independent state,
            including independent copies of all mutable objects contained within.
        """
        if memo is None:
            memo = {}

        d = id(self)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y

        cls = type(self)

        # If copy method is in the deepcopy dispatch then use it
        copier = _deepcopy_dispatch.get(cls)
        if copier is not None:
            y = copier(self, memo)
        else:
            # Handle if this object is a type subclass
            if issubclass(cls, type):
                y = _deepcopy_atomic(self, memo)
            else:
                reductor = dispatch_table.get(cls)
                if reductor:
                    rv = reductor(self)
                else:
                    reductor = getattr(self, "__reduce_ex__", None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(self, "__reduce__", None)
                        if reductor:
                            rv = reductor()
                        else:
                            raise Error("un(deep)copyable object of type %s" % cls)
                if isinstance(rv, str):
                    y = self
                else:
                    y = _reconstruct(self, memo, *rv)

        # If is its own copy, don't memoize.
        if y is not self:
            memo[d] = y
            _keep_alive(self, memo)  # Make sure x lives at least as long as d

        return y

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, *args: Any, **kwargs: Any) -> None:
        """Construct this object with the given arguments.

        This method is intended to be called during object initialization to set up the object's state. Unlike __init__,
        which is automatically called during object creation, construct must be explicitly called. This pattern allows
        for more flexible initialization strategies, such as deferred initialization or re-initialization of existing
        objects.

        In the BaseObject implementation, this method is empty and serves as a placeholder for derived classes to
        override. Derived classes should call super().construct(*args, **kwargs) to ensure proper initialization of the
        inheritance chain.

        Args:
            *args: Positional arguments, not used in this implementation but a placeholder for future expansion.
            **kwargs: Keyword arguments, not used in this implementation but a placeholder for future expansion.
        """

    def copy(self) -> Any:
        """Create a shallow copy of this object.

        This is a convenience method that delegates to the __copy__ magic method, making it easier to create shallow
        copies without having to import the copy module. It provides the same functionality as copy.copy(self).

        Returns:
            A shallow copy of this object, with the same type but independent top-level state.
        """
        return self.__copy__()

    def deepcopy(self, memo: dict | None = None) -> Any:
        """Create a deep copy of this object.

        This is a convenience method that delegates to the __deepcopy__ magic method, making it easier to create deep
        copies without having to import the copy module. It provides the same functionality as copy.deepcopy(self).

        Args:
            memo: A dictionary that maps object IDs to their copies, used to handle circular references.
                If None, a new dictionary is created.

        Returns:
            A deep copy of this object, with the same type but completely independent state,
            including independent copies of all mutable objects contained within.
        """
        return self.__deepcopy__(memo=memo)
