"""basecomponent.py
A basic component object for use in composite objects.

This module provides the BaseComponent class, which implements the Component part of the Composite design pattern.
It allows objects to be used as components within composite objects, maintaining a weak reference to their parent
composite to avoid circular references while enabling bidirectional navigation between components and composites.
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
        if self._composite is None:
            return None
        return self._composite()

    @composite.setter
    def composite(self, value: Any) -> None:
        self._composite = None if value is None else ReferenceType(value)

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        composite: Any = None,
        *,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            composite: Optional composite that owns this component.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments for construction.
        """
        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(composite=composite, **kwargs)

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

        Returns:
            The state returned will be either of the following types based on the presence of __dict__ and __slots__:
                None: __dict__ nor __slots__ are present.
                dict: __dict__ is present and __slots__ is not present.
                tuple[None, dict]: __dict__ is not present and __slots__ is present.
                tuple[dict, dict]: __dict__ is present and __slots__ is present.
        """
        state = super().__getstate__()
        composite = self.composite

        if state is None:
            return {"_composite": composite}
        elif isinstance(state, dict):
            state["_composite"] = composite
            return state
        elif isinstance(state, tuple):
            d, s = state
            if d is None:
                d = {}
            d["_composite"] = composite
            return d, s
        else:
            return None  # type: ignore[unreachable]

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
        # Removes strong reference
        composite = None
        if isinstance(state, dict):
            composite = state.pop("_composite", None)
        elif isinstance(state, tuple) and state[0] is not None:
            composite = state[0].pop("_composite", None)

        # Sets State
        super().__setstate__(state)

        # Sets weak reference
        self.composite = composite

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, composite: Any = None, **kwargs: Any) -> None:
        """Constructs this object with the given arguments.

        Args:
            composite: The object which this object is a component of.
            **kwargs: Keyword arguments for inheritance.
        """
        if composite is not None:
            self.composite = composite

        super().construct(**kwargs)
