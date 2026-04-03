"""basereducible.py
BaseReducible is an abstract class that implements basic functions for object reduction and pickling.

This module provides the BaseReducible class, which extends BaseObject to add functionality for object reduction and
pickling. It implements __getstate__ and __setstate__ methods to properly handle both __dict__ and __slots__ attributes
during serialization and deserialization.

The BaseReducible class serves as a foundation for objects that need to be serialized (pickled) and deserialized
(unpickled), ensuring that both regular attributes (stored in __dict__) and slot attributes (defined in __slots__) are
properly preserved during these operations. This is particularly important for classes that use __slots__ for memory
optimization or to restrict attribute assignment.
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
from typing import Any

# Local Packages #
from .baseobject import BaseObject


# Definitions #
# Classes #
class BaseReducible(BaseObject):
    """An abstract class that implements basic functions for object reduction and pickling.

    BaseReducible extends BaseObject to provide standardized methods for object serialization and deserialization
    through Python's pickle mechanism. It properly handles both regular attributes (stored in __dict__) and
    slot attributes (defined in __slots__), ensuring that all object state is preserved during pickling and unpickling.

    This class serves as a foundation for objects that need to be serialized, stored, and later reconstructed,
    such as objects that are persisted to disk or transmitted over a network.
    """

    # Magic Methods #
    # Reduction/Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the object's state for pickling.

        This method is called by the pickle module when serializing the object. It extracts the object's state from both
        __dict__ (if present) and __slots__ (if present), and returns it in a format that can be properly restored by
        __setstate__ during unpickling.

        The method handles four different cases:
        1. Neither __dict__ nor __slots__ are present: Returns None
        2. Only __dict__ is present: Returns a copy of the __dict__
        3. Only __slots__ is present: Returns a tuple of (None, slots_dict)
        4. Both __dict__ and __slots__ are present: Returns a tuple of (dict_copy, slots_dict)

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: Neither __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        # Gets dict
        _dict_: dict[str, Any] | None = getattr(self, "__dict__", None)
        if _dict_:
            _dict_ = _dict_.copy()
        else:
            _dict_ = None

        # Gets slots
        _slots_ = getattr(self, "__slots__", None)
        if _slots_:
            temp_slots = {}
            for s in _slots_:
                try:
                    temp_slots[s] = getattr(self, s)
                except AttributeError:
                    pass
            _slots_ = temp_slots
        else:
            _slots_ = None

        # Returns the correct state
        if _dict_ is not None and _slots_ is not None:
            return _dict_, _slots_
        elif _slots_ is not None:
            return None, _slots_
        elif _dict_ is not None:
            return _dict_
        else:
            return None

    def __setstate__(self, state: Any) -> None:
        """Sets the object's state from a pickled state.

        This method is called by the pickle module when deserializing the object. It restores the object's state from
        the data that was previously returned by __getstate__ during pickling. The method handles different state
        formats to properly restore both __dict__ and __slots__ attributes.

        The method handles four different cases based on the type of state:
        1. None: No state to restore, so nothing is done
        2. dict: The state represents __dict__ attributes, which are updated into the object's __dict__
        3. tuple[None, dict]: The state represents __slots__ attributes, which are set individually
        4. tuple[dict, dict]: The state represents both __dict__ and __slots__ attributes, which are restored
           accordingly

        If the state is of an unexpected type, a TypeError is raised.

        By default, the state can be one of the following types with the corresponding behavior:
            None: Will not set any state.
            dict: Will set the __dict__ attribute to the state.
            tuple[None, dict]: Will set the slot values to the second dict of the tuple.
            tuple[dict, dict]: Will set the __dict__ attribute to the first dict of the tuple and set the slot values
                to the second dict of the tuple.

        Args:
            state: An object which can be used to set the state of this object. This should be the value previously
                returned by __getstate__.

        Raises:
            TypeError: If the state is not None, dict, or tuple.
        """
        if isinstance(state, dict):
            self.__dict__.update(state)
        elif isinstance(state, tuple):
            if state[0] is not None:
                self.__dict__.update(state[0])
            for slot_name, value in state[1].items():
                setattr(self, slot_name, value)
        elif state is None:
            return
        else:
            msg = f"State must be None, dict, or tuple, not {type(state)}"
            raise TypeError(msg)
