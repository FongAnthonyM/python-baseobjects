"""baseclassregistry.py

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
from abc import abstractmethod
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseDict


# Definitions #
# Classes #
class BaseClassRegistry(BaseDict):
    """A registry for classes.

    Attributes:
        head_class: The head class of the registry.

    Args:
        head_class: The head class of the registry.
        init: Determines if this object will construct.
    """

    # Attributes #
    head_class: type | None = None

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        head_class: type | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any
    ) -> None:
        # Parent Initialization #
        super().__init__()

        # Object Construction #
        if init:
            self.construct(head_class=head_class, **kwargs)

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        head_class: type | None = None,
        **kwargs: Any
    ) -> None:
        """Constructs this object.

        Args:
            head_class: The head class of the registry.
            **kwargs: Keyword arguments for inheritance.
        """
        if head_class is not None:
            self.head_class = head_class

        super().construct(**kwargs)

    # Registry
    @abstractmethod
    def register_class(
        self,
        cls: type,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Registers a class with the given namespace and name.

        Args:
            cls: The class to register.
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.
        """

    @abstractmethod
    def get_class(self, *args, **kwargs) -> Any:
        """Gets a class from the registry.

        Args:
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.

        Returns:
            The requested class.
        """
