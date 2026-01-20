#!/usr/bin/env python
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
from typing import ClassVar

# Source Packages #
from baseobjects.wrappers import StaticWrapper


# Classes #
class SimpleObject:
    """A simple object to be wrapped."""

    # Attributes #
    # Defining attributes in the class namespace ensures the StaticWrapper can make descriptors without calling _wrap()
    value: int = 0
    name: str

    def __init__(self, value: int = 0) -> None:
        """Initialize the object."""
        self.value = value
        self.name = "SimpleObject"

    def get_value(self) -> int:
        """Get the value.

        Returns:
            The value.
        """
        return self.value

    def set_value(self, value: int) -> None:
        """Set the value."""
        self.value = value

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.name}(value={self.value})"


class ComplexObject:
    """A more complex object to be wrapped."""

    def __init__(self, items: list[int] | None = None) -> None:
        """Initialize the object."""
        # Defining attributes outside the class namespace means that StaticWrapper's _wrap() must be call so they are
        # available to the StaticWrapper
        self.items = items or []
        self.name = "ComplexObject"

    def add_item(self, item: int) -> None:
        """Add an item to the list."""
        self.items.append(item)

    def get_items(self) -> list[int]:
        """Get all items.

        Returns:
            The list of items.
        """
        return self.items

    def clear_items(self) -> None:
        """Clear all items."""
        self.items = []

    def __str__(self) -> str:
        """Return the string representation."""
        return f"{self.name}(items={self.items})"


class CustomStaticWrapper(StaticWrapper):
    """A custom StaticWrapper that wraps both simple and complex objects."""

    # Define which attributes contain objects to wrap
    _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("simple", SimpleObject), ("complex", ComplexObject)]

    def __init__(self, simple_obj: SimpleObject | None = None, complex_obj: ComplexObject | None = None) -> None:
        """Initialize the wrapper with simple and complex objects."""
        # Initialize attributes to store wrapped objects
        self._simple = simple_obj or SimpleObject()
        self._complex = complex_obj or ComplexObject()

    def get_combined_str(self) -> str:
        """Get a string representation of both wrapped objects.

        Returns:
            The combined string.
        """
        return f"Combined: {self.simple}, {self.complex}"  # type: ignore


# Example Sections #
def basic_usage_example() -> None:
    """Demonstrate basic usage of StaticWrapper."""
    print("\nBasic StaticWrapper Usage:")

    # Create objects to wrap
    simple = SimpleObject(10)
    complex_obj = ComplexObject([1, 2, 3])

    # Create a StaticWrapper subclass
    class MyWrapper(StaticWrapper):
        # Define which attributes contain objects to wrap
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("obj1", SimpleObject), ("obj2", ComplexObject)]

    # Create an instance of the wrapper
    wrapper = MyWrapper()

    # Set the wrapped objects
    wrapper._obj1 = simple  # type: ignore
    wrapper._obj2 = complex_obj  # type: ignore

    print("Created wrapper with two objects:")
    print(f"  simple: {simple}")
    print(f"  complex: {complex_obj}")

    # Default wrapping includes method and attributes defined in the class namespace
    print("\nCalling wrapped objects:")
    print(f"  wrapper.get_value(): {wrapper.get_value()} == 10")  # type: ignore
    print(f"  wrapper.value: {wrapper.value} == 10")  # type: ignore
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")  # type: ignore
    print(f"  wrapper.items exist: {hasattr(wrapper, 'items')} == False")

    # Call _wrap to create property descriptors for attributes no defined in the class namespace (runtime)
    wrapper._wrap()  # This can be called within the class __init__ but will slow class creation

    # Access wrapped object attributes
    print("\nAccessing wrapped object attributes:")
    print(f"  wrapper.value: {wrapper.value} == 10")  # type: ignore
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")  # type: ignore
    print(f"  wrapper.items: {wrapper.items} == [1, 2, 3]")  # type: ignore

    # Call wrapped object methods
    print("\nCalling wrapped object methods:")
    print(f"  wrapper.get_value(): {wrapper.get_value()} == 10")  # type: ignore
    wrapper.set_value(20)  # type: ignore
    print(f"  After wrapper.set_value(20), wrapper.value: {wrapper.value} == 20")  # type: ignore
    print(f"  simple.value: {simple.value} == 20")

    wrapper.add_item(4)  # type: ignore
    print(f"  After wrapper.add_item(4), wrapper.items: {wrapper.items} == [1, 2, 3, 4]")  # type: ignore
    print(f"  complex.items: {complex_obj.items} == [1, 2, 3, 4]")


def custom_wrapper_example() -> None:
    """Demonstrate using a custom StaticWrapper subclass."""
    print("\nCustom StaticWrapper Subclass Example:")

    # Create a custom wrapper
    wrapper = CustomStaticWrapper(SimpleObject(5), ComplexObject([10, 20, 30]))

    print("Created custom wrapper:")
    print(f"  wrapper.get_combined_str(): {wrapper.get_combined_str()}")

    # Call _wrap to create property descriptors for attributes
    wrapper._wrap()  # This can be called within the class __init__ but will slow class creation

    # Access and modify wrapped object attributes
    print("\nAccessing and modifying wrapped object attributes:")
    print(f"  Initial wrapper.value: {wrapper.value} == 5")  # type: ignore
    wrapper.value = 15  # type: ignore
    print(f"  After wrapper.value = 15: {wrapper.value} == 15")  # type: ignore

    print(f"  Initial wrapper.items: {wrapper.items} == [10, 20, 30]")  # type: ignore
    wrapper.add_item(40)  # type: ignore
    print(f"  After wrapper.add_item(40): {wrapper.items} == [10, 20, 30, 40]")  # type: ignore

    # Call a method from the wrapper itself
    print("\nCalling a method from the wrapper itself:")
    print(f"  wrapper.get_combined_str(): {wrapper.get_combined_str()}")


def attribute_resolution_example() -> None:
    """Demonstrate attribute resolution in StaticWrapper."""
    print("\nAttribute Resolution Example:")

    # Create objects with overlapping attribute names
    obj1 = SimpleObject(10)
    obj1.shared_attr = "from obj1"  # type: ignore

    obj2 = ComplexObject([1, 2, 3])
    obj2.shared_attr = "from obj2"  # type: ignore
    obj2.unique_attr = "only in obj2"  # type: ignore

    # Create a wrapper
    class AttributeWrapper(StaticWrapper):
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("first", SimpleObject), ("second", ComplexObject)]

    wrapper = AttributeWrapper()
    wrapper._first = obj1  # type: ignore
    wrapper._second = obj2  # type: ignore
    wrapper._wrap()

    print("Created wrapper with objects having overlapping attributes:")
    print(f"  obj1.shared_attr: {obj1.shared_attr}")  # type: ignore
    print(f"  obj2.shared_attr: {obj2.shared_attr}")  # type: ignore

    # Access attributes - first wrapped object takes precedence
    print("\nAccessing attributes (first wrapped object takes precedence):")
    print(f"  wrapper.shared_attr: {wrapper.shared_attr} == 'from obj1'")  # type: ignore
    print(f"  wrapper.unique_attr: {wrapper.unique_attr} == 'only in obj2'")  # type: ignore

    # Change the order of wrapped objects
    print("\nChanging the order of wrapped objects:")

    class ReversedWrapper(StaticWrapper):
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("first", ComplexObject), ("second", SimpleObject)]

    reversed_wrapper = ReversedWrapper()
    reversed_wrapper._first = obj2  # type: ignore
    reversed_wrapper._second = obj1  # type: ignore
    reversed_wrapper._wrap()

    print(f"  reversed_wrapper.shared_attr: {reversed_wrapper.shared_attr} == 'from obj2'")  # type: ignore


def rewrapping_example() -> None:
    """Demonstrate rewrapping objects in StaticWrapper."""
    print("\nRewrapping Example:")

    # Create a wrapper
    class RewrapWrapper(StaticWrapper):
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("obj", SimpleObject)]

    wrapper = RewrapWrapper()
    wrapper._obj = SimpleObject(10)  # type: ignore
    wrapper._wrap()

    print("Initial wrapper with SimpleObject:")
    print(f"  wrapper.value: {wrapper.value} == 10")  # type: ignore
    print(f"  wrapper.name: {wrapper.name} == 'SimpleObject'")  # type: ignore

    # Add a new attribute to the wrapped object
    wrapper._obj.new_attr = "added attribute"  # type: ignore

    # Need to rewrap to access the new attribute
    print("\nAdding a new attribute without rewrapping:")
    try:
        print(f"  wrapper.new_attr: {wrapper.new_attr}")  # type: ignore
    except AttributeError:
        print("  AttributeError: new_attr not accessible (need to rewrap)")

    # Rewrap to access the new attribute
    wrapper._wrap()
    print("\nAfter rewrapping:")
    print(f"  wrapper.new_attr: {wrapper.new_attr} == 'added attribute'")  # type: ignore

    # Replace the wrapped object
    print("\nReplacing wrapped object with a new SimpleObject:")
    wrapper._obj = SimpleObject(20)  # type: ignore
    wrapper._wrap()
    print(f"  wrapper.value: {wrapper.value} == 20")  # type: ignore


def performance_comparison_example() -> None:
    """Demonstrate performance comparison between direct access and StaticWrapper."""
    print("\nPerformance Comparison Example:")

    # Create objects
    simple = SimpleObject(10)

    # Create a wrapper
    class PerfWrapper(StaticWrapper):
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("obj", SimpleObject)]

    wrapper = PerfWrapper()
    wrapper._obj = simple  # type: ignore
    wrapper._wrap()

    # Measure direct access performance
    iterations = 1000000
    print(f"Running {iterations} iterations for each test...")

    # Direct access
    def direct_access() -> int:
        return simple.value

    direct_timer = timeit.Timer(direct_access)
    direct_time = direct_timer.timeit(number=iterations)

    # Reset value
    simple.value = 10

    # Wrapper access
    def wrapper_access() -> int:
        return wrapper.value  # type: ignore

    wrapper_timer = timeit.Timer(wrapper_access)
    wrapper_time = wrapper_timer.timeit(number=iterations)

    print(f"Direct access time: {direct_time:.6f} mircoseconds per-call")
    print(f"Wrapper access time: {wrapper_time:.6f} microseconds per-call")
    print(f"Ratio (wrapper/direct): {wrapper_time / direct_time:.2f}x slower")
    print("Note: StaticWrapper is typically only slightly slower than direct access")
    print("      because it uses property descriptors instead of dynamic lookup")


def error_handling_example() -> None:
    """Demonstrate error handling with StaticWrapper."""
    print("\nError Handling Example:")

    # Create objects
    simple = SimpleObject(10)

    # Create a wrapper
    class ErrorWrapper(StaticWrapper):
        _wrapped_map_: ClassVar[list[tuple[str, type | None]]] = [("obj", SimpleObject)]

    wrapper = ErrorWrapper()
    wrapper._obj = simple  # type: ignore
    wrapper._wrap()

    # Try to access a non-existent attribute
    print("Trying to access a non-existent attribute:")
    try:
        value = wrapper.non_existent_attr  # type: ignore
        print(f"  Value: {value}")
    except AttributeError:
        print("  AttributeError: attribute doesn't exist")

    # Add the attribute to the wrapped object
    print("\nAdding the attribute to the wrapped object:")
    simple.non_existent_attr = "Now it exists"  # type: ignore

    # Try again (will still fail without rewrapping)
    try:
        value = wrapper.non_existent_attr  # type: ignore
        print(f"  Value: {value}")
    except AttributeError:
        print("  AttributeError: still doesn't exist (need to rewrap)")

    # Rewrap and try again
    wrapper._wrap()
    print("\nAfter rewrapping:")
    try:
        value = wrapper.non_existent_attr  # type: ignore
        print(f"  Value: {value} == 'Now it exists'")
    except AttributeError as e:
        print(f"  AttributeError: {e}")


def compare_wrappers_example() -> None:
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
