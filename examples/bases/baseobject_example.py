#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""baseobject_example.py
An example of how to use BaseObject class.

This example demonstrates:
1. Creating classes that inherit from BaseObject
2. Using the construct method for initialization
3. Shallow copying (copy) of BaseObject instances
4. Deep copying (deepcopy) of BaseObject instances
5. Comparing original and copied objects
"""
# Imports #
# Standard Libraries #
from typing import Any, Dict, List

# Third-Party Packages #
from baseobjects.bases import BaseObject

# Local Packages #


# Classes #
class Person(BaseObject):
    """A simple class that inherits from BaseObject."""
    
    def __init__(self, name: str | None = None, age: int | None = None, *args: Any, **kwargs: Any):
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
        self.friends = []  # Mutable attribute to demonstrate deep vs shallow copy
        self.preferences = {}  # Another mutable attribute


class Employee(Person):
    """A class that extends Person and inherits BaseObject functionality."""

    employee_id: str
    department: str
    projects: List[str]
    
    def __init__(
        self,
        name: str | None = None,
        age: int | None = None,
        employee_id: str | None = None,
        department: str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize an Employee object.
        
        Args:
            name: The employee's name
            age: The employee's age
            employee_id: The employee's ID
            department: The employee's department
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        super().__init__(*args, **kwargs)
        self.construct(name=name, age=age, employee_id=employee_id, department=department)
    
    def construct(
        self,
        name: str,
        age: int,
        employee_id: str = "",
        department: str = "",
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Construct the Employee object.
        
        Args:
            name: The employee's name
            age: The employee's age
            employee_id: The employee's ID
            department: The employee's department
            *args: Additional arguments for parent classes
            **kwargs: Additional keyword arguments for parent classes
        """
        self.employee_id = employee_id
        self.department = department
        self.projects = []  # Mutable attribute to demonstrate deep vs shallow copy
        
        # Call parent's construct with remaining args/kwargs
        super().construct(name=name, age=age, *args, **kwargs)


# Example Sections #
def basic_baseobject_example():
    """Demonstrate basic usage of BaseObject."""
    print("\nBasic BaseObject Example:")
    
    # Create a Person instance
    person = Person("Alice", 30)
    print(f"Person: {person.name}, {person.age}")
    
    # Add some friends
    person.friends.append("Bob")
    person.friends.append("Charlie")
    print(f"Friends: {person.friends}")
    
    # Add some preferences
    person.preferences["color"] = "blue"
    person.preferences["food"] = "pizza"
    print(f"Preferences: {person.preferences}")
    
    # Create an Employee instance
    employee = Employee("Dave", 35, "E12345", "Engineering")
    print(f"Employee: {employee.name}, {employee.age}, {employee.employee_id}, {employee.department}")
    
    # Add some projects
    employee.projects.append("Project A")
    employee.projects.append("Project B")
    print(f"Projects: {employee.projects}")
    
    # Employee inherits Person's attributes
    employee.friends.append("Eve")
    print(f"Employee's friends: {employee.friends}")


def shallow_copy_example():
    """Demonstrate shallow copying of BaseObject instances."""
    print("\nShallow Copy Example:")
    
    # Create an original object
    original = Employee("Alice", 30, "E12345", "Engineering")
    original.friends.append("Bob")
    original.projects.append("Project X")
    original.preferences["color"] = "blue"
    
    print("Original object:")
    print(f"  Name: {original.name}")
    print(f"  Friends: {original.friends}")
    print(f"  Projects: {original.projects}")
    print(f"  Preferences: {original.preferences}")
    
    # Create a shallow copy
    shallow_copy = original.copy()
    
    print("\nShallow copy created")
    print(f"Are they the same object? {original is shallow_copy} == False")
    print(f"Do they have the same attribute values? {original.name == shallow_copy.name} == True")
    
    # Show that mutable attributes are shared
    print(f"Do they share the friends list? {id(original.friends) == id(shallow_copy.friends)} == True")
    print(f"Do they share the projects list? {id(original.projects) == id(shallow_copy.projects)} == True")
    print(f"Do they share the preferences dict? {id(original.preferences) == id(shallow_copy.preferences)} == True")
    
    # Modify the copy and show it affects the original's mutable attributes
    shallow_copy.friends.append("Charlie")
    shallow_copy.projects.append("Project Y")
    shallow_copy.preferences["food"] = "pizza"
    
    print("\nAfter modifying the shallow copy:")
    print(f"Original friends: {original.friends} == ['Bob', 'Charlie']")
    print(f"Original projects: {original.projects} == ['Project X', 'Project Y']")
    print(f"Original preferences: {original.preferences} == {{'color': 'blue', 'food': 'pizza'}}")


def deep_copy_example():
    """Demonstrate deep copying of BaseObject instances."""
    print("\nDeep Copy Example:")
    
    # Create an original object
    original = Employee("Bob", 40, "E67890", "Marketing")
    original.friends.append("Alice")
    original.projects.append("Project A")
    original.preferences["color"] = "green"
    
    print("Original object:")
    print(f"  Name: {original.name}")
    print(f"  Friends: {original.friends}")
    print(f"  Projects: {original.projects}")
    print(f"  Preferences: {original.preferences}")
    
    # Create a deep copy
    deep_copy = original.deepcopy()
    
    print("\nDeep copy created")
    print(f"Are they the same object? {original is deep_copy} == False")
    print(f"Do they have the same attribute values? {original.name == deep_copy.name} == True")
    
    # Show that mutable attributes are not shared
    print(f"Do they share the friends list? {id(original.friends) == id(deep_copy.friends)} == False")
    print(f"Do they share the projects list? {id(original.projects) == id(deep_copy.projects)} == False")
    print(f"Do they share the preferences dict? {id(original.preferences) == id(deep_copy.preferences)} == False")
    
    # Modify the copy and show it doesn't affect the original
    deep_copy.friends.append("Dave")
    deep_copy.projects.append("Project B")
    deep_copy.preferences["food"] = "pasta"
    
    print("\nAfter modifying the deep copy:")
    print(f"Original friends: {original.friends} == ['Alice']")
    print(f"Deep copy friends: {deep_copy.friends} == ['Alice', 'Dave']")
    print(f"Original projects: {original.projects} == ['Project A']")
    print(f"Deep copy projects: {deep_copy.projects} == ['Project A', 'Project B']")
    print(f"Original preferences: {original.preferences} == {{'color': 'green'}}")
    print(f"Deep copy preferences: {deep_copy.preferences} == {{'color': 'green', 'food': 'pasta'}}")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_baseobject_example()
    shallow_copy_example()
    deep_copy_example()