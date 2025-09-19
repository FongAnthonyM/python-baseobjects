#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""basecomponent_example.py
An example of how to create and use BaseComponent.

This example demonstrates:
1. Creating a basic component class
2. Connecting a component to a composite
3. Accessing composite attributes from a component
4. Modifying composite attributes from a component
5. Component serialization and deserialization
"""


# Imports #
# Standard Libraries #
import pickle

# Third-Party Packages #
from baseobjects.composition import BaseComponent
from baseobjects.bases import BaseObject

# Local Packages #


# Definitions #
# Classes #
class SimpleComposite(BaseObject):
    """A simple composite class that can be used with components.
    
    Attributes:
        value (int): A value that can be modified by components.
        name (str): A name that can be accessed by components.
    """
    # Attributes #
    value: int = 0
    name: str = "Default"


class ValueComponent(BaseComponent):
    """A component that can modify the value of its composite.
    
    This component demonstrates basic interaction with a composite.
    """
    def increment_value(self, amount: int = 1) -> None:
        """Increments the value of the composite.
        
        Args:
            amount: The amount to increment by. Defaults to 1.
        """
        self.composite.value += amount
    
    def get_value(self) -> int:
        """Gets the current value of the composite.
        
        Returns:
            The current value of the composite.
        """
        return self.composite.value


class NameComponent(BaseComponent):
    """A component that can access and modify the name of its composite."""
    
    def set_name(self, name: str) -> None:
        """Sets the name of the composite.
        
        Args:
            name: The new name for the composite.
        """
        self.composite.name = name
    
    def get_name(self) -> str:
        """Gets the current name of the composite.
        
        Returns:
            The current name of the composite.
        """
        return self.composite.name
    
    def get_formatted_name(self) -> str:
        """Gets a formatted version of the composite's name.
        
        Returns:
            A formatted version of the composite's name.
        """
        return f"Composite: {self.composite.name}"


# Functions #
# Example Sections #
def basic_component_usage():
    """Demonstrates basic usage of components with a composite."""
    print("Basic Component Usage:\n")
    
    # Create a composite
    print("Creating a simple composite...")
    composite = SimpleComposite()
    print(f"Initial composite value: {composite.value} == 0")
    print(f"Initial composite name: {composite.name} == 'Default'")
    print()
    
    # Create a component and connect it to the composite
    print("Creating a value component and connecting it to the composite...")
    value_component = ValueComponent(composite=composite)
    
    # Use the component to interact with the composite
    print("Using the component to increment the composite's value...")
    value_component.increment_value()
    print(f"Composite value after increment: {composite.value} == 1")
    
    # Increment by a specific amount
    print("Incrementing by a specific amount (5)...")
    value_component.increment_value(5)
    print(f"Composite value after increment by 5: {composite.value} == 6")
    
    # Get the value through the component
    print("Getting the value through the component...")
    component_value = value_component.get_value()
    print(f"Value retrieved through component: {component_value} == 6")
    print()


def multiple_components():
    """Demonstrates using multiple components with a single composite."""
    print("Multiple Components with a Single Composite:\n")
    
    # Create a composite
    print("Creating a simple composite...")
    composite = SimpleComposite()
    
    # Create multiple components
    print("Creating multiple components for the same composite...")
    value_component = ValueComponent(composite=composite)
    name_component = NameComponent(composite=composite)
    
    # Use the components to interact with the composite
    print("Using the value component to modify the composite's value...")
    value_component.increment_value(10)
    print(f"Composite value: {composite.value} == 10")
    
    print("Using the name component to modify the composite's name...")
    name_component.set_name("MyComposite")
    print(f"Composite name: {composite.name} == 'MyComposite'")
    
    # Get formatted name
    print("Getting formatted name through the name component...")
    formatted_name = name_component.get_formatted_name()
    print(f"Formatted name: {formatted_name} == 'Composite: MyComposite'")
    print()


def component_serialization():
    """Demonstrates serialization and deserialization of components."""
    print("Component Serialization and Deserialization:\n")
    
    # Create a composite and component
    print("Creating a composite and component...")
    composite = SimpleComposite()
    composite.value = 42
    composite.name = "SerializableComposite"
    
    value_component = ValueComponent(composite=composite)
    
    # Serialize the component
    print("Serializing the component...")
    serialized = pickle.dumps(value_component)
    print(f"Component serialized to {len(serialized)} bytes")
    
    # Modify the original composite
    print("Modifying the original composite...")
    composite.value = 100
    print(f"Original composite value changed to: {composite.value} == 100")
    
    # Deserialize to a new component
    print("Deserializing to a new component...")
    new_component = pickle.loads(serialized)
    
    # The new component needs a composite
    print("The deserialized component needs a composite reference...")
    new_composite = SimpleComposite()
    new_composite.value = 0
    new_component.composite = new_composite
    
    # Use the new component
    print("Using the deserialized component...")
    print(f"Initial value of new composite: {new_composite.value} == 0")
    new_component.increment_value(5)
    print(f"Value after increment: {new_composite.value} == 5")
    print()


def component_construction():
    """Demonstrates different ways to construct components."""
    print("Component Construction Methods:\n")
    
    # Create a composite
    composite = SimpleComposite()
    
    # Method 1: Pass composite during initialization
    print("Method 1: Pass composite during initialization...")
    component1 = ValueComponent(composite=composite)
    component1.increment_value()
    print(f"Composite value after increment: {composite.value} == 1")
    
    # Method 2: Create component first, then set composite
    print("\nMethod 2: Create component first, then set composite...")
    component2 = ValueComponent()
    component2.composite = composite
    component2.increment_value(2)
    print(f"Composite value after increment: {composite.value} == 3")
    
    # Method 3: Use the construct method
    print("\nMethod 3: Use the construct method...")
    component3 = ValueComponent(init=False)
    component3.construct(composite=composite)
    component3.increment_value(3)
    print(f"Composite value after increment: {composite.value} == 6")
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of components
    basic_component_usage()
    
    # Using multiple components with a single composite
    multiple_components()
    
    # Component serialization and deserialization
    component_serialization()
    
    # Different ways to construct components
    component_construction()