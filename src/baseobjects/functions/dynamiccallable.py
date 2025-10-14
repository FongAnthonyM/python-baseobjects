"""dynamiccallable.py
Abstract classes for creating callable classes that has multiplexed callback.
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
from types import FunctionType, MethodType
from typing import Any

# Local Packages #
from ..bases import BaseCallable, BaseFunction, BaseMethod
from ..typing import AnyCallable
from .callablemultiplexer import CallableMultiplexer, MethodMultiplexer


# Definitions #
# Classes #
class DynamicCallable(BaseCallable):
    """An abstract callable class that has multiplexed binding and callback.

    Attributes:
        default_bind_method: The name of the method used when binding this object.
        bind_multiplexer: The multiplexer which control the binding method being use.
        default_call_method: The name of the method used when this object is called.
        call_multiplexer: The multiplexer which control the call method being use.

    Args:
        func: The function to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    _cast_excluded: set = BaseCallable._cast_excluded | {"bind_multiplexer", "call_multiplexer"}

    default_bind_method: str = "bind_builtin"
    bind_multiplexer: MethodMultiplexer

    default_call_method: str = "call_wrapped"
    call_multiplexer: MethodMultiplexer

    # Properties #
    @property
    def bind_method(self) -> str | None:
        """The name of the method used when binding this object."""
        return self.bind_multiplexer.selected

    @bind_method.setter
    def bind_method(self, value: str) -> None:
        self.bind_multiplexer.select(value)
        self.default_bind_method = value

    @property
    def call_method(self) -> str | None:
        """The name of the method used when this object is called."""
        return self.call_multiplexer.selected

    @call_method.setter
    def call_method(self, value: str) -> None:
        self.call_multiplexer.select(value)
        self.default_call_method = value

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        bind_method: str | None = None,
        call_method: str | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize a dynamic callable with bind and call multiplexers.

        Args:
            func: Optional callable to wrap.
            *args: Additional positional arguments forwarded to BaseCallable.
            bind_method: Name of the bind method to select initially.
            call_method: Name of the call method to select initially.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseCallable.
        """
        # Attributes #
        self.bind_multiplexer = MethodMultiplexer(instance=self, select=self.default_bind_method, is_binding=False)
        self.call_multiplexer = MethodMultiplexer(instance=self, select=self.default_call_method, is_binding=False)

        # Parent Initialization #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func, *args, bind_method=bind_method, call_method=call_method, **kwargs)

    # Descriptor
    def __get__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a CallableMultiplexer.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.bind_multiplexer(*args, **kwargs)

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a MethodMultiplexer.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.call_multiplexer(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        bind_method: str | None = None,
        call_method: str | None = None,
        **kwargs: Any,
    ) -> None:
        """The constructor for this object.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        if bind_method is not None:
            self.bind_multiplexer.select(bind_method)

        if call_method is not None:
            self.call_multiplexer.select(call_method)

        super().construct(func, *args, **kwargs)


class DynamicMethod(DynamicCallable, BaseMethod):
    """An abstract method class that has multiplexed binding and callback."""

    # Attributes #
    default_bind_method: str = "bind_self"
    default_call_method: str = "call_wrapped"

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a MethodMultiplexer.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.call_multiplexer(self._self_(), *args, **kwargs)


class DynamicFunction(DynamicCallable, BaseFunction):
    """An abstract function class that has multiplexed bind and callback."""

    # Attributes #
    method_type: type[BaseMethod] = DynamicMethod
