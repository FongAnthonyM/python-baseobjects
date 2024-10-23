#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" composition_example.py
An example of how to create and use a Composite.
"""

# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #
from baseobjects.objects import ClassNamespaceRegister
from baseobjects.composition import BaseDispatchingComposite, BaseComponent


# Definitions #
# Classes #
class PrintingComponent(BaseComponent):
    """A component that prints information from its composite."""
    def print_information(self):
        """Prints the number attribute of the composite."""
        print(self.composite.number)


class AddingComponent(BaseComponent):
    """A component that adds a value to the composite's number attribute."""
    def add(self, a):
        """Adds a value to the composite's number attribute.

        Args:
            a (int): The value to add.
        """
        self.composite.number += a


class SubtractingComponent(BaseComponent):
    """A component that subtracts a value from the composite's number attribute."""
    def subtract(self, a):
        """Subtracts a value from the composite's number attribute.

        Args:
            a (int): The value to subtract.
        """
        self.composite.number -= a


class ExampleDispatchingComposite(BaseDispatchingComposite):
    """A composite class that holds and manages components.

    Attributes:
        default_component_types (dict): Default types of components.
        component_types_register (ClassNamespaceRegister): A register of component classes and their keyword arguments.
        number (int): A number attribute managed by the composite.
    """
    # Class Attributes #
    default_component_types = {"printing": (PrintingComponent, {}), "adding": (AddingComponent, {})}

    # Attributes #
    component_types_register: ClassNamespaceRegister = ClassNamespaceRegister()
    number: int = 0

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        class_name: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        **kwargs: Any
    ) -> None:
        # Parent Attributes #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                name=name,
                namespace=namespace,
                class_name=class_name,
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        name: str | None = None,
        namespace: str | None = None,
        class_name: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> None:
        """Constructs this object.

        Args:
            name: The name of the component to add.
            namespace: The namespace of the component to add.
            class_name: The class name of the component to add.
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            **kwargs: Keyword arguments for inheritance.
        """
        if name is not None and namespace is not None and class_name is not None:
            component_types = self.dispatch_component_types(name, namespace,class_name) | (component_types or {})

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def dispatch_component_types(
        self,
        name: str,
        namespace: str,
        class_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, tuple[type, dict[str, Any]]]:
        """A method that dispatches component types using the given arguments.

        Args:
            name: The name of the component to add.
            namespace: The namespace of the component to add.
            class_name: The class name of the component to add.
            *args: The arguments to use in dispatching.
            **kwargs: The keyword arguments to use in dispatching.

        Returns:
            A dictionary of the names of the components, their types, and their keyword arguments.
        """
        return {name: self.component_types_register.get_class(namespace, class_name)}


# Assignment
ExampleDispatchingComposite.component_types_register.register_class(
    SubtractingComponent,
    namespace="example",
    name="SubtractingComponent",
)

# Main #
if __name__ == "__main__":
    # Create the composite
    composite_one = ExampleDispatchingComposite()

    # View the components
    print(composite_one.components)

    # Create composite with string arguments
    composite_two = ExampleDispatchingComposite(
        name="subtraction",
        namespace="example",
        class_name="SubtractingComponent",
    )

    # View the components
    print(composite_two.components)
