"""sentinelobject.py
A module providing a sentinel object implementation.

This module provides the SentinelObject class, which is used to create unique sentinel values that can be used for
special cases in function arguments, return values, or as markers in data structures. Sentinel objects are singleton
instances that maintain their identity across the program's execution, making them ideal for representing special values
or states.

The SentinelObject class implements a registry pattern to ensure that only one instance exists for each unique
identifier. This means that two SentinelObject instances created with the same identifier will be the same object,
allowing for identity comparisons (using the `is` operator) rather than equality comparisons.
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
from typing import Any, ClassVar

# Local Packages #
from .basereducible import BaseReducible


# Definitions #
# Classes #
class SentinelObject(BaseReducible):
    """A singleton sentinel object for representing special values or states.

    SentinelObject implements the singleton pattern through a registry mechanism, ensuring that only one instance exists
    for each unique identifier. This makes sentinel objects ideal for representing special values or states in a
    program, as they can be compared using identity comparison (the `is` operator) rather than equality.

    The class inherits from BaseReducible, which provides proper pickling and unpickling support, ensuring that sentinel
    objects maintain their identity even when serialized and deserialized.

    Class Attributes:
        sentinel_registry: A class-level dictionary that maps identifiers to their corresponding sentinel objects.

    Attributes:
        identity: A unique identifier for the sentinel object. Can be a string, bytes, or integer.
    """

    # Class Attributes #
    __slots__ = ("identity",)
    sentinel_registry: ClassVar[dict[str | bytes | int, SentinelObject]] = {}

    # Attributes #
    identity: str | bytes | int

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, id_: str | bytes | int) -> SentinelObject:
        """Creates a new sentinel object or return an existing one with the same ID.

        This method implements the singleton pattern by checking if a sentinel object with the given ID already exists
        in the registry. If it does, that object is returned; otherwise, a new object is created, added to the registry,
        and returned.

        Args:
            id_: A unique identifier for the sentinel object. Can be a string, bytes, or integer.
                String and bytes identifiers are treated as distinct even if they have the same content.

        Returns:
            A sentinel object with the given ID, either newly created or retrieved from the registry.
        """
        if (sentinel := cls.sentinel_registry.get(id_, None)) is None:
            cls.sentinel_registry[id_] = sentinel = super().__new__(cls)
        return sentinel

    def __init__(self, id_: str | bytes | int) -> None:
        """Initializes the sentinel object with the given ID.

        Args:
            id_: A unique identifier for the sentinel object.
        """
        super().__init__()
        self.identity = id_

    def copy(self) -> Any:
        """Returns this object rather than creating a copy, preserving the singleton pattern.

        This method overrides the copy method from BaseObject to ensure that sentinel objects maintain their singleton
        nature when copied. Instead of creating a new object, it simply returns the original object.

        Returns:
            The original sentinel object (self).
        """
        return self

    def deepcopy(self, memo: Any | None = None) -> Any:
        """Returns this object rather than creating a deep copy, preserving the singleton pattern.

        This method overrides the deepcopy method from BaseObject to ensure that sentinel objects maintain their
        singleton nature when deep copied. Instead of creating a new object, it simply returns the original object,
        ignoring the memo dictionary.

        Args:
            memo: A dictionary mapping object IDs to their copies, used by the deepcopy algorithm.
                Ignored in this implementation.

        Returns:
            The original sentinel object (self).
        """
        return self

    # Reduction/Pickling
    def __reduce__(self) -> tuple[Any, tuple[Any]]:
        """Reduce the sentinel object for pickling.

        This method is called by the pickle module when serializing the object. It returns a tuple containing the class
        and the arguments needed to recreate the object. When unpickled, the __new__ method will be called with the
        identity, which will either retrieve the existing sentinel object from the registry or create a new one if it
        doesn't exist.

        Returns:
            A tuple containing the class and a tuple of arguments (identity) needed to recreate the object.
        """
        return self.__class__, (self.identity,)


# Constants #
DEFAULTSENTINEL = SentinelObject("DEFAULTSENTINEL")
SEARCHSENTINEL = SentinelObject("SEARCHSENTINEL")
