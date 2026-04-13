"""dynamiccallable.py
Abstract classes for creating callable classes that has multiplexed callback.

This module contains the abstract classes for creating callable classes that has multiplexed callback.
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
from ..bases import BaseCallable, BaseFunction, BaseMethod
from ..typing import AnyCallable
from .callablemultiplexer import MethodMultiplexer


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
    _cast_excluded: set[str] = BaseCallable._cast_excluded | {"bind_multiplexer", "call_multiplexer"}

    default_bind_method: str = "bind_builtin"
    bind_multiplexer: MethodMultiplexer

    default_call_method: str = "call_wrapped"
    call_multiplexer: MethodMultiplexer

    # Pickling
    def __getstate__(self) -> dict[str, Any] | tuple[dict[str, Any] | None, dict[str, Any]] | None:
        """Gets the state of this object for pickling.

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
        state = super().__getstate__()
        if state is None:
            d_state: dict[str, Any] = {}
            slots: dict[str, Any] | None = None
        elif isinstance(state, tuple):
            d_state = {} if state[0] is None else state[0].copy()
            slots = state[1]
        else:
            d_state = state.copy()
            slots = None

        # Store the selected methods and drop the multiplexer instances
        if (multiplexer := d_state.pop("bind_multiplexer", None)) is not None:
            d_state["_bind_method"] = multiplexer.selected
        if (multiplexer := d_state.pop("call_multiplexer", None)) is not None:
            d_state["_call_method"] = multiplexer.selected

        # Returns in the same structural shape as BaseReducible returns
        if slots is None:
            return d_state
        return (d_state, slots)

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
        """
        # Extract our saved config first
        match state:
            case dict():
                saved_bind = state.pop("_bind_method", None)
                saved_call = state.pop("_call_method", None)
            case tuple():
                if state[0] is not None:
                    saved_bind = state[0].pop("_bind_method", None)
                    saved_call = state[0].pop("_call_method", None)
                else:
                    saved_bind = None
                    saved_call = None
            case _:
                saved_bind = None
                saved_call = None

        # Restore base state
        super().__setstate__(state)

        # Recreate multiplexers
        self.bind_multiplexer = MethodMultiplexer(instance=self, select=self.default_bind_method, is_binding=False)
        self.call_multiplexer = MethodMultiplexer(instance=self, select=self.default_call_method, is_binding=False)
        if saved_bind is not None:
            self.bind_multiplexer.select(saved_bind)
            self.default_bind_method = saved_bind
        if saved_call is not None:
            self.call_multiplexer.select(saved_call)
            self.default_call_method = saved_call

    # Properties #
    @property
    def bind_method(self) -> str | None:
        """The name of the method used when binding this object."""
        return self.bind_multiplexer.selected  # type: ignore[no-any-return]

    @bind_method.setter
    def bind_method(self, value: str) -> None:
        self.bind_multiplexer.select(value)
        self.default_bind_method = value

    @property
    def call_method(self) -> str | None:
        """The name of the method used when this object is called."""
        return self.call_multiplexer.selected  # type: ignore[no-any-return]

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
        """Initializes this object with the given arguments.

        Args:
            func: Optional callable to wrap.
            *args: Additional positional arguments forwarded to BaseCallable.
            bind_method: Name of the bind method to select initially.
            call_method: Name of the call method to select initially.
            init: When True, construct the instance immediately.
            **kwargs: Additional keyword arguments forwarded to BaseCallable.
        """
        # Parent Initialization #
        super().__init__(*args, func=func, init=False, **kwargs)  # type: ignore[misc]

        # Attributes #
        self.bind_multiplexer = MethodMultiplexer(instance=self, select=self.default_bind_method, is_binding=False)
        self.call_multiplexer = MethodMultiplexer(instance=self, select=self.default_call_method, is_binding=False)

        # Object Construction #
        if init:
            self.construct(  # type: ignore[misc]
                *args,
                func=func,
                bind_method=bind_method,
                call_method=call_method,
                **kwargs,
            )

    # Descriptor
    def __get__(self, instance: Any = None, owner: type[Any] | None = None) -> Any:
        """This call delegates callback to a CallableMultiplexer.

        Args:
            instance: The object to bind the method to.
            owner: The class of the object to bind the method to.

        Returns:
            The bound method or itself.
        """
        return self.bind_multiplexer(instance, owner)

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
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            *args: Arguments for inheritance.
            bind_method: The name of the bind method to use initially.
            call_method: The name of the call method to use initially.
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

    # Magic Methods #
    # Calling
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """This call delegates callback to a MethodMultiplexer.

        Args:
            *args: Positional arguments of the wrapped function.
            **kwargs: Keyword arguments of the wrapped function.

        Returns:
            The output of the wrapped function.
        """
        if (reference := self._self_) is not None and (instance := reference()) is not None:
            return self.call_multiplexer(instance, *args, **kwargs)

        return self.call_multiplexer(*args, **kwargs)


class DynamicFunction(BaseFunction, DynamicCallable):
    """An abstract function class that has multiplexed bind and callback."""

    # Attributes #
    default_bind_method: str = "bind_builtin"
    default_call_method: str = "call_wrapped"
    bind_method_type: type[BaseMethod] = DynamicMethod
