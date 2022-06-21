""" basedecorator.py
An abstract class which implements the basic structure for creating decorators.
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
from ..types_ import AnyCallable, GetObjectMethod
from .basemethod import BaseMethod


# Definitions #
# Classes #
class BaseDecorator(BaseMethod):
    """An abstract class which implements the basic structure for creating decorators.
    
    Attributes:
        _call_method: The method that will be called when this object is called.
    
    Args:
        func: The function to wrap.
        get_method: The method that will be used for the __get__ method.
        call_method: The default call method to use.
        init: Determines if this object will construct.
    """
    # Magic Methods #
    # Construction/Destruction 
    def __init__(
        self,
        func: AnyCallable | None = None,
        get_method: GetObjectMethod | str | None = None,
        call_method: AnyCallable | str | None = None,
        init: bool | None = True,
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Override Attributes #
        self._call_method = self.construct_call

        # Object Construction #
        if init:
            self.construct(func=func, get_method=get_method, call_method=call_method)
            
    # Instance Methods #
    # Call Methods
    def construct_call(self, *args: Any, **kwargs: Any) -> "BaseDecorator":
        """A method for constructing this object via this object being called.

        Args:
            *args: The arguments from the call which can construct this object.
            **kwargs: The keyword arguments from the call which can construct this object.

        Returns:
            This object.
        """
        if args:
            self.construct(func=args[0])
        else:
            self.construct(**kwargs)
        return self
