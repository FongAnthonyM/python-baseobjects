"""basemeta.py
BaseMeta is an abstract metaclass that implements fundamental functions for metaclass objects.

This module provides the BaseMeta class, which is an abstract metaclass that inherits from ABCMeta and adds
functionality for copying and deep copying metaclass objects. It serves as a foundation for other metaclasses in the
baseobjects package.

Metaclasses are classes whose instances are classes themselves, rather than objects. They provide a way to customize
class creation and behavior. The BaseMeta class extends Python's ABCMeta (Abstract Base Class Metaclass) to add proper
support for copying and deep copying of metaclass instances (i.e., classes created with this metaclass). This is
particularly important for frameworks that need to manipulate or duplicate class definitions at runtime.
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
from abc import ABCMeta
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
class BaseMeta(ABCMeta):
    """An abstract metaclass that implements fundamental functions for metaclass objects.

    BaseMeta extends Python's ABCMeta (Abstract Base Class Metaclass) to provide proper support for copying and deep
    copying of metaclass instances (i.e., classes created with this metaclass). This is essential for frameworks that
    need to manipulate or duplicate class definitions at runtime.

    The metaclass implements the copy protocol through __copy__ and __deepcopy__ methods, which follow Python's standard
    copy algorithms but are adapted for the special nature of metaclass instances. These methods ensure that classes can
    be properly copied while maintaining their type structure and attributes.

    This class is designed to be used as a metaclass for other classes, typically by specifying it in the class
    definition: `class MyClass(metaclass=BaseMeta): ...`
    """

    # Magic Methods #
    # Construction/Destruction
    def __copy__(cls) -> Any:
        """Create a shallow copy of this metaclass instance (class).

        This method implements Python's copy protocol for shallow copying of metaclass instances (classes). It is called
        by the copy.copy() function when applied to a class created with this metaclass. The method follows Python's
        standard copy algorithm, adapted for metaclasses:

        1. First, it checks if a copy method is registered for this class in the copy dispatch table
        2. If the class is a subclass of type (which metaclass instances are), it uses _copy_immutable
        3. Otherwise, it attempts to use a registered reductor function or the object's __reduce_ex__ or __reduce__
           methods
        4. Finally, it reconstructs the class from the reduction result

        This implementation ensures proper handling of custom copy behavior, immutable objects, and reduction methods
        when copying class definitions.

        Returns:
            A shallow copy of this class, with the same metaclass but independent class attributes.

        Raises:
            Error: If the class cannot be shallow-copied because no suitable reduction or copy strategy is available.
        """
        meta_type = type(cls)

        copier = _copy_dispatch.get(meta_type)
        if copier:
            return copier(cls)

        if issubclass(meta_type, type):
            # treat it as a regular class:
            return _copy_immutable(cls)

        reductor = dispatch_table.get(meta_type)
        if reductor is not None:
            rv = reductor(cls)
        else:
            reductor = getattr(cls, "__reduce_ex__", None)
            if reductor is not None:
                rv = reductor(4)
            else:
                reductor = getattr(cls, "__reduce__", None)
                if reductor:
                    rv = reductor()
                else:
                    msg = f"un(shallow)copyable object of type {meta_type}"
                    raise Error(msg)

        if isinstance(rv, str):
            return cls
        return _reconstruct(cls, None, *rv)

    def __deepcopy__(cls, memo: dict | None = None, _nil: list | None = None) -> Any:
        """Create a deep copy of this metaclass instance (class).

        This method implements Python's copy protocol for deep copying of metaclass instances (classes). It is called by
        the copy.deepcopy() function when applied to a class created with this metaclass. The method follows Python's
        standard deep copy algorithm, adapted for metaclasses:

        1. If a memo dictionary is not provided, it creates one to track objects that have already been copied
           to prevent infinite recursion with circular references
        2. If this class has already been copied (present in the memo dictionary), it returns the existing copy
        3. It checks if a deepcopy method is registered for this class in the deepcopy dispatch table
        4. If the class is a subclass of type (which metaclass instances are), it uses _deepcopy_atomic
        5. Otherwise, it attempts to use a registered reductor function or the object's __reduce_ex__ or __reduce__
           methods
        6. Finally, it reconstructs the class from the reduction result and stores it in the memo dictionary

        This implementation ensures proper handling of circular references, custom deepcopy behavior, immutable objects,
        and reduction methods when copying class definitions.

        Args:
            memo: A dictionary that maps object IDs to their copies, used to handle circular references.
                If None, a new dictionary is created.
            _nil: An internal parameter used as a sentinel value for the memo dictionary lookup.
                This should not be specified by callers.

        Returns:
            A deep copy of this class, with the same metaclass but completely independent class attributes, including
            independent copies of all mutable objects contained within the class definition.

        Raises:
            Error: If the class cannot be deep-copied because no suitable reduction or deepcopy strategy is available.
        """
        if memo is None:
            memo = {}
        if _nil is None:
            _nil = []

        d = id(cls)
        y = memo.get(d, _nil)
        if y is not _nil:
            return y

        meta_type = type(cls)

        # If copy method is in the deepcopy dispatch then use it
        copier = _deepcopy_dispatch.get(meta_type)
        if copier is not None:
            y = copier(cls, memo)
        else:
            # Handle if this object is a type subclass
            if issubclass(meta_type, type):
                y = _deepcopy_atomic(cls, memo)
            else:
                reductor = dispatch_table.get(meta_type)
                if reductor:
                    rv = reductor(cls)
                else:
                    reductor = getattr(cls, "__reduce_ex__", None)
                    if reductor is not None:
                        rv = reductor(4)
                    else:
                        reductor = getattr(cls, "__reduce__", None)
                        if reductor:
                            rv = reductor()
                        else:
                            msg = f"un(deep)copyable object of type {meta_type}"
                            raise Error(msg)
                if isinstance(rv, str):
                    y = cls
                else:
                    y = _reconstruct(cls, memo, *rv)

        # If is its own copy, don't memoize.
        if y is not cls:
            memo[d] = y
            _keep_alive(cls, memo)  # Make sure x lives at least as long as d

        return y
