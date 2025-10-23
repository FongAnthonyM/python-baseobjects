#!/usr/bin/env python
"""basemeta_example.py
An example of how to use BaseMeta metaclass.

This example demonstrates:
1. Creating a metaclass using BaseMeta
2. Defining classes with custom metaclasses
3. Shallow copying (copy) of metaclasses and their instances
4. Deep copying (deepcopy) of metaclasses and their instances
5. Comparing original and copied objects
"""

# Imports #
# Standard Libraries #
import copy
from typing import Any, ClassVar

# Source Packages #
from baseobjects.bases import BaseMeta


# Classes #
class ExampleMeta(BaseMeta):
    """An example metaclass that extends BaseMeta."""

    registry: ClassVar[dict[str, type]] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        """Create a new class and register it in the registry."""
        cls = super().__new__(mcs, name, bases, namespace)
        mcs.registry[name] = cls
        return cls

    def get_registered_classes(self) -> list[str]:
        """Get a list of all registered class names."""
        return list(self.registry.keys())


class BaseWithMeta(metaclass=ExampleMeta):
    """A base class that uses ExampleMeta as its metaclass."""

    def __init__(self, name: str) -> None:
        """Initialize the base instance.

        Args:
            name: The name for this instance.
        """
        self.name = name
        self.data = {"key": "value"}
        self.items = [1, 2, 3]


class ChildClass(BaseWithMeta):
    """A child class that inherits from BaseWithMeta."""

    def __init__(self, name: str, value: int) -> None:
        """Initialize the child instance.

        Args:
            name: The name for this instance.
            value: An integer value associated with the instance.
        """
        super().__init__(name)
        self.value = value
        self.nested = {"nested_key": [4, 5, 6]}


# Example Sections #
def metaclass_creation_example() -> None:
    """Demonstrate creating and using a metaclass with BaseMeta."""
    print("\nMetaclass Creation Example:")

    # Show registered classes
    registered = BaseWithMeta.get_registered_classes()
    print(f"Registered classes: {registered} == ['BaseWithMeta', 'ChildClass']")

    # Create instances of classes with our metaclass
    base_instance = BaseWithMeta("base_example")
    child_instance = ChildClass("child_example", 42)

    print(f"Base instance name: {base_instance.name} == 'base_example'")
    print(f"Child instance name: {child_instance.name} == 'child_example'")
    print(f"Child instance value: {child_instance.value} == 42")

    # Verify metaclass
    print(f"BaseWithMeta's metaclass: {type(BaseWithMeta).__name__} == 'ExampleMeta'")
    print(f"ChildClass's metaclass: {type(ChildClass).__name__} == 'ExampleMeta'")


# Main #
if __name__ == "__main__":
    # Run examples
    metaclass_creation_example()
