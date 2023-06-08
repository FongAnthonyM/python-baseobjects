"""basecomponent.py

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
import weakref

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseComponent(BaseObject):
    """A basic component object.

    Attributes:
        _composite: A weak reference to the object which this object is a component of.

    Args:
        composite: The object which this object is a component of.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        composite: Any = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._composite: BaseComposite | None = None

        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(composite=composite, **kwargs)

    @property
    def composite(self) -> Any:
        """The composite object which this object is a component of."""
        try:
            return self._composite()
        except TypeError:
            return None

    @composite.setter
    def composite(self, value: Any) -> None:
        self._composite = None if value is None else weakref.ref(value)

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object

        Returns:
            dict: A dictionary of this object's attributes.
        """
        state = self.__dict__.copy()
        state["_composite"] = None
        return state

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
