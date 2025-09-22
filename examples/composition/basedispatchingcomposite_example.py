#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""basedispatchingcomposite_example.py
An example of how to create and use BaseDispatchingComposite.

This example demonstrates:
1. Creating a dispatching composite class
2. Registering component classes in a registry
3. Creating components using string identifiers
4. Dispatching component creation based on parameters
5. Dynamic component selection and creation
"""


# Imports #
# Standard Libraries #
from typing import Any, Dict, Tuple, Type, ClassVar

# Third-Party Packages #
from baseobjects.composition import BaseDispatchingComposite, BaseComponent
from baseobjects.classregistration import NamespaceClassRegistry

# Local Packages #


# Definitions #
# Classes #
class TextProcessingComponent(BaseComponent):
    """A component that processes text in various ways."""

    def process(self, text: str) -> str:
        """Process text according to the component's specific implementation.

        Args:
            text: The text to process.

        Returns:
            The processed text.
        """
        # This is a base implementation that will be overridden by subclasses
        return text


class UppercaseComponent(TextProcessingComponent):
    """A component that converts text to uppercase."""

    def process(self, text: str) -> str:
        """Convert text to uppercase.

        Args:
            text: The text to convert.

        Returns:
            The uppercase version of the text.
        """
        result = text.upper()
        self.composite.processed_text = result
        return result


class LowercaseComponent(TextProcessingComponent):
    """A component that converts text to lowercase."""

    def process(self, text: str) -> str:
        """Convert text to lowercase.

        Args:
            text: The text to convert.

        Returns:
            The lowercase version of the text.
        """
        result = text.lower()
        self.composite.processed_text = result
        return result


class ReverseComponent(TextProcessingComponent):
    """A component that reverses text."""

    def process(self, text: str) -> str:
        """Reverse the text.

        Args:
            text: The text to reverse.

        Returns:
            The reversed text.
        """
        result = text[::-1]
        self.composite.processed_text = result
        return result


class CountComponent(TextProcessingComponent):
    """A component that counts characters in text."""

    def process(self, text: str) -> str:
        """Count the characters in the text.

        Args:
            text: The text to count characters in.

        Returns:
            A string with the character count.
        """
        result = f"Character count: {len(text)}"
        self.composite.processed_text = result
        return result


class TextProcessor(BaseDispatchingComposite):
    """A composite that processes text using different components.

    This composite can dynamically create and use different text processing components based on string identifiers.

    Attributes:
        component_types_registry: Registry of available component types.
        processed_text: The result of the most recent text processing operation.
    """

    # Class Attributes #
    # Specify default components
    default_component_types: ClassVar[Dict[str, Tuple[Type[BaseComponent], Dict[str, Any]]]] = {
        "uppercase": (UppercaseComponent, {})
    }

    # Attributes #
    component_types_registry: NamespaceClassRegistry = (
        NamespaceClassRegistry()
    )  # Create a Registry to store component types
    processed_text: str = ""

    # Magic Methods #
    # Construction/Destruction
    def __init__(
        self,
        name: str | None = None,
        namespace: str | None = None,
        class_name: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        init: bool = True,
        **kwargs: Any,
    ) -> None:
        """Initialize the TextProcessor.

        Args:
            name: The name of the component to add.
            namespace: The namespace of the component to add.
            class_name: The class name of the component to add.
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            init: Whether to initialize the composite.
            **kwargs: Additional keyword arguments.
        """
        # Parent Initialization #
        super().__init__(init=False)

        # Object Construction #
        if init:
            self.construct(
                name=name,
                namespace=namespace,
                class_name=class_name,
                component_kwargs=component_kwargs,
                component_types=component_types,
                components=components,
                **kwargs,
            )

    # Instance Methods #
    # Constructors/Destructors
    def construct(
        self,
        name: str | None = None,
        namespace: str | None = None,
        class_name: str | None = None,
        component_kwargs: dict[str, dict[str, Any]] | None = None,
        component_types: dict[str, tuple[type, dict[str, Any]]] | None = None,
        components: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        """Construct this object.

        Args:
            name: The name of the component to add.
            namespace: The namespace of the component to add.
            class_name: The class name of the component to add.
            component_kwargs: Keyword arguments for creating the components.
            component_types: Component classes and their keyword arguments to instantiate.
            components: Components to add.
            **kwargs: Additional keyword arguments.
        """
        if name is not None and namespace is not None and class_name is not None:
            component_types = self.dispatch_component_types(name, namespace, class_name) | (component_types or {})

        super().construct(
            component_kwargs=component_kwargs,
            component_types=component_types,
            components=components,
            **kwargs,
        )

    def dispatch_component_types(
        self,
        name: str,
        namespace: str,
        class_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, tuple[type, dict[str, Any]]]:
        """Dispatch component types using the given arguments.

        Args:
            name: The name of the component to add.
            namespace: The namespace of the component to add.
            class_name: The class name of the component to add.
            *args: Positional arguments to use in dispatching.
            **kwargs: Keyword arguments to use in dispatching.

        Returns:
            A dictionary of the names of the components, their types, and their keyword arguments.
        """
        return {name: self.component_types_registry.get_class(namespace, class_name, with_kwargs=True, *args, **kwargs)}

    def process_text(self, text: str, component_name: str) -> str:
        """Process text using the specified component.

        Args:
            text: The text to process.
            component_name: The name of the component to use.

        Returns:
            The processed text.
        """
        if component_name not in self.components:
            raise ValueError(f"Component '{component_name}' not found")

        component = self.components[component_name]
        return component.process(text)


# Register components in the registry
TextProcessor.component_types_registry.register_class(
    LowercaseComponent,
    namespace="text",
    name="LowercaseComponent",
)

TextProcessor.component_types_registry.register_class(
    ReverseComponent,
    namespace="text",
    name="ReverseComponent",
)

TextProcessor.component_types_registry.register_class(
    CountComponent,
    namespace="text",
    name="CountComponent",
)


# Functions #
# Example Sections #
def basic_dispatching_composite_usage():
    """Demonstrates basic usage of a dispatching composite."""
    print("Basic Dispatching Composite Usage:\n")

    # Create a text processor with the default component (uppercase)
    print("Creating a text processor with the default component (uppercase)...")
    processor = TextProcessor()

    print("Components in the processor:")
    for name, component in processor.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Process text using the default component
    print("Processing text using the default component...")
    sample_text = "Hello, World!"
    result = processor.process_text(sample_text, "uppercase")
    print(f"Original text: {sample_text}")
    print(f"Processed text: {result} == 'HELLO, WORLD!'")
    assert processor.processed_text == "HELLO, WORLD!"
    print()


def creating_components_with_string_identifiers():
    """Demonstrates creating components using string identifiers."""
    print("Creating Components with String Identifiers:\n")

    # Create a text processor with a lowercase component
    print("Creating a text processor with a lowercase component...")
    processor = TextProcessor(name="lowercase", namespace="text", class_name="LowercaseComponent")

    print("Components in the processor:")
    for name, component in processor.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Process text using the lowercase component
    print("Processing text using the lowercase component...")
    sample_text = "Hello, World!"
    result = processor.process_text(sample_text, "lowercase")
    print(f"Original text: {sample_text}")
    print(f"Processed text: {result} == 'hello, world!'")
    assert processor.processed_text == "hello, world!"
    print()


def multiple_dispatched_components():
    """Demonstrates using multiple dispatched components."""
    print("Multiple Dispatched Components:\n")

    # Create a text processor with multiple components
    print("Creating a text processor with multiple components...")
    processor = TextProcessor()

    # Add components using string identifiers
    print("Adding components using string identifiers...")
    processor.construct(name="lowercase", namespace="text", class_name="LowercaseComponent")
    processor.construct(name="reverse", namespace="text", class_name="ReverseComponent")
    processor.construct(name="count", namespace="text", class_name="CountComponent")

    print("Components in the processor:")
    for name, component in processor.components.items():
        print(f"  - {name}: {type(component).__name__}")
    print()

    # Process text using different components
    sample_text = "Hello, World!"
    print(f"Original text: {sample_text}")

    # Uppercase
    result = processor.process_text(sample_text, "uppercase")
    print(f"Uppercase: {result} == 'HELLO, WORLD!'")

    # Lowercase
    result = processor.process_text(sample_text, "lowercase")
    print(f"Lowercase: {result} == 'hello, world!'")

    # Reverse
    result = processor.process_text(sample_text, "reverse")
    print(f"Reverse: {result} == '!dlroW ,olleH'")

    # Count
    result = processor.process_text(sample_text, "count")
    print(f"Count: {result} == 'Character count: 13'")
    print()


def dynamic_component_selection():
    """Demonstrates dynamic component selection based on user input."""
    print("Dynamic Component Selection:\n")

    # Create a text processor with all available components
    print("Creating a text processor with all available components...")
    processor = TextProcessor()
    processor.construct(name="lowercase", namespace="text", class_name="LowercaseComponent")
    processor.construct(name="reverse", namespace="text", class_name="ReverseComponent")
    processor.construct(name="count", namespace="text", class_name="CountComponent")

    # Simulate user input for component selection
    sample_text = "Hello, World!"
    print(f"Original text: {sample_text}")

    # List of operations to simulate user selection
    operations = ["uppercase", "lowercase", "reverse", "count"]

    print("Processing text with dynamically selected components:")
    for operation in operations:
        print(f"\nSelected operation: {operation}")
        try:
            result = processor.process_text(sample_text, operation)
            print(f"Result: {result}")
        except ValueError as e:
            print(f"Error: {e}")
    print()


def custom_component_registry():
    """Demonstrates creating and using a custom component registry."""
    print("Custom Component Registry:\n")

    # Create a new registry
    print("Creating a new component registry...")
    custom_registry = NamespaceClassRegistry()

    # Register components in the custom registry
    print("Registering components in the custom registry...")
    custom_registry.register_class(UppercaseComponent, namespace="custom", name="UpperCase")
    custom_registry.register_class(LowercaseComponent, namespace="custom", name="LowerCase")

    # Create a subclass of TextProcessor with the custom registry
    print("Creating a subclass of TextProcessor with the custom registry...")

    class CustomTextProcessor(TextProcessor):
        """A text processor with a custom component registry."""

        component_types_registry = custom_registry

    # Create an instance with a component from the custom registry
    print("Creating an instance with a component from the custom registry...")
    processor = CustomTextProcessor(name="custom_lower", namespace="custom", class_name="LowerCase")

    print("Components in the processor:")
    for name, component in processor.components.items():
        print(f"  - {name}: {type(component).__name__}")

    # Process text using the custom component
    sample_text = "Hello, World!"
    result = processor.process_text(sample_text, "custom_lower")
    print(f"\nOriginal text: {sample_text}")
    print(f"Processed text: {result} == 'hello, world!'")
    assert processor.processed_text == "hello, world!"
    print()


# Main #
if __name__ == "__main__":
    # Basic usage of a dispatching composite
    basic_dispatching_composite_usage()

    # Creating components with string identifiers
    creating_components_with_string_identifiers()

    # Using multiple dispatched components
    multiple_dispatched_components()

    # Dynamic component selection
    dynamic_component_selection()

    # Custom component registry
    custom_component_registry()
