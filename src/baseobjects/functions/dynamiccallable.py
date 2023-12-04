"""dynamiccallable.py
Abstract classes for creating callable classes that has multiplexed callback.
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
from ..typing import AnyCallable
from ..bases import BaseCallable, BaseFunction, BaseMethod
from .callablemultiplexer import CallableMultiplexer, MethodMultiplexer


# Definitions #
# Classes #
class DynamicCallable(BaseCallable):
    """An abstract callable class that has multiplexed callback.

    Attributes:
        _call_method: The name of the method used when this object is called.
        call_multiplexer: The multiplexer which control the call method being use.

    Args:
        func: The function to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    default_call_method: str | None = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._call_method: str = self.default_call_method
        self.call_multiplexer: MethodMultiplexer = MethodMultiplexer(instance=self, select=self.call_method)

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, *args, **kwargs)

    @property
    def call_method(self) -> str | None:
        """The name of the method used when this object is called."""
        return self._call_method

    @call_method.setter
    def call_method(self, value: str) -> None:
        self.call_multiplexer.select(value)
        self._call_method = value

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object

        Returns:
            A dictionary of this object's attributes.
        """
        state = self.__dict__.copy()
        state["call_multiplexer"] = (self.call_multiplexer.register, self.call_multiplexer.selected)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        self.__dict__.update(state)
        s, r = state["call_multiplexer"]
        self.call_multiplexer = MethodMultiplexer(instance=self, select=s, register=r)

    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a MethodMultiplexer.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.call_multiplexer(*args, **kwargs)

    # Instance Methods #
    # Calling
    def call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.__func__(*args, **kwargs)


class DynamicMethod(DynamicCallable, BaseMethod):
    """An abstract method class that has multiplexed callback."""

    default_call_method: str | None = "call"

    # Instance Methods #
    # Calling
    def call(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function with the instance as an argument.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self._func_.__get__(self._self_(), self.__owner__)(*args, **kwargs)


class DynamicFunction(DynamicCallable, BaseFunction):
    """An abstract function class that has multiplexed callback and binding.

    Attributes:
        _bind_method: The name of the method used when binding this object.
        bind_multiplexer: The multiplexer which control the binding method being use.

    Args:
        func: The function to wrap.
        *args: Arguments for inheritance.
        init: Determines if this object will construct.
        **kwargs: Keyword arguments for inheritance.
    """

    method_type: type[BaseMethod] = DynamicMethod
    default_bind_method: str | None = "bind"

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        # New Attributes #
        self._bind_method: str = self.default_bind_method
        self.bind_multiplexer: CallableMultiplexer = CallableMultiplexer(instance=self, select=self.bind_method)

        # Parent Attributes #
        super().__init__(*args, init=False, **kwargs)

        # Object Construction #
        if init:
            self.construct(func=func, *args, **kwargs)

    @property
    def bind_method(self) -> str | None:
        """The name of the method used when binding this object."""
        return self._bind_method

    @bind_method.setter
    def bind_method(self, value: str) -> None:
        self.bind_multiplexer.select(value)
        self._bind_method = value

    # Pickling
    def __getstate__(self) -> dict[str, Any]:
        """Creates a dictionary of attributes which can be used to rebuild this object

        Returns:
            A dictionary of this object's attributes.
        """
        state = super().__getstate__()
        state["bind_multiplexer"] = (self.bind_multiplexer.register, self.bind_multiplexer.selected)
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Builds this object based on a dictionary of corresponding attributes.

        Args:
            state: The attributes to build this object from.
        """
        super().__setstate__(state)
        s, r = state["bind_multiplexer"]
        self.bind_multiplexer = CallableMultiplexer(instance=self, select=s, register=r)

    # Descriptor
    def __get__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a CallableMultiplexer.

        Args:
            *args: The arguments of the wrapped function.
            **kwargs: The keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        return self.bind_multiplexer(*args, **kwargs)
