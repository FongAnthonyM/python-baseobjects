"""basecomposite.py
A basic composite object which is composed of component objects.
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
from collections.abc import Mapping
from itertools import chain
from typing import ClassVar, Any

# Third-Party Packages #

# Local Packages #
from ..bases import BaseObject


# Definitions #
# Classes #
class BaseComposite(BaseObject):
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
    default_component_types: ClassVar[dict[str, tuple[type, dict[str, Any]]]] = {}

    # Attributes #
    components: dict[str, Any] = {}

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        **kwargs: Any
    ) -> None:
        # Attributes #
        self.components: dict[str, Any] = self.components.copy()

        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> None:
        """Constructs this object.

        Args:
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            **kwargs: Keyword arguments for inheritance.
        """
        self.construct_components(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
        )

        super().construct(**kwargs)

    def construct_components(
        self,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
    ) -> None:
        """Constructs or adds components.

        Args:
            component_kwargs: The keyword arguments for creating the components.
            component_types: Component class and their keyword arguments to instantiate.
            components: Components to add.
        """
        new_kwargs = {} if component_kwargs is None else component_kwargs
        if components is None:
            components = {}

        # Check for overriding components, and remove redundant construction
        temp_types = self.default_component_types | ({} if component_types is None else component_types)
        type_names = set(temp_types.keys()) - set(components.keys()) - set(self.components.keys())

        # Create Construction Iterator #
        type_iter = ((n, temp_types[n]) for n in type_names)
        default_components_iter = ((n, c(composite=self, **(k | new_kwargs.get(n, {})))) for n, (c, k) in type_iter)

        self.components.update(default_components_iter)
        for name, component in components.items():
            component.composite = self
            self.components[name] = component

    # Components
    def create_component(
        self,
        name: str,
        component: type["BaseComponent"],
        *args: Any,
        **kwargs: Any,
    ) -> "BaseComponent":
        """Creates a new component.

        Args:
            name: The name of the new component.
            component: The new component type to create.
            *args: Positional arguments for the new component.
            **kwargs: Keyword arguments for the new component.
        """
        self.components[name] = component = component(*args, **({"composite": self} | kwargs))
        return component

    def add_component(self, name: str, component: Any) -> Any:
        """Adds an existing component to this composite.

        Args:
            name: The name of the component to add.
            component: The component to add.

        Returns:
            The added component.
        """
        self.components[name] = component
        component.composite = self
        return component

    def remove_component(self, name: str) -> Any:
        """Removes a component by name.

        Args:
            name: The name of the component to remove.

        Returns:
            The removed component.

        Raises:
            KeyError: If no component with the given name exists.
        """
        component = self.components[name]
        del self.components[name]
        if self is component.composite:
            component.composite = None
        return component
