"""basedispatchingcomposite.py
A composite object which includes methods for dispatching component objects during instantiation.

This module provides the BaseDispatchingComposite class, which extends the BaseComposite class with the ability to
dynamically determine which component types to instantiate based on input arguments. It uses a registry to store and
retrieve component classes organized by namespaces, and provides an abstract method for dispatching component types
that should be implemented by subclasses.
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

# Local Packages #
from ..classregistration import NamespaceClassRegistry
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseDispatchingComposite(BaseComposite):
    """A composite object which includes methods for dispatching component objects during instantiation.

    This class extends BaseComposite by adding a mechanism to dynamically determine which component types to instantiate
    based on input arguments. It uses a registry to store and retrieve component classes organized by namespaces, and
    provides an abstract method for dispatching component types that should be implemented by subclasses.

    The dispatching mechanism allows for flexible component creation based on runtime conditions or configuration,
    enabling more dynamic composite objects that can adapt their structure based on the provided arguments.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object. Inherited
            from BaseComposite.

    Attributes:
        component_types_registry: A registry of component classes and their keyword arguments organized by namespaces.
            Used to store and retrieve component types for dispatching.
        components: The components of this object. Inherited from BaseComposite.

    Args:
        component_kwargs: Keyword arguments for creating the components.
        component_types: Component classes and their keyword arguments to instantiate.
        components: Components to add.
        **kwargs: Keyword arguments for inheritance.
    """

    # Attributes #
    component_types_registry: NamespaceClassRegistry

    # Methods #
    def dispatch_component_types(self, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """An abstract method that dispatches component types using the given arguments.

        This method should be implemented by subclasses to determine which component types to instantiate based on the
        provided arguments. The implementation should analyze the arguments and return a dictionary mapping component
        names to their types and initialization keyword arguments.

        The returned dictionary will be used to create component instances during the composite object's construction
        process. This allows for dynamic component creation based on runtime conditions or configuration.

        Args:
            *args: Positional arguments to use in dispatching. These can be any values that help determine which
                component types to instantiate.
            **kwargs: Keyword arguments to use in dispatching. These can be any key-value pairs that help determine
                which component types to instantiate.

        Returns:
            A dictionary mapping component names (str) to tuples containing the component type (type) and a dictionary
            of keyword arguments (dict[str, Any]) to use when instantiating that component.
            For example: {'component_name': (ComponentClass, {'arg1': value1, 'arg2': value2})}

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        raise NotImplementedError("This method needs to be set to dispatch component types.")
