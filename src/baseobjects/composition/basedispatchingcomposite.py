"""basedispatchingcomposite.py
A composite object which includes methods for dispatching component objects during instantiation.
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

# Local Packages
from ..classregistration import NamespaceClassRegistry
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseDispatchingComposite(BaseComposite):
    """A composite object which includes methods for dispatching component objects during instantiation.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object.

    Attributes:
        component_types_registry: A registry of component classes and their keyword arguments.
        components: The components of this object.

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

        Args:
            *args: Positional arguments to use in dispatching.
            **kwargs: Keyword arguments to use in dispatching.

        Returns:
            A dictionary of the names of the components, their types, and their keyword arguments.
        """
        raise NotImplementedError("This method needs to be set to dispatch component types.")
