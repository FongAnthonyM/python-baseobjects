"""basedispatchingcomposite.py
A basic composite object which is composed of component objects.
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
from typing import Any

# Third-Party Packages #

# Local Packages #
from ..objects import ClassNamespaceRegister
from .basecomposite import BaseComposite


# Definitions #
# Classes #
class BaseDispatchingComposite(BaseComposite):
    """A basic composite object which is composed of component objects.

    Class Attributes:
        default_component_types: The default component classes and their keyword arguments for this object.
        default_components: The default components for this object.

    Attributes:
        components: The components of this object.

    Args:
        component_kwargs: Keyword arguments for creating the components.
        component_types: Component classes and their keyword arguments to instantiate.
        components: Components to add.
        **kwargs: Keyword arguments for inheritance.
    """

    # Class Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()

    # Class Methods #
    @classmethod
    def get_component_types(cls, *args: Any, **kwargs: Any) -> dict[str, tuple[type, dict[str, Any]]]:
        """Gets a class namespace, name, and keyword arguments from a given set of arguments.

        Args:
            *args: The arguments to get the namespace and name from.
            **kwargs: The keyword arguments to get the namespace and name from.

        Returns:
            The namespace and name of the class.
        """
        raise NotImplementedError("This method needs to be set to dispatch components.")

    # Instance Methods #
    # Constructors/Destructors
    # def construct(
    #     self,
    #     component_kwargs: dict[str, dict[str, Any]] | None = None,
    #     component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
    #     components: dict[str, Any] | None = None,
    #     load_kwargs: dict[str, Any] | None = None,
    #     **kwargs: Any
    # ) -> None:
    #     """Constructs this object.
    #
    #     Args:
    #         component_kwargs: Keyword arguments for creating the components.
    #         component_types: Component classes and their keyword arguments to instantiate.
    #         components: Components to add.
    #         **kwargs: Keyword arguments for inheritance.
    #     """
    #     component_types = self.load_component_types(**load_kwargs) | component_types
    #
    #     self.construct_components
    #
    #     super().construct(
    #         component_kwargs=component_kwargs,
    #         component_types=component_types,
    #         components=components,
    #         **kwargs,
    #     )
