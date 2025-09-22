#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""namespaceclassregistry_example.py
An example of how to create and use NamespaceClassRegistry.

This example demonstrates:
1. Creating a NamespaceClassRegistry
2. Registering classes with namespaces
3. Retrieving classes from the registry by namespace and name
4. Creating instances of registered classes
5. Handling missing classes and namespaces
"""


# Imports #
# Standard Libraries #
from typing import Any

# Third-Party Packages #
from baseobjects.classregistration import NamespaceClassRegistry
from baseobjects.bases import SEARCHSENTINEL

# Local Packages #


# Definitions #
# Classes #
# Example classes to register
class DataProcessor:
    """Base class for data processors."""

    def __init__(self, name: str) -> None:
        self.name = name

    def process(self, data: Any) -> Any:
        """Process data according to the processor's implementation.

        Args:
            data: The data to process.

        Returns:
            The processed data.
        """
        return data

    def __str__(self) -> str:
        return f"{self.name} (Base Processor)"


class TextProcessor(DataProcessor):
    """A processor for text data."""

    def process(self, data: str) -> str:
        """Process text data.

        Args:
            data: The text to process.

        Returns:
            The processed text.
        """
        return data.strip().upper()

    def __str__(self) -> str:
        return f"{self.name} (Text Processor)"


class NumberProcessor(DataProcessor):
    """A processor for numeric data."""

    def __init__(self, name: str, multiplier: float = 1.0) -> None:
        super().__init__(name)
        self.multiplier = multiplier

    def process(self, data: float) -> float:
        """Process numeric data.

        Args:
            data: The number to process.

        Returns:
            The processed number.
        """
        return data * self.multiplier

    def __str__(self) -> str:
        return f"{self.name} (Number Processor, multiplier={self.multiplier})"


class ListProcessor(DataProcessor):
    """A processor for list data."""

    def process(self, data: list) -> list:
        """Process list data.

        Args:
            data: The list to process.

        Returns:
            The processed list.
        """
        return sorted(data)

    def __str__(self) -> str:
        return f"{self.name} (List Processor)"


class DictionaryProcessor(DataProcessor):
    """A processor for dictionary data."""

    def process(self, data: dict) -> dict:
        """Process dictionary data.

        Args:
            data: The dictionary to process.

        Returns:
            The processed dictionary.
        """
        return {k.upper(): v for k, v in data.items()}

    def __str__(self) -> str:
        return f"{self.name} (Dictionary Processor)"


# Functions #
# Example Sections #
def basic_namespace_registry_usage():
    """Demonstrates basic usage of a namespace class registry."""
    print("Basic Namespace Registry Usage:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Register classes with namespaces
    print("Registering classes with namespaces...")
    registry.register_class(TextProcessor, namespace="text", name="TextProcessor")
    registry.register_class(NumberProcessor, namespace="numeric", name="NumberProcessor")
    registry.register_class(ListProcessor, namespace="collections", name="ListProcessor")
    registry.register_class(DictionaryProcessor, namespace="collections", name="DictionaryProcessor")

    # Print the registry structure
    print("\nRegistry structure:")
    for namespace, classes in registry.items():
        print(f"Namespace: {namespace}")
        for name, (cls, kwargs) in classes.items():
            print(f"  - {name}: {cls.__name__}")
    print()

    # Get classes from the registry
    print("Getting classes from the registry...")
    text_processor_class = registry.get_class("text", "TextProcessor")
    number_processor_class = registry.get_class("numeric", "NumberProcessor")
    list_processor_class = registry.get_class("collections", "ListProcessor")

    # Create instances
    print("Creating instances of retrieved classes...")
    text_processor = text_processor_class("Text Processor 1")
    number_processor = number_processor_class("Number Processor 1", multiplier=2.0)
    list_processor = list_processor_class("List Processor 1")

    # Use the instances
    print("\nProcessing data with each processor:")
    text_data = "  hello, world  "
    number_data = 5.0
    list_data = [3, 1, 4, 1, 5, 9]

    print(f"Text processor: '{text_processor.process(text_data)}' == 'HELLO, WORLD'")
    print(f"Number processor: {number_processor.process(number_data)} == 10.0")
    print(f"List processor: {list_processor.process(list_data)} == [1, 1, 3, 4, 5, 9]")
    print()


def default_values_and_error_handling():
    """Demonstrates handling missing classes and namespaces."""
    print("Default Values and Error Handling:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Register a class
    print("Registering a class...")
    registry.register_class(TextProcessor, namespace="text", name="TextProcessor")

    # Try to get a non-existent class with a default value
    print("\nTrying to get a non-existent class with a default value...")
    default_processor = DataProcessor("Default Processor")
    result = registry.get_class("text", "NonExistentProcessor", default=default_processor)
    print(f"Result: {result} (should be the default processor)")
    assert result == default_processor

    # Try to get a class from a non-existent namespace with a default value
    print("\nTrying to get a class from a non-existent namespace with a default value...")
    result = registry.get_class("non_existent", "TextProcessor", default=default_processor)
    print(f"Result: {result} (should be the default processor)")
    assert result == default_processor

    # Try to get a non-existent class without a default value (should raise KeyError)
    print("\nTrying to get a non-existent class without a default value...")
    try:
        registry.get_class("text", "NonExistentProcessor")
        print("This should not be printed!")
    except KeyError as e:
        print(f"KeyError raised as expected: {e}")

    # Try to get a class from a non-existent namespace without a default value (should raise KeyError)
    print("\nTrying to get a class from a non-existent namespace without a default value...")
    try:
        registry.get_class("non_existent", "TextProcessor")
        print("This should not be printed!")
    except KeyError as e:
        print(f"KeyError raised as expected: {e}")

    # Using SEARCHSENTINEL as the default value (should raise KeyError)
    print("\nUsing SEARCHSENTINEL as the default value...")
    try:
        registry.get_class("non_existent", "TextProcessor", default=SEARCHSENTINEL)
        print("This should not be printed!")
    except KeyError as e:
        print(f"KeyError raised as expected: {e}")
    print()


def class_kwargs_and_instantiation():
    """Demonstrates using class_kwargs and creating instances directly."""
    print("Class Kwargs and Instantiation:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Register classes with class_kwargs
    print("Registering classes with class_kwargs...")
    registry.register_class(
        NumberProcessor, namespace="numeric", name="DoubleProcessor", class_kwargs={"multiplier": 2.0}
    )

    registry.register_class(
        NumberProcessor, namespace="numeric", name="TripleProcessor", class_kwargs={"multiplier": 3.0}
    )

    registry.register_class(
        NumberProcessor, namespace="numeric", name="HalfProcessor", class_kwargs={"multiplier": 0.5}
    )

    # Get classes with their kwargs
    print("\nGetting classes with their kwargs...")
    double_class, double_kwargs = registry.get_class("numeric", "DoubleProcessor", with_kwargs=True)
    triple_class, triple_kwargs = registry.get_class("numeric", "TripleProcessor", with_kwargs=True)
    half_class, half_kwargs = registry.get_class("numeric", "HalfProcessor", with_kwargs=True)

    print(f"DoubleProcessor kwargs: {double_kwargs}")
    print(f"TripleProcessor kwargs: {triple_kwargs}")
    print(f"HalfProcessor kwargs: {half_kwargs}")

    # Create instances using the kwargs
    print("\nCreating instances using the kwargs...")
    double_processor = double_class("Double Processor", **double_kwargs)
    triple_processor = triple_class("Triple Processor", **triple_kwargs)
    half_processor = half_class("Half Processor", **half_kwargs)

    # Use the instances
    print("\nProcessing data with each processor:")
    number_data = 10.0

    print(f"Double processor: {double_processor.process(number_data)} == 20.0")
    print(f"Triple processor: {triple_processor.process(number_data)} == 30.0")
    print(f"Half processor: {half_processor.process(number_data)} == 5.0")

    # Create instances directly using get_new
    print("\nCreating instances directly using get_new...")
    direct_double = registry.get_new("numeric", "DoubleProcessor", name="Direct Double")
    direct_triple = registry.get_new("numeric", "TripleProcessor", name="Direct Triple")
    direct_half = registry.get_new("numeric", "HalfProcessor", name="Direct Half")

    # Use the directly created instances
    print("\nProcessing data with directly created processors:")
    print(f"Direct double processor: {direct_double.process(number_data)} == 20.0")
    print(f"Direct triple processor: {direct_triple.process(number_data)} == 30.0")
    print(f"Direct half processor: {direct_half.process(number_data)} == 5.0")

    # Override kwargs when creating instances
    print("\nOverriding kwargs when creating instances...")
    custom_double = registry.get_new(
        "numeric", "DoubleProcessor", name="Custom Double", class_kwargs={"multiplier": 4.0}
    )

    # Use the instance with overridden kwargs
    print(f"Custom double processor: {custom_double.process(number_data)} == 40.0")
    print()


def multiple_registration_methods():
    """Demonstrates different ways to register classes."""
    print("Multiple Registration Methods:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Method 1: Register individual classes
    print("\nMethod 1: Register individual classes...")
    registry.register_class(TextProcessor, namespace="text", name="TextProcessor")

    # Method 2: Register multiple classes using register_classes
    print("\nMethod 2: Register multiple classes using register_classes...")
    registry.register_classes(
        [
            (NumberProcessor, "numeric", "NumberProcessor", None),
            (ListProcessor, "collections", "ListProcessor", None),
        ]
    )

    # Method 3: Register classes using a dictionary in the constructor
    print("\nMethod 3: Register classes using a dictionary in the constructor...")
    new_registry = NamespaceClassRegistry(classes={"data": {"DictionaryProcessor": (DictionaryProcessor, {})}})

    # Print the registry structures
    print("\nFirst registry structure:")
    for namespace, classes in registry.items():
        print(f"Namespace: {namespace}")
        for name, (cls, kwargs) in classes.items():
            print(f"  - {name}: {cls.__name__}")

    print("\nSecond registry structure:")
    for namespace, classes in new_registry.items():
        print(f"Namespace: {namespace}")
        for name, (cls, kwargs) in classes.items():
            print(f"  - {name}: {cls.__name__}")

    # Method 4: Update classes from another registry
    print("\nMethod 4: Update classes from another registry...")
    registry.update_classes(new_registry)

    print("\nUpdated registry structure:")
    for namespace, classes in registry.items():
        print(f"Namespace: {namespace}")
        for name, (cls, kwargs) in classes.items():
            print(f"  - {name}: {cls.__name__}")
    print()


def module_import_feature():
    """Demonstrates the module import feature."""
    print("Module Import Feature:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Register a class
    print("Registering a class...")
    registry.register_class(TextProcessor, namespace="text", name="TextProcessor")

    # Try to get a class that doesn't exist but could be imported
    print("\nTrying to get a class that doesn't exist but could be imported...")
    print("(Note: This would normally try to import a module, but we'll simulate the behavior)")

    # Simulate the module import by registering the class after the first attempt
    def simulate_import(namespace, name, module):
        print(f"Simulating import of module '{module}'...")
        registry.register_class(NumberProcessor, namespace=namespace, name=name)
        return registry.get_class(namespace, name)

    # First attempt (would normally fail and try to import)
    number_processor_class = registry.get_class("numeric", "NumberProcessor", default=None)
    if number_processor_class is None:
        print("Class not found in registry, would attempt to import module...")
        number_processor_class = simulate_import("numeric", "NumberProcessor", "numeric.processors")

    # Create and use the instance
    print("\nCreating and using the instance...")
    number_processor = number_processor_class("Imported Processor")
    number_data = 7.0
    print(f"Number processor: {number_processor.process(number_data)} == 7.0")
    print()


def processor_factory():
    """Demonstrates using the registry as a factory for processors."""
    print("Processor Factory:\n")

    # Create a registry
    print("Creating a namespace class registry...")
    registry = NamespaceClassRegistry()

    # Register classes
    print("Registering classes...")
    registry.register_class(TextProcessor, namespace="text", name="TextProcessor")
    registry.register_class(NumberProcessor, namespace="numeric", name="NumberProcessor")
    registry.register_class(ListProcessor, namespace="collections", name="ListProcessor")
    registry.register_class(DictionaryProcessor, namespace="collections", name="DictionaryProcessor")

    # Create a factory function
    def create_processor(data_type: str, processor_name: str, **kwargs: Any) -> DataProcessor:
        """Factory function to create data processors.

        Args:
            data_type: The type of data to process (namespace).
            processor_name: The name of the processor to create.
            **kwargs: Additional parameters for the processor constructor.

        Returns:
            An instance of the requested processor type.

        Raises:
            KeyError: If the processor type is not found in the registry.
        """
        return registry.get_new(data_type, processor_name, **kwargs)

    # Use the factory to create processors
    print("Using the factory to create processors...")

    processors = [
        ("text", "TextProcessor", {"name": "Text Processor"}),
        ("numeric", "NumberProcessor", {"name": "Number Processor", "multiplier": 2.5}),
        ("collections", "ListProcessor", {"name": "List Processor"}),
        ("collections", "DictionaryProcessor", {"name": "Dictionary Processor"}),
    ]

    for data_type, processor_name, kwargs in processors:
        try:
            processor = create_processor(data_type, processor_name, **kwargs)
            print(f"\nCreated {processor_name}:")
            print(f"  - Description: {processor}")
        except KeyError as e:
            print(f"\nError creating {processor_name}: {e}")

    # Process some data with the created processors
    print("\nProcessing data with the created processors...")

    text_processor = create_processor("text", "TextProcessor", name="Text Processor")
    number_processor = create_processor("numeric", "NumberProcessor", name="Number Processor", multiplier=2.5)
    list_processor = create_processor("collections", "ListProcessor", name="List Processor")
    dict_processor = create_processor("collections", "DictionaryProcessor", name="Dictionary Processor")

    text_data = "  hello, world  "
    number_data = 4.0
    list_data = [3, 1, 4, 1, 5, 9]
    dict_data = {"name": "John", "age": 30}

    print(f"Text processor: '{text_processor.process(text_data)}' == 'HELLO, WORLD'")
    print(f"Number processor: {number_processor.process(number_data)} == 10.0")
    print(f"List processor: {list_processor.process(list_data)} == [1, 1, 3, 4, 5, 9]")
    print(f"Dictionary processor: {dict_processor.process(dict_data)} == {{'NAME': 'John', 'AGE': 30}}")
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of a namespace class registry
    basic_namespace_registry_usage()

    # Handling missing classes and namespaces
    default_values_and_error_handling()

    # Using class_kwargs and creating instances directly
    class_kwargs_and_instantiation()

    # Different ways to register classes
    multiple_registration_methods()

    # Module import feature
    module_import_feature()

    # Using the registry as a factory
    processor_factory()
