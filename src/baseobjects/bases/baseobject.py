"""baseobject.py
BaseObject is an abstract class which implements some basic functions that all objects should have.
"""
# Package Header #
from ..header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #
from abc import ABC
from copy import (
    _copy_dispatch,
    _copy_immutable,
    _deepcopy_dispatch,
    _deepcopy_atomic,
    _keep_alive,
    _reconstruct,
    Error,
)
from copyreg import dispatch_table
import sys
from typing import Any

# Third-Party Packages #

# Local Packages #


# Definitions #
# Classes #
class BaseObject(ABC):
    """An abstract class that implements some basic functions that all objects should have."""

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def __copy__(self) -> Any:
        """The copy magic method (shallow).

        Returns:
            A shallow copy of this object.
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
        """The deepcopy magic method based on python's deepcopy function.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
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

    # Pickling
    def __getstate__(self) -> None | dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]]:
        """Gets the object's state for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        # Get dict
        if _dict_ := getattr(self, "__dict__", None):
            _dict_ = _dict_.copy()

        # Get slots
        if _slots_ := getattr(self, "__slots__", None):
            _slots_ = {s: getattr(self, s) for s in _slots_}

        # Return the correct state
        match _dict_, _slots_:
            case None, None:
                return None
            case dict(), None | ():
                return _dict_
            case None, dict():
                return None, _slots_
            case dict(), dict():
                return _dict_, _slots_

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object.
        """
        match state:
            case dict():
                self.__dict__.update(state)
            case tuple():
                if state[0] is not None:
                    self.__dict__.update(state[0])
                for slot_name, value in state[1].items():
                    setattr(self, slot_name, value)
            case None:
                return
            case _:
                raise TypeError(f"State must be None, dict, or tuple, not {type(state)}")

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, *args: Any, **kwargs: Any) -> None:
        """Constructs this object.

        Args:
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """

    def copy(self) -> Any:
        """Creates a shallow copy of this object.

        Returns:
            A shallow copy of this object.
        """
        return self.__copy__()

    def deepcopy(self, memo: dict | None = None) -> Any:
        """Creates a deep copy of this object.

        Args:
            memo: A dictionary of user defined information to pass to another deepcopy call which it will handle.

        Returns:
            A deep copy of this object.
        """
        return self.__deepcopy__(memo=memo)
