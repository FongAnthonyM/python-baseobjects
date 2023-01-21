""" component.py

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
from .composite import BaseObject


# Definitions #
# Classes #
class Component(BaseObject):
    """A basic component object.

    Attributes:
        _composite: A weak reference to the object which this object is a component of.

    Args:
        composite: The object which this object is a component of.
        init: Determines if this object will construct.
    """
    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        composite: Any = None,
        init: bool =True,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._composite: Any = None

        # Parent Attributes #
        super().__init__(*args, init=init, **kwargs)

        # Object Construction #
        if init:
            self.construct(composite=composite)

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

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, composite: Any = None, **kwargs) -> None:
        """Constructs this object.

        Args:
            composite: The object which this object is a component of.
        """
        if composite is not None:
            self.composite = composite

        super().construct(**kwargs)