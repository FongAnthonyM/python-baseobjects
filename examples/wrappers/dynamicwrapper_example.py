#!/usr/bin/env python
"""dynamicwrapper_example.py
An example of how to use DynamicWrapper class.

This example demonstrates:
1. Creating and using a DynamicWrapper
2. Wrapping objects with DynamicWrapper
3. Accessing wrapped object attributes and methods
4. Creating custom DynamicWrapper subclasses
5. Dynamic attribute resolution
6. Performance comparison with normal attribute access
"""


# Imports #
# Standard Libraries #
import time
from typing import List

# Source Packages #
from baseobjects.wrappers import DynamicWrapper


# Classes #
class SimpleObject:
    """A simple object to be wrapped."""

    def __init__(self, value: int = 0):
        self.value = value
        self.name = "SimpleObject"

    def get_value(self) -> int:
        """Get the value."""
        return self.value

    def set_value(self, value: int) -> None:
        """Set the value."""
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}(value={self.value})"


class ComplexObject:
    """A more complex object to be wrapped."""

    def __init__(self, items: List[int] = None):
        self.items = items or []
        self.name = "ComplexObject"

    def add_item(self, item: int) -> None:
        """Add an item to the list."""
        self.items.append(item)

    def get_items(self) -> List[int]:
        """Get all items."""
        return self.items

    def clear_items(self) -> None:
        """Clear all items."""
        self.items = []

    def __str__(self) -> str:
        return f"{self.name}(items={self.items})"


class CustomDynamicWrapper(DynamicWrapper):
    """A custom DynamicWrapper that wraps both simple and complex objects."""

    # Define which attributes contain objects to wrap
    _wrapped_map_ = ["simple", "complex"]

    # Define the wrapped object attributes
    _simple = None
    _complex = None

    def __init__(self, simple_obj: SimpleObject = None, complex_obj: ComplexObject = None):
        """Initialize the wrapper with simple and complex objects."""
        super().__init__()
        self.simple = simple_obj or SimpleObject()
        self.complex = complex_obj or ComplexObject()

    def get_combined_str(self) -> str:
        """Get a string representation of both wrapped objects."""
        return f"Combined: {self.simple}, {self.complex}"


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of DynamicWrapper."""
    print("\nBasic DynamicWrapper Usage:")

    # Create objects to wrap
    simple = SimpleObject(10)
    complex = ComplexObject([1, 2, 3])

    # Create a DynamicWrapper subclass
    class MyWrapper(DynamicWrapper):
        # Define which attributes contain objects to wrap
        _wrapped_map_ = ["obj1", "obj2"]

    # Create an instance of the wrapper
    wrapper = MyWrapper()
    wrapper.obj1 = simple
    wrapper.obj2 = complex

    print("Created wrapper with two objects:")
    print(f"  simple: {simple}")
    print(f"  complex: {complex}")

    # Access wrapped object attributes
    print("\nAccessing wrapped object attributes:")
    print(f"  wrapper.value: {wrapper.value} == 10")
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")
    print(f"  wrapper.items: {wrapper.items} == [1, 2, 3]")

    # Call wrapped object methods
    print("\nCalling wrapped object methods:")
    print(f"  wrapper.get_value(): {wrapper.get_value()} == 10")
    wrapper.set_value(20)
    print(f"  After wrapper.set_value(20), wrapper.value: {wrapper.value} == 20")
    print(f"  simple.value: {simple.value} == 20")

    wrapper.add_item(4)
    print(f"  After wrapper.add_item(4), wrapper.items: {wrapper.items} == [1, 2, 3, 4]")
    print(f"  complex.items: {complex.items} == [1, 2, 3, 4]")


def custom_wrapper_example():
    """Demonstrate using a custom DynamicWrapper subclass."""
    print("\nCustom DynamicWrapper Subclass Example:")

    # Create a custom wrapper
    wrapper = CustomDynamicWrapper(SimpleObject(5), ComplexObject([10, 20, 30]))

    print("Created custom wrapper:")
    print(f"  wrapper.get_combined_str(): {wrapper.get_combined_str()}")

    # Access and modify wrapped object attributes
    print("\nAccessing and modifying wrapped object attributes:")
    print(f"  Initial wrapper.value: {wrapper.value} == 5")
    wrapper.value = 15
    print(f"  After wrapper.value = 15: {wrapper.value} == 15")

    print(f"  Initial wrapper.items: {wrapper.items} == [10, 20, 30]")
    wrapper.add_item(40)
    print(f"  After wrapper.add_item(40): {wrapper.items} == [10, 20, 30, 40]")

    # Call a method from the wrapper itself
    print("\nCalling a method from the wrapper itself:")
    print(f"  wrapper.get_combined_str(): {wrapper.get_combined_str()}")


def attribute_resolution_example():
    """Demonstrate attribute resolution in DynamicWrapper."""
    print("\nAttribute Resolution Example:")

    # Create objects with overlapping attribute names
    obj1 = SimpleObject(10)
    obj1.shared_attr = "from obj1"

    obj2 = ComplexObject([1, 2, 3])
    obj2.shared_attr = "from obj2"
    obj2.unique_attr = "only in obj2"

    # Create a wrapper
    class AttributeWrapper(DynamicWrapper):
        _wrapped_map_ = ["first", "second"]

    wrapper = AttributeWrapper()
    wrapper.first = obj1
    wrapper.second = obj2

    print("Created wrapper with objects having overlapping attributes:")
    print(f"  obj1.shared_attr: {obj1.shared_attr}")
    print(f"  obj2.shared_attr: {obj2.shared_attr}")

    # Access attributes - first wrapped object takes precedence
    print("\nAccessing attributes (first wrapped object takes precedence):")
    print(f"  wrapper.shared_attr: {wrapper.shared_attr} == 'from obj1'")
    print(f"  wrapper.unique_attr: {wrapper.unique_attr} == 'only in obj2'")

    # Change the order of wrapped objects
    print("\nChanging the order of wrapped objects:")
    wrapper = AttributeWrapper()
    wrapper.first = obj2
    wrapper.second = obj1

    print(f"  wrapper.shared_attr: {wrapper.shared_attr} == 'from obj2'")


def dynamic_attribute_example():
    """Demonstrate dynamic attribute handling in DynamicWrapper."""
    print("\nDynamic Attribute Example:")

    # Create a wrapper
    class DynamicAttrWrapper(DynamicWrapper):
        _wrapped_map_ = ["obj"]

    wrapper = DynamicAttrWrapper()
    wrapper.obj = SimpleObject(10)

    print("Initial wrapper with SimpleObject:")
    print(f"  wrapper.value: {wrapper.value} == 10")
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")

    # Dynamically replace the wrapped object
    print("\nReplacing wrapped object with ComplexObject:")
    wrapper.obj = ComplexObject([1, 2, 3])

    # Now different attributes are available
    print("Accessing new attributes:")
    print(f"  wrapper.items: {wrapper.items} == [1, 2, 3]")
    print(f"  wrapper.name: {wrapper.name} == 'ComplexObject'")

    # Try to access attribute from previous object (should fail)
    print("\nTrying to access attribute from previous object:")
    try:
        value = wrapper.value
        print(f"  Value: {value}")
    except AttributeError:
        print("  AttributeError: attribute no longer exists")

    # Add a new attribute to the wrapped object at runtime
    print("\nAdding a new attribute to the wrapped object at runtime:")
    wrapper.obj.new_attr = "dynamically added"
    print(f"  wrapper.new_attr: {wrapper.new_attr} == 'dynamically added'")


def performance_comparison_example():
    """Demonstrate performance comparison between direct access and DynamicWrapper."""
    print("\nPerformance Comparison Example:")

    # Create objects
    simple = SimpleObject(10)

    # Create a wrapper
    class PerfWrapper(DynamicWrapper):
        _wrapped_map_ = ["obj"]

    wrapper = PerfWrapper()
    wrapper.obj = simple

    # Measure direct access performance
    iterations = 100000
    print(f"Running {iterations} iterations for each test...")

    # Direct access
    start_time = time.time()
    for _ in range(iterations):
        value = simple.value
        simple.value = value + 1
    direct_time = time.time() - start_time

    # Reset value
    simple.value = 10

    # Wrapper access
    start_time = time.time()
    for _ in range(iterations):
        value = wrapper.value
        wrapper.value = value + 1
    wrapper_time = time.time() - start_time

    print(f"Direct access time: {direct_time:.6f} seconds")
    print(f"Wrapper access time: {wrapper_time:.6f} seconds")
    print(f"Ratio (wrapper/direct): {wrapper_time / direct_time:.2f}x slower")
    print("Note: DynamicWrapper is typically around 4.4x slower than direct access")


def error_handling_example():
    """Demonstrate error handling with DynamicWrapper."""
    print("\nError Handling Example:")

    # Create objects
    simple = SimpleObject(10)

    # Create a wrapper
    class ErrorWrapper(DynamicWrapper):
        _wrapped_map_ = ["obj"]

    wrapper = ErrorWrapper()
    wrapper.obj = simple

    # Try to access a non-existent attribute
    print("Trying to access a non-existent attribute:")
    try:
        value = wrapper.non_existent_attr
        print(f"  Value: {value}")
    except AttributeError:
        print("  AttributeError: attribute doesn't exist")

    # Add the attribute to the wrapped object
    print("\nAdding the attribute to the wrapped object:")
    simple.non_existent_attr = "Now it exists"

    # Try again
    try:
        value = wrapper.non_existent_attr
        print(f"  Value: {value} == 'Now it exists'")
    except AttributeError as e:
        print(f"  AttributeError: {e}")


def compare_wrappers_example():
    """Compare DynamicWrapper with StaticWrapper."""
    print("\nComparing DynamicWrapper with StaticWrapper:")

    print("DynamicWrapper advantages:")
    print("  1. Can handle dynamically changing wrapped objects")
    print("  2. No need to call _wrap() after changing wrapped objects")
    print("  3. More flexible with attribute resolution")
    print("  4. Simpler to use for quick prototyping")

    print("\nDynamicWrapper disadvantages:")
    print("  1. Slower performance (typically 4.4x slower than direct access)")
    print("  2. No IDE auto-completion for wrapped object attributes")
    print("  3. Less explicit about which attributes are available")

    print("\nWhen to use DynamicWrapper:")
    print("  - When wrapped objects change frequently during runtime")
    print("  - When you need to wrap various indeterminate object types")
    print("  - When performance is not a critical concern")
    print("  - For quick prototyping and development")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    custom_wrapper_example()
    attribute_resolution_example()
    dynamic_attribute_example()
    performance_comparison_example()
    error_handling_example()
    compare_wrappers_example()
