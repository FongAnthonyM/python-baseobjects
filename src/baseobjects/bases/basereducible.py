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
from typing import Any

# Third-Party Packages #

# Local Packages #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseReducible(BaseObject):
    """An abstract class that implements some basic functions for reduction."""

    # Magic Methods #
    # Reduction/Pickling
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
