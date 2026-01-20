"""namespaceclassregistry.py
A registry for classes organized by namespaces.

This module provides the NamespaceClassRegistry class, which extends BaseClassRegistry to organize registered classes by
namespaces, allowing for more structured class registration and retrieval.
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
from collections.abc import Iterable, Mapping
from copy import deepcopy
from importlib import import_module
from typing import Any, ClassVar
from warnings import warn

# Local Packages #
from ..bases import DEFAULTSENTINEL
from .baseclassregistry import BaseClassRegistry


# Definitions #
# Classes #
class NamespaceClassRegistry(BaseClassRegistry):
    """A registry for classes in namespaces.

    Attributes:
        default_classes: The default namespaces, classes, and their keyword arguments for this object.
    """

    # Attributes #
    default_classes: ClassVar[dict[str, dict[str, tuple[type, dict[str, Any]]]]] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        classes: dict[str, dict[str, tuple[type, dict[str, Any]]]] | Iterable[Any] | None = None,
        head_class: type | None = None,
        *args: Any,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initializes this object with the given arguments.

        Args:
            classes: Classes and their namespaces to add, can be an iterable of iterables or a dictionary.
            head_class: The head class of the registered classes.
            *args: Positional arguments for inheritance.
            init: Determines if this object will construct.
            **kwargs: Keyword arguments for inheritance.
        """
        # Parent Initialization #
        super().__init__()

        # Attributes #
        self.data.update(((n, deepcopy(ns)) for n, ns in self.default_classes.items()))

        # Object Construction #
        if init:
            self.construct(
                head_class=head_class,
                classes=classes,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(  # type: ignore[override]
        self,
        classes: dict[str, dict[str, tuple[type, dict[str, Any]]]] | Iterable[Any] | None = None,
        head_class: type | None = None,
        **kwargs: Any,
    ) -> None:
        """Constructs this object with the given arguments.

        Args:
            classes: Classes to add, can be an iterable of iterables or a dictionary.
            head_class: The head class of the registered classes.
            **kwargs: Keyword arguments for inheritance.
        """
        if isinstance(classes, Mapping):
            self.data.update(((n, deepcopy(ns)) for n, ns in classes.items()))
        elif isinstance(classes, Iterable):
            self.register_classes(classes)

        super().construct(head_class=head_class, **kwargs)

    # Registry
    def register_class(
        self,
        cls: type,
        namespace: str | None = None,
        name: str | None = None,
        class_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Registers a class with the given namespace and name.

        Args:
            cls: The class to registry.
            namespace: The namespace of the subclass.
            name: The name of the subclass.
            class_kwargs: The keyword arguments for creating the class.
        """
        if namespace is None:
            namespace = cls.__dict__.get("_module_", cls.__module__)

        if name is None:
            name = cls.__name__

        if class_kwargs is None:
            class_kwargs = {}

        if (namespace_types := self.get(namespace, None)) is not None:
            namespace_types[name] = (cls, class_kwargs)
        else:
            self.data[namespace] = {name: (cls, class_kwargs)}

    def register_classes(self, classes: Iterable[Iterable[Any]]) -> None:
        """Registers multiple classes.

        Args:
            classes: The classes to registry as an iterable of the arguments for register_class.
        """
        for cls in classes:
            self.register_class(*cls)

    def update_classes(self, classes: dict[str, dict[str, tuple[type, dict[str, Any]]]] | Any) -> None:
        """Updates the classes.

        Args:
            classes: The namespaces and classes to update.
        """
        self.data.update(((n, deepcopy(ns)) for n, ns in classes.items()))

    def get_class(
        self,
        namespace: str,
        name: str,
        module: str | None = None,
        default: Any = DEFAULTSENTINEL,
        with_kwargs: bool = False,
    ) -> Any:
        """Gets a class from the registry.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the class to get.
            module: The module to import if the class is not found.
            default: The default value to return if the class is not found.
                If DEFAULTSENTINEL, raises KeyError when not found.
            with_kwargs: Determines if the class and its keyword arguments should be returned.

        Returns:
            The requested class if with_kwargs is False, or a tuple of (class, kwargs) if with_kwargs is True.
            If the class is not found and default is not DEFAULTSENTINEL, returns default.

        Raises:
            KeyError: If the namespace or class is not found and default is DEFAULTSENTINEL.
        """
        if (namespace_types := self.data.get(namespace, None)) is None and module is not None:
            try:
                import_module(module)
            except Exception as e:
                msg = f"Failed to import module '{module}' with error: {e}, skipping."
                warn(msg, stacklevel=2)
            else:
                namespace_types = self.data.get(namespace, None)

        if namespace_types is None:
            if default is DEFAULTSENTINEL:
                msg = f"Namespace '{namespace}' not found."
                raise KeyError(msg)
            return default
        elif (class_ := namespace_types.get(name, None)) is None and module is not None:
            try:
                import_module(module)
            except Exception as e:
                msg = f"Failed to import module '{module}' with error: {e}, skipping."
                warn(msg, stacklevel=2)
            else:
                class_ = namespace_types.get(name, None)

        if class_ is None:
            if default is DEFAULTSENTINEL:
                msg = f"Class '{name}' not found in namespace '{namespace}'."
                raise KeyError(msg)
            return default
        else:
            return class_ if with_kwargs else class_[0]

    def get_new(
        self,
        namespace: str,
        name: str,
        module: str | None = None,
        default: Any = DEFAULTSENTINEL,
        with_kwargs: bool = True,
        class_kwargs: dict[str, Any] | None = None,
    ) -> Any:
        """Gets a new instance of a class from the registry.

        Args:
            namespace: The namespace of the subclass.
            name: The name of the class to get.
            module: The module to import if the class is not found.
            default: The default value to return if the class is not found.
                     If DEFAULTSENTINEL, raises KeyError when not found.
            with_kwargs: Determines if the default keyword arguments should be used.
            class_kwargs: The keyword arguments for the class.

        Returns:
            A new instance of the requested class, or default if the class is not found
            and default is not DEFAULTSENTINEL.
        """
        if class_kwargs is None:
            class_kwargs = {}

        cls, d_kwargs = self.get_class(namespace, name, module, default, with_kwargs=True)
        return cls(**((d_kwargs | class_kwargs) if with_kwargs else class_kwargs))
