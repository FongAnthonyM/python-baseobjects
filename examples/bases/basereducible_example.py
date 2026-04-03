#!/usr/bin/env python
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

# Source Packages #
from baseobjects.bases import BaseReducible


# Classes #
class Person(BaseReducible):
    """A simple class that inherits from BaseReducible using __dict__."""

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any) -> None:
        """Initializes a Person object.

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
        self.friends: list[str] = []  # Mutable attribute to demonstrate pickling


class SlottedPerson(BaseReducible):
    """A class that inherits from BaseReducible using __slots__."""

    __slots__ = ("age", "friends", "name")

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any) -> None:
        """Initializes a SlottedPerson object.

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
        self.friends: list[str] = []  # Mutable attribute to demonstrate pickling


class HybridPerson(BaseReducible):
    """A class that inherits from BaseReducible using both __slots__ and __dict__."""

    __slots__ = ("age", "name")

    def __init__(self, name: str = "", age: int = 0, *args: Any, **kwargs: Any) -> None:
        """Initializes a HybridPerson object.

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
        self.friends: list[str] = []  # This will go in __dict__ since it's not in __slots__
        self.hobbies: list[str] = []  # This will also go in __dict__


# Example Sections #
def dict_based_example() -> None:
    """Demonstrates pickling and unpickling of dict-based BaseReducible objects."""
    print("\nDict-Based BaseReducible Example:")

    # Creates a Person instance
    person = Person("Alice", 30)
    print(f"Original person: {person.name}, {person.age}")

    # Adds some friends
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

    # Verifies the unpickled object
    print(f"Unpickled person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")

    # Compares original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same friends object? {id(person.friends) == id(unpickled_person.friends)} == False")


def slotted_example() -> None:
    """Demonstrates pickling and unpickling of slotted BaseReducible objects."""
    print("\nSlotted BaseReducible Example:")

    # Creates a SlottedPerson instance
    person = SlottedPerson("Bob", 25)
    print(f"Original slotted person: {person.name}, {person.age}")

    # Adds some friends
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

    # Verifies the unpickled object
    print(f"Unpickled slotted person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")

    # Compares original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same friends object? {id(person.friends) == id(unpickled_person.friends)} == False")

    # Demonstrates that __slots__ restricts attribute assignment
    try:
        person.new_attribute = "This will fail"  # type: ignore
        print("Attribute assignment succeeded (unexpected)")
    except AttributeError as e:
        print(f"Attribute assignment failed as expected: {e}")


def hybrid_example() -> None:
    """Demonstrates pickling and unpickling of hybrid BaseReducible objects with both __slots__ and __dict__."""
    print("\nHybrid BaseReducible Example:")

    # Creates a HybridPerson instance
    person = HybridPerson("Charlie", 40)
    print(f"Original hybrid person: {person.name}, {person.age}")

    # Adds some friends and hobbies
    person.friends.append("Alice")
    person.hobbies.append("Reading")
    person.hobbies.append("Hiking")
    print(f"Friends: {person.friends}")
    print(f"Hobbies: {person.hobbies}")

    # Adds a dynamic attribute (goes to __dict__)
    person.favorite_color = "Blue"  # type: ignore
    print(f"Favorite color: {person.favorite_color}")  # type: ignore

    # Pickle the object
    print("\nPickling the hybrid person object...")
    pickled_data = pickle.dumps(person)
    print(f"Pickled data size: {len(pickled_data)} bytes")

    # Unpickle the object
    print("\nUnpickling the hybrid person object...")
    unpickled_person = pickle.loads(pickled_data)

    # Verifies the unpickled object
    print(f"Unpickled hybrid person: {unpickled_person.name}, {unpickled_person.age}")
    print(f"Unpickled friends: {unpickled_person.friends}")
    print(f"Unpickled hobbies: {unpickled_person.hobbies}")
    print(f"Unpickled favorite color: {unpickled_person.favorite_color}")

    # Compares original and unpickled objects
    print("\nComparing original and unpickled objects:")
    print(f"Same object? {person is unpickled_person} == False")
    print(f"Same name? {person.name == unpickled_person.name} == True")
    print(f"Same age? {person.age == unpickled_person.age} == True")
    print(f"Same friends list? {person.friends == unpickled_person.friends} == True")
    print(f"Same hobbies list? {person.hobbies == unpickled_person.hobbies} == True")
    print(f"Same favorite color? {person.favorite_color == unpickled_person.favorite_color} == True")  # type: ignore

    # Demonstrates that __slots__ restricts attribute assignment for slot names
    try:
        person.name = "Updated Name"
        print(f"Slot attribute update succeeded: {person.name} == 'Updated Name'")
    except AttributeError as e:
        print(f"Slot attribute update failed: {e}")


# Main #
if __name__ == "__main__":
    # Runs examples
    dict_based_example()
    slotted_example()
    hybrid_example()
