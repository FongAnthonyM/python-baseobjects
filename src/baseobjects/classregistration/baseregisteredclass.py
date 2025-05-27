"""An abstract class which registers subclasses, allowing subclass dispatching.

This module provides the BaseRegisteredClass, which is an abstract base class for classes that
register their subclasses in a registry, enabling subclass dispatching based on various criteria.
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
from typing import ClassVar, Any, Optional

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject
from .baseclassregistry import BaseClassRegistry


# Definitions #
# Classes #
class BaseRegisteredClass(BaseObject):
    """An abstract class which registers subclasses, allowing subclass dispatching.

    Attributes:
        class_registry: A registry of all subclasses of this class.
        class_registry_type: The type of registry to use for storing subclasses.
        class_registration: Determines if this class/subclass will be added to the registry.
    """

    # Class Attributes #
    class_registry_type: ClassVar[type[BaseClassRegistry]]
    class_registry: ClassVar[BaseClassRegistry | None] = None
    class_registration: ClassVar[bool] = False

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            **kwargs: Keyword arguments for creating a subclass.
        """
        super().__init_subclass__(**kwargs)

        # Add subclass to the registry.
        if cls.class_registration:
            if cls.class_registry is None:
                cls.create_class_registry()
            elif not cls.class_registry:
                cls.class_registry.head_class = cls

            cls.register_class()

    # Register
    @classmethod
    def create_class_registry(cls) -> None:
        """Creates a class registry for this class."""
        cls.class_registry = cls.class_registry_type(head_class=cls)

    @classmethod
    def register_class(cls, *args: Any, **kwargs: Any) -> None:
        """Registers this class with the given namespace and name.

        Args:
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError

    @classmethod
    def get_registered_class(cls, *args: Any, **kwargs: Any) -> Optional["BaseRegisteredClass"]:
        """Gets a subclass from the registry.

        Args:
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.

        Returns:
            The requested subclass, or None if not found.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError
