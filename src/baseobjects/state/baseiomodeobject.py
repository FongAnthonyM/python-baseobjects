"""baseiomodeobject.py
A base class for objects that have an I/O mode and decorators for managing state-dependent methods.

This module provides the BaseIOModeObject class, which is an abstract base class for objects that need to track an I/O
mode and whether they are open or closed. It also includes decorator classes, like staterestriction, that can be used
to manage and restrict access to methods of BaseIOModeObject instances based on their current state.
"""

# Header #
__package_name__ = "baseobjects"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2026, Anthony Fong"
__license__ = "MIT"

__version__ = "1.12.0"


# Imports #
# Standard Libraries #
from abc import abstractmethod
from collections.abc import AsyncIterator, Iterable, Iterator
from contextlib import asynccontextmanager, contextmanager
from enum import StrEnum
from io import UnsupportedOperation
from typing import Any, Self

# Local Packages #
from ..bases import BaseObject, SentinelObject
from ..functions import BaseDecorator
from ..typing import AnyCallable, CallMethod


# Definitions #
# Classes #
class BaseIOModeObject(BaseObject):
    """A base class for objects that have an I/O mode.

    This class provides the fundamental structure for objects that can be opened and closed, and that have a specific
    I/O mode. It includes properties for checking the open state and current mode, as well as abstract methods for
    opening and closing the object.

    Attributes:
        _valid_modes: The valid modes for this object.
        _mode_registry: A registry of valid modes groups for this object.
        _is_open: Determines if the object is open.
        _mode: The current I/O mode of the object.
    """

    # Attributes #
    _valid_modes: type[StrEnum]
    _mode_registry: dict[str, set[str | StrEnum]] = {}

    _is_open: bool = False
    _mode: StrEnum

    # Properties #
    @property
    def valid_modes(self) -> type[StrEnum]:
        """The valid modes for this object."""
        return self._valid_modes

    @property
    def is_open(self) -> bool:
        """The open state of the I/O mode object."""
        return self._is_open

    @property
    def mode(self) -> StrEnum:
        """The I/O mode of the object."""
        return self._mode

    @mode.setter
    def mode(self, value: StrEnum | str) -> None:
        """Sets the I/O mode of the object.

        Args:
            value: The I/O mode to set.
        """
        self._mode = self.valid_modes(value)

    # Magic Methods #
    # Representation #
    def __repr__(self) -> str:
        """The representation of the object.

        Returns:
            The representation of the object.
        """
        mode = getattr(self, "_mode", None)
        return f"<{self.__class__.__name__}(is_open={self.is_open}, mode={mode!r})>"

    # Context Manager #
    def __enter__(self) -> Self:
        """Opens the I/O mode object when entering the context.

        Returns:
            This object.
        """
        return self if self.is_open else self.open()

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Closes the I/O mode object when exiting the context.

        Args:
            exc_type: The type of exception raised in the context, if any.
            exc_value: The exception instance raised in the context, if any.
            traceback: The traceback for the exception raised in the context, if any.
        """
        self.close()

    async def __aenter__(self) -> Self:
        """Asynchronously opens the I/O mode object when entering the context.

        Returns:
            This object.
        """
        return self if self.is_open else await self.open_async()

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Asynchronously closes the I/O mode object when exiting the context.

        Args:
            exc_type: The type of exception raised in the context, if any.
            exc_value: The exception instance raised in the context, if any.
            traceback: The traceback for the exception raised in the context, if any.
        """
        return await self.close_async()

    # Instance Methods #
    # Validation #
    def validate_mode(self, mode: str | StrEnum) -> bool:
        """Checks if a mode is valid for this object.

        Args:
            mode: The mode to check.

        Returns:
            True if the mode is valid, False otherwise.
        """
        try:
            self.valid_modes(mode)
        except (ValueError, AttributeError):
            return False
        return True

    def require_open(self) -> None:
        """Ensures that the object is open.

        Raises:
            ValueError: If the object is closed.
        """
        if not self.is_open:
            msg = f"Operation on a closed {self.__class__.__name__} is not allowed."
            raise ValueError(msg)

    def require_closed(self) -> None:
        """Ensures that the object is closed.

        Raises:
            ValueError: If the object is open.
        """
        if self.is_open:
            msg = f"Operation on an open {self.__class__.__name__} is not allowed."
            raise ValueError(msg)

    def require_mode(
        self,
        modes: str | StrEnum | Iterable[str | StrEnum] | None = None,
        mode_group: str | None = None,
    ) -> None:
        """Ensures that the object is in one of the given modes.

        Args:
            modes: The valid modes.
            mode_group: The mode group to check for valid modes.

        Raises:
            KeyError: If the mode group is not valid.
            UnsupportedOperation: If the object's mode is not in the given modes.
        """
        not_modes = True
        if modes is None:
            not_modes = False
        elif isinstance(modes, str | StrEnum) and self._mode == modes:
            not_modes = False
        elif isinstance(modes, set):
            not_modes = self._mode not in modes
        else:
            not_modes = self._mode not in set(modes)

        not_group = True
        if mode_group is None:
            not_group = False
        else:
            group = self._mode_registry.get(mode_group, None)
            if group is None:
                msg = f"Mode group {mode_group} is not valid for this object. Registry: {self._mode_registry}"
                raise KeyError(msg)
            not_group = self._mode not in group

        if not_modes or not_group:
            msg = f"Mode {self._mode} is not valid for this operation."
            raise UnsupportedOperation(msg)

    # State Management #
    @abstractmethod
    def open(self, *args: Any, **kwargs: Any) -> Self:
        """Opens the I/O mode object.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Returns:
            This object.
        """
        self._is_open = True
        return self

    async def open_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously opens the I/O mode object."""
        msg = "Async open is not implemented for this object."
        raise NotImplementedError(msg)

    @abstractmethod
    def close(self, *args: Any, **kwargs: Any) -> None:
        """Closes the I/O mode object.

        Args:
            *args: Positional arguments for closing the object.
            **kwargs: Keyword arguments for closing the object.
        """
        self._is_open = False

    async def close_async(self, *args: Any, **kwargs: Any) -> None:
        """Asynchronously closes the I/O mode object."""
        msg = "Async close is not implemented for this object."
        raise NotImplementedError(msg)

    def ensure_open(self, *args: Any, **kwargs: Any) -> Self:
        """Opens the object if it is not already open.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Returns:
            This object.
        """
        return self if self.is_open else self.open(*args, **kwargs)

    async def ensure_open_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously opens the object if it is not already open.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Returns:
            This object.
        """
        return self if self.is_open else await self.open_async(*args, **kwargs)

    def reopen(self, *args: Any, **kwargs: Any) -> Self:
        """Closes and then opens the object.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Returns:
            This object.
        """
        self.close()
        return self.open(*args, **kwargs)

    async def reopen_async(self, *args: Any, **kwargs: Any) -> Self:
        """Asynchronously closes and then opens the object.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Returns:
            This object.
        """
        await self.close_async()
        return await self.open_async(*args, **kwargs)

    @contextmanager
    def as_open(self, *args: Any, **kwargs: Any) -> Iterator[Self]:
        """A context manager that ensures the object is open.

        If the object is not already open, it will be opened on entering the context and closed on exiting.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Yields:
            This object.
        """
        was_open = self.is_open
        if not was_open:
            self.open(*args, **kwargs)
        try:
            yield self
        finally:
            if not was_open:
                self.close()

    @asynccontextmanager
    async def as_open_async(self, *args: Any, **kwargs: Any) -> AsyncIterator[Self]:
        """An asynchronous context manager that ensures the object is open.

        If the object is not already open, it will be asynchronously opened on entering the context and
        asynchronously closed on exiting.

        Args:
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.

        Yields:
            This object.
        """
        was_open = self.is_open
        if not was_open:
            await self.open_async(*args, **kwargs)
        try:
            yield self
        finally:
            if not was_open:
                await self.close_async()


class staterestriction(BaseDecorator):  # noqa: N801
    """A decorator that restricts access to methods based on the object's open state and mode.

    This decorator wraps methods of BaseIOModeObject instances and ensures that they are only called when the object is
    in the correct state (open or closed) and has a valid I/O mode.

    Attributes:
        OPEN_STATE_SENTINEL: A sentinel value for the open state.
        open_state: The open state the I/O mode object must be in to be called.
        all_modes: Determines if all modes are valid.
        valid_modes: The valid modes the I/O mode object must be in to be called.
    """

    # Attributes #
    OPEN_STATE_SENTINEL: SentinelObject = SentinelObject("OPEN_STATE_SENTINEL")
    open_state: bool | None = None
    all_modes: bool = True
    valid_modes: set[StrEnum | str] | None = None
    mode_group: str | None = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: Any | None = None,
        open_state: bool | SentinelObject | None = OPEN_STATE_SENTINEL,
        valid_modes: bool | str | StrEnum | Iterable[str | StrEnum] | None = None,
        mode_group: str | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes a new staterestriction instance.

        Args:
            func: The function to wrap.
            open_state: The open state the I/O mode object must be in to be called.
            valid_modes: The valid modes the I/O mode object must be in to be called.
            mode_group: The mode group to check for valid modes.
            *args: Arguments for inheritance.
            init: Determines if the object should be constructed.
            **kwargs: Keyword arguments for inheritance.
        """
        # Super Initialization #
        super().__init__(init=False)

        # Construction #
        if init:
            self.construct(func, open_state, valid_modes, mode_group, *args, **kwargs)

    # Calling #
    def call_state_restriction(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function if the object's state and mode are valid.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function call.
        """
        if args:
            obj = args[0]
            if self.open_state is True:
                obj.require_open()
            elif self.open_state is False:
                obj.require_closed()

            if not self.all_modes:
                obj.require_mode(self.valid_modes, self.mode_group)

        return self.call_binding(*args, **kwargs)

    # Descriptor #
    def __set__(self, instance: Any, value: Any) -> None:
        """Sets the value of the attribute on the instance.

        Args:
            instance: The instance to set the value on.
            value: The value to set.
        """
        if self.__wrapped__ is not None:
            instance.__dict__[self.__wrapped__.__name__] = value

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        open_state: bool | SentinelObject | None = OPEN_STATE_SENTINEL,
        valid_modes: bool | str | StrEnum | Iterable[str] | Iterable[StrEnum] | None = None,
        mode_group: str | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap. If provided, this will be set as the wrapped function.
            open_state: The open state the I/O mode object must be in to be called.
            valid_modes: The valid modes the I/O mode object must be in to be called.
            mode_group: The mode group to check for valid modes.
            *args: Arguments for inheritance.
            **kwargs: Keyword arguments for inheritance.
        """
        # Super Construction #
        super().construct(func, *args, **kwargs)

        # Construction #
        if not isinstance(open_state, SentinelObject):
            self.open_state = open_state

        if valid_modes is not None:
            if isinstance(valid_modes, bool):
                self.all_modes = valid_modes
            else:
                self.all_modes = False
                if isinstance(valid_modes, str):
                    self.valid_modes = {valid_modes}
                else:
                    self.valid_modes = set(valid_modes)

        if mode_group is not None:
            self.mode_group = mode_group
            self.all_modes = False




class asopen(BaseDecorator):  # noqa: N801
    """A decorator that ensures the object is open for the duration of the wrapped function call.

    This decorator wraps methods of BaseIOModeObject instances and ensures that they are called within an
    asopen context, opening the object if it's closed and closing it after the call if it was opened.

    Attributes:
        args: Positional arguments for opening the object.
        kwargs: Keyword arguments for opening the object.
    """

    # Attributes #
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes a new asopen instance.

        Args:
            func: The function to wrap.
            *args: Positional arguments for opening the object.
            init: Determines if the object should be constructed.
            **kwargs: Keyword arguments for opening the object.
        """
        # Super Initialization #
        super().__init__(init=False)

        # Construction #
        if init:
            self.construct(func, *args, **kwargs)

    # Calling #
    def call_wrapped(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function within an asopen context.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function call.
        """
        if args:
            with args[0].as_open(*self.args, **self.kwargs):
                return super().call_wrapped(*args, **kwargs)
        else:
            return super().call_wrapped(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.
        """
        # Super Construction #
        super().construct(func)

        # Construction #
        self.args = args
        self.kwargs = kwargs


class asopenasync(BaseDecorator):  # noqa: N801
    """A decorator that asynchronously ensures the object is open for the duration of the wrapped function call.

    This decorator wraps asynchronous methods of BaseIOModeObject instances and ensures that they are called within an
    asopenasync context, asynchronously opening the object if it's closed and asynchronously closing it after the call
    if it was opened.

    Attributes:
        args: Positional arguments for opening the object.
        kwargs: Keyword arguments for opening the object.
    """

    # Attributes #
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes a new asopenasync instance.

        Args:
            func: The function to wrap.
            *args: Positional arguments for opening the object.
            init: Determines if the object should be constructed.
            **kwargs: Keyword arguments for opening the object.
        """
        # Super Initialization #
        super().__init__(init=False)

        # Construction #
        if init:
            self.construct(func, *args, **kwargs)

    # Calling #
    def call_wrapped(self, *args: Any, **kwargs: Any) -> Any:
        """Calls the wrapped function within an asopenasync context.

        Args:
            *args: Positional arguments for the wrapped function.
            **kwargs: Keyword arguments for the wrapped function.

        Returns:
            The result of the wrapped function call.
        """
        if args:
            parent_call = super().call_wrapped

            async def wrap() -> Any:
                async with args[0].as_open_async(*self.args, **self.kwargs):
                    return await parent_call(*args, **kwargs)

            return wrap()
        else:
            return super().call_wrapped(*args, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        func: AnyCallable | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            func: The function to wrap.
            *args: Positional arguments for opening the object.
            **kwargs: Keyword arguments for opening the object.
        """
        # Super Construction #
        super().construct(func)

        # Construction #
        self.args = args
        self.kwargs = kwargs
