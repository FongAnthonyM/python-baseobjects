#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""staticwrapper_example.py
An example of how to use StaticWrapper class.

This example demonstrates:
1. Creating and using a StaticWrapper
2. Wrapping objects with StaticWrapper
3. Accessing wrapped object attributes and methods
4. Creating custom StaticWrapper subclasses
5. Static attribute resolution
6. Performance comparison with normal attribute access and DynamicWrapper
"""


# Imports #
# Standard Libraries #
import timeit
from typing import List

# Third-Party Packages #
from baseobjects.wrappers import StaticWrapper

# Local Packages #


# Classes #
class SimpleObject:
    """A simple object to be wrapped."""

    # Attributes #
    # Defining attributes in the class namespace ensures the StaticWrapper can make descriptors without calling _wrap()
    value: int = 0
    name: str
    
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
        # Defining attributes outside the class namespace means that StaticWrapper's _wrap() must be call so they are
        # available to the StaticWrapper
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


class CustomStaticWrapper(StaticWrapper):
    """A custom StaticWrapper that wraps both simple and complex objects."""
    
    # Define which attributes contain objects to wrap
    _wrapped_map_ = [("simple", SimpleObject), ("complex", ComplexObject)]
    
    def __init__(self, simple_obj: SimpleObject = None, complex_obj: ComplexObject = None):
        """Initialize the wrapper with simple and complex objects."""
        # Initialize attributes to store wrapped objects
        self._simple = simple_obj or SimpleObject()
        self._complex = complex_obj or ComplexObject()
    
    def get_combined_str(self) -> str:
        """Get a string representation of both wrapped objects."""
        return f"Combined: {self.simple}, {self.complex}"


# Example Sections #
def basic_usage_example():
    """Demonstrate basic usage of StaticWrapper."""
    print("\nBasic StaticWrapper Usage:")
    
    # Create objects to wrap
    simple = SimpleObject(10)
    complex = ComplexObject([1, 2, 3])
    
    # Create a StaticWrapper subclass
    class MyWrapper(StaticWrapper):
        # Define which attributes contain objects to wrap
        _wrapped_map_ = [("obj1", SimpleObject), ("obj2", ComplexObject)]
    
    # Create an instance of the wrapper
    wrapper = MyWrapper()
    
    # Set the wrapped objects
    wrapper._obj1 = simple
    wrapper._obj2 = complex
    
    print("Created wrapper with two objects:")
    print(f"  simple: {simple}")
    print(f"  complex: {complex}")

    # Default wrapping includes method and attributes defined in the class namespace
    print("\nCalling wrapped objects:")
    print(f"  wrapper.get_value(): {wrapper.get_value()} == 10")
    print(f"  wrapper.value: {wrapper.value} == 10")
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")
    print(f"  wrapper.items exist: {hasattr(wrapper, 'items')} == False")

    # Call _wrap to create property descriptors for attributes no defined in the class namespace (runtime)
    wrapper._wrap()  # This can be called within the class __init__ but will slow class creation

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
    """Demonstrate using a custom StaticWrapper subclass."""
    print("\nCustom StaticWrapper Subclass Example:")
    
    # Create a custom wrapper
    wrapper = CustomStaticWrapper(
        SimpleObject(5),
        ComplexObject([10, 20, 30])
    )
    
    print("Created custom wrapper:")
    print(f"  wrapper.get_combined_str(): {wrapper.get_combined_str()}")

    # Call _wrap to create property descriptors for attributes
    wrapper._wrap()  # This can be called within the class __init__ but will slow class creation
    
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
    """Demonstrate attribute resolution in StaticWrapper."""
    print("\nAttribute Resolution Example:")
    
    # Create objects with overlapping attribute names
    obj1 = SimpleObject(10)
    obj1.shared_attr = "from obj1"
    
    obj2 = ComplexObject([1, 2, 3])
    obj2.shared_attr = "from obj2"
    obj2.unique_attr = "only in obj2"
    
    # Create a wrapper
    class AttributeWrapper(StaticWrapper):
        _wrapped_map_ = [("first", SimpleObject), ("second", ComplexObject)]
    
    wrapper = AttributeWrapper()
    wrapper._first = obj1
    wrapper._second = obj2
    wrapper._wrap()
    
    print("Created wrapper with objects having overlapping attributes:")
    print(f"  obj1.shared_attr: {obj1.shared_attr}")
    print(f"  obj2.shared_attr: {obj2.shared_attr}")
    
    # Access attributes - first wrapped object takes precedence
    print("\nAccessing attributes (first wrapped object takes precedence):")
    print(f"  wrapper.shared_attr: {wrapper.shared_attr} == 'from obj1'")
    print(f"  wrapper.unique_attr: {wrapper.unique_attr} == 'only in obj2'")
    
    # Change the order of wrapped objects
    print("\nChanging the order of wrapped objects:")
    class ReversedWrapper(StaticWrapper):
        _wrapped_map_ = [("first", ComplexObject), ("second", SimpleObject)]
    
    reversed_wrapper = ReversedWrapper()
    reversed_wrapper._first = obj2
    reversed_wrapper._second = obj1
    reversed_wrapper._wrap()
    
    print(f"  reversed_wrapper.shared_attr: {reversed_wrapper.shared_attr} == 'from obj2'")


def rewrapping_example():
    """Demonstrate rewrapping objects in StaticWrapper."""
    print("\nRewrapping Example:")
    
    # Create a wrapper
    class RewrapWrapper(StaticWrapper):
        _wrapped_map_ = [("obj", SimpleObject)]
    
    wrapper = RewrapWrapper()
    wrapper._obj = SimpleObject(10)
    wrapper._wrap()
    
    print("Initial wrapper with SimpleObject:")
    print(f"  wrapper.value: {wrapper.value} == 10")
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")
    
    # Add a new attribute to the wrapped object
    wrapper._obj.new_attr = "added attribute"
    
    # Need to rewrap to access the new attribute
    print("\nAdding a new attribute without rewrapping:")
    try:
        print(f"  wrapper.new_attr: {wrapper.new_attr}")
    except AttributeError:
        print("  AttributeError: new_attr not accessible (need to rewrap)")
    
    # Rewrap to access the new attribute
    wrapper._wrap()
    print("\nAfter rewrapping:")
    print(f"  wrapper.new_attr: {wrapper.new_attr} == 'added attribute'")
    
    # Replace the wrapped object
    print("\nReplacing wrapped object with a new SimpleObject:")
    wrapper._obj = SimpleObject(20)
    wrapper._wrap()
    print(f"  wrapper.value: {wrapper.value} == 20")


def performance_comparison_example():
    """Demonstrate performance comparison between direct access and StaticWrapper."""
    print("\nPerformance Comparison Example:")
    
    # Create objects
    simple = SimpleObject(10)
    
    # Create a wrapper
    class PerfWrapper(StaticWrapper):
        _wrapped_map_ = [("obj", SimpleObject)]
    
    wrapper = PerfWrapper()
    wrapper._obj = simple
    wrapper._wrap()
    
    # Measure direct access performance
    iterations = 1000000
    print(f"Running {iterations} iterations for each test...")

    # Direct access
    def direct_access():
        return simple.value

    direct_timer = timeit.Timer(direct_access)
    direct_time = direct_timer.timeit(number=iterations)

    # Reset value
    simple.value = 10

    # Wrapper access
    def wrapper_access():
        return wrapper.value

    wrapper_timer = timeit.Timer(wrapper_access)
    wrapper_time = wrapper_timer.timeit(number=iterations)
    
    print(f"Direct access time: {direct_time:.6f} mircoseconds per-call")
    print(f"Wrapper access time: {wrapper_time:.6f} microseconds per-call")
    print(f"Ratio (wrapper/direct): {wrapper_time/direct_time:.2f}x slower")
    print("Note: StaticWrapper is typically only slightly slower than direct access")
    print("      because it uses property descriptors instead of dynamic lookup")


def error_handling_example():
    """Demonstrate error handling with StaticWrapper."""
    print("\nError Handling Example:")
    
    # Create objects
    simple = SimpleObject(10)
    
    # Create a wrapper
    class ErrorWrapper(StaticWrapper):
        _wrapped_map_ = [("obj", SimpleObject)]
    
    wrapper = ErrorWrapper()
    wrapper._obj = simple
    wrapper._wrap()
    
    # Try to access a non-existent attribute
    print("Trying to access a non-existent attribute:")
    try:
        value = wrapper.non_existent_attr
        print(f"  Value: {value}")
    except AttributeError as e:
        print(f"  AttributeError: attribute doesn't exist")
    
    # Add the attribute to the wrapped object
    print("\nAdding the attribute to the wrapped object:")
    simple.non_existent_attr = "Now it exists"
    
    # Try again (will still fail without rewrapping)
    try:
        value = wrapper.non_existent_attr
        print(f"  Value: {value}")
    except AttributeError:
        print("  AttributeError: still doesn't exist (need to rewrap)")
    
    # Rewrap and try again
    wrapper._wrap()
    print("\nAfter rewrapping:")
    try:
        value = wrapper.non_existent_attr
        print(f"  Value: {value} == 'Now it exists'")
    except AttributeError as e:
        print(f"  AttributeError: {e}")


def compare_wrappers_example():
    """Compare StaticWrapper with DynamicWrapper."""
    print("\nComparing StaticWrapper with DynamicWrapper:")
    
    print("StaticWrapper advantages:")
    print("  1. Better performance (close to direct attribute access)")
    print("  2. More explicit about which attributes are available")
    print("  3. Better for stable object structures")
    
    print("\nStaticWrapper disadvantages:")
    print("  1. Requires explicit _wrap() call to access attributes")
    print("  2. Requires explicit _wrap() or _rewrap() call when attributes are added or removed")
    print("  3. All instances must wrap the same object types")
    print("  4. Less flexible with dynamically changing objects")
    
    print("\nWhen to use StaticWrapper:")
    print("  - When performance is a critical concern")
    print("  - When wrapped objects have a stable structure")
    print("  - When all instances wrap the same types of objects")


# Main #
if __name__ == "__main__":
    # Run examples
    basic_usage_example()
    custom_wrapper_example()
    attribute_resolution_example()
    rewrapping_example()
    performance_comparison_example()
    error_handling_example()
    compare_wrappers_example()