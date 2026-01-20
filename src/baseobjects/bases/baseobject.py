"""baseobject.py
BaseObject is an abstract class that implements fundamental functions that all objects should have.

This module provides the BaseObject class, which is an abstract base class that implements fundamental functionality
that should be available in all objects, such as copying and deep copying. It serves as a foundation for other classes
in the baseobjects package and provides a consistent interface for object manipulation.

The BaseObject class is designed to be a head class for object hierarchies, providing common functionality that ensures
consistent behavior across all derived classes.
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
from abc import ABC
from copy import copy, deepcopy
from typing import Any


# Definitions #
# Classes #
class BaseObject(ABC):
    """An abstract class that implements fundamental functions that all objects should have.

    BaseObject serves as a foundation class for creating well-behaved Python objects. It provides implementations for
    essential object operations such as copying and deep copying. These implementations follow Python's standard
    protocols and handle edge cases appropriately.

    This class is designed to be subclassed rather than instantiated directly.
    """

    # Magic Methods #
    # Construction/Destruction #
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initializes a new BaseObject instance.

        This is a minimal initialization method that accepts arbitrary positional and keyword arguments but does not
        perform any operations with them. This allows derived classes to have flexible initialization signatures without
        needing to explicitly handle parent class arguments.

        In most cases, derived classes should call super().__init__(*args, **kwargs) to ensure proper initialization of
        the inheritance chain, even though this base implementation is empty.

        Args:
            *args: Positional arguments, not used in this implementation but a placeholder for future expansion.
            **kwargs: Keyword arguments, not used in this implementation but a placeholder for future expansion.
        """

    # Instance Methods #
    # Constructors/Destructors
    def construct(self, *args: Any, **kwargs: Any) -> None:
        """Constructs this object with the given arguments.

        This method is intended to be called during object initialization to set up the object's state. Unlike __init__,
        which is automatically called during object creation, construct must be explicitly called. This pattern allows
        for more flexible initialization strategies, such as deferred initialization or re-initialization of existing
        objects.

        In the BaseObject implementation, this method is empty and serves as a placeholder for derived classes to
        override. Derived classes should call ``super().construct(*args, **kwargs)`` to ensure proper initialization
        of the inheritance chain.

        Args:
            *args: Positional arguments, not used in this implementation but a placeholder for future expansion.
            **kwargs: Keyword arguments, not used in this implementation but a placeholder for future expansion.
        """

    def copy(self) -> Any:
        """Creates a shallow copy of this object.

        This is a convenience method that delegates to the copy.copy function, making it easier to create shallow
        copies without having to import the copy module.

        Returns:
            A shallow copy of this object, with the same type but independent top-level state.
        """
        return copy(self)

    def deepcopy(self, memo: dict[Any, Any] | None = None) -> Any:
        """Creates a deep copy of this object.

        This is a convenience method that delegates to the copy.deepcopy function, making it easier to create deep
        copies without having to import the copy module.

        Args:
            memo: A dictionary that maps object IDs to their copies, used to handle circular references.
                If None, a new dictionary is created.

        Returns:
            A deep copy of this object, with the same type but completely independent state,
            including independent copies of all mutable objects contained within.
        """
        return deepcopy(self, memo)
