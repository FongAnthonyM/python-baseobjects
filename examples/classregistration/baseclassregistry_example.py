#!/usr/bin/env python
"""baseclassregistry_example.py
An example of how to create and use BaseClassRegistry.

This example demonstrates:
1. Creating a concrete implementation of BaseClassRegistry
2. Registering classes in the registry
3. Retrieving classes from the registry
4. Using the registry to create instances of registered classes
"""


# Imports #
# Standard Libraries #
from typing import Any, Type

# Source Packages #
from baseobjects.classregistration import BaseClassRegistry


# Definitions #
# Classes #
class SimpleClassRegistry(BaseClassRegistry):
    """A simple implementation of BaseClassRegistry.

    This registry uses class names as keys to store and retrieve classes.
    """

    def register_class(self, cls: type, name: str | None = None, **kwargs: Any) -> None:
        """Registers a class with the given name.

        Args:
            cls: The class to register.
            name: The name to register the class under. If None, uses the class name.
            **kwargs: Additional keyword arguments (not used in this implementation).
        """
        if name is None:
            name = cls.__name__

        self[name] = cls

    def get_class(self, name: str, default: Any = None) -> type:
        """Gets a class from the registry by name.

        Args:
            name: The name of the class to retrieve.
            default: The default value to return if the class is not found.

        Returns:
            The requested class, or the default value if not found.
        """
        return self.get(name, default)


# Example classes to register
class Animal:
    """Base class for animals."""

    def __init__(self, name: str) -> None:
        self.name = name

    def speak(self) -> str:
        """Returns the sound the animal makes."""
        return "..."


class Dog(Animal):
    """A dog that can bark."""

    def speak(self) -> str:
        """Returns the sound a dog makes."""
        return f"{self.name} says: Woof!"


class Cat(Animal):
    """A cat that can meow."""

    def speak(self) -> str:
        """Returns the sound a cat makes."""
        return f"{self.name} says: Meow!"


class Bird(Animal):
    """A bird that can tweet."""

    def speak(self) -> str:
        """Returns the sound a bird makes."""
        return f"{self.name} says: Tweet!"


# Functions #
# Example Sections #
def basic_registry_usage() -> None:
    """Demonstrates basic usage of a class registry."""
    print("Basic Class Registry Usage:\n")

    # Create a registry
    print("Creating a class registry...")
    registry = SimpleClassRegistry()

    # Register classes
    print("Registering classes...")
    registry.register_class(Dog)
    registry.register_class(Cat)
    registry.register_class(Bird)

    print("Classes in registry:")
    for name, cls in registry.items():
        print(f"  - {name}: {cls.__name__}")
    print()

    # Get classes from the registry
    print("Getting classes from the registry...")
    dog_class = registry.get_class("Dog")
    cat_class = registry.get_class("Cat")

    # Create instances
    print("Creating instances of retrieved classes...")
    dog = dog_class("Buddy")
    cat = cat_class("Whiskers")

    # Use the instances
    print(f"Dog instance: {dog.speak()} == 'Buddy says: Woof!'")
    print(f"Cat instance: {cat.speak()} == 'Whiskers says: Meow!'")

    # Try to get a non-existent class
    print("\nTrying to get a non-existent class...")
    fish_class = registry.get_class("Fish", default=None)
    print(f"Result: {fish_class} == None")
    print()


def custom_registry_keys() -> None:
    """Demonstrates using custom keys for class registration."""
    print("Custom Registry Keys:\n")

    # Create a registry
    print("Creating a class registry...")
    registry = SimpleClassRegistry()

    # Register classes with custom names
    print("Registering classes with custom names...")
    registry.register_class(Dog, name="canine")
    registry.register_class(Cat, name="feline")
    registry.register_class(Bird, name="avian")

    print("Classes in registry:")
    for name, cls in registry.items():
        print(f"  - {name}: {cls.__name__}")
    print()

    # Get classes from the registry using custom names
    print("Getting classes from the registry using custom names...")
    dog_class = registry.get_class("canine")
    cat_class = registry.get_class("feline")
    bird_class = registry.get_class("avian")

    # Create instances
    print("Creating instances of retrieved classes...")
    dog = dog_class("Rex")
    cat = cat_class("Felix")
    bird = bird_class("Tweety")

    # Use the instances
    print(f"Dog instance: {dog.speak()} == 'Rex says: Woof!'")
    print(f"Cat instance: {cat.speak()} == 'Felix says: Meow!'")
    print(f"Bird instance: {bird.speak()} == 'Tweety says: Tweet!'")
    print()


def factory_pattern() -> None:
    """Demonstrates using a class registry as a factory."""
    print("Factory Pattern with Class Registry:\n")

    # Create a registry
    print("Creating a class registry...")
    registry = SimpleClassRegistry()

    # Register classes
    print("Registering classes...")
    registry.register_class(Dog)
    registry.register_class(Cat)
    registry.register_class(Bird)

    # Create a factory function
    def create_animal(animal_type: str, name: str) -> Animal:
        """Factory function to create animals.

        Args:
            animal_type: The type of animal to create.
            name: The name of the animal.

        Returns:
            An instance of the requested animal type.

        Raises:
            ValueError: If the animal type is not found in the registry.
        """
        animal_class = registry.get_class(animal_type)
        if animal_class is None:
            msg = f"Unknown animal type: {animal_type}"
            raise ValueError(msg)
        return animal_class(name)

    # Use the factory to create animals
    print("Using the factory to create animals...")

    animals = [
        ("Dog", "Rover"),
        ("Cat", "Mittens"),
        ("Bird", "Polly"),
    ]

    for animal_type, name in animals:
        try:
            animal = create_animal(animal_type, name)
            print(f"Created {animal_type}: {animal.speak()}")
        except ValueError as e:
            print(f"Error: {e}")

    # Try to create an unknown animal type
    print("\nTrying to create an unknown animal type...")
    try:
        animal = create_animal("Fish", "Nemo")
        print(f"Created Fish: {animal.speak()}")
    except ValueError as e:
        print(f"Error: {e} == 'Unknown animal type: Fish'")
    print()


def registry_with_head_class() -> None:
    """Demonstrates using a registry with a head class."""
    print("Registry with Head Class:\n")

    # Create a registry with a head class
    print("Creating a class registry with Animal as the head class...")
    registry = SimpleClassRegistry(head_class=Animal)

    # Register classes
    print("Registering classes...")
    registry.register_class(Dog)
    registry.register_class(Cat)
    registry.register_class(Bird)

    print(f"Head class: {registry.head_class.__name__}")
    print("Classes in registry:")
    for name, cls in registry.items():
        print(f"  - {name}: {cls.__name__}")
    print()

    # Create instances using the head class as a base
    print("Creating instances and checking if they are instances of the head class...")
    dog = registry.get_class("Dog")("Fido")
    cat = registry.get_class("Cat")("Garfield")

    print(f"Is dog an instance of Animal? {isinstance(dog, Animal)} == True")
    print(f"Is cat an instance of Animal? {isinstance(cat, Animal)} == True")
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of a class registry
    basic_registry_usage()

    # Using custom keys for class registration
    custom_registry_keys()

    # Using a class registry as a factory
    factory_pattern()

    # Using a registry with a head class
    registry_with_head_class()
