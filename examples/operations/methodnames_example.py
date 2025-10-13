#!/usr/bin/env python
"""methodnames_example.py
An example of how to use the method name functions from the methodnames module.

This example demonstrates:
1. Basic usage of get_method_names and get_public_method_names
2. Using iter_method_names and iter_public_method_names for iteration
3. Comparing method names between different objects
4. Practical applications for method name introspection
"""


# Imports #
# Standard Libraries #
import datetime
import json

# Source Packages #
from baseobjects.operations import (
    get_method_names,
    get_public_method_names,
    iter_method_names,
    iter_public_method_names,
)


# Example Classes #
class ExampleClass:
    """A simple example class to demonstrate method name functions."""

    def __init__(self, value=0):
        self.value = value

    def public_method(self):
        """A public method."""
        return self.value

    def another_public_method(self, x):
        """Another public method."""
        return self.value + x

    def _private_method(self):
        """A private method (by convention)."""
        return self.value * 2

    def __special_method__(self):
        """A special method."""
        return self.value**2


class DerivedClass(ExampleClass):
    """A derived class that inherits from ExampleClass."""

    def additional_method(self):
        """An additional public method."""
        return self.value - 1

    def _another_private_method(self):
        """Another private method."""
        return self.value / 2


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of get_method_names and get_public_method_names."""
    print("\nBasic Usage Example:")

    # Create an instance of ExampleClass
    obj = ExampleClass(10)

    # Get all method names
    all_methods = get_method_names(obj)

    print(f"All methods of ExampleClass:")
    for method in all_methods:
        print(f"  {method}")

    # Get public method names
    public_methods = get_public_method_names(obj)

    print(f"\nPublic methods of ExampleClass:")
    for method in public_methods:
        print(f"  {method}")

    # Verify that private methods are excluded from public methods
    private_methods = [m for m in all_methods if m.startswith("_")]

    print(f"\nPrivate methods of ExampleClass:")
    for method in private_methods:
        print(f"  {method}")

    # Verify that all methods = public methods + private methods
    print(f"\nVerification:")
    print(f"  All methods count: {len(all_methods)}")
    print(f"  Public methods count: {len(public_methods)}")
    print(f"  Private methods count: {len(private_methods)}")
    print(f"  Public + Private = All: {len(public_methods) + len(private_methods) == len(all_methods)}")


def iterator_example():
    """Demonstrate using iter_method_names and iter_public_method_names."""
    print("\nIterator Example:")

    # Create an instance of ExampleClass
    obj = ExampleClass(10)

    # Use iter_method_names to iterate over all methods
    print("Using iter_method_names:")
    for method in iter_method_names(obj):
        print(f"  {method}")

    # Use iter_public_method_names to iterate over public methods
    print("\nUsing iter_public_method_names:")
    for method in iter_public_method_names(obj):
        print(f"  {method}")

    # Use the iterators with list comprehensions
    all_methods = [method for method in iter_method_names(obj)]
    public_methods = [method for method in iter_public_method_names(obj)]

    print("\nUsing list comprehensions:")
    print(f"  All methods: {all_methods}")
    print(f"  Public methods: {public_methods}")

    # Use the iterators with other iteration tools
    print("\nUsing other iteration tools:")

    # Filter methods that contain 'public'
    public_in_name = list(filter(lambda m: "public" in m, iter_method_names(obj)))
    print(f"  Methods containing 'public': {public_in_name}")

    # Map methods to uppercase
    uppercase_methods = list(map(str.upper, iter_public_method_names(obj)))
    print(f"  Public methods in uppercase: {uppercase_methods}")


def comparing_objects_example():
    """Demonstrate comparing method names between different objects."""
    print("\nComparing Objects Example:")

    # Create instances of different classes
    base_obj = ExampleClass(10)
    derived_obj = DerivedClass(20)

    # Get method names for both objects
    base_methods = get_method_names(base_obj)
    derived_methods = get_method_names(derived_obj)

    print(f"Base class methods:")
    for method in base_methods:
        print(f"  {method}")

    print(f"\nDerived class methods:")
    for method in derived_methods:
        print(f"  {method}")

    # Find methods that are in the derived class but not in the base class
    new_methods = [m for m in derived_methods if m not in base_methods]

    print(f"\nMethods added in the derived class:")
    for method in new_methods:
        print(f"  {method}")

    # Find common methods
    common_methods = [m for m in derived_methods if m in base_methods]

    print(f"\nMethods common to both classes:")
    for method in common_methods:
        print(f"  {method}")

    # Compare public methods
    base_public = get_public_method_names(base_obj)
    derived_public = get_public_method_names(derived_obj)

    print(f"\nPublic methods added in the derived class:")
    for method in [m for m in derived_public if m not in base_public]:
        print(f"  {method}")


def built_in_objects_example():
    """Demonstrate using method name functions with built-in objects."""
    print("\nBuilt-in Objects Example:")

    # Get method names for different built-in objects
    string_methods = get_method_names("Hello, World!")
    list_methods = get_method_names([1, 2, 3])
    dict_methods = get_method_names({"a": 1, "b": 2})

    print(f"String has {len(string_methods)} methods")
    print(f"List has {len(list_methods)} methods")
    print(f"Dictionary has {len(dict_methods)} methods")

    # Find methods that are common to all three types
    common_methods = set(string_methods) & set(list_methods) & set(dict_methods)

    print(f"\nMethods common to strings, lists, and dictionaries:")
    for method in sorted(common_methods):
        print(f"  {method}")

    # Find methods unique to each type
    string_unique = set(string_methods) - set(list_methods) - set(dict_methods)
    list_unique = set(list_methods) - set(string_methods) - set(dict_methods)
    dict_unique = set(dict_methods) - set(string_methods) - set(list_methods)

    print(f"\nSome methods unique to strings:")
    for method in sorted(list(string_unique)[:5]):  # Show just the first 5
        print(f"  {method}")

    print(f"\nSome methods unique to lists:")
    for method in sorted(list(list_unique)[:5]):  # Show just the first 5
        print(f"  {method}")

    print(f"\nSome methods unique to dictionaries:")
    for method in sorted(list(dict_unique)[:5]):  # Show just the first 5
        print(f"  {method}")


def standard_library_example():
    """Demonstrate using method name functions with standard library objects."""
    print("\nStandard Library Example:")

    # Create some standard library objects
    dt = datetime.datetime.now()
    js = json.JSONEncoder()

    # Get their method names
    dt_methods = get_public_method_names(dt)
    js_methods = get_public_method_names(js)

    print(f"Public methods of datetime.datetime:")
    for method in sorted(dt_methods)[:10]:  # Show just the first 10
        print(f"  {method}")

    print(f"\nPublic methods of json.JSONEncoder:")
    for method in sorted(js_methods):
        print(f"  {method}")

    # Check if specific methods exist
    print("\nChecking for specific methods:")
    print(f"  datetime has 'strftime': {'strftime' in dt_methods}")
    print(f"  JSONEncoder has 'encode': {'encode' in js_methods}")


def practical_example():
    """Demonstrate a practical use case for method name functions."""
    print("\nPractical Example - Simple Object Inspector:")

    def inspect_object(obj):
        """A simple object inspector function."""
        # Get basic object information
        obj_type = type(obj).__name__
        obj_module = type(obj).__module__

        # Get method counts
        all_methods = get_method_names(obj)
        public_methods = get_public_method_names(obj)
        private_methods = [m for m in all_methods if m.startswith("_") and not m.startswith("__")]
        special_methods = [m for m in all_methods if m.startswith("__") and m.endswith("__")]

        # Print the inspection results
        print(f"Object Inspection for: {obj}")
        print(f"  Type: {obj_type}")
        print(f"  Module: {obj_module}")
        print(f"  Method counts:")
        print(f"    Total methods: {len(all_methods)}")
        print(f"    Public methods: {len(public_methods)}")
        print(f"    Private methods: {len(private_methods)}")
        print(f"    Special methods: {len(special_methods)}")

        # Print some example methods from each category
        if public_methods:
            print(f"  Public method examples: {', '.join(sorted(public_methods)[:3])}")
        if private_methods:
            print(f"  Private method examples: {', '.join(sorted(private_methods)[:3])}")
        if special_methods:
            print(f"  Special method examples: {', '.join(sorted(special_methods)[:3])}")

        # Check for common special methods
        common_special = ["__str__", "__repr__", "__eq__", "__hash__"]
        implemented = [m for m in common_special if m in special_methods]

        print(f"  Implements: {', '.join(implemented) if implemented else 'No common special methods'}")

    # Inspect different types of objects
    print("Inspecting a string:")
    inspect_object("Hello, World!")

    print("\nInspecting a list:")
    inspect_object([1, 2, 3])

    print("\nInspecting a custom object:")
    inspect_object(ExampleClass(42))

    print("\nInspecting a derived object:")
    inspect_object(DerivedClass(42))


def method_calling_example():
    """Demonstrate calling methods discovered through method name functions."""
    print("\nMethod Calling Example:")

    # Create an object
    obj = ExampleClass(5)

    # Get its public methods
    public_methods = get_public_method_names(obj)

    print(f"Public methods of ExampleClass: {public_methods}")

    # Call each public method and show the result
    print("\nCalling each public method:")
    for method_name in public_methods:
        # Get the method object
        method = getattr(obj, method_name)

        # Check if it's callable
        if callable(method):
            try:
                # Try to call the method with no arguments
                result = method()
                print(f"  {method_name}() => {result}")
            except TypeError:
                # If it requires arguments, try with a default value
                try:
                    result = method(1)
                    print(f"  {method_name}(1) => {result}")
                except TypeError as e:
                    print(f"  {method_name} => Error: {e}")

    # Demonstrate dynamic method calling based on user input
    print("\nDynamic method calling:")

    # Simulate user input
    user_inputs = ["public_method", "another_public_method", "nonexistent_method"]

    for user_input in user_inputs:
        print(f"User requested method: {user_input}")

        # Check if the method exists
        if user_input in public_methods:
            # Get the method
            method = getattr(obj, user_input)

            # Call the method with appropriate arguments
            if user_input == "another_public_method":
                result = method(10)
                print(f"  Result: {result}")
            else:
                result = method()
                print(f"  Result: {result}")
        else:
            print(f"  Error: Method '{user_input}' does not exist or is not public")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    iterator_example()
    comparing_objects_example()
    built_in_objects_example()
    standard_library_example()
    practical_example()
    method_calling_example()
