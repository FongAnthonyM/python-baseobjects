"""An abstract class which registers subclasses with namespaces, allowing subclass dispatching.

This module provides the NamespaceRegisteredClass, which extends BaseRegisteredClass to add namespace-based
registration and retrieval of subclasses.
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
from .baseclassregistry import BaseClassRegistry
from .baseregisteredclass import BaseRegisteredClass
from .namespaceclassregistry import NamespaceClassRegistry


# Definitions #
# Classes #
class NamespaceRegisteredClass(BaseRegisteredClass):
    """An abstract class which registers subclasses, allowing subclass dispatching.

    Attributes:
        class_registry: A registry of all subclasses of this class.
        class_registry_head: The root class of the registered classes.
        class_registry_namespace: The namespace of the subclass.
        class_registry_name: The name of which the subclass will be registered as.
        class_registration: Determines if this class/subclass will be added to the registry.
        _module_: Optional module name to use instead of __module__ for namespace.
    """

    # Class Attributes #
    _module_: ClassVar[str | None] = None

    class_registry_type: ClassVar[type[BaseClassRegistry]] = NamespaceClassRegistry
    class_registry_namespace: ClassVar[str | None] = None
    class_registry_name: ClassVar[str | None] = None

    # Class Methods #
    # Construction/Destruction
    def __init_subclass__(cls, namespace: str | None = None, name: str | None = None, **kwargs: Any) -> None:
        """The init when creating a subclass.

        Args:
            namespace: The namespace to register the subclass under. If None, uses class_registry_namespace.
            name: The name to register the subclass as. If None, uses class_registry_name or class name.
            **kwargs: Keyword arguments for creating a subclass.
        """
        super().__init_subclass__(**kwargs)

        # Add subclass to the registry.
        if cls.class_registration:
            if cls.class_registry is None:
                cls.create_class_registry()
            elif not cls.class_registry:
                cls.class_registry_head = cls

            cls.register_class(namespace=namespace or cls.class_registry_namespace, name=name)

    # Register
    @classmethod
    def register_class(
        cls,
        namespace: str | None = None,
        name: str | None = None,
        class_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Registers this class with the given namespace and name.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass.
            class_kwargs: The keyword arguments for creating the class.
        """
        if namespace is None:
            if "class_registry_namespace" in cls.__dict__:
                namespace = cls.class_registry_namespace
            else:
                namespace = cls.__dict__.get("_module_", cls.__module__)
                namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace
        else:
            namespace = namespace[4:] if namespace.split(".")[0] == "src" else namespace

        if name is None:
            name = cls.class_registry_name if "class_registry_name" in cls.__dict__ else cls.__name__

        cls.class_registry.register_classes(cls, namespace, name)

    @classmethod
    def get_registered_class(cls, namespace: str, name: str, module: str | None = None) -> Optional["BaseRegisteredClass"]:
        """Gets a subclass from the registry.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the subclass to get.
            module: The module to import if the subclass is not found.

        Returns:
            The requested subclass, or None if not found.
        """
        return cls.class_registry.get_class(namespace, name, module)
