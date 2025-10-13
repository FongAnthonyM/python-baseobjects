"""baseregisteredclass.py
An abstract class which registers subclasses.

This module provides the BaseRegisteredClass, which is an abstract base which class outlines the interface for
registering subclasses and retrieving them from a registry. BaseRegisteredClass does not implement any registration
mechanics or contain registered classes but provides the interface for developers to implement their own registration
and storage mechanisms.
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
from typing import Any, ClassVar, Optional

# Local Packages #
from ..bases import BaseObject
from .baseclassregistry import BaseClassRegistry


# Definitions #
# Classes #
class BaseRegisteredClass(BaseObject):
    """A base class which outlines registering subclasses.

    BaseRegisteredClass outlines the interface for registering subclasses and retrieving them from a registry. The
    premise is, a subclass of BaseRegisteredClass will act as the head class for the registration hierarchy which tracks
    its subclasses through class registration.

    A head class does not need to directly inherit from BaseRegisteredClass, but by setting the "class_registration"
    boolean it will start registering classes and that subclass will become a head class of a hierarchy.
    Generally, "class_registration" determines if a subclass will be registered, and the first class to set it to True
    becomes the head class of a new hierarchy. The head class creates a registry to store the registered class of the
    new hierarchy. Any subclasses of the head class with "class_registration" set to True are registered in the root
    class's registry. (Note: Setting "class_registration" acts as a toggle for registering subclasses, so after setting
    it to True, any subsequent subclasses have "class_registration" set to True until they are set back to False.)

    To give developers more control over the registration process, the exact registry type, registration, and retrieval
    are not specified here. Therefore, at some point, the registration mechanics must be implemented, either before a
    hierarchy head class or within the head class itself.

    Attributes:
        class_registry_type: The type of registry to use for storing subclasses.
        class_registry: A registry of the subclasses.
        class_registration: Determines if this class/subclass will be added to the registry.
    """

    # Class Attributes #
    class_registry_type: ClassVar[type[BaseClassRegistry]]
    class_registry: ClassVar[BaseClassRegistry | None] = None
    class_registration: ClassVar[bool] = False

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, register_kwargs: dict[str, Any] | None = None, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            register_kwargs: Keyword arguments for registering the subclass.
            **kwargs: Keyword arguments for creating a subclass.
        """
        super().__init_subclass__(**kwargs)

        # Add subclass to the registry.
        if cls.class_registration:
            if cls.class_registry is None:
                cls.create_class_registry()
            elif not cls.class_registry:
                cls.class_registry.head_class = cls

            cls.register_class(**(register_kwargs or {}))

    # Register
    @classmethod
    def create_class_registry(cls) -> None:
        """Creates a class registry for this class."""
        cls.class_registry = cls.class_registry_type(head_class=cls)

    @classmethod
    @abstractmethod
    def register_class(cls, *args: Any, **kwargs: Any) -> None:
        """Registers this class.

        Args:
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.
        """

    @classmethod
    @abstractmethod
    def get_registered_class(cls, *args: Any, **kwargs: Any) -> Optional["BaseRegisteredClass"]:
        """Gets a subclass from the registry.

        Args:
            *args: Positional arguments to implement.
            **kwargs: Keyword arguments to implement.

        Returns:
            The requested subclass, or None if not found.
        """
