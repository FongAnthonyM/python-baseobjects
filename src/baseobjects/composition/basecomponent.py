"""basecomponent.py

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
from weakref import ReferenceType

# Third-Party Packages #

# Local Packages #
from ..bases import BaseReducible
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseComponent(BaseReducible):
    """A basic component object.

    Attributes:
        _composite: A weak reference to the object which this object is a component of.

    Args:
        composite: The object which this object is a component of.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _composite: ReferenceType[BaseComposite] | None = None

    # Properties #
    @property
    def composite(self) -> Any:
        """The composite object which this object is a component of."""
        try:
            return self._composite()
        except TypeError:
            return None

    @composite.setter
    def composite(self, value: Any) -> None:
        self._composite = None if value is None else ReferenceType(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        composite: Any = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(composite=composite, **kwargs)

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
        state = super().__getstate__()
        state["_composite"] = self.composite  # Make a strong reference for pickle
        return state

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
        # Remove strong reference
        _composite = state.pop("_composite", None)

        # Set State
        super().__setstate__(state)

        # Set weak reference
        self.composite = _composite

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, composite: Any = None, **kwargs: Any) -> None:
        """Constructs this object.

        Args:
            composite: The object which this object is a component of.
            **kwargs: Keyword arguments for inheritance.
        """
        if composite is not None:
            self.composite = composite

        super().construct(**kwargs)
