"""registeredclass.py
An abstract class which registers subclasses, allowing subclass dispatching.
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
from typing import Any, Optional

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class RegisteredClass(BaseObject):
    """An abstract class which registers subclasses, allowing subclass dispatching.

    Class Attributes:
        head_class: The root class of the registered classes.
        namespace: The namespace of the subclass.
        name: The name of which the subclass will be registered as.
        register: A register of all subclasses of this class.
        registration: Determines if this class/subclass will be added to the register.
    """

    head_class: Optional["RegisteredClass"] = None
    namespace: str | None = None
    name: str | None = None
    register: dict[str, dict[str, type]] | None = None
    registration: bool = False

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            **kwargs: The keyword arguments for creating a subclass.
        """
        super().__init_subclass__(**kwargs)

        # Add subclass to the register.
        if cls.registration:
            if cls.register is None:
                raise NotImplementedError("The root registered class must create a register.")

            if not cls.register:
                cls.head_class = cls

            cls.register_class(namespace=cls.namespace, name=cls.name)

    # Register
    @classmethod
    def register_class(cls, namespace: str | None = None, name: str | None = None) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
        """
        namespace = cls.__module__ if namespace is None else namespace
        cls.namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace
        cls.name = cls.__name__ if name is None else name

        namespace_types = cls.register.get(cls.namespace, None)
        if namespace_types is not None:
            namespace_types[cls.name] = cls
        else:
            cls.register[cls.namespace] = {cls.name: cls}

    @classmethod
    def get_registered_class(cls, namespace: str, name: str) -> Optional["RegisteredClass"]:
        """Gets a subclass from the register.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass to get.

        Returns:
            The requested subclass.
        """
        namespace_types = cls.register.get(namespace, None)
        return None if namespace_types is None else namespace_types.get(name, None)
