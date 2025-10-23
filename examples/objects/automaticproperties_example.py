#!/usr/bin/env python
"""automaticproperties_example.py
An example of how to use AutomaticProperties class.

This example demonstrates:
1. Creating a class with automatic properties
2. Using different property function factories
3. Customizing property get, set, and delete behavior
4. Creating properties with different access patterns
5. Extending AutomaticProperties for specialized behavior
"""

# Imports #
# Standard Libraries #
from typing import Any, ClassVar, NoReturn

# Source Packages #
from baseobjects.objects import AutomaticProperties
from baseobjects.typing import PropertyCallbacks


# Classes #
class Person(AutomaticProperties):
    """A simple person class with automatic properties."""

    # Class Attributes #
    properties = {"name": "_name", "age": "_age", "email": "_email"}

    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize a person with name, age, and email.

        Args:
            name: The person's name
            age: The person's age
            email: The person's email address
        """
        self._name = name
        self._age = age
        self._email = email


class ValidatedPerson(AutomaticProperties):
    """A person class with validated properties."""

    # Class Attributes #
    properties = {"name": "_name", "age": "_age", "email": "_email"}

    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize a person with name, age, and email.

        Args:
            name: The person's name
            age: The person's age
            email: The person's email address
        """
        self._name = name
        self._age = age
        self._email = email

    # Property Methods #
    def property_set(self, value: Any, name: str) -> None:
        """Override the default property_set method to add validation.

        Args:
            value: The value to set
            name: The name of the property
        """
        if name == "_age" and value < 0:
            msg = "Age cannot be negative"
            raise ValueError(msg)
        if name == "_email" and "@" not in value:
            msg = "Invalid email format"
            raise ValueError(msg)

        setattr(self, name, value)


class CustomPropertyPerson(AutomaticProperties):
    """A person class with custom property factory methods."""

    # Class Attributes #
    properties = {
        "name": ("custom_property_factory", "_name", {}),
        "age": ("custom_property_factory", "_age", {}),
        "email": ("custom_property_factory", "_email", {}),
    }

    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize a person with name, age, and email.

        Args:
            name: The person's name
            age: The person's age
            email: The person's email address
        """
        self._name = name
        self._age = age
        self._email = email
        self._access_count = {}

    @classmethod
    def custom_property_factory(cls, info: str) -> PropertyCallbacks:
        """A custom factory method for creating property modification methods.

        Args:
            info: The name of the attribute to access

        Returns:
            A tuple of get, set, and delete functions
        """
        name = info

        def _get(self):
            # Track access count
            if name not in self._access_count:
                self._access_count[name] = 0
            self._access_count[name] += 1
            return getattr(self, name)

        def _set(self, value) -> None:
            setattr(self, name, value)

        def _del(self) -> None:
            delattr(self, name)

        return _get, _set, _del


class ReadOnlyPerson(AutomaticProperties):
    """A person class with read-only properties."""

    # Class Attributes #
    properties = {
        "name": ("readonly_property_factory", "_name", {}),
        "age": ("readonly_property_factory", "_age", {}),
        "email": ("readonly_property_factory", "_email", {}),
    }

    def __init__(self, name: str = "", age: int = 0, email: str = "") -> None:
        """Initialize a person with name, age, and email.

        Args:
            name: The person's name
            age: The person's age
            email: The person's email address
        """
        self._name = name
        self._age = age
        self._email = email

    @classmethod
    def readonly_property_factory(cls, info: str) -> PropertyCallbacks:
        """A factory method for creating read-only property methods.

        Args:
            info: The name of the attribute to access

        Returns:
            A tuple of get, set, and delete functions
        """
        name = info

        def _get(self):
            return getattr(self, name)

        def _set(self, value) -> NoReturn:
            msg = f"Property '{name[1:]}' is read-only"
            raise AttributeError(msg)

        def _del(self) -> NoReturn:
            msg = f"Property '{name[1:]}' is read-only"
            raise AttributeError(msg)

        return _get, _set, _del


# Example Sections #
def basic_automaticproperties_example() -> None:
    """Demonstrate basic usage of AutomaticProperties."""
    print("\nBasic AutomaticProperties Example:")

    # Create a person with automatic properties
    person = Person(name="John Doe", age=30, email="john@example.com")

    # Access properties
    print(f"Name: {person.name} == 'John Doe'")
    print(f"Age: {person.age} == 30")
    print(f"Email: {person.email} == 'john@example.com'")

    # Modify properties
    person.name = "Jane Doe"
    person.age = 28
    person.email = "jane@example.com"

    # Access modified properties
    print("\nAfter modification:")
    print(f"Name: {person.name} == 'Jane Doe'")
    print(f"Age: {person.age} == 28")
    print(f"Email: {person.email} == 'jane@example.com'")


def validated_properties_example() -> None:
    """Demonstrate properties with validation."""
    print("\nValidated Properties Example:")

    # Create a person with validated properties
    person = ValidatedPerson(name="John Doe", age=30, email="john@example.com")

    # Access properties
    print(f"Name: {person.name} == 'John Doe'")
    print(f"Age: {person.age} == 30")
    print(f"Email: {person.email} == 'john@example.com'")

    # Modify properties with valid values
    person.name = "Jane Doe"
    person.age = 28
    person.email = "jane@example.com"

    print("\nAfter valid modification:")
    print(f"Name: {person.name} == 'Jane Doe'")
    print(f"Age: {person.age} == 28")
    print(f"Email: {person.email} == 'jane@example.com'")

    # Try to set invalid values
    print("\nTrying invalid values:")
    try:
        person.age = -5
        print("Age set to -5")
    except ValueError as e:
        print(f"Error setting age: {e}")

    try:
        person.email = "invalid-email"
        print("Email set to 'invalid-email'")
    except ValueError as e:
        print(f"Error setting email: {e}")


def custom_property_factory_example() -> None:
    """Demonstrate custom property factory methods."""
    print("\nCustom Property Factory Example:")

    # Create a person with custom property factory
    person = CustomPropertyPerson(name="John Doe", age=30, email="john@example.com")

    # Access properties multiple times
    print(f"Name: {person.name} == 'John Doe'")
    print(f"Name again: {person.name} == 'John Doe'")
    print(f"Age: {person.age} == 30")
    print(f"Email: {person.email} == 'john@example.com'")

    # Check access counts
    print("\nAccess counts:")
    print(f"Name access count: {person._access_count.get('_name', 0)} == 2")
    print(f"Age access count: {person._access_count.get('_age', 0)} == 1")
    print(f"Email access count: {person._access_count.get('_email', 0)} == 1")


def readonly_properties_example() -> None:
    """Demonstrate read-only properties."""
    print("\nRead-Only Properties Example:")

    # Create a person with read-only properties
    person = ReadOnlyPerson(name="John Doe", age=30, email="john@example.com")

    # Access properties
    print(f"Name: {person.name} == 'John Doe'")
    print(f"Age: {person.age} == 30")
    print(f"Email: {person.email} == 'john@example.com'")

    # Try to modify properties
    print("\nTrying to modify read-only properties:")
    try:
        person.name = "Jane Doe"
        print("Name changed to 'Jane Doe'")
    except AttributeError as e:
        print(f"Error changing name: {e}")

    try:
        person.age = 28
        print("Age changed to 28")
    except AttributeError as e:
        print(f"Error changing age: {e}")

    # Try to delete properties
    print("\nTrying to delete read-only properties:")
    try:
        del person.email
        print("Email deleted")
    except AttributeError as e:
        print(f"Error deleting email: {e}")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_automaticproperties_example()
    validated_properties_example()
    custom_property_factory_example()
    readonly_properties_example()
