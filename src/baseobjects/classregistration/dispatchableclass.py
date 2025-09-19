"""dispatchableclass.py
An abstract class which registers subclasses and dispatches itself to subclasses when __new__ is called.

This module provides the DispatchableClass class, which extends BaseRegisteredClass to add automatic dispatching
functionality. When instantiated, it can automatically select and instantiate the appropriate subclass based on the
provided arguments. This enables factory-like behavior where the correct implementation is chosen at runtime based
on input parameters, without requiring explicit conditional logic.
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

# Third-Party Packages #

# Local Packages #
from .baseregisteredclass import BaseRegisteredClass


# Definitions #
# Classes #
class DispatchableClass(BaseRegisteredClass):
    """An abstract class which registers subclasses and dispatches itself to subclasses when __new__ is called.

    DispatchableClass extends BaseRegisteredClass to add automatic dispatching functionality. When instantiated, it can
    dispatch itself to the correct subclass based on the provided arguments. This enables factory-like behavior where
    the correct implementation is chosen at runtime based on input parameters, without requiring explicit conditional
    logic. However, DispatchableClass does not implement class registration and dispatching, so it must be implemented
    in a subclass.
    """

    # Class Methods #
    @classmethod
    def get_class_information(cls, *args: Any, **kwargs: Any) -> Any:
        """Gets a class's lookup information from a given set of arguments.

        Args:
            *args: Positional arguments to get the namespace and name from.
            **kwargs: Keyword arguments to get the namespace and name from.

        Returns:
            The class lookup information.
        """
        raise NotImplementedError("This method needs to be implemented to dispatch classes.")

    # Magic Methods #
    # Construction/Destruction
    def __new__(cls, *args: Any, **kwargs: Any) -> BaseRegisteredClass:
        """With the given input, will return the correct subclass."""
        if cls is cls.class_registry.head_class and (kwargs or args):
            class_ = cls.get_registered_class(*cls.get_class_information(*args, **kwargs))
            if class_ is not None and class_ is not cls.class_registry.head_class:
                return class_(*args, **kwargs)
        return super().__new__(cls)
