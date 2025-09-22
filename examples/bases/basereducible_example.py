#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""basereducible_example.py
An example of how to use BaseReducible class.

This example demonstrates:
1. Creating classes that inherit from BaseReducible
2. Using __slots__ for memory optimization
3. Pickling and unpickling BaseReducible objects
4. Handling both __dict__ and __slots__ attributes during serialization
5. Comparing original and deserialized objects
"""
# Imports #
# Standard Libraries #
import pickle
from typing import Any

# Third-Party Packages #
from baseobjects.bases import BaseReducible

# Local Packages #


# Classes #
class Person(BaseReducible):
    """A simple class that inherits from BaseReducible using __dict__."""

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any):
        """Initialize a Person object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(*args, **kwargs)
        self.construct(name=name, age=age)

    def construct(self, name: str, age: int, *args: Any, **kwargs: Any) -> None:
        """Construct the Person object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        self.name = name
        self.age = age
        self.friends = []  # Mutable attribute to demonstrate pickling


class SlottedPerson(BaseReducible):
    """A class that inherits from BaseReducible using __slots__."""

    __slots__ = ("name", "age", "friends")

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any):
        """Initialize a SlottedPerson object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(*args, **kwargs)
        self.construct(name=name, age=age)

    def construct(self, name: str, age: int, *args: Any, **kwargs: Any) -> None:
        """Construct the SlottedPerson object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        self.name = name
        self.age = age
        self.friends = []  # Mutable attribute to demonstrate pickling


class HybridPerson(BaseReducible):
    """A class that inherits from BaseReducible using both __slots__ and __dict__."""

    __slots__ = ("name", "age")

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any):
        """Initialize a HybridPerson object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(*args, **kwargs)
        self.construct(name=name, age=age)

    def construct(self, name: str, age: int, *args: Any, **kwargs: Any) -> None:
        """Construct the HybridPerson object.

        Args:
            name: The person's name
            age: The person's age
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        self.name = name
        self.age = age
        self.friends = []  # This will go in __dict__ since it's not in __slots__
        self.hobbies = []  # This will also go in __dict__


# Example Sections #
def dict_based_example():
    """Demonstrate pickling and unpickling of dict-based BaseReducible objects."""
    print("\nDict-Based BaseReducible Example:")

    # Create a Person instance
    person = Person("Alice", 30)
    print(f"Original person: {person.name}, {person.age}")

    # Add some friends
    person.friends.append("Bob")
    person.friends.append("Charlie")
    print(f"Friends: {person.friends}")

    # Pickle the object
    print("\nPickling the person object...")
    pickled_data = pickle.dumps(person)
    print(f"Pickled data size: {len(pickled_data)} bytes")

    # Unpickle the object
    print("\nUnpickling the person object...")
    unpickled_person = pickle.loads(pickled_data)

    # Verify the unpickled object
    print(f"Unpickled person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")

    # Compare original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same friends object? {id(person.friends) == id(unpickled_person.friends)} == False")


def slotted_example():
    """Demonstrate pickling and unpickling of slotted BaseReducible objects."""
    print("\nSlotted BaseReducible Example:")

    # Create a SlottedPerson instance
    person = SlottedPerson("Bob", 25)
    print(f"Original slotted person: {person.name}, {person.age}")

    # Add some friends
    person.friends.append("Alice")
    person.friends.append("Dave")
    print(f"Friends: {person.friends}")

    # Pickle the object
    print("\nPickling the slotted person object...")
    pickled_data = pickle.dumps(person)
    print(f"Pickled data size: {len(pickled_data)} bytes")

    # Unpickle the object
    print("\nUnpickling the slotted person object...")
    unpickled_person = pickle.loads(pickled_data)

    # Verify the unpickled object
    print(f"Unpickled slotted person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")

    # Compare original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same friends object? {id(person.friends) == id(unpickled_person.friends)} == False")

    # Demonstrate that __slots__ restricts attribute assignment
    try:
        person.new_attribute = "This will fail"
        print("Attribute assignment succeeded (unexpected)")
    except AttributeError as e:
        print(f"Attribute assignment failed as expected: {e}")


def hybrid_example():
    """Demonstrate pickling and unpickling of hybrid BaseReducible objects with both __slots__ and __dict__."""
    print("\nHybrid BaseReducible Example:")

    # Create a HybridPerson instance
    person = HybridPerson("Charlie", 40)
    print(f"Original hybrid person: {person.name}, {person.age}")

    # Add some friends and hobbies
    person.friends.append("Alice")
    person.hobbies.append("Reading")
    person.hobbies.append("Hiking")
    print(f"Friends: {person.friends}")
    print(f"Hobbies: {person.hobbies}")

    # Add a dynamic attribute (goes to __dict__)
    person.favorite_color = "Blue"
    print(f"Favorite color: {person.favorite_color}")

    # Pickle the object
    print("\nPickling the hybrid person object...")
    pickled_data = pickle.dumps(person)
    print(f"Pickled data size: {len(pickled_data)} bytes")

    # Unpickle the object
    print("\nUnpickling the hybrid person object...")
    unpickled_person = pickle.loads(pickled_data)

    # Verify the unpickled object
    print(f"Unpickled hybrid person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")
    print(f"Unpickled hobbies: {unpickled_person.hobbies}")
    print(f"Unpickled favorite color: {unpickled_person.favorite_color}")

    # Compare original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same hobbies list? {person.hobbies == unpickled_person.hobbies} == True")
    print(f"Same favorite color? {person.favorite_color == unpickled_person.favorite_color} == True")

    # Demonstrate that __slots__ restricts attribute assignment for slot names
    try:
        person.name = "Updated Name"
        print(f"Slot attribute update succeeded: {person.name} == 'Updated Name'")
    except AttributeError as e:
        print(f"Slot attribute update failed: {e}")


# Main #
if __name__ == "__main__":
    # Run examples
    dict_based_example()
    slotted_example()
    hybrid_example()
