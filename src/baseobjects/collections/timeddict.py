"""timeddict.py
A dictionary that clears its contents after a specified time has passed.
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
from collections.abc import Hashable
from contextlib import contextmanager
from time import perf_counter
from typing import Any

# Local Packages #
from ..bases import BaseDict


# Definitions #
# Classes #
class TimedDict(BaseDict):
    """A dictionary that clears its contents after a time has elapsed.

    Attributes:
        is_timed: Determines if the dictionary will be reset periodically.
        _lifetime: The period between dictionary resets in seconds.
        expiration: The next time the dictionary will be rest.

    Args:
        dict_: The dictionary to copy into this dictionary.
        **kwargs: The keywords to add to this dictionary.
    """

    # Attributes #
    is_timed: bool = True
    _lifetime: int | float | None = None
    expiration: int | float | None = None

    _data: dict[Hashable, Any]

    # Properties #
    @property
    def lifetime(self) -> int | float | None:
        """The period between dictionary resets in seconds."""
        return self._lifetime

    @lifetime.setter
    def lifetime(self, value: int | float | None) -> None:
        self._lifetime = value
        self.reset_expiration()

    @property
    def data(self) -> dict[Hashable, Any]:
        """The data of the dictionary."""
        self.verify()
        return self._data

    # Magic Methods #
    # Construction/Destruction
    def __init__(self, dict_: dict[Hashable, Any] | None = None, /, **kwargs: Any) -> None:
        # Attributes #
        self._data: dict[Hashable, Any] = {}

        # Object Construction #
        if dict_ is not None:
            self.update(dict_)
        if kwargs:
            self.update(kwargs)

    # Instance Methods #
    # Mapping
    def clear(self) -> None:
        """Clears the contents of the dictionary and resets the expiration."""
        self._data.clear()
        self.reset_expiration()

    # Time Verification
    def reset_expiration(self) -> None:
        """Updates the expiration to a new future time."""
        if self.lifetime is not None:
            self.expiration = perf_counter() + self.lifetime

    @contextmanager
    def pause_timer(self) -> None:
        """A context manager that will stop clearing the dictionary until it is returned."""
        left_over = 0.0
        if self.expiration is not None:
            left_over = self.expiration - perf_counter()
            self.expiration = None
        self.is_timed = False
        yield None
        self.expiration = perf_counter() + left_over
        self.is_timed = True

    @contextmanager
    def pause_reset_timer(self) -> None:
        """A context manager that will stop clearing the dictionary until it is returned, resting the expiration."""
        self.is_timed = False
        yield None
        self.is_timed = True
        self.reset_expiration()

    def clear_condition(self, *args: Any, **kwargs: Any) -> bool:
        """The condition used to determine if the dictionary should be cleared.

        Args:
            *args: Arguments that could be used to determine if the dictionary should be cleared.
            **kwargs: Keyword arguments that could be used to determine if the dictionary should be cleared.

        Returns:
            bool: Determines if the cache should be cleared.
        """
        return self.is_timed and self._lifetime is not None and perf_counter() >= self.expiration

    def verify(self) -> None:
        """Verifies if the dictionary should be cleared and then clears it."""
        if self.clear_condition():
            self.clear()
